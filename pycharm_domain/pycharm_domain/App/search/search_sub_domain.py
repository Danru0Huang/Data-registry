from ..config import graph, CLASS_LIST_SubDomain, CLASS_LIST_Attribute
from .search_mdr import get_mdr_table_info


# def get_sub_domain_options_list():
#     """
#     获取数据库中存在的子域名称及描述信息列表
#     :return:
#     """
#     query = "match (n:子域) return n.name, n.describe"
#     data = graph.run(query).data()
#     result = []
#     item = {}
#     for line in data:
#         item["label"] = line["n.name"]
#         item["value"] = line["n.name"]
#         item["describe"] = line["n.describe"]
#         result.append(item)
#         item = {}
#     return result

# def get_sub_domain_options():
#     """
#     获取数据库中存在的子域名称、描述信息，及其直接拥有的表格列表
#     :return: 一个结构化的列表，其中包含子域信息和每个子域下的表格列表
#     """
#     # 修改查询以返回每个子域及其拥有的表格
#     query = """
#     MATCH (sub_domain:子域)-[:拥有]->(table:表)
#     WITH sub_domain.name AS sub_domain_name, sub_domain.describe AS sub_domain_describe,
#          collect(table.name) AS table_names, collect(table.identifier) AS table_identifiers
#     RETURN sub_domain_name, sub_domain_describe, table_names, table_identifiers
#     """
#     data = graph.run(query).data()
#     result = []
#
#     for line in data:
#         # 构造每个子域及其拥有的表格的数据结构
#         tables_info = []
#         for table_name, table_identifier in zip(line["table_names"], line["table_identifiers"]):
#             tables_info.append({
#                 "value": table_identifier,  # 表格标识符作为值
#                 "label": table_name  # 表格名作为展示标签
#             })
#         sub_domain_info = {
#             "value": line["sub_domain_name"],  # 子域名作为值
#             "label": line["sub_domain_describe"],  # 子域描述作为展示标签
#             "children": tables_info  # 子域拥有的表格列表
#         }
#         result.append(sub_domain_info)
#
# return result

def get_sub_domain_and_table_options_list():
    """
    获取子域及其表格
    :return:
    """
    # 获取子域信息--子域名称及描述
    query = "match(sub_domain:子域) " \
            "return id(sub_domain) as sub_domain_id, sub_domain.name as sub_domain_name, " \
            "sub_domain.describe as sub_domain_describe"
    data = graph.run(query).data()
    sub_domain = {}
    for line in data:
        sub_domain[line["sub_domain_id"]] = {"value": line["sub_domain_name"], "label": line["sub_domain_describe"]}

    # 获取表格数据
    query = "match(sub_domain:子域) -[:拥有]-> (table:表) " \
            "return id(sub_domain) as sub_domain_id, table.identifier as table_identifier, table.name as table_name"
    data = graph.run(query).data()
    table_of_sub_domain = {}
    for line in data:
        if line["sub_domain_id"] in table_of_sub_domain:
            table_of_sub_domain[line["sub_domain_id"]].append({"value": line["table_identifier"],
                                                               "label": line["table_name"]})
        else:
            table_of_sub_domain[line["sub_domain_id"]] = [{"value": line["table_identifier"],
                                                           "label": line["table_name"]}]

    # 将表格数据与子域数据关联
    for k, v in table_of_sub_domain.items():
        sub_domain[k]["children"] = v

    # 返回前端数据
    result = []
    for k, v in sub_domain.items():
        result.append(v)

    return result


def get_sub_domain_table_options_list():
    query = "match (n:表) return n.identifier, n.name"
    data = graph.run(query).data()
    result = []
    item = {}
    for line in data:
        item["label"] = line["n.name"]
        item["value"] = line["n.identifier"]
        result.append(item)
        item = {}
    return result


def get_sub_domain_options_list():
    """
    获取数据库中存在的子域名称及描述信息列表
    :return:
    """
    query = "match (n:子域) return n.name, n.describe"
    data = graph.run(query).data()
    result = []
    item = {}
    for line in data:
        item["label"] = line["n.name"]
        item["value"] = line["n.name"]
        item["describe"] = line["n.describe"]
        result.append(item)
        item = {}
    return result


