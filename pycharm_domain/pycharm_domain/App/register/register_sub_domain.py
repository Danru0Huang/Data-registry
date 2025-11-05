from werkzeug.utils import secure_filename
import pandas as pd
from ..config import graph
from py2neo import Node, Relationship
from .register_mdr import get_time


def get_id(label):
    """
    获取本次注册的标识符序号
    :param label:
    :return:
    """
    query = "MATCH (n:%s) RETURN n.name" % label
    result = graph.run(query).data()

    if not result or not result[0].get("n.name"):
        # 如果节点不存在，创建初始节点
        node = Node(label, name=1)
        graph.create(node)
        return 1

    return result[0]["n.name"]


def update_id(label, ID):
    """
    更新该类别的标识符序号
    :param label:
    :param ID:
    :return:
    """
    query = "MATCH (n:%s) SET n.name = %d" % (label, ID)
    graph.run(query)


def add_sub_domain_info(name, describe):
    """
    创建新的子域
    :param name: 子域名称
    :param describe: 子域描述信息
    :return:
    """
    node = Node("子域", name=name, describe=describe)
    graph.create(node)
    return "子域创建成功"


def normalize_value(value):
    """
    标准化值：将浮点数转换为整数字符串（如果小数部分为0）
    :param value: 原始值
    :return: 标准化后的值
    """
    # 如果是浮点数且小数部分为0，转换为整数
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return value


def register_sub_domain_of_file(file, filename):
    """
    按照MFI-3改进模型规范对该子域文件进行注册
    :param file: 文件
    :param filename: 文件名称
    :return: 注册提示信息
    """
    ID_table = get_id("表ID")
    ID_attribute = get_id("表属性ID")
    ID_attribute_value = get_id("表属性值ID")
    newFilename = filename[:-5]

    # 注册表
    identifier_table = f"TA{str(ID_table).zfill(3)}"
    node_table = Node("表", name=newFilename, identifier=identifier_table)
    graph.create(node_table)
    ID_table += 1
    update_id("表ID", ID_table)

    # 注册属性及属性值
    df = pd.read_excel(file)
    for column_name, column_data in df.items():
        # 注册表属性
        identifier_attribute = f"AN{str(ID_attribute).zfill(3)}"
        node_attribute = Node("表属性", name=column_name, identifier=identifier_attribute, evolution="")
        graph.create(node_attribute)
        ID_attribute += 1

        # 创建表与表属性关系
        relation = Relationship(node_table, "由组成", node_attribute)
        graph.create(relation)

        # 注册表属性值
        for value in column_data:
            if pd.notnull(value):
                # 标准化值（浮点数转整数）
                normalized_value = normalize_value(value)
                identifier_attribute_value = f"AV{str(ID_attribute_value).zfill(3)}"
                node_attribute_value = Node("表属性值", name=normalized_value, identifier=identifier_attribute_value)
                graph.create(node_attribute_value)
                ID_attribute_value += 1

                relation = Relationship(node_attribute, "约束值", node_attribute_value)
                graph.create(relation)

    update_id("表属性ID", ID_attribute)
    update_id("表属性值ID", ID_attribute_value)

    return identifier_table


def add_relation_between_table_and_sub_domain_info(sub_domain_name, identifier):
    """
    添加子域与表之间的联系
    :param sub_domain_name: 子域名称
    :param identifier: 表的标识符
    :return:
    """
    # 检查子域是否存在
    node_sub_domain = graph.nodes.match("子域", name=sub_domain_name).first()
    if not node_sub_domain:
        return {"success": False, "message": f"子域 '{sub_domain_name}' 不存在，请先创建子域"}

    # 检查表是否存在
    node_table = graph.nodes.match("表", identifier=identifier).first()
    if not node_table:
        return {"success": False, "message": f"表 '{identifier}' 不存在"}

    # 创建表与子域关系
    relation = Relationship(node_sub_domain, "拥有", node_table)
    graph.create(relation)

    # 注册演化信息
    table_name = node_table["name"]
    describe = node_sub_domain["describe"]
    type_ = "子域新增数据"
    cause = "注册表(" + table_name + "-" + identifier + ")"
    result = describe + "新增表(" + table_name + "-" + identifier + ")"
    time = get_time()
    user = "管理员"
    message = "变更类型:" + type_ + ";变更原因:" + cause + ";变更结果:" + result + \
              ";操作时间:" + time + ";操作人员:" + user + ";"
    node_evolution = Node("演化", name=identifier, evolution=message, table_name=table_name)
    graph.create(node_evolution)
    relation = Relationship(node_sub_domain, "演化", node_evolution)
    graph.create(relation)

    return {"success": True, "message": "创建成功"}


def add_relation_between_attribute_and_data_element_info(identifier_table,
                                                         name_attribute, identifier_data_element):
    """
    添加表属性与数据元之间的联系
    :param identifier_table: 表标识符
    :param name_attribute: 属性名称
    :param identifier_data_element: 数据元标识符
    :return:
    """
    cypher = "match(t:表) -[r2:由组成]-> (a:表属性) " \
             "where t.identifier = '%s' and a.name = '%s' " \
             "match(n:数据元) where n.identifier = '%s' " \
             "create (a) -[r:数据元]-> (n) return a, n" % (identifier_table,
                                                        name_attribute, identifier_data_element)
    result = graph.run(cypher).data()
    if result is None:
        return "关系添加失败"
    else:
        return "关系添加成功"


def add_relation_between_attribute_and_value_domain_info(sub_domain_name, identifier_table,
                                                         name_attribute, identifier_value_domain):
    """
    添加表属性与值域之间的联系
    :param sub_domain_name: 子域名称
    :param identifier_table: 表标识符
    :param name_attribute: 表属性名称
    :param identifier_value_domain: 值域标识符
    :return:
    """
    cypher = "match(d:子域) -[:拥有]-> (t:表) -[r2:由组成]-> (a:表属性) " \
             "where d.name = '%s' and t.identifier = '%s' and a.name = '%s' " \
             "match(n:值域) where n.identifier = '%s' " \
             "create (a) -[r:值域]-> (n) return a, n" % (sub_domain_name, identifier_table,
                                                       name_attribute, identifier_value_domain)
    result = graph.run(cypher).data()
    if result is None:
        return "关系添加失败"
    else:
        return "关系添加成功"


def add_relation_between_attribute_value_and_permissible_values_info(sub_domain_name, identifier_table,
                                                                     name_attribute_value,
                                                                     identifier_permissible_values):
    """
    添加表属性值与可允许值之间的关系
    :param sub_domain_name: 子域名称
    :param identifier_table: 表标识符
    :param name_attribute_value: 表属性值名称
    :param identifier_permissible_values: 可允许值标识符
    :return:
    """
    cypher = "match(d:子域) -[:拥有]-> (t:表) -[r2:由组成]-> (a:表属性) -[:约束值]-> (p:表属性值) " \
             "where d.name = '%s' and t.identifier = '%s' and p.name = '%s' " \
             "match(n:可允许值) where n.identifier = '%s' " \
             "create (p) -[r:映射]-> (n) return a, n" % (sub_domain_name, identifier_table,
                                                         name_attribute_value, identifier_permissible_values)

    result = graph.run(cypher).data()
    if result is None:
        return "关系添加失败"
    else:
        return "关系添加成功"
