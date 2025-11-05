import os
import sys
from dotenv import load_dotenv

# 添加项目路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain_experimental.plan_and_execute import PlanAndExecute, load_agent_executor, load_chat_planner
from langchain_core.prompts import ChatPromptTemplate
from Metadata_Regirstry.tools import tools
from langchain_openai import ChatOpenAI
from config import Config
# 加载环境变量
load_dotenv()

import pandas as pd
import numpy as np
import json
import time
from datetime import datetime

# 导入算法模块
from Data_pre.data_quality_validator import DataQualityValidator
from Mapping.semantic_matcher import SemanticMatcher
from neo4j import GraphDatabase


# LLM 初始化 - 使用 .env 配置
openai_config = Config.get_openai_config()
llm = ChatOpenAI(
    model=openai_config["model"],  # 从 .env 读取
    temperature=openai_config["temperature"],  # 从 .env 读取
    openai_api_key=openai_config["api_key"],
    openai_api_base=openai_config["base_url"],
    max_retries=openai_config["max_retries"],
    max_tokens=openai_config["max_tokens"]  # 从 .env 读取
)

# 初始化数据库连接 - 使用 .env 配置
neo4j_config = Config.get_neo4j_config()
driver = GraphDatabase.driver(neo4j_config["uri"], auth=(neo4j_config["user"], neo4j_config["password"]))

# 初始化算法模块
data_validator = DataQualityValidator()
semantic_matcher = SemanticMatcher(driver, similarity_threshold=0.7)

