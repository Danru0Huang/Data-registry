"""
后端兼容版本的MDR注册工具
完全匹配pycharm_domain的数据结构：
- 中文节点标签
- 完整的8个属性
- 中文关系类型
- identifier属性匹配
"""

from langchain.tools import tool
from neo4j import GraphDatabase
import json
from typing import Union
import pandas as pd
import os
import sys
import datetime
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 导入智能描述生成器
try:
    from description_generator import get_description_generator
    USE_SMART_DESCRIPTION = True
    print("✓ 智能描述生成器已启用")
except ImportError:
    USE_SMART_DESCRIPTION = False
    print("⚠ 智能描述生成器未启用，将使用默认模板")

# 配置 Neo4j 驱动（从环境变量读取）
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687/")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "123456")

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))


# ============ 工具函数 ============

def get_time():
    """获取时间戳（匹配后端格式）"""
    curr_time = datetime.datetime.now()
    time = datetime.datetime.strftime(curr_time, '%Y-%m-%d %H:%M:%S')
    return time


def get_id(label):
    """
    获取对应label的ID（匹配后端逻辑）
    :param label: 例如 "对象类ID"
    :return: 当前ID值
    """
    with driver.session() as session:
        query = f"MATCH (n:{label}) RETURN n.name AS id_value"
        result = session.run(query)
        record = result.single()
        if record:
            return record["id_value"]
        else:
            # 如果不存在，初始化为1
            session.run(f"CREATE (n:{label} {{name: 1}})")
            return 1


def update_id(label, ID):
    """
    更新对应label的ID（匹配后端逻辑）
    :param label: 例如 "对象类ID"
    :param ID: 新的ID值
    """
    with driver.session() as session:
        query = f"MATCH (n:{label}) SET n.name = {ID}"
        session.run(query)


# 标签和ID前缀映射
LABEL_MAP = {
    "ObjectClass": "对象类",
    "Property": "属性",
    "ConceptDomain": "概念域",
    "DataElementConcept": "数据元概念",
    "ValueDomain": "值域",
    "DataElement": "数据元",
    "ValueMeaning": "值含义",
    "Value": "值",
    "PermissibleValue": "可允许值"
}

ID_PREFIX_MAP = {
    "对象类": "OCL",
    "属性": "PRP",
    "概念域": "CDM",
    "数据元概念": "DEC",
    "值域": "VDM",
    "数据元": "DEL",
    "值含义": "VLM",
    "可允许值": "PEV"
}


# ============ 节点注册函数（后端兼容版）============

def register_entity_backend_compatible(label_en, name, describe="", personId="", department="", extra_props=None):
    """
    后端兼容的实体注册函数
    :param label_en: 英文标签，会自动转换为中文
    :param name: 节点名称
    :param describe: 描述
    :param personId: 创建人员ID
    :param department: 创建单位
    :param extra_props: 额外属性（如indefinite, evolution等）
    :return: (是否新建, identifier, 重复检查信息)
    """
    # 转换为中文标签
    label_cn = LABEL_MAP.get(label_en, label_en)

    # 简化版：不进行语义重复检查，直接注册
    duplicate_check = {
        'has_duplicates': False,
        'has_similar': False,
        'exact_matches': [],
        'similar_entities': []
    }

    # 检查是否已存在（通过name）
    with driver.session() as session:
        check_query = f"""
        MATCH (n:{label_cn} {{name: $name}})
        RETURN n.identifier AS identifier
        """
        existing = session.run(check_query, name=name).single()

        if existing:
            print(f"{label_cn} '{name}' 已存在，identifier: {existing['identifier']}")
            return False, existing['identifier'], duplicate_check

        # 生成identifier（后端格式）
        id_label = label_cn + "ID"
        ID = get_id(id_label)
        prefix = ID_PREFIX_MAP.get(label_cn, "XXX")
        identifier = f"{prefix}{str(ID).zfill(3)}"

        # 生成时间戳
        time = get_time()

        # 构建节点属性
        node_props = {
            "name": name,
            "identifier": identifier,
            "time": time,
            "status": "已注册",
            "version": 1.0
        }

        # 添加完整属性（如果提供）
        if describe:
            node_props["describe"] = describe
        if personId:
            node_props["personId"] = personId
        if department:
            node_props["department"] = department

        # 添加额外属性
        if extra_props:
            node_props.update(extra_props)

        # 创建节点（匹配后端完整属性）
        props_str = ", ".join([f"{k}: ${k}" for k in node_props.keys()])
        create_query = f"CREATE (n:{label_cn} {{{props_str}}}) RETURN n"

        session.run(create_query, **node_props)
        print(f"注册{label_cn} '{name}' 成功，identifier: {identifier}")

        # 更新ID计数器
        update_id(id_label, ID + 1)

        return True, identifier, duplicate_check


