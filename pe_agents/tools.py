from langchain.tools import tool
from neo4j import GraphDatabase
import json
from typing import Union
import pandas as pd
import os
import sys
from dotenv import load_dotenv

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from Data_pre.data_quality_validator import DataQualityValidator
from Mapping.semantic_matcher import SemanticMatcher

# 加载环境变量
load_dotenv()

# 配置 Neo4j 驱动（从环境变量读取）
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687/")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "123456")  

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

# 初始化算法模块
data_validator = DataQualityValidator()
semantic_matcher = SemanticMatcher(driver, similarity_threshold=0.7)

# ID生成器
class IDGenerator:
    @staticmethod
    def generate_id(prefix):
        with driver.session() as session:
            query = f"""
            MATCH (n:{prefix}ID)
            RETURN n.name AS count
            """
            result = session.run(query)
            current_count = result.single()
            if current_count:
                count = int(current_count["count"])
            else:
                session.run(f"CREATE (n:{prefix}ID {{name: 1}})")
                count = 1

            session.run(f"MERGE (n:{prefix}ID) SET n.name = $new_count", new_count=count + 1)
        return f"{prefix}{count:03d}"

# 节点注册函数
def register_entity(label, name):
    """
    通用注册函数，用于创建节点，避免重复注册。
    返回值：是否新注册节点 (True/False)
    """
    with driver.session() as session:
        # 检查是否已经存在
        check_query = f"""
        MATCH (n:{label} {{name: $name}})
        RETURN n
        """
        existing_node = session.run(check_query, name=name).single()
        if existing_node:
            print(f"{label} '{name}' 已存在，跳过注册")
            return False  # 节点已存在，返回 False

        # 如果不存在，则进行注册
        unique_id = IDGenerator.generate_id(label)

        query = f"""
        CREATE (entity:{label} {{id: $id, name: $name}})
        RETURN entity
        """
        try:
            session.run(query, id=unique_id, name=name)
            print(f"注册{label} '{name}' 成功，ID: {unique_id}")
            return True  # 新注册节点，返回 True
        except Exception as e:
            print(f"注册{label} '{name}' 失败: {str(e)}")
            raise

def register_entity_with_duplicate_check(label, name):
    """
    增强的实体注册函数，集成重复检查
    """
    # 1. 首先进行重复检查
    duplicate_check = semantic_matcher.check_duplicate_before_registration(name, label)
    
    if duplicate_check['has_duplicates']:
        exact_matches = duplicate_check['exact_matches']
        print(f"警告：发现重复实体 '{name}' (类型: {label})")
        for match in exact_matches:
            print(f"  - 相似度 {match['similarity_score']}: {match['entity']['name']}")
        
        # 对于几乎完全相同的实体，跳过注册
        if any(match['similarity_score'] >= 0.95 for match in exact_matches):
            print(f"实体 '{name}' 几乎完全重复，跳过注册")
            return False, duplicate_check
    
    elif duplicate_check['has_similar']:
        print(f"提示：发现相似实体 '{name}' (类型: {label})")
        for similar in duplicate_check['similar_entities'][:3]:  # 显示前3个相似实体
            print(f"  - 相似度 {similar['similarity_score']}: {similar['entity']['name']}")
    
    # 2. 进行实际注册
    with driver.session() as session:
        # 检查是否已经存在
        check_query = f"""
        MATCH (n:{label} {{name: $name}})
        RETURN n
        """
        existing_node = session.run(check_query, name=name).single()
        if existing_node:
            print(f"{label} '{name}' 已存在，跳过注册")
            return False, duplicate_check

        # 如果不存在，则进行注册
        unique_id = IDGenerator.generate_id(label)

        query = f"""
        CREATE (entity:{label} {{id: $id, name: $name}})
        RETURN entity
        """
        try:
            session.run(query, id=unique_id, name=name)
            print(f"注册{label} '{name}' 成功，ID: {unique_id}")
            return True, duplicate_check
        except Exception as e:
            print(f"注册{label} '{name}' 失败: {str(e)}")
            raise