#planner_prompt
planner_prompt = """
    你是一个智能计划智能体，你的任务是根据输入的本体类和属性以及值和值含义，按照 MDR 规范的步骤顺序生成六大注册类的计划。

    **重要特性：**
    - 集成了数据质量验证：系统会自动检查数据质量并提供修复建议
    - 集成了语义相似度检测：注册前会自动检查是否存在相似实体，避免重复注册
    - 支持智能去重：对于高相似度的实体，系统会提供合并或重命名建议
    
    **增强规则：**
    - 如果数据质量检查发现严重问题，计划中应包含数据清洗步骤
    - 如果检测到潜在重复实体，计划中应包含相似性检查和用户确认步骤
    - 如果 {values} 为空、null、nan 或空字符串，则跳过步骤5和6（值域注册和值含义注册）
    - 如果 {values} 有具体值，则执行完整的7步注册流程
    - 如果 {value_meanings} 为空、null、nan 或空字符串，则跳过步骤6（值含义注册）
    - **请确保严格按照提供的输入值 {values} 、值含义{value_meanings}注册，不允许更改、缺少或推测新的值**
    - **保持原始语言**：如果输入是英文，保持英文；如果输入是中文，保持中文。不要翻译。

    输入的本体类：{ontology_class}
    输入的属性：{attribute}
    输入的值：{values}
    输入的值含义：{value_meanings}

    请生成如下增强注册信息：
    0. **数据质量检查**：在正式注册前进行数据质量验证和相似度检测
    1. **object_class**：从输入的类 {ontology_class} 直接生成对象类，保持原始语言不翻译
    2. **property**：从输入的属性 {attribute} 生成property的注册内容，保持原始语言不翻译
    3. **concept_domain**：为property生成对应concept_domain，保持原始语言不翻译
    4. **data_element_concept**：根据object_class和property组合生成，保持原始语言不翻译
    5. **value_domain**：根据property生成value_domain，保持原始语言不翻译。**如果{values}为空，则跳过此步骤**
    6. **value_meanings**：**如果{values}为空或{value_meanings}为空，则跳过此步骤**，保持原始语言不翻译
    7. **data_element**：基于data_element_concept生成data_element，保持原始语言不翻译

    增强的任务计划包括以下步骤：
    0. 数据质量检查与重复检测：使用 validate_and_check_duplicates 工具
    1. 注册object_class：使用 register_object_class 工具，格式为：
    register_object_class(object_class="{object_class}")
    2. 注册property：使用 register_property 工具，格式为：
    register_property(property_name="{property}")
    3. 注册concept_domain：使用 register_concept_domain 工具，格式为：
    register_concept_domain(concept_domain="{concept_domain}")
    4. 注册data_element_concept，与3个类有关，分别是object_class{object_class}、property{property}、concept_domain{concept_domain}关联：使用 register_data_element_concept_with_relationships 工具，格式为：
    register_data_element_concept_with_relationships(
        data_element_concept="{data_element_concept}", 
        object_class="{object_class}", 
        property="{property}",
        concept_domain="{concept_domain}")
    5. **注册value_domain**：无论{values}是否为空，都注册值域：
       - 如果{values}不为空，使用 register_value_domain_with_values 工具：
       register_value_domain_with_values(
           value_domain="{value_domain}", 
           concept_domain="{concept_domain}",
           values="{values}")
       - 如果{values}为空，使用 register_value_domain_with_relationship 工具（仅建立关系）：
       register_value_domain_with_relationship(
           value_domain="{value_domain}", 
           concept_domain="{concept_domain}")
    6. **条件注册值含义value_meanings**：如果{values}不为空且{value_meanings}不为空，则注册值含义：使用 `register_value_meanings_with_relationship` 工具，格式为：
    register_value_meanings_with_relationship( 
        concept_domain="{concept_domain}",
        values="{values}",
        value_meanings="{value_meanings}")
    **如果{values}为空或{value_meanings}为空，则跳过此步骤并说明原因。**
    7. 注册数据元data_element，与2个类有关，分别是data_element_concept{data_element_concept}、value_domain{value_domain}关联：使用 register_data_element_with_relationships 工具，格式为：
    register_data_element_with_relationships(
        data_element="{data_element}", 
        data_element_concept="{data_element_concept}", 
        value_domain="{value_domain}")

    **案例1 - 英文有可枚举值的情况**
    输入的本体类：Clinical Study
    输入的属性：TelephoneNumberType
    输入的值：Cellular; Facsimile; Home; Mobile Telephone; Modem; Pager; Work
    输入的值含义：Cellular Telephone; Facsimile Machine; Home; Mobile Telephone; Modem Device Component; Pager; Worksite
    生成的任务计划需包括以下步骤：
    0. 数据质量检查与重复检测：使用 validate_and_check_duplicates 工具
    1. 注册object_class：使用 register_object_class 工具，格式为：
    register_object_class(object_class="Clinical Study")
    2. 注册property：使用 register_property 工具，格式为：
    register_property(property_name="TelephoneNumberType")
    3. 注册concept_domain：使用 register_concept_domain 工具，格式为：
    register_concept_domain(concept_domain="TelephoneNumberType")
    4. 注册data_element_concept，与3个类有关，分别是object_class、property、concept_domain关联：使用 register_data_element_concept_with_relationships 工具，格式为：
    register_data_element_concept_with_relationships(
        data_element_concept="Clinical StudyTelephoneNumberType", 
        object_class="Clinical Study", 
        property="TelephoneNumberType",
        concept_domain="TelephoneNumberType")
    5. 注册value_domain，与1个类有关，是concept_domain关联，存在可枚举的值需要注册：使用 register_value_domain_with_values 工具，格式为：
    register_value_domain_with_values(
        value_domain="TelephoneNumberType", 
        concept_domain="TelephoneNumberType",
        values="Cellular; Facsimile; Home; Mobile Telephone; Modem; Pager; Work")
    6. 注册值含义value_meanings：使用 `register_value_meanings_with_relationship` 工具，格式为：
    register_value_meanings_with_relationship( 
        concept_domain="TelephoneNumberType",
        values="Cellular; Facsimile; Home; Mobile Telephone; Modem; Pager; Work",
        value_meanings="Cellular Telephone; Facsimile Machine; Home; Mobile Telephone; Modem Device Component; Pager; Worksite")
    7. 注册数据元data_element，与2个类有关，分别是data_element_concept、value_domain关联：使用 register_data_element_with_relationships 工具，格式为：
    register_data_element_with_relationships(
        data_element="DEClinical StudyTelephoneNumberType", 
        data_element_concept="Clinical StudyTelephoneNumberType", 
        value_domain="TelephoneNumberType")

    **案例2 - 中文无可枚举值的情况**
    输入的本体类：专利
    输入的属性：申请日期
    输入的值：[空值]
    输入的值含义：[空值]
    生成的任务计划需包括以下步骤：
    0. 数据质量检查与重复检测：使用 validate_and_check_duplicates 工具
    1. 注册object_class：使用 register_object_class 工具，格式为：
    register_object_class(object_class="专利")
    2. 注册property：使用 register_property 工具，格式为：
    register_property(property_name="申请日期")
    3. 注册concept_domain：使用 register_concept_domain 工具，格式为：
    register_concept_domain(concept_domain="日期")
    4. 注册data_element_concept，与3个类有关，分别是object_class、property、concept_domain关联：使用 register_data_element_concept_with_relationships 工具，格式为：
    register_data_element_concept_with_relationships(
        data_element_concept="专利申请日期", 
        object_class="专利", 
        property="申请日期",
        concept_domain="日期")
    5. **跳过value_domain注册**：由于输入的值[空值]为空，跳过value_domain注册步骤。
    6. **跳过值含义注册**：由于输入的值[空值]为空，跳过值含义注册步骤。
    7. 注册数据元data_element，与2个类有关，分别是data_element_concept、value_domain关联：使用 register_data_element_with_relationships 工具，格式为：
    register_data_element_with_relationships(
        data_element="DE专利申请日期", 
        data_element_concept="专利申请日期", 
        value_domain="日期")
     **如果检测到数据质量问题或潜在重复，计划应包含相应的处理建议**
"""