def get_json_data(data_of_graph, identifier_attribute_list, identifier_attribute_value_list):
    json_data = {'data': [], "links": []}
    id_to_id = {}
    # name_to_id = {}
    count = 0
    identifier_attribute = {}
    identifier_attribute_value = {}

    for line in identifier_attribute_list:
        identifier_attribute[line["id"]] = line["identifier"]

    for line in identifier_attribute_value_list:
        identifier_attribute_value[line["id"]] = line["identifier"]

    for i in data_of_graph:
        _i = i["start_id"]
        if not (_i in id_to_id):
            id_to_id[_i] = count
            count += 1
            if i["start_labels"] == "表属性":
                node = {"name": i["start_name"], "category": CLASS_LIST_SubDomain[i["start_labels"]],
                        "identifier": identifier_attribute["start_id"]}
            elif i["start_labels"] == "表属性值":
                node = {"name": i["start_name"], "category": CLASS_LIST_SubDomain[i["start_labels"]],
                        "identifier": identifier_attribute_value["start_id"]}
            else:
                node = {"name": i["start_name"], "category": CLASS_LIST_SubDomain[i["start_labels"]]}
            json_data["data"].append(node)

        _i = i["end_id"]
        if not (_i in id_to_id):
            id_to_id[_i] = count
            count += 1
            if i["end_labels"] == "表属性":
                node = {"name": i["end_name"], "category": CLASS_LIST_SubDomain[i["end_labels"]],
                        "identifier": identifier_attribute[i["end_id"]]}
            elif i["end_labels"] == "表属性值":
                node = {"name": i["end_name"], "category": CLASS_LIST_SubDomain[i["end_labels"]],
                        "identifier": identifier_attribute_value[i["end_id"]]}
            else:
                node = {"name": i["end_name"], "category": CLASS_LIST_SubDomain[i["end_labels"]]}
            json_data["data"].append(node)
    # for i in data_of_graph:
    #     _name = i["start_name"]
    #     if not (_name in name_to_id):
    #         name_to_id[_name] = count
    #         count += 1
    #         node = {"name": i["start_name"], "category": CLASS_LIST_SubDomain[i["start_labels"]]}
    #         json_data["data"].append(node)
    #
    #     _name = i["end_name"]
    #     if not (_name in name_to_id):
    #         name_to_id[_name] = count
    #         count += 1
    #         node = {"name": i["end_name"], "category": CLASS_LIST_SubDomain[i["end_labels"]]}
    #         json_data["data"].append(node)

    # for i in data_of_graph:
    #     edge = {"source": name_to_id[i["start_name"]], "target": name_to_id[i["end_name"]],
    #             "value": i["relationship"]}
    #     json_data['links'].append(edge)

    for i in data_of_graph:
        # 处理边
        edge = {"source": id_to_id[i["start_id"]], "target": id_to_id[i["end_id"]],
                "value": i["relationship"]}
        json_data['links'].append(edge)

    return json_data


