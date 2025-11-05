# -*- coding: utf-8 -*-
"""
优化的MDR注册系统 - 解决超token问题
"""

from langchain_experimental.plan_and_execute import PlanAndExecute, load_agent_executor, load_chat_planner
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
import os
import sys
import pandas as pd
import numpy as np
from dotenv import load_dotenv

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from Metadata_Regirstry.tools import tools
from config import Config

# 加载环境变量
load_dotenv()

# 设置DeepSeek API配置（从环境变量读取）
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_BASE_URL"] = os.getenv("OPENAI_BASE_URL", "https://api.deepseek.com/v1")  

llm = ChatOpenAI(
    model="deepseek-chat",  
    temperature=0,
    max_retries=3  
)

# 精简的提示词 - 减少token使用
planner_prompt = """
你是一个MDR注册计划智能体，根据输入生成注册计划。

**核心规则：**
- 值为空则跳过值域和值含义注册
- 严格按照输入值注册，不翻译，保持原始语言
- 值为空用register_value_domain_with_relationship，有值用register_value_domain_with_values

**7步注册流程：**
1. object_class: register_object_class(object_class="{object_class}")
2. property: register_property(property_name="{property}")
3. concept_domain: register_concept_domain(concept_domain="{concept_domain}")  
4. data_element_concept: register_data_element_concept_with_relationships(...)
5. value_domain: 根据是否有值选择注册方式
6. value_meanings: 值和值含义都非空时注册
7. data_element: register_data_element_with_relationships(...)

输入：本体类='{ontology_class}', 属性='{attribute}', 值='{values}', 值含义='{value_meanings}'
生成简洁的注册计划。
"""

# 简化的执行器提示词
executor_prompt = """
执行MDR注册计划，严格按照步骤执行。

**执行规则：**
- 跳过计划中标记为跳过的步骤
- 保持原始语言，不翻译
- 空值处理：用register_value_domain_with_relationship
- 有值处理：用register_value_domain_with_values + register_value_meanings_with_relationship

当前任务：{step_description}

工具调用格式：
1. register_object_class(object_class="...")
2. register_property(property_name="...")
3. register_concept_domain(concept_domain="...")
4. register_data_element_concept_with_relationships(...)
5. register_value_domain_with_values(...) 或 register_value_domain_with_relationship(...)
6. register_value_meanings_with_relationship(...)
7. register_data_element_with_relationships(...)

返回执行结果或错误信息。
"""

# 初始化
planner = load_chat_planner(llm, planner_prompt)
executor = load_agent_executor(llm, tools, verbose=False)  # 减少verbose输出
agent = PlanAndExecute(planner=planner, executor=executor, verbose=False)

# 读取MDM-01共享域数据
df = pd.read_excel(Config.SHARED_DOMAIN_FILE)

# 修复列名编码问题
expected_columns = ['本体类', '属性', '值', '值含义', '代码', '数据类型', '属性描述', '来源文件']
if len(df.columns) == len(expected_columns):
    df.columns = expected_columns
    print("已修复shared_domain.xlsx的列名编码问题")

def process_data(df):
    """处理数据格式"""
    grouped_data = {}
    for _, row in df.iterrows():
        ontology_class = row["本体类"]
        attribute = row["属性"]
        value_str = row.get("值", "")
        meaning_str = row.get("值含义", "")

        # 处理空值
        if pd.isna(value_str) or value_str == "nan" or value_str == "null":
            value_str = ""
        if pd.isna(meaning_str) or meaning_str == "nan" or meaning_str == "null":
            meaning_str = ""

        if ontology_class not in grouped_data:
            grouped_data[ontology_class] = {}
        
        grouped_data[ontology_class][attribute] = {
            "value_str": value_str,
            "meaning_str": meaning_str
        }
    return grouped_data

def process_single_attribute(ontology_class, attribute, details):
    """处理单个属性，减少token使用"""
    try:
        # 简化的输入描述
        has_values = "有" if details['value_str'] else "无"
        has_meanings = "有" if details['meaning_str'] else "无"
        
        input_description = (
            f"本体类='{ontology_class}', 属性='{attribute}', "
            f"值{has_values}, 值含义{has_meanings}"
        )
        
        result = agent.invoke({"input": input_description})
        print(f"✓ {ontology_class}.{attribute}")
        return True
        
    except Exception as e:
        print(f"✗ {ontology_class}.{attribute}: {str(e)[:100]}")
        return False

def process_in_small_batches(data, batch_size=1):
    """更小的批次处理，避免超token"""
    total_success = 0
    total_error = 0
    
    ontology_classes = list(data.keys())
    
    for i in range(0, len(ontology_classes), batch_size):
        batch_classes = ontology_classes[i:i + batch_size]
        
        print(f"\n📦 处理批次 {i//batch_size + 1}/{len(ontology_classes)//batch_size + 1}")
        
        for ontology_class in batch_classes:
            print(f"\n🏥 处理本体类: {ontology_class}")
            attributes = data[ontology_class]
            
            for attribute, details in attributes.items():
                success = process_single_attribute(ontology_class, attribute, details)
                if success:
                    total_success += 1
                else:
                    total_error += 1
                
                # 每个属性处理后短暂暂停，避免API限制
                import time
                time.sleep(0.5)
    
    print(f"\n📊 注册完成统计:")
    print(f"✅ 成功: {total_success}")
    print(f"❌ 失败: {total_error}")
    print(f"📈 总计: {total_success + total_error}")

# 主流程
if __name__ == "__main__":
    print("🚀 开始MDM-01共享域数据注册 (优化版)")
    
    data = process_data(df)
    print(f"📋 共处理 {len(data)} 个本体类")
    
    # 使用更小的批次和简化的处理
    process_in_small_batches(data, batch_size=1)
    
    print("\n✨ 全部完成!")