# 使用 load_chat_planner 生成 Planner 实例
planner = load_chat_planner(llm, planner_prompt)

# 执行器提示
executor_prompt = """
你是一个增强的执行智能体，集成了数据质量验证和语义相似度检测功能。

**增强功能：**
- 在注册前自动进行数据质量检查
- 自动检测潜在的重复实体
- 提供智能的重复处理建议
- 支持数据清洗和修复

**执行规则：**
- 严格按照计划智能体的任务执行每一步，不许跳过任何一步
- 如果数据质量检查发现问题，应根据建议进行处理
- 如果检测到高相似度实体，应提示用户确认是否继续注册
- 确保使用工具时参数的个数正确
- **保持原始语言**：严格按照计划中的参数执行，不翻译、不转换语言

当前任务：{step_description}
    
请执行以下操作：
0. **数据质量检查**：在正式注册前进行数据质量验证和相似度检测
1. 如果任务是注册object_class，使用 `register_object_class` 工具：
   格式：`register_object_class(object_class="{object_class}")`
2. 如果任务是注册property，使用 `register_property` 工具：
   格式：`register_property(property_name="{property}")`
3. 如果任务是生成concept_domain，使用 `register_concept_domain` 工具：
   格式：`register_concept_domain(concept_domain="{concept_domain}")`
4. 如果任务是生成data_element_concept，与3个类有关，分别object_class、property、concept_domain关联，使用 `register_data_element_concept_with_relationships` 工具：
   格式：`register_data_element_concept_with_relationships(
        data_element_concept="{data_element_concept}", 
        object_class="{object_class}", 
        property="{property}", 
        concept_domain="{concept_domain}")`
5. 如果任务是生成value_domain，与1个类有关，concept_domain关联：
   - 如果{values}不为空，使用 `register_value_domain_with_values` 工具：
   格式：`register_value_domain_with_values(
        value_domain="{value_domain}", 
        concept_domain="{concept_domain}",
        values="{values}")`
   - 如果{values}为空，使用 `register_value_domain_with_relationship` 工具（仅建立关系）：
   格式：`register_value_domain_with_relationship(
        value_domain="{value_domain}", 
        concept_domain="{concept_domain}")`
6. 如果任务注册值含义value_meanings，与1个类有关，concept_domain关联，使用 `register_value_meanings_with_relationship` 工具：
   格式：`register_value_meanings_with_relationship( 
        concept_domain="{concept_domain}",
        values="{values}",
        value_meanings="{value_meanings}")`
7. 如果任务是生成data_element，与2个类有关，分别是data_element_concept、value_domain关联，使用 `register_data_element_with_relationships` 工具：
   格式：`register_data_element_with_relationships(
        data_element="{data_element}", 
        data_element_concept="{data_element_concept}", 
        value_domain="{value_domain}")`

    **案例1 - 英文有可枚举值的情况**
    按照计划进行注册：
    0. **数据质量检查**：在正式注册前进行数据质量验证和相似度检测
    1. 注册object_class：使用register_object_class(object_class="Clinical Study")
    输出：对象类 'Clinical Study' 已存在，继续检查是否需要建立关系或执行其他操作
    2. 注册property：使用register_property(property_name="TelephoneNumberType")
    输出：已成功注册属性 'TelephoneNumberType'，继续按计划进行下一步
    3. 注册concept_domain：使用register_concept_domain(concept_domain="TelephoneNumberType")
    输出：已成功注册概念域 'TelephoneNumberType'，继续按计划进行下一步
    4. 注册data_element_concept，与3个类有关，分别是object_class、property、concept_domain关联：
    使用register_data_element_concept_with_relationships(
        data_element_concept="Clinical StudyTelephoneNumberType", 
        object_class="Clinical Study", 
        property="TelephoneNumberType",
        concept_domain="TelephoneNumberType")
    输出：已成功注册数据元概念 'Clinical StudyTelephoneNumberType'，并与对象类Clinical Study，属性TelephoneNumberType和概念域TelephoneNumberType建立关系，继续按计划进行下一步
    5. 注册value_domain，与1个类有关，是concept_domain关联，存在可枚举的值需要注册：
    使用register_value_domain_with_values(
        value_domain="TelephoneNumberType", 
        concept_domain="TelephoneNumberType",
        values="Cellular; Facsimile; Home; Mobile Telephone; Modem; Pager; Work")
    输出：已成功注册值域 'TelephoneNumberType'，并与概念域建立关系，其中可枚举值单独注册并与值域建立关系
    6. 注册值含义value_meanings：使用 `register_value_meanings_with_relationship` 工具：
    使用register_value_meanings_with_relationship( 
        concept_domain="TelephoneNumberType",
        values="Cellular; Facsimile; Home; Mobile Telephone; Modem; Pager; Work",
        value_meanings="Cellular Telephone; Facsimile Machine; Home; Mobile Telephone; Modem Device Component; Pager; Worksite")
    输出：已成功注册值含义，并与概念域TelephoneNumberType建立关系，其中值含义单独注册并与可枚举值建立关系
    7. 注册数据元data_element，与2个类有关，分别是data_element_concept、value_domain关联：
    使用register_data_element_with_relationships(
        data_element="DEClinical StudyTelephoneNumberType", 
        data_element_concept="Clinical StudyTelephoneNumberType", 
        value_domain="TelephoneNumberType")
    输出：已成功注册数据元 'DEClinical StudyTelephoneNumberType'，并与数据元概念Clinical StudyTelephoneNumberType和值域TelephoneNumberType建立关系，完成全部注册计划

    **案例2 - 中文无可枚举值的情况**
    按照计划进行注册：
    0. **数据质量检查**：在正式注册前进行数据质量验证和相似度检测
    1. 注册object_class：使用register_object_class(object_class="专利")
    输出：对象类 '专利' 已存在，继续检查是否需要建立关系或执行其他操作
    2. 注册property：使用register_property(property_name="申请日期")
    输出：已成功注册属性 '申请日期'，继续按计划进行下一步
    3. 注册concept_domain：使用register_concept_domain(concept_domain="日期")
    输出：已成功注册概念域 '日期'，继续按计划进行下一步
    4. 注册data_element_concept，与3个类有关，分别是object_class、property、concept_domain关联：
    使用register_data_element_concept_with_relationships(
        data_element_concept="专利申请日期", 
        object_class="专利", 
        property="申请日期",
        concept_domain="日期")
    输出：已成功注册数据元概念 '专利申请日期'，并与对象类专利，属性申请日期和概念域日期建立关系，继续按计划进行下一步
    5. 注册value_domain，与1个类有关，是concept_domain关联，由于输入的值为空，使用register_value_domain_with_relationship工具注册值域：
    使用register_value_domain_with_relationship(
        value_domain="日期", 
        concept_domain="日期")
    输出：已成功注册值域 '日期'，并与概念域建立关系，由于无可枚举值，仅建立关系。
    6. **跳过值含义注册**：由于输入的值为空，跳过值含义注册步骤。
    输出：根据计划要求，由于输入值为空，跳过值含义注册步骤。
    7. 注册数据元data_element，与2个类有关，分别是data_element_concept、value_domain关联：
    使用register_data_element_with_relationships(
        data_element="DE专利申请日期", 
        data_element_concept="专利申请日期", 
        value_domain="日期")
    输出：已成功注册数据元 'DE专利申请日期'，并与数据元概念专利申请日期和值域日期建立关系，完成全部注册计划
"""  