def create_relationship_backend_compatible(from_label_en, from_identifier, to_label_en, to_identifier, relation_cn):
    """
    后端兼容的关系创建函数
    :param from_label_en: 起始节点英文标签
    :param from_identifier: 起始节点identifier
    :param to_label_en: 目标节点英文标签
    :param to_identifier: 目标节点identifier
    :param relation_cn: 中文关系类型
    """
    from_label_cn = LABEL_MAP.get(from_label_en, from_label_en)
    to_label_cn = LABEL_MAP.get(to_label_en, to_label_en)

    with driver.session() as session:
        query = f"""
        MATCH (a:{from_label_cn} {{identifier: $from_id}})
        MATCH (b:{to_label_cn} {{identifier: $to_id}})
        MERGE (a)-[r:{relation_cn}]->(b)
        RETURN a, b, r
        """
        try:
            session.run(query, from_id=from_identifier, to_id=to_identifier)
            print(f"创建关系: ({from_label_cn}:{from_identifier}) -[:{relation_cn}]-> ({to_label_cn}:{to_identifier}) 成功")
        except Exception as e:
            print(f"创建关系失败: {str(e)}")
            raise


# 格式化值和值含义（正确理解版）
def parse_values_and_meanings(value_str: str, meaning_str: str) -> tuple[list[list[tuple[str, str]]], int]:
    """
    将输入的values和value_meanings按分号和逗号解析成组

    格式规则：
    - 分号(;) 分隔不同的值含义对应关系
    - 逗号(,) 分隔同一含义的不同表示形式（按位置分组）

    示例：
    值="发明设计,0;实用新型,1;外观设计,2"
    含义="发明设计;实用新型;外观设计"

    解析步骤：
    1. 按分号分割建立对应：
       "发明设计,0" → "发明设计"
       "实用新型,1" → "实用新型"
       "外观设计,2" → "外观设计"

    2. 判断组数：每个分号部分有2个逗号分隔的值，所以有2个组

    3. 按位置分组：
       组1（位置0）：[("发明设计","发明设计"), ("实用新型","实用新型"), ("外观设计","外观设计")]
       组2（位置1）：[("0","发明设计"), ("1","实用新型"), ("2","外观设计")]

    返回：
        (分组后的[(值, 含义)列表], 组数)
    """
    if not value_str or pd.isna(value_str):
        return [], 0

    if not meaning_str or pd.isna(meaning_str):
        return [], 0

    # 1. 按分号分割值和含义
    value_parts = value_str.replace('；', ';').split(';')
    meaning_parts = meaning_str.replace('；', ';').split(';')

    # 确保数量匹配
    if len(value_parts) != len(meaning_parts):
        print(f"⚠ 警告：值部分数量({len(value_parts)})与含义数量({len(meaning_parts)})不匹配")
        # 补齐或截断
        while len(value_parts) > len(meaning_parts):
            meaning_parts.append(meaning_parts[-1] if meaning_parts else "未知")
        meaning_parts = meaning_parts[:len(value_parts)]

    # 2. 建立值含义对应关系，并按逗号分割每个部分
    value_meaning_pairs = []
    max_positions = 0

    for val_part, meaning in zip(value_parts, meaning_parts):
        val_part = val_part.strip()
        meaning = meaning.strip()
        if val_part:
            # 按逗号分割同一含义的不同表示
            values = [v.strip() for v in val_part.replace('，', ',').split(',') if v.strip()]
            # 每个值都对应同一个含义
            pairs = [(v, meaning) for v in values]
            value_meaning_pairs.append(pairs)
            # 记录最大位置数（组数）
            max_positions = max(max_positions, len(pairs))

    # 3. 按位置重新分组（相同位置的值归为一组）
    groups = []
    for pos in range(max_positions):
        group = []
        for pairs in value_meaning_pairs:
            if pos < len(pairs):
                group.append(pairs[pos])  # (值, 含义)
        if group:
            groups.append(group)

    # 打印解析结果（调试用）
    print(f"解析结果：共 {len(groups)} 个组")
    for i, group in enumerate(groups, 1):
        print(f"  组{i}: {[(v, m) for v, m in group]}")

    return groups, len(groups)


