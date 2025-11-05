from ..config import graph
from ..register.register_mdr import get_time, get_id, update_id
from py2neo import Node, Relationship


def update_mdr_info(label, identifier, properties):
    """
    修改mdr注册信息
    :param label: 标签
    :param identifier: 节点标识符
    :param properties: 属性列表
    :return:
    """
    properties["time"] = get_time()
    version = properties["version"]
    version += 1.0
    properties["version"] = version
    node = graph.nodes.match(label, identifier=identifier).first()
    node.update(properties)
    graph.push(node)
    return "更新成功"


def add_value_meanings_info(identifier_conceptual_domain, value_meanings):
    node_conceptual_domain = graph.nodes.match("概念域", identifier=identifier_conceptual_domain).first()
    ID = get_id("值含义ID")
    for value_meaning in value_meanings:
        identifier = f"VLM{str(ID).zfill(3)}"
        node_value_meaning = Node("值含义", name=value_meaning, identifier=identifier, time=get_time(), version="2.0智能化",
                                  status="已注册")
        graph.create(node_value_meaning)

        relation = Relationship(node_conceptual_domain, "值含义", node_value_meaning)
        graph.create(relation)

        ID += 1

    update_id("值含义ID", ID)

    return "注册成功"


def add_permissible_values_info(identifier_value_domain, enumerable):
    node_value_domain = graph.nodes.match("值域", identifier=identifier_value_domain).first()
    groups = {}
    if enumerable:
        for line in enumerable:
            num = line["num"]
            value = line["value"]
            valueMeaning = line["valueMeaning"]
            if num in groups:
                groups[num].append({"value": value, "valueMeaning": valueMeaning})
            else:
                groups[num] = []
                groups[num].append({"value": value, "valueMeaning": valueMeaning})
        ID_PEV = get_id("可允许值ID")
        for k, vs in groups.items():
            groupName = "组" + k
            nodeGroup = graph.nodes.match("值域组", name=groupName, identifier=identifier_value_domain).first()
            if nodeGroup is None:
                nodeGroup = Node("值域组", name=groupName, identifier=identifier_value_domain)
                graph.create(nodeGroup)
                relation = Relationship(node_value_domain, "组", nodeGroup)
                graph.create(relation)
            for v in vs:
                identifierValue = f"PEV{str(ID_PEV).zfill(3)}"
                nodeValue = Node("可允许值", name=v["value"], identifier=identifierValue)
                graph.create(nodeValue)
                relation = Relationship(nodeGroup, "可允许值", nodeValue)
                graph.create(relation)
                nodeValueMeaning = graph.nodes.match("值含义", identifier=v["valueMeaning"]).first()
                relation = Relationship(nodeValue, "值含义", nodeValueMeaning)
                graph.create(relation)
                ID_PEV += 1
        update_id("可允许值ID", ID_PEV)

    return "注册成功"