# 初始化执行器
executor = load_agent_executor(llm, tools, verbose=True)

# 创建并运行 PlanAndExecute Agent
agent = PlanAndExecute(planner=planner, executor=executor, verbose=True)

def process_data_with_quality_check(df):
    """
    增强的数据处理函数，集成数据质量检查和语义匹配
    """
    print("开始数据质量检查...")
    
    # 1. 数据质量验证
    validation_result = data_validator.validate_data_batch(df)
    quality_score = data_validator.get_quality_score(validation_result)
    
    print(f"数据质量评分: {quality_score}/100")
    print(f"通过验证的记录: {validation_result['passed_records']}/{validation_result['total_records']}")
    
    if validation_result['issues']:
        print(f" 发现 {len(validation_result['issues'])} 个数据质量问题:")
        for issue in validation_result['issues'][:5]:  # 显示前5个问题
            print(f"   - 行{issue['row_idx']}: {issue['message']}")
        
        if len(validation_result['issues']) > 5:
            print(f"   ... 还有 {len(validation_result['issues']) - 5} 个问题")
    
    # 2. 使用清洗后的数据
    cleaned_df = validation_result['cleaned_data']
    
    # 3. 准备注册数据
    grouped_data = {}
    duplicate_check_results = []
    
    for _, row in cleaned_df.iterrows():
        ontology_class = row["本体类"]
        attribute = row["属性"]
        value_str = row.get("值", "")
        meaning_str = row.get("值含义", "")

        # 处理空值
        if pd.isna(value_str) or value_str == "nan" or value_str == "null" or value_str == "":
            value_str = ""
        if pd.isna(meaning_str) or meaning_str == "nan" or meaning_str == "null" or meaning_str == "":
            meaning_str = ""

        # 语义相似度检查
        print(f"\n 检查实体相似度: {ontology_class}.{attribute}")
        
        # 检查对象类重复
        oc_duplicate = semantic_matcher.check_duplicate_before_registration(ontology_class, "ObjectClass")
        prop_duplicate = semantic_matcher.check_duplicate_before_registration(attribute, "Property")
        
        duplicate_info = {
            'ontology_class': ontology_class,
            'attribute': attribute,
            'object_class_check': oc_duplicate,
            'property_check': prop_duplicate
        }
        duplicate_check_results.append(duplicate_info)
        
        # 显示重复检查结果
        if oc_duplicate['has_duplicates']:
            print(f"   对象类 '{ontology_class}' 发现重复实体")
        elif oc_duplicate['has_similar']:
            print(f"   对象类 '{ontology_class}' 发现相似实体")
        
        if prop_duplicate['has_duplicates']:
            print(f"   属性 '{attribute}' 发现重复实体")
        elif prop_duplicate['has_similar']:
            print(f"   属性 '{attribute}' 发现相似实体")

        if ontology_class not in grouped_data:
            grouped_data[ontology_class] = {}
        
        grouped_data[ontology_class][attribute] = {
            "value_str": value_str,
            "meaning_str": meaning_str,
            "quality_issues": [issue for issue in validation_result['issues'] 
                             if issue.get('ontology_class') == ontology_class and issue.get('attribute') == attribute],
            "duplicate_check": duplicate_info
        }
    
    return grouped_data, validation_result, duplicate_check_results

