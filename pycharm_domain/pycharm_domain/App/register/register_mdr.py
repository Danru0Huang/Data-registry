"""
本文件用于完成MDR的注册
"""
from ..config import graph
from py2neo import Node, Relationship
import datetime


def get_time():
    """
    获取时间戳
    :return:
    """
    curr_time = datetime.datetime.now()
    time = datetime.datetime.strftime(curr_time, '%Y-%m-%d %H:%M:%S')
    return time


def get_id(label):
    """
    获取对应label的ID
    :param label:
    :return:
    """
    query = "MATCH (n:%s) RETURN n.name" % label
    ID = graph.run(query).data()[0]["n.name"]
    return ID


def update_id(label, ID):
    """
    更新对应label的ID
    :param label:
    :param ID:
    :return:
    """
    query = "MATCH (n:%s) SET n.name = %d" % (label, ID)
    graph.run(query)


def register_object_class(name, describe, personId, department):
    """
    MDR对象类注册
    :param name:
    :param describe:
    :param personId:
    :param department:
    :return:
    """
    time = get_time()
    ID = get_id("对象类ID")
    identifier = f"OCL{str(ID).zfill(3)}"
    status = "已注册"
    version = "2.0智能化"
    node = Node("对象类", name=name, describe=describe, personId=personId, department=department,
                time=time, identifier=identifier, status=status, version=version)
    graph.create(node)
    ID += 1
    update_id("对象类ID", ID)
    return "对象类注册成功"


def register_property(name, describe, personId, department):
    """
    属性注册
    :param name:
    :param describe:
    :param personId:
    :param department:
    :return:
    """
    time = get_time()
    ID = get_id("属性ID")
    identifier = f"PRP{str(ID).zfill(3)}"
    status = "已注册"
    version = "2.0智能化"
    node = Node("属性", name=name, describe=describe, personId=personId, department=department,
                time=time, identifier=identifier, status=status, version=version)
    graph.create(node)
    ID += 1
    update_id("属性ID", ID)
    return "属性注册成功"


def register_conceptual_domain(name, describe, personId, department, valueMeanings):
    """
    概念域注册
    :param name:
    :param describe:
    :param personId:
    :param department:
    :param valueMeanings:
    :return:
    """
    time = get_time()
    ID_CD = get_id("概念域ID")
    identifierCD = f"CDM{str(ID_CD).zfill(3)}"
    status = "已注册"
    version = "2.0智能化"
    node = Node("概念域", name=name, describe=describe, personId=personId, department=department,
                time=time, identifier=identifierCD, status=status, version=version)
    graph.create(node)
    # 若该概念域的取值为可枚举值，则注册对应的值含义
    if len(valueMeanings) > 0:
        ID_VM = get_id("值含义ID")
        for valueMeaning in valueMeanings:
            identifierVM = f"VLM{str(ID_VM).zfill(3)}"
            nodeVM = Node("值含义", name=valueMeaning, identifier=identifierVM, time=time,
                          version=version, status=status)
            graph.create(nodeVM)

            relation = Relationship(node, "值含义", nodeVM)
            graph.create(relation)

            ID_VM += 1

        update_id("值含义ID", ID_VM)

    ID_CD += 1
    update_id("概念域ID", ID_CD)

    return "概念域注册成功"


def register_data_element_concept(name, describe, personId, department, object_class, property, conceptual_domain):
    """
    注册数据元概念
    :param name:
    :param describe:
    :param personId:
    :param department:
    :param object_class:
    :param property:
    :param conceptual_domain:
    :return:
    """
    time = get_time()
    ID = get_id("数据元概念ID")
    identifier = f"DEC{str(ID).zfill(3)}"
    status = "已注册"
    version = "2.0智能化"
    node = Node("数据元概念", name=name, describe=describe, personId=personId, department=department,
                time=time, identifier=identifier, status=status, version=version)
    graph.create(node)
    ID += 1
    update_id("数据元概念ID", ID)

    nodeOB = graph.nodes.match("对象类", identifier=object_class).first()
    relation = Relationship(node, "对象类", nodeOB)
    graph.create(relation)

    nodePR = graph.nodes.match("属性", identifier=property).first()
    relation = Relationship(node, "属性", nodePR)
    graph.create(relation)

    nodeCD = graph.nodes.match("概念域", identifier=conceptual_domain).first()
    relation = Relationship(node, "概念域", nodeCD)
    graph.create(relation)

    return "数据元概念注册成功"