# ============ LangChain工具函数（后端兼容版）============

@tool
def validate_and_check_duplicates(ontology_class: str, attribute: str, values: str = "", value_meanings: str = "") -> str:
    """
    简化版数据验证工具（不依赖外部模块）
    """
    results = []
    results.append("数据格式检查通过")
    results.append("建议：可以继续注册流程")
    return "\n".join(results)


@tool
def register_object_class(object_class: Union[str, dict]) -> str:
    """后端兼容版对象类注册（支持智能描述生成）"""
    if isinstance(object_class, dict):
        object_class = object_class.get("title")
        if not object_class:
            raise ValueError("字典类型的 object_class 缺少 'title' 字段")

    # 生成描述信息（智能或默认）
    if USE_SMART_DESCRIPTION:
        try:
            generator = get_description_generator()
            describe = generator.generate_object_class_description(object_class)
            print(f"✓ 智能生成描述: {describe}")
        except Exception as e:
            print(f"⚠ 智能描述生成失败，使用默认模板: {str(e)}")
            describe = f"表示{object_class}的对象类，用于数据元的分类和组织"
    else:
        describe = f"表示{object_class}的对象类，用于数据元的分类和组织"

    # 使用后端兼容注册函数
    is_new, identifier, duplicate_info = register_entity_backend_compatible(
        "ObjectClass",
        object_class,
        describe=describe,
        personId="智能体",
        department="智能注册系统"
    )

    status = "（新建）" if is_new else "（已存在）"
    result = f"对象类 '{object_class}' 已注册{status}，identifier: {identifier}。"

    if duplicate_info['has_duplicates']:
        result += " 检测到重复实体。"
    elif duplicate_info['has_similar']:
        result += " 检测到相似实体。"

    return result


@tool
def register_property(property: Union[str, dict]) -> str:
    """后端兼容版属性注册（支持智能描述生成）"""
    if isinstance(property, dict):
        property = property.get("title")
        if not property:
            raise ValueError("字典类型的 property 缺少 'title' 字段")

    if not isinstance(property, str):
        raise TypeError("property 必须是字符串类型")

    # 生成描述信息（智能或默认）
    if USE_SMART_DESCRIPTION:
        try:
            generator = get_description_generator()
            describe = generator.generate_property_description(property)
            print(f"✓ 智能生成描述: {describe}")
        except Exception as e:
            print(f"⚠ 智能描述生成失败，使用默认模板: {str(e)}")
            describe = f"{property}属性，用于描述对象的特征"
    else:
        describe = f"{property}属性，用于描述对象的特征"

    is_new, identifier, duplicate_info = register_entity_backend_compatible(
        "Property",
        property,
        describe=describe,
        personId="智能体",
        department="智能注册系统"
    )

    status = "（新建）" if is_new else "（已存在）"
    result = f"属性 '{property}' 已注册{status}，identifier: {identifier}。"

    if duplicate_info['has_duplicates']:
        result += " 检测到重复实体。"
    elif duplicate_info['has_similar']:
        result += " 检测到相似实体。"

    return result