def enhanced_process_in_batches(data, batch_size=1):
    """
    增强的批处理函数，支持质量检查和重复检测
    """
    # 加载之前的进度
    progress, completed_set = load_progress()
    
    ontology_classes = list(data.keys())
    total_success = 0
    total_error = 0
    total_skipped = 0
    skipped_count = 0
    
    print(f"\n开始增强版注册处理，共 {len(ontology_classes)} 个本体类")
    
    # 确定开始位置
    start_class_idx, resume_class, start_attr_idx = get_start_position(data, progress)
    
    if resume_class:
        print(f" 从 {resume_class} 的第 {start_attr_idx} 个属性继续")
    
    processing_started = False if resume_class else True
    
    for i in range(start_class_idx, len(ontology_classes), batch_size):
        batch_classes = ontology_classes[i:i + batch_size]
        batch_data = {cls: data[cls] for cls in batch_classes}
        
        print(f"\n 处理批次 {i//batch_size + 1}/{len(ontology_classes)//batch_size + 1}")
        
        for ontology_class, attributes in batch_data.items():
            if not processing_started and ontology_class == resume_class:
                processing_started = True
            elif not processing_started:
                continue
                
            print(f"\n 处理本体类: {ontology_class}")
            
            attributes_list = list(attributes.items())
            start_idx = start_attr_idx if processing_started and ontology_class == resume_class else 0
            
            for j in range(start_idx, len(attributes_list)):
                attribute, details = attributes_list[j]
                
                # 检查是否已经处理过
                if should_skip_registration(ontology_class, attribute, completed_set):
                    skipped_count += 1
                    continue
                
                # 检查重复和质量问题
                duplicate_check = details.get('duplicate_check', {})
                quality_issues = details.get('quality_issues', [])
                
                # 处理重复检测结果
                should_skip = False
                
                if duplicate_check.get('object_class_check', {}).get('has_duplicates'):
                    print(f"跳过重复的对象类: {ontology_class}")
                    total_skipped += 1
                    should_skip = True
                
                if duplicate_check.get('property_check', {}).get('has_duplicates'):
                    print(f"跳过重复的属性: {attribute}")
                    total_skipped += 1
                    should_skip = True
                
                if should_skip:
                    save_completed_record(ontology_class, attribute)  # 标记为已处理
                    continue
                
                # 处理质量问题
                if quality_issues:
                    high_severity_issues = [issue for issue in quality_issues if issue['severity'] == 'high']
                    if high_severity_issues:
                        print(f" 跳过质量问题严重的记录: {ontology_class}.{attribute}")
                        total_error += 1
                        save_progress(ontology_class, attribute, success=False)
                        continue
                
                # 构建增强的输入描述
                has_values = "有" if details['value_str'] else "无"
                has_meanings = "有" if details['meaning_str'] else "无"
                quality_status = "良好" if not quality_issues else f"有{len(quality_issues)}个问题"
                
                input_description = (
                    f"本体类='{ontology_class}', 属性='{attribute}', "
                    f"值{has_values}, 值含义{has_meanings}, 数据质量={quality_status}"
                )
                
                # 添加重复检查信息
                if duplicate_check.get('object_class_check', {}).get('has_similar'):
                    input_description += f", 对象类存在相似实体"
                if duplicate_check.get('property_check', {}).get('has_similar'):
                    input_description += f", 属性存在相似实体"
                
                try:
                    print(f"开始注册: {ontology_class}.{attribute}")
                    result = agent.invoke({"input": input_description})
                    print(f" 注册完成: {ontology_class}.{attribute}")
                    total_success += 1
                    
                    # 保存完成记录
                    save_completed_record(ontology_class, attribute)
                    
                except Exception as e:
                    error_msg = str(e)
                    if "token" in error_msg.lower():
                        print(f" Token超限: {ontology_class}.{attribute}")
                    else:
                        print(f" 注册失败: {ontology_class}.{attribute} - {error_msg[:100]}")
                    
                    total_error += 1
                    save_progress(ontology_class, attribute, success=False)
                    continue
                
                # 保存进度
                save_progress(ontology_class, attribute, success=True)
                
                # 短暂暂停，避免API限制
                time.sleep(0.3)
            
            # 重置开始位置
            if processing_started and ontology_class == resume_class:
                start_attr_idx = 0
    
    print(f"\n增强版注册统计:")
    print(f"成功: {total_success}")
    print(f"失败: {total_error}")
    print(f"重复跳过: {total_skipped}")
    print(f"已完成跳过: {skipped_count}")
    print(f"总计: {total_success + total_error + total_skipped + skipped_count}")
    
    if total_error == 0:
        print("\n所有注册完成！可以删除进度文件:")
        print(f"   - {PROGRESS_FILE}")
        print(f"   - {COMPLETED_FILE}")

