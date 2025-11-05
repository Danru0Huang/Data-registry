from ..config import graph
from ..register.register_mdr import get_time


def delete_attribute_value_info(identifier_attribute_value):
    """
    删除表属性值
    :param identifier_attribute_value: 表属性值标识符
    :return:
    """
    # 获取演化信息
    cypher = "match(a:子域) -[:拥有]-> (b:表) -[:由组成]-> (c:表属性) -[:约束值]-> (d:表属性值)" \
             "where d.identifier = '{0}' " \
             "return a.describe as describe, b.name as table_name, " \
             "b.identifier as table_identifier, c.name as attribute_name, c.identifier as attribute_identifier, " \
             "d.name as name_attribute_value".format(identifier_attribute_value)
    data = graph.run(cypher).data()[0]
    describe = data["describe"]
    table_name = data["table_name"]
    table_identifier = data["table_identifier"]
    attribute_name = data["attribute_name"]
    attribute_identifier = data["attribute_identifier"]
    name_attribute_value = data["name_attribute_value"]

    # 删除操作
    cypher = "match(n:表属性值) where n.identifier = '{0}' detach delete n".format(identifier_attribute_value)
    graph.run(cypher)

    # 更新演化信息
    type_ = "子域删除属性值"
    cause = "删除属性值（" + name_attribute_value + "-" + identifier_attribute_value + ")"
    result = describe + "删除表(" + table_name + "-" + table_identifier + ")-->属性(" + \
             attribute_name + "-" + attribute_identifier + ")-->属性值(" + name_attribute_value \
             + "-" + identifier_attribute_value + ")"
    time = get_time()
    user = "管理员"
    message = "变更类型:" + type_ + ";变更原因:" + cause + ";变更结果:" + result + \
              ";操作时间:" + time + ";操作人员:" + user + ";"
    node_evolution = graph.nodes.match("演化", name=table_identifier).first()
    message_evolution = node_evolution["evolution"]
    message_evolution = str(message_evolution)
    message_evolution = message_evolution + "???" + message
    node_evolution["evolution"] = message_evolution
    graph.push(node_evolution)

    return "属性值删除成功"


def delete_attribute_info(identifier_attribute):
    """
    删除表属性及其相关的表属性值节点
    :param identifier_attribute: 表属性标识符
    :return:
    """
    # 获取演化信息
    cypher = "match(a:子域) -[:拥有]-> (b:表) -[:由组成]-> (c:表属性) " \
             "where c.identifier = '{0}' " \
             "return a.describe as describe, b.name as table_name, " \
             "b.identifier as table_identifier, c.name as name_attribute".format(identifier_attribute)
    data = graph.run(cypher).data()[0]
    describe = data["describe"]
    table_name = data["table_name"]
    table_identifier = data["table_identifier"]
    name_attribute = data["name_attribute"]

    # 删除操作
    cypher = "match(n:表属性) where n.identifier = '{0}' " \
             "optional match (n) -[r:约束值]-> (m) detach delete n,m".format(identifier_attribute)
    graph.run(cypher)

    # 更新演化信息
    type_ = "子域删除属性"
    cause = "删除属性(" + name_attribute + "-" + identifier_attribute + ")"
    result = describe + "删除表(" + table_name + "-" + table_identifier + ")-->属性(" + \
             name_attribute + "-" + identifier_attribute + ")"
    time = get_time()
    user = "管理员"
    message = "变更类型:" + type_ + ";变更原因:" + cause + ";变更结果:" + result + \
              ";操作时间:" + time + ";操作人员:" + user + ";"
    node_evolution = graph.nodes.match("演化", name=table_identifier).first()
    message_evolution = node_evolution["evolution"]
    message_evolution = str(message_evolution)
    message_evolution = message_evolution + "???" + message
    node_evolution["evolution"] = message_evolution
    graph.push(node_evolution)
    return "表属性删除成功"