def get_graph_of_table_info(sub_domain_name, identifier_table):
    """
    通过子域名称以及表标识符获取子域图谱数据
    :param sub_domain_name:
    :param identifier_table:
    :return:
    """
    cypher1 = "match(d:子域) -[r1:拥有]-> (t:表) " \
              "where d.name = '{0}' and t.identifier = '{1}' " \
              "return d.name as start_name, id(d) as start_id, type(r1) as relationship, " \
              "t.name as end_name, id(t) as end_id," \
              "labels(d)[0] as start_labels, labels(t)[0] as end_labels " \
              "union all " \
              "match(d:子域) -[:拥有]-> (t:表) -[r2:由组成]-> (a:表属性) " \
              "where d.name = '{0}' and t.identifier = '{1}' " \
              "return t.name as start_name, id(t) as start_id, type(r2) as relationship, " \
              "a.name as end_name, id(a) as end_id, " \
              "labels(t)[0] as start_labels, labels(a)[0] as end_labels " \
              "union all " \
              "match(d:子域) -[:拥有]-> (t:表) -[:由组成]-> (a:表属性) -[r3:约束值]-> (v:表属性值) " \
              "where d.name = '{0}' and t.identifier = '{1}' " \
              "return a.name as start_name, id(a) as start_id, " \
              "type(r3) as relationship, v.name as end_name, id(v) as end_id, " \
              "labels(a)[0] as start_labels, labels(v)[0] as end_labels " \
              "union all " \
              "match(d:子域) -[:拥有]-> (t:表) -[:由组成]-> (a:表属性) -[r4:数据元]-> (e:数据元)" \
              "where d.name = '{0}' and t.identifier = '{1}' " \
              "return a.name as start_name, id(a) as start_id, " \
              "type(r4) as relationship, e.name as end_name, id(e) as end_id, " \
              "labels(a)[0] as start_labels, labels(e)[0] as end_labels " \
              "union all " \
              "match(d:子域) -[:拥有]-> (t:表) -[:由组成]-> (a:表属性) -[:数据元]-> (e:数据元) -[r5:值域]-> (vd:值域) " \
              "where d.name = '{0}' and t.identifier = '{1}' " \
              "return e.name as start_name, id(e) as start_id, " \
              "type(r5) as relationship, vd.name as end_name, id(vd) as end_id, " \
              "labels(e)[0] as start_labels, labels(vd)[0] as end_labels " \
              "union all " \
              "match(d:子域) -[:拥有]-> (t:表) -[:由组成]-> (a:表属性) -[:数据元]-> (e:数据元) -[:值域]-> (vd:值域) -[r6:组]-> (g:值域组) " \
              "where d.name = '{0}' and t.identifier = '{1}' " \
              "return vd.name as start_name, id(vd) as start_id, " \
              "type(r6) as relationship, g.name as end_name, id(g) as end_id, " \
              "labels(vd)[0] as start_labels, labels(g)[0] as end_labels " \
              "union all " \
              "match(d:子域) -[:拥有]-> (t:表) -[:由组成]-> (a:表属性)" \
              " -[:数据元]-> (e:数据元) -[:值域]-> (vd:值域) -[:组]-> (g:值域组) -[r7:可允许值]-> (p:可允许值)" \
              "where d.name = '{0}' and t.identifier = '{1}' " \
              "return g.name as start_name, id(g) as start_id, " \
              "type(r7) as relationship, p.name as end_name, id(p) as end_id, " \
              "labels(g)[0] as start_labels, labels(p)[0] as end_labels " \
              "union all " \
              "match(d:子域) -[:拥有]-> (t:表) -[:由组成]-> (a:表属性) -[r8:值域]-> (vd:值域) " \
              "where d.name = '{0}' and t.identifier = '{1}' " \
              "return a.name as start_name, id(a) as start_id, " \
              "type(r8) as relationship, vd.name as end_name, id(vd) as end_id, " \
              "labels(a)[0] as start_labels, labels(vd)[0] as end_labels " \
              "union all " \
              "match(d:子域) -[:拥有]-> (t:表) -[:由组成]-> (a:表属性) -[:约束值]-> (v:表属性值) -[r9:可允许值]-> (p:可允许值)" \
              "where d.name = '{0}' and t.identifier = '{1}' " \
              "return v.name as start_name, id(v) as start_id, " \
              "type(r9) as relationship, p.name as end_name, id(p) as end_id, " \
              "labels(v)[0] as start_labels, labels(p)[0] as end_labels " \
              "union all " \
              "match(d:子域) -[:拥有]-> (t:表) -[:由组成]-> (a:表属性) -[:约束值]-> (v:表属性值) -[r10:映射]-> (p:可允许值)" \
              "where d.name = '{0}' and t.identifier = '{1}' " \
              "return v.name as start_name, id(v) as start_id, " \
              "type(r10) as relationship, p.name as end_name, id(p) as end_id, " \
              "labels(v)[0] as start_labels, labels(p)[0] as end_labels ".format(sub_domain_name, identifier_table)
    cypher2 = "match(d:子域) -[:拥有]-> (t:表) -[r2:由组成]-> (a:表属性) " \
              "where d.name = '{0}' and t.identifier = '{1}' " \
              "return id(a) as id, a.name as name, a.identifier as identifier".format(sub_domain_name, identifier_table)
    data_of_identifier_attribute = graph.run(cypher2).data()
    cypher2 = "match(d:子域) -[:拥有]-> (t:表) -[r2:由组成]-> (a:表属性) -[r3:约束值]-> (v:表属性值) " \
              "where d.name = '{0}' and t.identifier = '{1}' " \
              "return id(v) as id, v.name as name, v.identifier as identifier".format(sub_domain_name, identifier_table)
    data_of_identifier_attribute_value = graph.run(cypher2).data()
    data1 = graph.run(cypher1)
    data_of_graph = list(data1)
    return get_json_data(data_of_graph, data_of_identifier_attribute, data_of_identifier_attribute_value)