# 断点续传功能
PROGRESS_FILE = "registration_progress.json"
COMPLETED_FILE = "registration_completed.json"

def load_progress():
    """加载之前的注册进度"""
    progress = {}
    completed = set()
    
    if os.path.exists(PROGRESS_FILE):
        try:
            with open(PROGRESS_FILE, 'r', encoding='utf-8') as f:
                progress = json.load(f)
            print(f"加载进度文件，上次处理到: {progress.get('last_processed', '无记录')}")
        except Exception as e:
            print(f"加载进度文件失败: {e}")
    
    if os.path.exists(COMPLETED_FILE):
        try:
            with open(COMPLETED_FILE, 'r', encoding='utf-8') as f:
                completed_data = json.load(f)
                completed = set(completed_data.get('completed', []))
            print(f"已完成的注册数量: {len(completed)}")
        except Exception as e:
            print(f"加载完成记录失败: {e}")
    
    return progress, completed

def save_progress(ontology_class, attribute, success=True):
    """保存当前注册进度"""
    progress = {
        'last_processed': f"{ontology_class}.{attribute}",
        'last_updated': datetime.now().isoformat(),
        'ontology_class': ontology_class,
        'attribute': attribute,
        'success': success
    }
    
    try:
        with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
            json.dump(progress, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"  保存进度失败: {e}")