def delete_table_info(identifier_table):
    """
    删除表及其相关信息
    :param identifier_table:
    :return:
    """
    # 获取表名
    node_table = graph.nodes.match("表", identifier=identifier_table).first()
    table_name = node_table["name"]

    # 获取子域描述
    cypher = "match(a:子域) -[:拥有]-> (b:表) " \
             "where b.identifier = '{0}' " \
             "return a.describe as describe".format(identifier_table)
    describe = graph.run(cypher).data()[0]["describe"]

    # 删除操作
    cypher = "match (n:表) -[r1:由组成]-> (m:表属性) " \
             "where n.identifier = '{0}' " \
             "return m.identifier".format(identifier_table)
    result = graph.run(cypher).data()
    if len(result) > 0:
        cypher = "match (n:表) -[r1:由组成]-> (m:表属性) " \
                 "where n.identifier = '{0}' " \
                 "optional match(n) -[r1:由组成]-> (m) -[r2:约束值]-> (a:表属性值) " \
                 "detach delete n,m,a".format(identifier_table)
        graph.run(cypher)
    else:
        cypher = "match (n:表) where n.identifier = '{0}' detach delete n".format(identifier_table)
        graph.run(cypher)

    # 注册演化信息
    type_ = "子域删除数据"
    cause = "删除表(" + table_name + "-" + identifier_table + ")"
    result = describe + "删除表(" + table_name + "-" + identifier_table + ")"
    time = get_time()
    user = "管理员"
    message = "变更类型:" + type_ + ";变更原因:" + cause + ";变更结果:" + result + \
              ";操作时间:" + time + ";操作人员:" + user + ";"
    node_evolution = graph.nodes.match("演化", name=identifier_table).first()
    message_evolution = node_evolution["evolution"]
    message_evolution = str(message_evolution)
    message_evolution = message_evolution + "???" + message
    node_evolution["evolution"] = message_evolution
    graph.push(node_evolution)

    return "表删除成功"


def update_sub_domain_info(label, identifier, name):
    """
    更新子域节点信息
    :param label: 子域的节点类别
    :param identifier: 节点标识符
    :param name: 要修改的信息
    :return:
    """
    # 更新操作
    node = graph.nodes.match(label, identifier=identifier).first()
    _name = node["name"]
    node["name"] = name
    graph.push(node)

    # 更新演化信息
    table_identifier = ""
    message = ""
    if label == "表属性":
        cypher = "match(a:子域) -[:拥有]-> (b:表) -[:由组成]-> (c:表属性) " \
                 "where c.identifier = '{0}' " \
                 "return a.describe as describe, b.name as table_name, b.identifier as table_identifier, " \
                 "c.identifier as attribute_identifier".format(identifier)
        data = graph.run(cypher).data()[0]
        describe = data["describe"]
        table_name = data["table_name"]
        table_identifier = data["table_identifier"]
        attribute_identifier = data["attribute_identifier"]

        type_ = "子域修改属性"
        cause = describe + "修改属性-->属性(" + _name + "-" + attribute_identifier + \
                ")==>属性(" + name + '-' + attribute_identifier + ")"
        result = describe + "修改表(" + table_name + "-" + table_identifier + ")==>属性(" + _name + "-->" + name + ")"
        time = get_time()
        user = "管理员"
        message = "变更类型:" + type_ + ";变更原因:" + cause + ";变更结果:" + result + \
                  ";操作时间:" + time + ";操作人员:" + user + ";"
    elif label == "表属性值":
        cypher = "match(a:子域) -[:拥有]-> (b:表) -[:由组成]-> (c:表属性) -[:约束值]-> (d:表属性值) " \
                 "where d.identifier = '{0}' " \
                 "return a.describe as describe, b.name as table_name, b.identifier as table_identifier, " \
                 "c.name as attribute_name, c.identifier as attribute_identifier".format(identifier)
        data = graph.run(cypher).data()[0]
        describe = data["describe"]
        table_name = data["table_name"]
        table_identifier = data["table_identifier"]
        attribute_name = data["attribute_name"]
        attribute_identifier = data["attribute_identifier"]

        type_ = "子域修改属性值"
        cause = describe + "修改属性值-->属性值(" + _name + "-" + identifier + \
                ")==>属性值(" + name + '-' + identifier + ")"
        result = describe + "修改表(" + table_name + "-" + table_identifier + ")-->属性(" + attribute_name + \
                 attribute_identifier + ")==>属性值(" + _name + "-->" + name + ")"
        time = get_time()
        user = "管理员"
        message = "变更类型:" + type_ + ";变更原因:" + cause + ";变更结果:" + result + \
                  ";操作时间:" + time + ";操作人员:" + user + ";"

    node_evolution = graph.nodes.match("演化", name=table_identifier).first()
    message_evolution = node_evolution["evolution"]
    message_evolution = str(message_evolution)
    message_evolution = message_evolution + "???" + message
    node_evolution["evolution"] = message_evolution
    graph.push(node_evolution)
    return "修改成功"
