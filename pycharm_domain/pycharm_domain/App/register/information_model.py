"""
用于完成信息模型注册的相关功能
"""
from ..config import graph
from py2neo import Node, Relationship
from .register_mdr import get_time


# def register_class(model_name, class_name):
#     model_name_node = graph.nodes.match("ModelType", name=model_name).first()
#     if model_name_node is None:
#         model_name_node = Node("ModelType", name=model_name)
#         graph.create(model_name_node)
#
#     class_node = Node("ModelClass", name=class_name)
#     graph.create(class_node)
#     relationship = Relationship(model_name_node, "modelClass", class_node)
#     graph.create(relationship)
#
#     return "Information model class registered successfully"


# def register_property(class_name, property_names):
#     class_node = graph.nodes.match("ModelClass", name=class_name).first()
#     if class_node:
#         for property_name in property_names:
#             property_node = Node("ModelProperty", name=property_name)
#             graph.create(property_node)
#
#             relationship = Relationship(class_node, "modelProperty", property_node)
#             graph.create(relationship)
#
#         return "Properties registered successfully"
#     else:
#         return "Ontology not found"


# def register_relation(class1_name, class2_name, relation_name):
#     class1_node = graph.nodes.match("ModelClass", name=class1_name).first()
#     class2_node = graph.nodes.match("ModelClass", name=class2_name).first()
#
#     relationship = Relationship(class1_node, relation_name, class2_node)
#     graph.create(relationship)
#
#     return 'Relationship registered successfully'


# def get_model_class_options_list(name):
#     cypher = "match(n:ModelType) -[:modelClass]-> (c) where n.name = '%s' return c.name as name" % name
#     results = graph.run(cypher).data()
#     data = []
#     for result in results:
#         item = {"label": result["name"], "value": result["name"]}
#         data.append(item)
#     print(data)
#     return data


# def add_model_info(model_name, class_name):
#     cypher = "create(n:ModelType {name: '%s'}) -[:modelClass]-> (c:ModelClass {name: '%s'}) " \
#              "return n ,c" % (model_name, class_name)
#     result = graph.run(cypher).data()
#     if result is None:
#         return "模型添加失败"
#     else:
#         return "模型添加成功"


def add_model_info(model_name, class_name):
    """
    注册新的信息模型，要求新注册模型时，必须为该模型新建一个类一起注册
    :param model_name: 新增模型名称
    :param class_name: 新增类名称
    :return: 注册提示信息
    """
    cypher = "create(n:模型 {name: '%s'}) -[:类]-> (c:模型类 {name: '%s'}) " \
             "return n ,c" % (model_name, class_name)
    result = graph.run(cypher).data()
    if result is None:
        return "模型添加失败"
    else:
        return "模型添加成功"


def add_class_of_name(class_name, model_name, evolution, attribute_name, attribute_identifier):
    """
    注册信息模型中的模型类
    :param attribute_identifier:
    :param attribute_name:
    :param evolution:
    :param class_name: 本次要注册的类名称
    :param model_name: 模型名称
    :return: 注册提示信息
    """
    describe = ''
    table_name = ''
    table_identifier = ''
    evolution_message_model = ""
    evolution_message_attribute = ""
    if evolution == "yes":
        cypher = "match(n:模型) where n.name = '{0}' return n.evolution".format(model_name)
        evolution_message_model = graph.run(cypher).data()[0]["n.evolution"]
        if evolution_message_model is None:
            evolution_message_model = ""
        else:
            evolution_message_model = str(evolution_message_model)
        cypher = "match(a:子域) -[:拥有]-> (b:表) -[:由组成]-> (c:表属性) " \
                 "where c.identifier = '{0}' " \
                 "return a.describe as describe, " \
                 "b.name as table_name, b.identifier as table_identifier".format(attribute_identifier)
        temp = graph.run(cypher).data()[0]
        describe = temp["describe"]
        table_name = temp["table_name"]
        table_identifier = temp["table_identifier"]
        cypher = "match(n:表属性) where n.identifier = '{0}' return n.evolution".format(attribute_identifier)
        evolution_message_attribute = graph.run(cypher).data()[0]["n.evolution"]
        if evolution_message_attribute is None:
            evolution_message_attribute = ""
        else:
            evolution_message_attribute = str(evolution_message_attribute)
    cypher = "create(c:模型类 {name: '%s'}) " \
             "with c " \
             "match(n:模型 {name: '%s'}) " \
             "create (n) -[:类]-> (c) return n,c" % (class_name, model_name)
    result = graph.run(cypher).data()

    if evolution == "yes":
        type_ = "子域引起信息模型新增类"
        cause = describe + "新增表(" + table_name + "-" + table_identifier + ")-->属性(" + \
                attribute_name + "-" + attribute_identifier + ")"
        result = "模型(" + model_name + ")" + "添加类(" + class_name + ")"
        time = get_time()
        user = "管理员"
        # message = {"type": type, "cause": cause, "result": result, "time": time, "user": user}
        message = "变更类型:" + type_ + ";变更原因:" + cause + ";变更结果:" + result + \
                  ";操作时间:" + time + ";操作人员:" + user + ";"
        evolution_message_model = evolution_message_model + "???" + message
        evolution_message_attribute = evolution_message_attribute + "???" + message
        node = graph.nodes.match("模型", name=model_name).first()
        node["evolution"] = evolution_message_model
        graph.push(node)
        node = graph.nodes.match("表属性", identifier=attribute_identifier).first()
        node["evolution"] = evolution_message_attribute
        graph.push(node)

        node_evolution = graph.nodes.match("演化", name=table_identifier).first()
        message_evolution = node_evolution["evolution"]
        message_evolution = str(message_evolution)
        message_evolution = message_evolution + "???" + message
        node_evolution["evolution"] = message_evolution
        graph.push(node_evolution)
    if result is None:
        return "类添加失败"
    else:
        return "类添加成功"