def save_completed_record(ontology_class, attribute):
    """保存已完成的注册记录"""
    completed_record = []
    
    # 先读取现有的完成记录
    if os.path.exists(COMPLETED_FILE):
        try:
            with open(COMPLETED_FILE, 'r', encoding='utf-8') as f:
                existing_data = json.load(f)
                completed_record = existing_data.get('completed', [])
        except:
            pass
    
    # 添加新的完成记录
    record_key = f"{ontology_class}.{attribute}"
    if record_key not in completed_record:
        completed_record.append(record_key)
    
    try:
        with open(COMPLETED_FILE, 'w', encoding='utf-8') as f:
            json.dump({
                'completed': completed_record,
                'total_completed': len(completed_record),
                'last_updated': datetime.now().isoformat()
            }, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"  保存完成记录失败: {e}")

def reset_progress():
    """重置注册进度"""
    try:
        if os.path.exists(PROGRESS_FILE):
            os.remove(PROGRESS_FILE)
            print(f"已删除进度文件: {PROGRESS_FILE}")

        if os.path.exists(COMPLETED_FILE):
            os.remove(COMPLETED_FILE)
            print(f"已删除完成记录文件: {COMPLETED_FILE}")

        print("进度重置完成")
    except Exception as e:
        print(f"重置进度时出错: {e}")

def should_skip_registration(ontology_class, attribute, completed_set):
    """判断是否应该跳过已完成的注册"""
    record_key = f"{ontology_class}.{attribute}"
    return record_key in completed_set

def get_start_position(data, progress):
    """根据进度确定开始位置"""
    if not progress or 'ontology_class' not in progress:
        return 0, None, None
    
    last_class = progress['ontology_class']
    last_attr = progress['attribute']
    
    ontology_classes = list(data.keys())
    
    try:
        class_index = ontology_classes.index(last_class)
        attributes = list(data[last_class].keys())
        
        try:
            attr_index = attributes.index(last_attr)
            # 从下一个属性开始
            return class_index, last_class, attr_index + 1
        except ValueError:
            # 如果找不到属性，从下一个类开始
            return class_index + 1, None, None
    except ValueError:
        # 如果找不到类，从开头开始
        return 0, None, None