# def get_graph_of_domian_info(sub_domain_name):
#     """
#     通过子域名称以及表标识符获取数据元
#     :param sub_domain_name:
#     :return:
#     """
#     cypher1 = "MATCH (d:子域 {name: '{0}'})-[r1:拥有]->(t:表) " \
#               "RETURN d.name as start_name, id(d) as start_id, type(r1) as relationship, " \
#               "t.name as end_name, id(t) as end_id, labels(d)[0] as start_labels, labels(t)[0] as end_labels " \
#               "UNION ALL " \
#               "MATCH (d:子域 {name: '{0}'})-[r2:拥有]->(t:表)-[r3:由组成]->(a:表属性)-[r4:数据元]->(e:数据元) " \
#               "RETURN t.name as start_name, id(t) as start_id, type(r3) as relationship, " \
#               "a.name as end_name, id(a) as end_id, labels(t)[0] as start_labels, labels(a)[0] as end_labels " \
#               "UNION ALL " \
#               "MATCH (d:子域 {name: '{0}'})-[r5:拥有]->(t:表)-[:由组成]->(a:表属性)-[:数据元]->(e:数据元)-[r6:值域]->(vd:值域) " \
#               "RETURN a.name as start_name, id(a) as start_id, type(r6) as relationship, " \
#               "vd.name as end_name, id(vd) as end_id, labels(a)[0] as start_labels, labels(vd)[0] as end_labels " \
#               "UNION ALL " \
#               "MATCH (d:子域 {name: '{0}'})-[r7:拥有]->(t:表)-[:由组成]->(a:表属性)-[:数据元]->
#               (e:数据元)-[:值域]->(vd:值域)-[r8:组]->(g:值域组) " \
#               "RETURN vd.name as start_name, id(vd) as start_id, type(r8) as relationship, " \
#               "g.name as end_name, id(g) as end_id, labels(vd)[0] as start_labels, labels(g)[0] as end_labels " \
#               "UNION ALL " \
#               "MATCH (d:子域 {name: '{0}'})-[r9:拥有]->(t:表)-[:由组成]->(a:表属性)-[:数据元]->
#               (e:数据元)-[:值域]->(vd:值域)-[:组]->(g:值域组)-[r10:可允许值]->(p:可允许值) " \
#               "RETURN g.name as start_name, id(g) as start_id, type(r10) as relationship, " \
#               "p.name as end_name, id(p) as end_id, labels(g)[0] as start_labels, labels(p)[0] as end_labels ".format(
#         sub_domain_name)
#
#     print(cypher1)
#     data1 = graph.run(cypher1)
#     data_of_graph = list(data1)
#     return get_json_data(data_of_graph)


def get_mdr_table_through_sub_domain_info(identifier_attribute):
    """
    通过表属性值获取mdr六个类别的表格数据
    :param identifier_attribute:
    :return:
    """
    # 获取数据元标识符
    query = "match(a:表属性 {identifier: '%s'}) -[:数据元]-> (b:数据元) " \
            "return b.identifier as identifier" % identifier_attribute
    identifier_data_element = graph.run(query).data()
    # 判断该表属性是否和数据元建立关系
    if len(identifier_data_element) < 1:
        return {"message": "NO"}
    identifier_data_element = identifier_data_element[0]["identifier"]
    # 获取数据元表格信息
    data_element = get_mdr_table_info("数据元", identifier_data_element)

    # 获取值域念标识符
    query = "match(a:数据元 {identifier: '%s'}) -[:值域]-> (b:值域) " \
            "return b.identifier as identifier" % identifier_data_element
    identifier_value_domain = graph.run(query).data()[0]["identifier"]
    # 获取值域表格信息
    value_domain = get_mdr_table_info("值域", identifier_value_domain)

    # 获取数据元概念标识符
    query = "match(a:数据元 {identifier: '%s'}) -[:数据元概念]-> (b:数据元概念) " \
            "return b.identifier as identifier" % identifier_data_element
    identifier_data_element_concept = graph.run(query).data()[0]["identifier"]
    # 获取数据元概念表格信息
    data_element_concept = get_mdr_table_info("数据元概念", identifier_data_element_concept)

    # 获取对象类标识符
    query = "match(a:数据元概念 {identifier: '%s'}) - [:对象类]-> (b:对象类) " \
            "return b.identifier as identifier" % identifier_data_element_concept
    identifier_object_class = graph.run(query).data()[0]["identifier"]
    # 获取对象类表格信息
    object_class = get_mdr_table_info("对象类", identifier_object_class)

    # 获取属性标识符
    query = "match(a:数据元概念 {identifier: '%s'}) - [:属性]-> (b:属性) " \
            "return b.identifier as identifier" % identifier_data_element_concept
    identifier_property = graph.run(query).data()[0]["identifier"]
    # 获取属性表格信息
    property = get_mdr_table_info("属性", identifier_property)

    # 获取概念域标识符
    query = "match(a:数据元概念 {identifier: '%s'}) - [:概念域]-> (b:概念域) " \
            "return b.identifier as identifier" % identifier_data_element_concept
    identifier_conceptual_domain = graph.run(query).data()[0]["identifier"]
    # 获取概念域表格信息
    conceptual_domain = get_mdr_table_info("概念域", identifier_conceptual_domain)

    result = {"object_class": object_class, "property": property, "conceptual_domain": conceptual_domain,
              "data_element_concept": data_element_concept, "value_domain": value_domain,
              "data_element": data_element, "message": "YES"}

    return result