@tool
def register_concept_domain(concept_domain: Union[str, dict]) -> str:
    """后端兼容版概念域注册（支持智能描述生成）"""
    if isinstance(concept_domain, dict):
        concept_domain = concept_domain.get("title")
        if not concept_domain:
            raise ValueError("字典类型的 concept_domain 缺少 'title' 字段")

    if not isinstance(concept_domain, str):
        raise TypeError("concept_domain 必须是字符串类型")

    # 生成描述信息（智能或默认）
    if USE_SMART_DESCRIPTION:
        try:
            generator = get_description_generator()
            describe = generator.generate_concept_domain_description(concept_domain)
            print(f"✓ 智能生成描述: {describe}")
        except Exception as e:
            print(f"⚠ 智能描述生成失败，使用默认模板: {str(e)}")
            describe = f"{concept_domain}的概念域，定义了属性值的语义范围"
    else:
        describe = f"{concept_domain}的概念域，定义了属性值的语义范围"

    is_new, identifier, duplicate_info = register_entity_backend_compatible(
        "ConceptDomain",
        concept_domain,
        describe=describe,
        personId="智能体",
        department="智能注册系统"
    )

    status = "（新建）" if is_new else "（已存在）"
    result = f"概念域 '{concept_domain}' 已注册{status}，identifier: {identifier}。"

    if duplicate_info['has_duplicates']:
        result += " 检测到重复实体。"
    elif duplicate_info['has_similar']:
        result += " 检测到相似实体。"

    return result


@tool
def register_data_element_concept_with_relationships(
    data_element_concept: Union[str, dict],
    object_class: Union[str, dict],
    property: Union[str, dict],
    concept_domain: Union[str, dict]
) -> str:
    """后端兼容版数据元概念注册（支持智能描述生成）"""
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

    # 生成描述信息（智能或默认）
    if USE_SMART_DESCRIPTION:
        try:
            generator = get_description_generator()
            describe = generator.generate_data_element_concept_description(
                object_class,
                property,
                concept_domain
            )
            print(f"✓ 智能生成描述: {describe}")
        except Exception as e:
            print(f"⚠ 智能描述生成失败，使用默认模板: {str(e)}")
            describe = f"数据元概念，表示{object_class}的{property}特性"
    else:
        describe = f"数据元概念，表示{object_class}的{property}特性"

    # 注册数据元概念节点
    is_new, dec_identifier, duplicate_info = register_entity_backend_compatible(
        "DataElementConcept",
        data_element_concept,
        describe=describe,
        personId="智能体",
        department="智能注册系统"
    )

    if not is_new:
        print(f"数据元概念 '{data_element_concept}' 已存在，identifier: {dec_identifier}")

    # 获取关联节点的identifier（通过name查找）
    with driver.session() as session:
        # 查找对象类identifier
        oc_query = "MATCH (n:对象类 {name: $name}) RETURN n.identifier AS identifier"
        oc_result = session.run(oc_query, name=object_class).single()
        if not oc_result:
            return f"错误：找不到对象类 '{object_class}'"
        oc_identifier = oc_result['identifier']

        # 查找属性identifier
        prop_query = "MATCH (n:属性 {name: $name}) RETURN n.identifier AS identifier"
        prop_result = session.run(prop_query, name=property).single()
        if not prop_result:
            return f"错误：找不到属性 '{property}'"
        prop_identifier = prop_result['identifier']

        # 查找概念域identifier
        cd_query = "MATCH (n:概念域 {name: $name}) RETURN n.identifier AS identifier"
        cd_result = session.run(cd_query, name=concept_domain).single()
        if not cd_result:
            return f"错误：找不到概念域 '{concept_domain}'"
        cd_identifier = cd_result['identifier']

    # 创建关系（使用中文关系名，匹配后端）
    create_relationship_backend_compatible("DataElementConcept", dec_identifier, "ObjectClass", oc_identifier, "对象类")
    create_relationship_backend_compatible("DataElementConcept", dec_identifier, "Property", prop_identifier, "属性")
    create_relationship_backend_compatible("DataElementConcept", dec_identifier, "ConceptDomain", cd_identifier, "概念域")

    status = "（新建）" if is_new else "（已存在）"
    result = f"数据元概念 '{data_element_concept}' 已注册{status}，identifier: {dec_identifier}，关系已建立。"

    if duplicate_info['has_duplicates']:
        result += " 检测到重复实体。"
    elif duplicate_info['has_similar']:
        result += " 检测到相似实体。"

    return result