# 创建关系
def create_relationship(from_label, from_name, to_label, to_name, relation):
    """
    创建两个节点之间的关系，避免重复创建。
    """
    with driver.session() as session:
        query = f"""
        MATCH (a:{from_label} {{name: $from_name}})
        MATCH (b:{to_label} {{name: $to_name}})
        MERGE (a)-[r:{relation}]->(b)
        RETURN a, b, r
        """
        try:
            session.run(query, from_name=from_name, to_name=to_name)
            print(f"创建关系: ({from_label}:{from_name}) -[:{relation}]-> ({to_label}:{to_name}) 成功")
        except Exception as e:
            print(f"创建关系失败: {str(e)}")
            raise

# 格式化值和值含义
def parse_values_and_meanings(value_str: str, meaning_str: str) -> tuple[list[list[str]], list[str]]:
    """
    将输入的values和value_meanings按分号分组，然后进行转置操作

    例如：values="发明设计，0；实用新型，1；外观设计，2"
         meanings="专利类型名称；专利类型代码"

    解析过程：
    1. 按分号分割: ["发明设计，0", "实用新型，1", "外观设计，2"]
    2. 每组按逗号分割: [["发明设计", "0"], ["实用新型", "1"], ["外观设计", "2"]]
    3. 转置操作: [["发明设计", "实用新型", "外观设计"], ["0", "1", "2"]]
    4. 对应含义: ["专利类型名称", "专利类型代码"]

    最终结果：
    - 组1: ["发明设计", "实用新型", "外观设计"] → "专利类型名称"
    - 组2: ["0", "1", "2"] → "专利类型代码"

    注意：数据中可能使用中文分号"；"和中文逗号"，"

    支持多种格式：
    1. "显示值,代码;显示值,代码" - 标准格式（会进行转置）
    2. "值1;值2;值3" - 只有分号分隔的单个值（不转置）
    3. "值1,值2;值3,值4" - 混合格式（会进行转置）
    """
    if not value_str or pd.isna(value_str):
        return [], []

    if not meaning_str or pd.isna(meaning_str):
        return [], []

    # 解析值组：按分号分割组，每组内按逗号分割单个值
    # 处理中文分号和英文分号
    value_groups = value_str.replace('；', ';').split(';')
    grouped_values = []
    for group in value_groups:
        if group.strip():
            # 处理中文逗号和英文逗号
            values = [v.strip() for v in group.replace('，', ',').split(',') if v.strip()]
            if values:
                grouped_values.append(values)

    # 转置操作：将 [["发明设计", "0"], ["实用新型", "1"], ["外观设计", "2"]]
    # 转换为 [["发明设计", "实用新型", "外观设计"], ["0", "1", "2"]]
    transposed = False  # 标记是否进行了转置
    if grouped_values:
        # 检查是否所有组的长度一致（如果不一致，说明数据不规范，不进行转置）
        first_length = len(grouped_values[0])
        if all(len(group) == first_length for group in grouped_values) and first_length > 1:
            # 所有组长度一致且大于1，进行转置
            transposed_values = []
            for i in range(first_length):
                transposed_values.append([group[i] for group in grouped_values])
            grouped_values = transposed_values
            transposed = True

    # 解析值含义：按分号分割
    # 处理中文分号和英文分号
    value_meanings = [meaning.strip() for meaning in meaning_str.replace('；', ';').split(';') if meaning.strip()]

    # 确保值组和含义数量匹配
    # 如果进行了转置，含义数量应该等于每组的长度（即枚举项数量）
    # 如果没有转置，含义数量应该等于组的数量
    if grouped_values:
        if transposed:
            # 转置后，含义数量应该等于每组的长度
            expected_meaning_count = len(grouped_values[0]) if grouped_values else 0
        else:
            # 未转置，含义数量应该等于组的数量
            expected_meaning_count = len(grouped_values)

        # 如果含义数量少于期望数量，用最后一个含义填充
        while len(value_meanings) < expected_meaning_count:
            if value_meanings:
                value_meanings.append(value_meanings[-1])
            else:
                value_meanings.append("未知")

        # 如果含义数量多于期望数量，截断含义列表
        if len(value_meanings) > expected_meaning_count:
            value_meanings = value_meanings[:expected_meaning_count]

    return grouped_values, value_meanings