def get_sub_domain_properties_list(identifier_table):
    """
    通过表格标识符获取该表下的属性与属性值列表
    :param identifier_table: 表标识符
    :return:
    """
    query = "match(t:表 {identifier: '%s'}) -[:由组成]-> (a:表属性) " \
            "optional match(a:表属性) -[:约束值]-> (b:表属性值)  " \
            "return a.identifier as attribute_identifier, a.name as attribute_name, " \
            "b.identifier as attribute_value_identifier, b.name as attribute_value_name" % identifier_table
    data = graph.run(query).data()
    attributes = {}
    for line in data:
        if line["attribute_identifier"] in attributes:
            attributes[line["attribute_identifier"]]["children"].append({"value": line["attribute_value_identifier"],
                                                                         "label": line["attribute_value_name"]})
        else:
            attributes[line["attribute_identifier"]] = {"value": line["attribute_identifier"],
                                                        "label": line["attribute_name"]}
            if line["attribute_value_identifier"] is not None:
                attributes[line["attribute_identifier"]]["children"] = [{"value": line["attribute_value_identifier"],
                                                                         "label": line["attribute_value_name"]}]

    result = []
    for k, v in attributes.items():
        result.append(v)

    return result


def get_sub_domain_exist_attribute_value_options_list(identifier_table):
    cypher = "match(n:表) -[:由组成]-> (a:表属性) -[:约束值]-> (m:表属性值) " \
             "where n.identifier = '{0}' " \
             "return a.identifier as identifier_attribute, a.name as name_attribute" \
             ", m.identifier as identifier_attribute_value, m.name as name_attribute_value".format(identifier_table)
    data = graph.run(cypher).data()
    result = []
    attribute = {}
    for line in data:
        if line["identifier_attribute"] in attribute:
            attribute[line["identifier_attribute"]]["children"].append({"label": line["name_attribute_value"],
                                                                        "value": line["identifier_attribute_value"]})
        else:
            attribute[line["identifier_attribute"]] = {"label": line["name_attribute"],
                                                       "value": line["identifier_attribute"]}
            attribute[line["identifier_attribute"]]["children"] = [{"label": line["name_attribute_value"],
                                                                    "value": line["identifier_attribute_value"]}]

    for k, v in attribute.items():
        result.append(v)
    return result