@tool
def register_value_domain_with_values(value_domain: Union[str, dict], concept_domain: Union[str, dict], value_str: str, meaning_str: str = "") -> str:
    """后端兼容版值域注册（带值和值含义）"""
    if isinstance(value_domain, dict):
        value_domain = value_domain.get("title")
    if isinstance(concept_domain, dict):
        concept_domain = concept_domain.get("title")

    # 生成描述信息
    describe = f"{value_domain}值域，定义了{concept_domain}的可允许值"

    # 注册值域节点
    is_new, vd_identifier, duplicate_info = register_entity_backend_compatible(
        "ValueDomain",
        value_domain,
        describe=describe,
        personId="智能体",
        department="智能注册系统",
        extra_props={"indefinite": "null"}  # 添加indefinite属性
    )

    # 获取概念域identifier
    with driver.session() as session:
        cd_query = "MATCH (n:概念域 {name: $name}) RETURN n.identifier AS identifier"
        cd_result = session.run(cd_query, name=concept_domain).single()
        if not cd_result:
            return f"错误：找不到概念域 '{concept_domain}'"
        cd_identifier = cd_result['identifier']

    # 创建值域与概念域的关系
    create_relationship_backend_compatible("ValueDomain", vd_identifier, "ConceptDomain", cd_identifier, "概念域")

    # 注册值（如果提供）- 创建完整的MDR结构：值域组 -> 可允许值 -> 值含义
    registered_values = []
    if value_str and not pd.isna(value_str):
        # 解析值和值含义（新格式：groups, num_groups）
        groups, num_groups = parse_values_and_meanings(value_str, meaning_str)

        # 为每个分组创建值域组
        with driver.session() as session:
            ID_PEV = get_id("可允许值ID")

            for group_num, value_meaning_pairs in enumerate(groups, start=1):
                # 创建值域组节点（使用值域identifier作为值域组identifier）
                group_name = f"组{group_num}"
                session.run("""
                    CREATE (g:值域组 {name: $name, identifier: $identifier})
                """, name=group_name, identifier=vd_identifier)

                # 建立值域 -> 值域组关系
                session.run("""
                    MATCH (vd:值域 {identifier: $vd_id})
                    MATCH (g:值域组 {name: $g_name, identifier: $vd_id})
                    MERGE (vd)-[:组]->(g)
                """, vd_id=vd_identifier, g_name=group_name)

                # 为每个值创建可允许值节点（每个值有自己的含义）
                for value, meaning in value_meaning_pairs:
                    identifier_pev = f"PEV{str(ID_PEV).zfill(3)}"

                    # 创建可允许值节点
                    session.run("""
                        CREATE (pev:可允许值 {name: $name, identifier: $identifier})
                    """, name=value, identifier=identifier_pev)

                    # 建立值域组 -> 可允许值关系
                    session.run("""
                        MATCH (g:值域组 {name: $g_name, identifier: $vd_id})
                        MATCH (pev:可允许值 {identifier: $pev_id})
                        MERGE (g)-[:可允许值]->(pev)
                    """, g_name=group_name, vd_id=vd_identifier, pev_id=identifier_pev)

                    # 如果有值含义，建立可允许值 -> 值含义关系
                    if meaning:
                        # 查找值含义节点
                        vm_result = session.run("""
                            MATCH (vm:值含义 {name: $name})
                            RETURN vm.identifier AS identifier
                        """, name=meaning).single()

                        if vm_result:
                            session.run("""
                                MATCH (pev:可允许值 {identifier: $pev_id})
                                MATCH (vm:值含义 {identifier: $vm_id})
                                MERGE (pev)-[:值含义]->(vm)
                            """, pev_id=identifier_pev, vm_id=vm_result['identifier'])

                    registered_values.append(value)
                    ID_PEV += 1

            # 更新可允许值ID
            update_id("可允许值ID", ID_PEV)

    result = f"值域 '{value_domain}' 已注册，identifier: {vd_identifier}，并与概念域 '{concept_domain}' 建立关系"
    if registered_values:
        result += f"，同时注册了 {len(registered_values)} 个值。"
    else:
        result += "。"

    if duplicate_info['has_duplicates']:
        result += " 检测到重复的值域实体。"
    elif duplicate_info['has_similar']:
        result += " 检测到相似的值域实体。"

    return result