# 数据质量验证和重复检查工具
@tool
def validate_and_check_duplicates(ontology_class: str, attribute: str, values: str = "", value_meanings: str = "") -> str:
    """
    执行数据质量验证和重复检查的综合工具
    
    Args:
        ontology_class: 本体类名称
        attribute: 属性名称  
        values: 值字符串
        value_meanings: 值含义字符串
        
    Returns:
        验证和检查结果的详细报告
    """
    results = []
    
    # 1. 数据质量检查
    test_data = pd.DataFrame([{
        '本体类': ontology_class,
        '属性': attribute,
        '值': values,
        '值含义': value_meanings
    }])
    
    validation_result = data_validator.validate_data_batch(test_data)
    quality_score = data_validator.get_quality_score(validation_result)
    
    results.append(f"数据质量评分: {quality_score}/100")
    
    if validation_result['issues']:
        results.append(f"发现 {len(validation_result['issues'])} 个质量问题:")
        for issue in validation_result['issues']:
            results.append(f"  - {issue['severity']}: {issue['message']}")
    else:
        results.append("数据质量检查通过")
    
    # 2. 重复检查
    oc_check = semantic_matcher.check_duplicate_before_registration(ontology_class, "ObjectClass")
    prop_check = semantic_matcher.check_duplicate_before_registration(attribute, "Property")
    
    if oc_check['has_duplicates']:
        results.append(f"警告：对象类 '{ontology_class}' 存在重复实体")
    elif oc_check['has_similar']:
        results.append(f"提示：对象类 '{ontology_class}' 存在相似实体")
    
    if prop_check['has_duplicates']:
        results.append(f"警告：属性 '{attribute}' 存在重复实体")
    elif prop_check['has_similar']:
        results.append(f"提示：属性 '{attribute}' 存在相似实体")
    
    # 3. 综合建议
    if validation_result['issues'] and any(issue['severity'] == 'high' for issue in validation_result['issues']):
        results.append("建议：修复严重的数据质量问题后再进行注册")
    elif oc_check['has_duplicates'] or prop_check['has_duplicates']:
        results.append("建议：确认是否确实需要注册重复实体")
    else:
        results.append("建议：可以继续注册流程")
    
    return "\n".join(results)

# 增强版注册工具（集成重复检查）
@tool
def register_object_class(object_class: Union[str, dict]) -> str:
    """增强版对象类注册，集成重复检查"""
    if isinstance(object_class, dict):
        object_class = object_class.get("title")
        if not object_class:
            raise ValueError("字典类型的 object_class 缺少 'title' 字段")
    
    # 使用增强的注册函数
    is_new, duplicate_info = register_entity_with_duplicate_check("ObjectClass", object_class)
    
    status = "（新建）" if is_new else "（已存在）"
    result = f"对象类 '{object_class}' 已注册{status}。"
    
    # 添加重复检查信息
    if duplicate_info['has_duplicates']:
        result += " 检测到重复实体。"
    elif duplicate_info['has_similar']:
        result += " 检测到相似实体。"
    
    return result

@tool
def register_property(property: Union[str, dict]) -> str:
    """增强版属性注册，集成重复检查"""
    if isinstance(property, dict):
        property = property.get("title")
        if not property:
            raise ValueError("字典类型的 property 缺少 'title' 字段")
    
    if not isinstance(property, str):
        raise TypeError("property 必须是字符串类型")
    
    # 使用增强的注册函数
    is_new, duplicate_info = register_entity_with_duplicate_check("Property", property)
    
    status = "（新建）" if is_new else "（已存在）"
    result = f"属性 '{property}' 已注册{status}。"
    
    # 添加重复检查信息
    if duplicate_info['has_duplicates']:
        result += " 检测到重复实体。"
    elif duplicate_info['has_similar']:
        result += " 检测到相似实体。"
    
    return result

@tool
def register_concept_domain(concept_domain: Union[str, dict]) -> str:
    """增强版概念域注册，集成重复检查"""
    if isinstance(concept_domain, dict):
        concept_domain = concept_domain.get("title")
        if not concept_domain:
            raise ValueError("字典类型的 concept_domain 缺少 'title' 字段")
    
    if not isinstance(concept_domain, str):
        raise TypeError("concept_domain 必须是字符串类型")
    
    # 使用增强的注册函数
    is_new, duplicate_info = register_entity_with_duplicate_check("ConceptDomain", concept_domain)
    
    status = "（新建）" if is_new else "（已存在）"
    result = f"概念域 '{concept_domain}' 已注册{status}。"
    
    # 添加重复检查信息
    if duplicate_info['has_duplicates']:
        result += " 检测到重复实体。"
    elif duplicate_info['has_similar']:
        result += " 检测到相似实体。"
    
    return result