def get_graph_of_attribute_info(identifier_attribute):
    """
    通过表属性标识符查询表属性相关的子图谱
    :param identifier_attribute: 表属性标识符
    :return:
    """
    query = "match(a1:表属性) -[r:数据元]-> (a2:数据元) " \
            "where a1.identifier ='{0}' " \
            "return a1.name as start_name, id(a1) as start_id, a1.identifier as start_identifier," \
            "type(r) as relationship, " \
            "a2.name as end_name, id(a2) as end_id, a2.identifier as end_identifier, " \
            "labels(a1)[0] as start_labels, labels(a2)[0] as end_labels " \
            "union all " \
            "match(a1:表属性) -[:数据元]-> (a2:数据元) -[r:值域]-> (a3:值域) " \
            "where a1.identifier ='{0}' " \
            "return a2.name as start_name, id(a2) as start_id, a2.identifier as start_identifier," \
            "type(r) as relationship, " \
            "a3.name as end_name, id(a3) as end_id, a3.identifier as end_identifier, " \
            "labels(a2)[0] as start_labels, labels(a3)[0] as end_labels " \
            "union all " \
            "match(a1:表属性) -[:数据元]-> (a2:数据元) -[:值域]-> (a3:值域) -[r:组]-> (a4:值域组) " \
            "where a1.identifier ='{0}' " \
            "return a3.name as start_name, id(a3) as start_id, a3.identifier as start_identifier, " \
            "type(r) as relationship, " \
            "a4.name as end_name, id(a4) as end_id, a4.identifier as end_identifier, " \
            "labels(a3)[0] as start_labels, labels(a4)[0] as end_labels " \
            "union all " \
            "match(a1:表属性) -[:数据元]-> (a2:数据元) -[:值域]-> (a3:值域) -[:组]-> (a4:值域组) -[r:可允许值]-> (a5:可允许值) " \
            "where a1.identifier ='{0}' " \
            "return a4.name as start_name, id(a4) as start_id, a4.identifier as start_identifier, " \
            "type(r) as relationship, " \
            "a5.name as end_name, id(a5) as end_id, a5.identifier as end_identifier, " \
            "labels(a4)[0] as start_labels, labels(a5)[0] as end_labels " \
            "union all " \
            "match(a1:表属性) -[:数据元]-> (a2:数据元) -[:值域]-> (a3:值域) -[:组]-> " \
            "(a4:值域组) -[:可允许值]-> (a5:可允许值) -[r:值含义]-> (a6:值含义) " \
            "where a1.identifier ='{0}' " \
            "return a5.name as start_name, id(a5) as start_id, a5.identifier as start_identifier, " \
            "type(r) as relationship, " \
            "a6.name as end_name, id(a6) as end_id, a6.identifier as end_identifier, " \
            "labels(a5)[0] as start_labels, labels(a6)[0] as end_labels " \
            "union all " \
            "match(a1:表属性) -[r:约束值]-> (a2:表属性值) " \
            "where a1.identifier ='{0}' " \
            "return a1.name as start_name, id(a1) as start_id, a1.identifier as start_identifier, " \
            "type(r) as relationship, " \
            "a2.name as end_name, id(a2) as end_id, a2.identifier as end_identifier, " \
            "labels(a1)[0] as start_labels, labels(a2)[0] as end_labels " \
            "union all " \
            "match(a1:表属性) -[:约束值]-> (a2:表属性值) -[r:可允许值]-> (a3:可允许值) " \
            "where a1.identifier ='{0}' " \
            "return a2.name as start_name, id(a2) as start_id, a2.identifier as start_identifier, " \
            "type(r) as relationship, " \
            "a3.name as end_name, id(a3) as end_id, a3.identifier as end_identifier, " \
            "labels(a2)[0] as start_labels, labels(a3)[0] as end_labels ".format(identifier_attribute)
    data = graph.run(query)
    data_of_graph = list(data)
    if len(data_of_graph) == 0:
        cypher = "match(a:表属性) where a.identifier = '{0}' " \
                 "return a.name as name, labels(a) as labels, a.identifier as identifier".format(identifier_attribute)
        data_of_node = graph.run(cypher).data()[0]
        print(data_of_node)
        node = {"name": data_of_node["name"], "category": CLASS_LIST_Attribute[data_of_node["labels"][0]],
                "identifier": data_of_node["identifier"]}
        result = {"data": [node], "links": []}
        return result
    return get_json_data_of_attribute_graph(data_of_graph)


def get_json_data_of_attribute_graph(data_of_graph):
    json_data = {'data': [], "links": []}
    id_to_id = {}
    count = 0
    for i in data_of_graph:
        _i = i["start_id"]
        if not (_i in id_to_id):
            id_to_id[_i] = count
            count += 1
            node = {"name": i["start_name"], "category": CLASS_LIST_Attribute[i["start_labels"]],
                    "identifier": i["start_identifier"]}
            json_data["data"].append(node)

        _i = i["end_id"]
        if not (_i in id_to_id):
            id_to_id[_i] = count
            count += 1
            node = {"name": i["end_name"], "category": CLASS_LIST_Attribute[i["end_labels"]],
                    "identifier": i["end_identifier"]}
            json_data["data"].append(node)

    for i in data_of_graph:
        # 处理边
        edge = {"source": id_to_id[i["start_id"]], "target": id_to_id[i["end_id"]],
                "value": i["relationship"]}
        json_data['links'].append(edge)

    return json_data