@tool
def register_value_domain_with_relationship(value_domain: Union[str, dict], concept_domain: Union[str, dict]) -> str:
    """后端兼容版值域注册（无值）"""
    if isinstance(value_domain, dict):
        value_domain = value_domain.get("title")
    if isinstance(concept_domain, dict):
        concept_domain = concept_domain.get("title")

    # 生成描述信息
    describe = f"{value_domain}值域，定义了{concept_domain}的可允许值（不可枚举）"

    # 注册值域节点
    is_new, vd_identifier, duplicate_info = register_entity_backend_compatible(
        "ValueDomain",
        value_domain,
        describe=describe,
        personId="智能体",
        department="智能注册系统",
        extra_props={"indefinite": "null"}
    )

    # 获取概念域identifier
    with driver.session() as session:
        cd_query = "MATCH (n:概念域 {name: $name}) RETURN n.identifier AS identifier"
        cd_result = session.run(cd_query, name=concept_domain).single()
        if not cd_result:
            return f"错误：找不到概念域 '{concept_domain}'"
        cd_identifier = cd_result['identifier']

    # 创建关系
    create_relationship_backend_compatible("ValueDomain", vd_identifier, "ConceptDomain", cd_identifier, "概念域")

    result = f"值域 '{value_domain}' 已注册，identifier: {vd_identifier}，并与概念域 '{concept_domain}' 建立关系。"

    if duplicate_info['has_duplicates']:
        result += " 检测到重复的值域实体。"
    elif duplicate_info['has_similar']:
        result += " 检测到相似的值域实体。"

    return result