@tool
def register_data_element_concept_with_relationships(data_element_concept: Union[str, dict], 
                                                     object_class: Union[str, dict], 
                                                     property: Union[str, dict], 
                                                     concept_domain: Union[str, dict], 
                                                     ) -> str:
    """增强版数据元概念注册"""
    # 参数处理
    if isinstance(data_element_concept, dict):
        data_element_concept = data_element_concept.get("title")
    if isinstance(object_class, dict):
        object_class = object_class.get("title")
    if isinstance(property, dict):
        property = property.get("title")
    if isinstance(concept_domain, dict):
        concept_domain = concept_domain.get("title")
    
    if not all(isinstance(arg, str) for arg in [data_element_concept, object_class, property, concept_domain]):
        raise TypeError("所有参数必须是字符串类型")
    
    # 使用增强的注册函数
    is_new, duplicate_info = register_entity_with_duplicate_check("DataElementConcept", data_element_concept)
    
    if not is_new:
        print(f"数据元概念 '{data_element_concept}' 已存在，跳过节点注册，继续创建关系")

    # 创建关系
    create_relationship("DataElementConcept", data_element_concept, "ObjectClass", object_class, "HAS_OBJECT_CLASS")
    create_relationship("DataElementConcept", data_element_concept, "Property", property, "HAS_PROPERTY")
    create_relationship("DataElementConcept", data_element_concept, "ConceptDomain", concept_domain, "HAS_CONCEPT_DOMAIN")

    status = "（新建）" if is_new else "（已存在）"
    result = f"数据元概念 '{data_element_concept}' 已注册{status}，关系已建立。"
    
    if duplicate_info['has_duplicates']:
        result += " 检测到重复实体。"
    elif duplicate_info['has_similar']:
        result += " 检测到相似实体。"
    
    return result

@tool
def register_value_domain_with_values(value_domain: Union[str, dict], concept_domain: Union[str, dict], value_str: str) -> str:
    """增强版值域注册（带值）"""
    # 处理输入
    if isinstance(value_domain, dict):
        value_domain = value_domain.get("title")
    if isinstance(concept_domain, dict):
        concept_domain = concept_domain.get("title")
    
    if not value_str or pd.isna(value_str):
        grouped_values = []
    else:
        value_str_processed = value_str.replace('；', ';').replace('，', ',')
        value_groups = value_str_processed.split(';')
        grouped_values = []
        for group in value_groups:
            if group.strip():
                values = [v.strip() for v in group.split(',') if v.strip()]
                if values:
                    grouped_values.append(values)

    # 使用增强的注册函数
    is_new_value_domain, duplicate_info = register_entity_with_duplicate_check("ValueDomain", value_domain)
    if is_new_value_domain:
        create_relationship("ValueDomain", value_domain, "ConceptDomain", concept_domain, "BASED_ON")

    # 注册值及其关系
    registered_values = []
    for group in grouped_values:
        for value in group:
            is_new_value, _ = register_entity_with_duplicate_check("Value", value)
            if is_new_value:
                create_relationship("ValueDomain", value_domain, "Value", value, "INCLUDE")
                registered_values.append(value)
            else:
                create_relationship("ValueDomain", value_domain, "Value", value, "INCLUDE")
                registered_values.append(value)
    
    result = f"值域 '{value_domain}' 已注册，并与概念域 '{concept_domain}' 建立关系，同时注册了 {len(registered_values)} 个值：{', '.join(registered_values)}。"
    
    if duplicate_info['has_duplicates']:
        result += " 检测到重复的值域实体。"
    elif duplicate_info['has_similar']:
        result += " 检测到相似的值域实体。"
    
    return result