# 批处理 - 支持断点续传
def process_in_batches(data, batch_size=1):
    """
    支持断点续传的批次处理函数
    """
    # 加载之前的进度
    progress, completed_set = load_progress()
    
    ontology_classes = list(data.keys())
    total_success = 0
    total_error = 0
    skipped_count = 0
    
    # 确定开始位置
    start_class_idx, resume_class, start_attr_idx = get_start_position(data, progress)
    
    print(f" 开始处理，共 {len(ontology_classes)} 个本体类")
    if resume_class:
        print(f" 从 {resume_class} 的第 {start_attr_idx} 个属性继续")
    
    processing_started = False if resume_class else True
    
    for i in range(start_class_idx, len(ontology_classes), batch_size):
        batch_classes = ontology_classes[i:i + batch_size]
        batch_data = {cls: data[cls] for cls in batch_classes}
        
        print(f"\n 处理批次 {i//batch_size + 1}/{len(ontology_classes)//batch_size + 1}")
        
        for ontology_class, attributes in batch_data.items():
            # 如果正在恢复，检查是否需要跳过
            if not processing_started and ontology_class == resume_class:
                processing_started = True
            elif not processing_started:
                continue
                
            print(f"\n 处理本体类: {ontology_class}")
            
            attributes_list = list(attributes.items())
            start_idx = start_attr_idx if processing_started and ontology_class == resume_class else 0
            
            for j in range(start_idx, len(attributes_list)):
                attribute, details = attributes_list[j]
                
                # 检查是否已经处理过
                if should_skip_registration(ontology_class, attribute, completed_set):
                    skipped_count += 1
                    continue
                
                # 简化的输入描述，减少token
                has_values = "有" if details['value_str'] else "无"
                has_meanings = "有" if details['meaning_str'] else "无"
                
                input_description = (
                    f"本体类='{ontology_class}', 属性='{attribute}', "
                    f"值{has_values}, 值含义{has_meanings}"
                )
                
                try:
                    result = agent.invoke({"input": input_description})
                    print(f" 注册完成: {ontology_class}.{attribute}")
                    total_success += 1
                    
                    # 保存完成记录
                    save_completed_record(ontology_class, attribute)
                    
                except Exception as e:
                    error_msg = str(e)
                    if "token" in error_msg.lower():
                        print(f"  Token超限: {ontology_class}.{attribute}")
                    else:
                        print(f" 注册失败: {ontology_class}.{attribute} - {error_msg[:100]}")
                    
                    total_error += 1
                    # 即使是失败也保存进度，避免重复处理
                    save_progress(ontology_class, attribute, success=False)
                    continue
                
                # 保存进度
                save_progress(ontology_class, attribute, success=True)
                
                # 短暂暂停，避免API限制
                time.sleep(0.3)
            
            # 重置开始位置（只在第一个类需要特殊处理）
            if processing_started and ontology_class == resume_class:
                start_attr_idx = 0
    
    print(f"\n注册统计 - 成功: {total_success}, 失败: {total_error}, 跳过: {skipped_count}, 总计: {total_success + total_error + skipped_count}")
    
    if total_error == 0:
        print(" 所有注册完成！可以删除进度文件:")
        print(f"   - {PROGRESS_FILE}")
        print(f"   - {COMPLETED_FILE}")

def main():
    """增强版主函数"""
    print("开始MDM-01共享域数据智能注册系统 (集成数据质量检查和重复检测)")
    print("=" * 80)
    
    # 检查文件是否存在
    if not os.path.exists(Config.SHARED_DOMAIN_FILE):
        print(f"错误: {Config.SHARED_DOMAIN_FILE} 文件不存在")
        print("请先运行 extract_shared_domain.py 生成共享域数据")
        return
    
    # 读取数据
    df = pd.read_excel(Config.SHARED_DOMAIN_FILE)
    
    # 修复列名编码问题
    if len(df.columns) == 8:
        # 8列数据（shared_domain.xlsx格式）
        expected_columns = ['本体类', '属性', '值', '值含义', '代码', '数据类型', '属性描述', '来源文件']
        df.columns = expected_columns
        print("已修复列名编码问题（8列格式）")
    elif len(df.columns) == 4:
        # 4列数据（ontology_data_all.xlsx格式）
        expected_columns = ['本体类', '属性', '值', '值含义']
        df.columns = expected_columns
        print("已修复列名编码问题（4列格式）")
    
    # 使用增强的数据处理功能
    try:
        data, validation_result, duplicate_results = process_data_with_quality_check(df)
        
        if not data:
            print("没有数据需要处理")
            return
        
        print(f"\n数据概览:")
        print(f"   - 本体类数量: {len(data)}")
        total_attributes = sum(len(attributes) for attributes in data.values())
        print(f"   - 总属性数量: {total_attributes}")
        
        # 显示质量和重复检查摘要
        total_quality_issues = len(validation_result['issues'])
        total_duplicates = sum(1 for result in duplicate_results 
                             if result['object_class_check']['has_duplicates'] or 
                                result['property_check']['has_duplicates'])
        
        print(f"   - 数据质量问题: {total_quality_issues}")
        print(f"   - 检测到重复: {total_duplicates}")
        
        # 加载进度信息
        progress, completed_set = load_progress()
        if completed_set:
            print(f"   - 已完成的注册: {len(completed_set)}")
        
        print("\n" + "=" * 80)
        
        # 开始增强处理
        enhanced_process_in_batches(data, batch_size=1)
        
    except KeyboardInterrupt:
        print("\n\n用户中断注册，进度已保存")
        print("下次运行时会自动从断点继续")
        
    except Exception as e:
        print(f"\n\n处理过程出错: {e}")
        print("进度已保存，下次运行时会自动从断点继续")
        
    finally:
        # 关闭数据库连接
        driver.close()
        
    print("\n增强版注册任务结束")

if __name__ == "__main__":
    # 检查是否有重置参数
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--reset":
        reset_progress()
    else:
        main()