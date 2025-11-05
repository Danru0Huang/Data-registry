from ..config import graph, CLASS_LIST_Model


def get_model_class_name_options_list(model_name):
    """
    通过模型名称，查询该名称下所拥有的类名称，并返回支持前端列名成下拉列表的选中
    :param model_name: 模型名称
    :return: 类名称列表
    """
    cypher = "match(n:模型) -[:类]-> (c) where n.name = '%s' return c.name as name" % model_name
    results = graph.run(cypher).data()
    data = []
    for result in results:
        item = {"label": result["name"], "value": result["name"]}
        data.append(item)
    return data


def get_all_class_number():
    """
    查询信息模型下所有类别的节点数量，并返回节点数量列表
    :return: 节点数量列表
    """
    cypher = "MATCH (n) RETURN labels(n)[0] as label, count(*) as node_count"
    results = graph.run(cypher).data()
    data = []
    for result in results:
        item = {"label": result["label"], "node_count": result["node_count"]}
        data.append(item)
    return data


def get_model_type_options_list():
    """
    获取模型名字列表
    :return:
    """
    cypher = "match(n:模型) return n.name as name"
    results = graph.run(cypher).data()
    data = []
    for result in results:
        item = {"label": result["name"], "value": result["name"]}
        data.append(item)
    print(data)
    return data


def get_class_name_and_property_name_options_list(model_name):
    """
    通过模型名称获取该模型下的类及其属性列表
    :param model_name: 模型名称
    :return:
    """
    cypher = "match(a:模型) -[:类]-> (b:模型类) " \
             "where a.name = '{0}' " \
             "optional  match(a:模型) -[:类]-> (b:模型类) -[:属性]-> (c:模型属性)  " \
             "return b.name as class_name, c.name as property_name".format(model_name)
    data = graph.run(cypher).data()
    class_list = {}
    for line in data:
        if line["class_name"] in class_list:
            class_list[line["class_name"]]["children"].append({"value": line["property_name"],
                                                               "label": line["property_name"]})
        else:
            class_list[line["class_name"]] = {"value": line["class_name"], "label": line["class_name"]}
            if line["property_name"] is not None:
                class_list[line["class_name"]]["children"] = [{"value": line["property_name"],
                                                               "label": line["property_name"]}]

    result = []
    for k, v in class_list.items():
        result.append(v)

    return result



def get_sub_domain_lists():
    """
    获取子域名字列表以及对应的表格标识符
    :return: 子域列表和表格标识符列表
    """
    cypher = "MATCH (n:子域)-[:拥有]->(t:表) RETURN n.name as name, t.identifier as identifier"
    results = graph.run(cypher).data()
    data = [{"name": result["name"], "id": result["identifier"]} for result in results]
    print(data)
    return data


def get_sub_domain_table_relations(sub_domain_name):
    """
    根据子域名称，获取该子域下所有表格的名称和标识符
    :param sub_domain_name: 子域的名称
    :return: 与子域相关联的所有表格的名称（文件名）和标识符的列表
    """
    query = """
    MATCH (sub_domain:子域 {name: $sub_domain_name})-[:拥有]->(table:表)
    RETURN table.name AS filename, table.identifier AS identifier
    """
    # 执行Cypher查询，传入子域名称作为参数
    data = graph.run(query, sub_domain_name=sub_domain_name).data()

    # 处理查询结果，构建最终的返回列表
    result = [{"filename": row["filename"], "identifier": row["identifier"]} for row in data]

    return result