def add_property_of_name(property_names, model_name, class_name, evolution, attribute_name, attribute_identifier):
    """
    注册信息模型的属性
    :param attribute_identifier:
    :param attribute_name:
    :param evolution:
    :param property_names: 本次要注册的属性名称列表
    :param model_name: 模型名称，方便定位查询找到对应的模型类
    :param class_name: 本次属性要挂在到对应类下面的类名称
    :return: 注册提示信息
    """
    describe = ''
    table_name = ''
    table_identifier = ''
    evolution_message_model = ""
    evolution_message_attribute = ""
    message = ""
    if evolution == "yes":
        cypher = "match(n:模型) where n.name = '{0}' return n.evolution".format(model_name)
        evolution_message_model = graph.run(cypher).data()[0]["n.evolution"]
        if evolution_message_model is None:
            evolution_message_model = ""
        else:
            evolution_message_model = str(evolution_message_model)
        cypher = "match(a:子域) -[:拥有]-> (b:表) -[:由组成]-> (c:表属性) " \
                 "where c.identifier = '{0}' " \
                 "return a.describe as describe, " \
                 "b.name as table_name, b.identifier as table_identifier".format(attribute_identifier)
        temp = graph.run(cypher).data()[0]
        describe = temp["describe"]
        table_name = temp["table_name"]
        table_identifier = temp["table_identifier"]
        cypher = "match(n:表属性) where n.identifier = '{0}' return n.evolution".format(attribute_identifier)
        evolution_message_attribute = graph.run(cypher).data()[0]["n.evolution"]
        if evolution_message_attribute is None:
            evolution_message_attribute = ""
        else:
            evolution_message_attribute = str(evolution_message_attribute)

    # 循环注册每一个属性
    for property_name in property_names:
        cypher = "create(p:模型属性 {name: '%s'}) " \
                 "with p " \
                 "match(n:模型 {name: '%s'}) -[:类]-> (c:模型类 {name:'%s'}) " \
                 "create (c) -[:属性]-> (p) return n,c,p" % (property_name, model_name, class_name)
        result = graph.run(cypher).data()
        if evolution == "yes":
            type_ = "子域引起信息模型新增属性"
            cause = describe + "新增表(" + table_name + "-" + table_identifier + ")-->属性(" + attribute_name + "-" + \
                    attribute_identifier + ")"
            result = "模型(" + model_name + ")" + "的类(" + class_name + ")新增属性(" + property_name + ")"
            time = get_time()
            user = "管理员"
            # message = {"type": type, "cause": cause, "result": result, "time": time, "user": user}
            message = "变更类型:" + type_ + ";变更原因:" + cause + ";变更结果:" + result + \
                      ";操作时间:" + time + ";操作人员:" + user + ";"
            evolution_message_model = evolution_message_model + "???" + message
            evolution_message_attribute = evolution_message_attribute + "???" + message

    if evolution == "yes":
        node = graph.nodes.match("模型", name=model_name).first()
        node["evolution"] = evolution_message_model
        graph.push(node)
        node = graph.nodes.match("表属性", identifier=attribute_identifier).first()
        node["evolution"] = evolution_message_attribute
        graph.push(node)

        node_evolution = graph.nodes.match("演化", name=table_identifier).first()
        message_evolution = node_evolution["evolution"]
        message_evolution = str(message_evolution)
        message_evolution = message_evolution + "???" + message
        node_evolution["evolution"] = message_evolution
        graph.push(node_evolution)

    return "属性添加成功"


def add_relation_info(model_name, class_name1, class_name2, relation):
    """
    注册信息模型中两个类之间的关系
    :param model_name: 模型名称：用于定位，找到对应的类
    :param class_name1: 第一个类名称，关系中的起始节点
    :param class_name2: 第二个类名称，关系中的尾节点
    :param relation: 关系名称
    :return: 注册提示信息
    """
    cypher = "match(n:模型 {name: '%s'}) -[:类]-> (c1:模型类 {name:'%s'})  " \
             "match(n:模型 {name: '%s'}) -[:类]-> (c2:模型类 {name:'%s'}) " \
             "create (c1) -[r:%s]-> (c2) return c1, c2" % (model_name, class_name1, model_name, class_name2, relation)
    result = graph.run(cypher).data()
    if result is None:
        return "关系添加失败"
    else:
        return "关系添加成功"


def register_model_of_file(data):
    """
    通过json文件注册模型
    :param data:
    :return:
    """
    model_name = data["model_name"]
    node = graph.nodes.match("模型", name=model_name).first()
    if node is not None:
        return "该参考域数据目录已注册！！！"
    node_model = Node("模型", name=model_name)
    graph.create(node_model)
    model_class = data["model_class"]
    for line in model_class:
        node_model_class = Node("模型类", name=line["model_class_name"])
        graph.create(node_model_class)
        relation = Relationship(node_model, "类", node_model_class)
        graph.create(relation)
        if "model_properties" in line:
            for property in line["model_properties"]:
                node_model_property = Node("模型属性", name=property["model_property_name"])
                graph.create(node_model_property)
                relation = Relationship(node_model_class, "属性", node_model_property)
                graph.create(relation)

    return "参考域数据目录导入成功"