def register_mdr_value_domain_list(name, describe, personId, department, conceptual_domain, indefinite, enumerable):
    """
    MDR值域注册
    :param name:
    :param describe:
    :param personId:
    :param department:
    :param conceptual_domain:
    :param indefinite:
    :param enumerable:
    :return:
    """
    time = get_time()
    ID = get_id("值域ID")
    identifier = f"VDM{str(ID).zfill(3)}"
    status = "已注册"
    version = "2.0智能化"
    if indefinite == "":
        indefinite = "null"
    node = Node("值域", name=name, describe=describe, personId=personId, department=department,
                time=time, identifier=identifier, status=status, version=version, indefinite=indefinite)
    graph.create(node)
    ID += 1
    update_id("值域ID", ID)

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
            nodeGroup = Node("值域组", name=groupName, identifier=identifier)
            graph.create(nodeGroup)
            relation = Relationship(node, "组", nodeGroup)
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

    nodeCD = graph.nodes.match("概念域", identifier=conceptual_domain).first()
    relation = Relationship(node, "概念域", nodeCD)
    graph.create(relation)

    return "值域注册成功"


def register_data_element(name, describe, personId, department, dataElementConcept, valueDomain, evolution,
                          attribute_name, attribute_identifier):
    """
    注册MDR数据元
    :param attribute_identifier:
    :param attribute_name:
    :param evolution:
    :param name:
    :param describe:
    :param personId:
    :param department:
    :param dataElementConcept:
    :param valueDomain:
    :return:
    """
    time = get_time()
    ID = get_id("数据元ID")
    identifier = f"DEL{str(ID).zfill(3)}"

    evolution_message = ""
    describe_sub = ""
    table_name = ""
    table_identifier = ""
    if evolution == "yes":
        cypher = "match(a:子域) -[:拥有]-> (b:表) -[:由组成]-> (c:表属性) " \
                 "where c.identifier = '{0}' " \
                 "return a.describe as describe, b.name as table_name, " \
                 "b.identifier as table_identifier".format(attribute_identifier)
        data = graph.run(cypher).data()[0]
        describe_sub = data["describe"]
        table_name = data["table_name"]
        table_identifier = data["table_identifier"]
        evolution_message = "由" + describe_sub + "新增表(" + table_name + "-" + table_identifier + ")-->属性(" + \
                            attribute_name + "-" + attribute_identifier + ")引起概念(" + name + "-" + identifier + ")增加"
    else:
        evolution_message = "暂无演化信息"

    status = "已注册"
    version = "2.0智能化"
    node = Node("数据元", name=name, describe=describe, personId=personId, department=department,
                time=time, identifier=identifier, status=status, version=version, evolution=evolution_message)
    graph.create(node)
    ID += 1
    update_id("数据元ID", ID)

    nodeDEC = graph.nodes.match("数据元概念", identifier=dataElementConcept).first()
    relation1 = Relationship(node, "数据元概念", nodeDEC)
    graph.create(relation1)

    nodeVD = graph.nodes.match("值域", identifier=valueDomain).first()
    relation2 = Relationship(node, "值域", nodeVD)
    graph.create(relation2)

    if evolution == "yes":
        cypher = "match(n:表属性) where n.identifier = '{0}' return n.evolution".format(attribute_identifier)
        evolution_message_attribute = graph.run(cypher).data()[0]["n.evolution"]
        if evolution_message_attribute is None:
            evolution_message_attribute = ""
        else:
            evolution_message_attribute = str(evolution_message_attribute)

        type_ = "子域引起概念术语增加"
        cause = describe_sub + "新增表(" + table_name + "-" + table_identifier + ")-->属性(" + attribute_name + "-" + \
                attribute_identifier + ")"
        result = "新增概念(" + name + "-" + identifier + ")"
        time = get_time()
        user = "管理员"
        # message = {"type": type, "cause": cause, "result": result, "time": time, "user": user}
        message = "变更类型:" + type_ + ";变更原因:" + cause + ";变更结果:" + result + \
                  ";操作时间:" + time + ";操作人员:" + user + ";"
        evolution_message_attribute = evolution_message_attribute + "???" + message

        node = graph.nodes.match("表属性", identifier=attribute_identifier).first()
        node["evolution"] = evolution_message_attribute
        graph.push(node)

        node_evolution = graph.nodes.match("演化", name=table_identifier).first()
        message_evolution = node_evolution["evolution"]
        message_evolution = str(message_evolution)
        message_evolution = message_evolution + "???" + message
        node_evolution["evolution"] = message_evolution
        graph.push(node_evolution)

    return "数据元注册成功", identifier