def query_graph_of_model(name):
    """
    从数据库中查询信息模型的图谱数据，经过数据处理之后返回前端
    :param name: 模型名称
    :return: 处理后的图谱数据及表格数据
    """
    cypher = "match(t:模型) -[r1:类]-> (c:模型类) " \
             "where t.name ='%s' " \
             "return t.name as start_name, id(t) as start_id, type(r1) as relationship, " \
             "c.name as end_name, id(c) as end_id, " \
             "labels(t)[0] as start_labels, labels(c)[0] as end_labels " \
             "union all " \
             "match(t:模型) -[:类]-> (c:模型类) -[r2:属性]->(p:模型属性) " \
             "where t.name = '%s' " \
             "return c.name as start_name, id(c) as start_id, type(r2) as relationship, " \
             "p.name as end_name, id(p) as end_id, " \
             "labels(c)[0] as start_labels, labels(p)[0] as end_labels " \
             "union all " \
             "match(t:模型) -[:类]-> (c1:模型类) -[r3]-> (c2:模型类) " \
             "where t.name ='%s' " \
             "return c1.name as start_name, id(c1) as start_id, type(r3) as relationship, " \
             "c2.name as end_name, id(c2) as end_id, " \
             "labels(c1)[0] as start_labels, labels(c2)[0] as end_labels" % (name, name, name)
    # cypher = "MATCH (m:数据元概念 {name: '专利法律状态'})-[:属性]->(c1:属性) " \
    #          "MATCH (m)-[:对象类]->(c2:对象类) " \
    #          "MATCH (h1:数据元 {name: 'DE专利法律状态'})-[:数据元概念]->(m) " \
    #          "MATCH (m)-[:概念域]->(p1:概念域) " \
    #          "MATCH (h1)-[:值域]->(p2:值域) " \
    #          "RETURN m, c1, c2, h1, p1, p2"

    data = graph.run(cypher)
    data = list(data)
    return get_json_data(data)


def get_json_data(data):
    """
    将数据库中读取到的数据进行处理，分别获得前端图谱中的节点信息、边信息以及表格信息
    :param data: 数据库中查询到的数据
    :return:
    """
    json_data = {'data': [], "links": [], "tableData": []}  # 返回前端的数据：节点信息、边信息、表格信息
    # name_to_id = {}
    id_to_id = {}
    count = 0
    for i in data:
        _i = i["start_id"]
        if not (_i in id_to_id):
            id_to_id[_i] = count
            count += 1
            node = {"name": i["start_name"], "category": CLASS_LIST_Model[i["start_labels"]]}
            json_data["data"].append(node)

        _i = i["end_id"]
        if not (_i in id_to_id):
            id_to_id[_i] = count
            count += 1
            node = {"name": i["end_name"], "category": CLASS_LIST_Model[i["end_labels"]]}
            json_data["data"].append(node)
    # for i in data:
    #     # 为每一个节点分配一个id，并将节点信息存储
    #     _name = i["start_name"]
    #     if not (_name in name_to_id):
    #         name_to_id[_name] = count
    #         count += 1
    #         node = {"name": i["start_name"], "category": CLASS_LIST_Model[i["start_labels"]]}
    #         json_data["data"].append(node)
    #
    #     _name = i["end_name"]
    #     if not (_name in name_to_id):
    #         name_to_id[_name] = count
    #         count += 1
    #         node = {"name": i["end_name"], "category": CLASS_LIST_Model[i["end_labels"]]}
    #         json_data["data"].append(node)

    for i in data:
        # 处理边
        edge = {"source": id_to_id[i["start_id"]], "target": id_to_id[i["end_id"]],
                "value": i["relationship"]}
        json_data['links'].append(edge)

    # 处理表格信息，将每一个类及其对应的属性提取
    modelClass_list = []
    modelClass = {}
    for i in data:
        if i["relationship"] == "属性":
            if i["start_name"] in modelClass:
                modelClass[i["start_name"]].append({"value": i["end_name"]})
            else:
                # modelClass[i["start_name"]] = {}
                modelClass[i["start_name"]] = [{"value": i["end_name"]}]
    for i in data:
        if i["start_labels"] == "模型":
            if not i["end_name"] in modelClass:
                modelClass[i["end_name"]] = [{"value": "暂无属性"}]
    for k, v in modelClass.items():
        modelClass_list.append({"name": k, "values": v})
    for i in data:
        table_item = {"start": i["start_name"], "relation": i["relationship"], "end": i["end_name"]}
        json_data["tableData"].append(table_item)
    # print(json_data)
    json_data["list"] = modelClass_list
    print(modelClass_list)
    return json_data