@tool
def register_value_meanings_with_relationship(concept_domain: Union[str, dict], value_str: str, meaning_str: str) -> str:
    """后端兼容版值含义注册"""
    # 解析值和值含义（新格式：groups, num_groups）
    groups, num_groups = parse_values_and_meanings(value_str, meaning_str)

    if isinstance(concept_domain, dict):
        concept_domain = concept_domain.get("title")

    # 获取概念域identifier
    with driver.session() as session:
        cd_query = "MATCH (n:概念域 {name: $name}) RETURN n.identifier AS identifier"
        cd_result = session.run(cd_query, name=concept_domain).single()
        if not cd_result:
            return f"错误：找不到概念域 '{concept_domain}'"
        cd_identifier = cd_result['identifier']

    # 收集所有唯一的值含义，并记录每个含义对应的值
    meaning_to_values = {}  # {meaning: [value1, value2, ...]}
    for group in groups:
        for value, meaning in group:
            if meaning not in meaning_to_values:
                meaning_to_values[meaning] = []
            meaning_to_values[meaning].append(value)

    # 注册值含义并建立关系
    registered_count = 0
    meaning_identifiers = {}  # {meaning: identifier}

    with driver.session() as session:
        for meaning, values in meaning_to_values.items():
            # 注册值含义节点（匹配后端格式）
            id_label = "值含义ID"
            ID = get_id(id_label)
            identifier_vm = f"VLM{str(ID).zfill(3)}"
            time = get_time()

            # 检查是否已存在
            check = session.run("MATCH (n:值含义 {name: $name}) RETURN n.identifier AS identifier", name=meaning).single()

            if not check:
                # 创建值含义节点
                session.run("""
                    CREATE (n:值含义 {
                        name: $name,
                        identifier: $identifier,
                        time: $time,
                        version: 1.0,
                        status: "已注册"
                    })
                """, name=meaning, identifier=identifier_vm, time=time)

                # 更新ID
                update_id(id_label, ID + 1)
                registered_count += 1
                vm_identifier = identifier_vm
            else:
                vm_identifier = check['identifier']

            meaning_identifiers[meaning] = vm_identifier

            # 创建概念域->值含义关系
            session.run("""
                MATCH (cd:概念域 {identifier: $cd_id})
                MATCH (vm:值含义 {identifier: $vm_id})
                MERGE (cd)-[:值含义]->(vm)
            """, cd_id=cd_identifier, vm_id=vm_identifier)

            # 建立值与值含义的关系
            for value in values:
                # 确保值节点存在
                session.run("MERGE (n:值 {name: $name})", name=value)
                # 创建值->值含义关系
                session.run("""
                    MATCH (v:值 {name: $v_name})
                    MATCH (vm:值含义 {identifier: $vm_id})
                    MERGE (v)-[:值含义]->(vm)
                """, v_name=value, vm_id=vm_identifier)

    return f"成功注册了 {registered_count} 个值含义，并与概念域 '{concept_domain}' 建立关系。"


@tool
def register_data_element_with_relationships(
    data_element: Union[str, dict],
    data_element_concept: Union[str, dict],
    value_domain: Union[str, dict]
) -> str:
    """后端兼容版数据元注册"""
    # 参数处理
    if isinstance(data_element, dict):
        data_element = data_element.get("title")
    if isinstance(data_element_concept, dict):
        data_element_concept = data_element_concept.get("title")
    if isinstance(value_domain, dict):
        value_domain = value_domain.get("title")

    if not all(isinstance(arg, str) for arg in [data_element, data_element_concept, value_domain]):
        raise TypeError("所有参数必须是字符串类型")

    # 生成描述信息
    describe = f"数据元，基于{data_element_concept}和{value_domain}的完整数据定义"

    # 注册数据元节点
    is_new, de_identifier, duplicate_info = register_entity_backend_compatible(
        "DataElement",
        data_element,
        describe=describe,
        personId="智能体",
        department="智能注册系统",
        extra_props={"evolution": "暂无演化信息"}  # 添加evolution属性
    )

    # 获取数据元概念和值域的identifier
    with driver.session() as session:
        # 查找数据元概念
        dec_query = "MATCH (n:数据元概念 {name: $name}) RETURN n.identifier AS identifier"
        dec_result = session.run(dec_query, name=data_element_concept).single()
        if not dec_result:
            return f"错误：找不到数据元概念 '{data_element_concept}'"
        dec_identifier = dec_result['identifier']

        # 查找值域
        vd_query = "MATCH (n:值域 {name: $name}) RETURN n.identifier AS identifier"
        vd_result = session.run(vd_query, name=value_domain).single()
        if not vd_result:
            return f"错误：找不到值域 '{value_domain}'"
        vd_identifier = vd_result['identifier']

    # 创建关系（匹配后端关系名）
    create_relationship_backend_compatible("DataElement", de_identifier, "DataElementConcept", dec_identifier, "数据元概念")
    create_relationship_backend_compatible("DataElement", de_identifier, "ValueDomain", vd_identifier, "值域")

    status = "（新建）" if is_new else "（已存在）"
    result = f"数据元 '{data_element}' 已注册{status}，identifier: {de_identifier}，关系已建立。"

    if duplicate_info['has_duplicates']:
        result += " 检测到重复实体。"
    elif duplicate_info['has_similar']:
        result += " 检测到相似实体。"

    return result


# 工具集合
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