@tool
def register_value_domain_with_relationship(value_domain: Union[str, dict], concept_domain: Union[str, dict]) -> str:
    """增强版值域注册（无值）"""
    # 处理输入
    if isinstance(value_domain, dict):
        value_domain = value_domain.get("title")
    if isinstance(concept_domain, dict):
        concept_domain = concept_domain.get("title")
    
    # 使用增强的注册函数
    is_new_value_domain, duplicate_info = register_entity_with_duplicate_check("ValueDomain", value_domain)
    if is_new_value_domain:
        create_relationship("ValueDomain", value_domain, "ConceptDomain", concept_domain, "BASED_ON")
    
    result = f"值域 '{value_domain}' 已注册，并与概念域 '{concept_domain}' 建立关系。"
    
    if duplicate_info['has_duplicates']:
        result += " 检测到重复的值域实体。"
    elif duplicate_info['has_similar']:
        result += " 检测到相似的值域实体。"
    
    return result

@tool  
def register_value_meanings_with_relationship(concept_domain: Union[str, dict], value_str: str, meaning_str: str) -> str:
    """增强版值含义注册"""
    # 格式化值和值含义
    grouped_values, value_meanings = parse_values_and_meanings(value_str, meaning_str)

    # 输入验证
    if isinstance(concept_domain, dict):
        concept_domain = concept_domain.get("title")
    
    # 注册值含义
    # 新逻辑：遍历每个含义（按位置索引），每个含义关联所有组在该位置的值
    # 例如：组1=["发明设计","实用新型","外观设计"], 组2=["0","1","2"], 含义=["发明设计","实用新型","外观设计"]
    #      含义[0]="发明设计" 关联 组1[0]="发明设计" 和 组2[0]="0"
    #      含义[1]="实用新型" 关联 组1[1]="实用新型" 和 组2[1]="1"
    #      含义[2]="外观设计" 关联 组1[2]="外观设计" 和 组2[2]="2"
    registered_count = 0
    for i, meaning in enumerate(value_meanings):
        # 注册值含义到概念域
        is_new_meaning, duplicate_info = register_entity_with_duplicate_check("ValueMeaning", meaning)
        if is_new_meaning:
            create_relationship("ConceptDomain", concept_domain, "ValueMeaning", meaning, "INCLUDE")
            registered_count += 1

        # 遍历所有组，将每组在位置 i 的值关联到这个含义
        for group in grouped_values:
            if i < len(group):  # 确保组内有该位置的值
                value = group[i]
                # 确保值已注册
                is_new_value, _ = register_entity_with_duplicate_check("Value", value)
                # 建立值与值含义的关系
                create_relationship("Value", value, "ValueMeaning", meaning, "HAS_MEANING")
    
    return f"成功注册了 {registered_count} 个值含义，并与概念域 '{concept_domain}' 建立关系。"

@tool
def register_data_element_with_relationships(data_element: Union[str, dict], 
                                             data_element_concept: Union[str, dict], 
                                             value_domain: Union[str, dict], 
                                             ) -> str:
    """增强版数据元注册"""
    # 参数处理
    if isinstance(data_element, dict):
        data_element = data_element.get("title")
    if isinstance(data_element_concept, dict):
        data_element_concept = data_element_concept.get("title")
    if isinstance(value_domain, dict):
        value_domain = value_domain.get("title")
    
    if not all(isinstance(arg, str) for arg in [data_element, data_element_concept, value_domain]):
        raise TypeError("所有参数必须是字符串类型")
    
    # 使用增强的注册函数
    is_new, duplicate_info = register_entity_with_duplicate_check("DataElement", data_element)
    
    if not is_new:
        print(f"数据元 '{data_element}' 已存在，跳过节点注册，继续创建关系")

    # 创建关系
    create_relationship("DataElement", data_element, "DataElementConcept", data_element_concept, "BASED_ON")
    create_relationship("DataElement", data_element, "ValueDomain", value_domain, "HAS_VALUE_DOMAIN")

    status = "（新建）" if is_new else "（已存在）"
    result = f"数据元 '{data_element}' 已注册{status}，关系已建立。"
    
    if duplicate_info['has_duplicates']:
        result += " 检测到重复实体。"
    elif duplicate_info['has_similar']:
        result += " 检测到相似实体。"
    
    return result

# 增强版工具集合
tools = [
    validate_and_check_duplicates, 
    register_object_class,
    register_property,
    register_concept_domain,
    register_data_element_concept_with_relationships,
    register_value_domain_with_values,
    register_value_domain_with_relationship,
    register_value_meanings_with_relationship,
    register_data_element_with_relationships,
]

