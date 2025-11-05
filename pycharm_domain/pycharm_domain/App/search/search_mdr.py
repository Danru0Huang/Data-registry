from ..config import graph, CLASS_LIST_MDR


def get_object_class_option_list():
    """
    获得MDR对象类列表信息，支持前端对象类下拉选择器
    :return:
    """
    query = "match (n:对象类) return n.identifier, n.name"
    data = graph.run(query).data()
    result = []
    item = {}
    for line in data:
        item["label"] = line["n.name"]
        item["value"] = line["n.identifier"]
        result.append(item)
        item = {}
    return result


def get_property_option_list():
    """
    获得MDR属性列表信息，支持前端属性选择器
    :return:
    """
    query = "match (n:属性) return n.identifier, n.name"
    data = graph.run(query).data()
    result = []
    item = {}
    for line in data:
        item["label"] = line["n.name"]
        item["value"] = line["n.identifier"]
        result.append(item)
        item = {}
    return result


def get_conceptual_domain_option_list():
    """
    获得概念域信息列表，之前前端概念域选择器
    :return:
    """
    query = "match (n:概念域) return n.identifier, n.name"
    data = graph.run(query).data()
    result = []
    item = {}
    for line in data:
        item["label"] = line["n.name"]
        item["value"] = line["n.identifier"]
        result.append(item)
        item = {}
    return result


def get_value_meanings_option_list():
    """
    获得值含义列表，支持前端值含义选择器
    :return:
    """
    query = "match (n:值含义) return n.identifier, n.name"
    data = graph.run(query).data()
    result = []
    item = {}
    for line in data:
        item["label"] = line["n.name"]
        item["value"] = line["n.identifier"]
        result.append(item)
        item = {}
    return result


def get_data_element_concept_option_list():
    """
    获得数据元概念列表，支持前端数据元概念选择器
    :return:
    """
    query = "match (n:数据元概念) return n.identifier, n.name"
    data = graph.run(query).data()
    result = []
    item = {}
    for line in data:
        item["label"] = line["n.name"]
        item["value"] = line["n.identifier"]
        result.append(item)
        item = {}
    return result


def get_value_domain_option_list():
    """
    获取MDR值域列表，支持前端值域选择器
    :return:
    """
    query = "match (n:值域) return n.identifier, n.name"
    data = graph.run(query).data()
    result = []
    item = {}
    for line in data:
        item["label"] = line["n.name"]
        item["value"] = line["n.identifier"]
        result.append(item)
        item = {}
    return result


def get_data_element_option_list():
    """
    获取MDR数据元列表，支持前端数据元选择器
    :return:
    """
    query = "match (n:数据元) return n.identifier, n.name"
    data = graph.run(query).data()
    result = []
    item = {}
    for line in data:
        item["label"] = line["n.name"]
        item["value"] = line["n.identifier"]
        result.append(item)
        item = {}
    return result


def get_value_domain_and_permissible_values_option_list():
    """
    获取值域与可允许值的级联选择器列表信息
    :return:
    """
    query = "match(n:值域) -[:组]-> (g:值域组) -[:可允许值]-> (p:可允许值) " \
            "return n.name as v_name, n.identifier as v_identifier, p.name as p_name, p.identifier as p_identifier"
    data = graph.run(query).data()
    result = []
    value_domain = {}
    for line in data:
        if line["v_identifier"] in value_domain:
            value_domain[line["v_identifier"]]["children"].append(
                {"value": line["p_identifier"], "label": line["p_name"]})
        else:
            value_domain[line["v_identifier"]] = {"value": line["v_identifier"], "label": line["v_name"],
                                                  "children": [
                                                      {"value": line["p_identifier"], "label": line["p_name"]}]}

    for k, v in value_domain.items():
        result.append(v)
    return result


def get_mdr_table_list_info(label):
    """
    通过label获取MDR六个类别的注册信息，并以表格列表的数据形式返回由前端展示
    :param label:
    :return:
    """
    if label == "对象类" or label == "属性":
        cypher = "match(n:%s)  " \
                 "return n.name as name, n.identifier as identifier, " \
                 "n.personId as personId, n.time as time, " \
                 "n.describe as describe, n.department as department, " \
                 "n.version as version, n.status as status" % label
        result = graph.run(cypher).data()
        result = list(result)
        return result
    elif label == "概念域":
        cypher = "match(n:%s) " \
                 "optional match(n) -[:值含义]-> (v:值含义) " \
                 "return n.name as name, n.identifier as identifier, " \
                 "n.personId as personId, n.time as time, " \
                 "n.describe as describe, n.department as department, " \
                 "n.version as version, n.status as status, " \
                 "v.name as vName, v.identifier as vIdentifier, " \
                 "v.status as vStatus, v.time as vTime, v.version as vVersion" % label
        results = graph.run(cypher).data()
        conceptualDomains = {}
        for result in results:
            if result["identifier"] in conceptualDomains:
                valueMeaning = {"vName": result["vName"], "vIdentifier": result["vIdentifier"],
                                "vStatus": result["vStatus"], "vTime": result["vTime"], "vVersion": result["vVersion"]}
                conceptualDomains[result["identifier"]]["valueMeanings"]["valueMeanings"].append(valueMeaning)
            else:
                conceptualDomains[result["identifier"]] = {}
                conceptualDomains[result["identifier"]]["name"] = result["name"]
                conceptualDomains[result["identifier"]]["identifier"] = result["identifier"]
                conceptualDomains[result["identifier"]]["personId"] = result["personId"]
                conceptualDomains[result["identifier"]]["time"] = result["time"]
                conceptualDomains[result["identifier"]]["describe"] = result["describe"]
                conceptualDomains[result["identifier"]]["department"] = result["department"]
                conceptualDomains[result["identifier"]]["version"] = result["version"]
                conceptualDomains[result["identifier"]]["status"] = result["status"]
                valueMeaning = {"vName": result["vName"], "vIdentifier": result["vIdentifier"],
                                "vStatus": result["vStatus"], "vTime": result["vTime"], "vVersion": result["vVersion"]}
                conceptualDomains[result["identifier"]]["valueMeanings"] = {"valueMeanings": [valueMeaning]}
        data = []
        for key, value in conceptualDomains.items():
            data.append(value)
        return data
    elif label == "数据元概念":
        cypher = "MATCH (n:%s) " \
                 "OPTIONAL MATCH (n)-[:对象类]->(ocl) " \
                 "WITH n, ocl " \
                 "MATCH (n)-[:属性]->(prp) " \
                 "WITH n, ocl, prp " \
                 "MATCH (n)-[:概念域]->(cdm) " \
                 "RETURN n.name AS name, n.identifier AS identifier, n.personId AS personId, " \
                 "n.time AS time, n.describe AS describe, n.department AS department, n.version AS version," \
                 "n.status AS status, ocl.name AS OCLName, ocl.identifier AS OCLIdentifier, prp.name AS PRPName, " \
                 "prp.identifier AS PRPIdentifier, cdm.name AS CDMName, cdm.identifier AS CDMIdentifier" % label
        result = graph.run(cypher).data()
        result = list(result)
        return result
    elif label == "值域":
        cypher1 = "match(n:值域) " \
                  "optional match(n) -[:组]->(group)-[:可允许值]->(pev)-[:值含义]->(vlm) " \
                  "return n.name as name, n.identifier as identifier, n.personId as personId, n.time as time, " \
                  "n.describe as describe, n.department as department, n.version as version, n.status as status, " \
                  "n.indefinite as indefinite," \
                  "pev.name as PEVName, pev.identifier as PEVIdentifier, " \
                  "vlm.name as VLMName, vlm.identifier as VLMIdentifier"
        results1 = graph.run(cypher1).data()
        cypher2 = "match(a:值域) -[:概念域]-> (b:概念域) return a.identifier as identifier, " \
                  "b.name as CDMName, b.identifier as CDMIdentifier"
        results2 = graph.run(cypher2).data()
        conceptual_domain = {}
        for result in results2:
            conceptual_domain[result["identifier"]] = {}
            conceptual_domain[result["identifier"]]["CDMName"] = result["CDMName"]
            conceptual_domain[result["identifier"]]["CDMIdentifier"] = result["CDMIdentifier"]

        valueDomains = {}
        for result in results1:
            if result["identifier"] in valueDomains:
                permissibleValue = {"PEVName": result["PEVName"], "PEVIdentifier": result["PEVIdentifier"],
                                    "VLMName": result["VLMName"], "VLMIdentifier": result["VLMIdentifier"]}
                valueDomains[result["identifier"]]["permissibleValues"]["permissibleValues"].append(permissibleValue)
            else:
                valueDomains[result["identifier"]] = {}
                valueDomains[result["identifier"]]["name"] = result["name"]
                valueDomains[result["identifier"]]["identifier"] = result["identifier"]
                valueDomains[result["identifier"]]["personId"] = result["personId"]
                valueDomains[result["identifier"]]["time"] = result["time"]
                valueDomains[result["identifier"]]["describe"] = result["describe"]
                valueDomains[result["identifier"]]["department"] = result["department"]
                valueDomains[result["identifier"]]["version"] = result["version"]
                valueDomains[result["identifier"]]["status"] = result["status"]
                if result["indefinite"] == "null":
                    result["indefinite"] = "暂无信息"
                valueDomains[result["identifier"]]["indefinite"] = result["indefinite"]
                valueDomains[result["identifier"]]["CDMName"] = conceptual_domain[result["identifier"]]["CDMName"]
                valueDomains[result["identifier"]]["CDMIdentifier"] = \
                    conceptual_domain[result["identifier"]]["CDMIdentifier"]
                permissibleValue = {"PEVName": result["PEVName"], "PEVIdentifier": result["PEVIdentifier"],
                                    "VLMName": result["VLMName"], "VLMIdentifier": result["VLMIdentifier"]}
                valueDomains[result["identifier"]]["permissibleValues"] = {"permissibleValues": [permissibleValue]}

        data = []
        for key, value in valueDomains.items():
            data.append(value)
        return data
    elif label == "数据元":
        cypher = "match(n:数据元) " \
                 "optional match(n) -[:数据元概念]-> (dec) " \
                 "with n,dec " \
                 "match(n) -[:值域]-> (vdm) " \
                 "return n.name as name, n.identifier as identifier, n.personId as personId, n.time as time," \
                 " n.describe as describe, n.department as department, n.version as version, n.status as status, " \
                 "dec.name as DECName, dec.identifier as DECIdentifier, " \
                 "vdm.name as VDMName, vdm.identifier as VDMIdentifier"
        result = graph.run(cypher).data()
        result = list(result)
        return result


def get_mdr_table_info(label, identifier):
    """
    通过指定label和标识符，获取MDR六个类别中，具体某一个注册项的信息
    :param label:
    :param identifier:
    :return:
    """
    if label == "对象类" or label == "属性":
        cypher = "match(n:%s) where n.identifier='%s' " \
                 "return n.name as name, n.identifier as identifier, " \
                 "n.personId as personId, n.time as time, " \
                 "n.describe as describe, n.department as department, " \
                 "n.version as version, n.status as status" % (label, identifier)
        result = graph.run(cypher).data()
        return result
    if label == "概念域":
        cypher1 = "match(n:%s) where n.identifier='%s' " \
                  "return n.name as name, n.identifier as identifier, " \
                  "n.personId as personId, n.time as time, " \
                  "n.describe as describe, n.department as department, " \
                  "n.version as version, n.status as status" % (label, identifier)
        conceptual_domain = graph.run(cypher1).data()

        cypher2 = "match(n:%s) -[:值含义]-> (v:值含义) where n.identifier='%s' " \
                  "return v.name as name, v.identifier as identifier, v.status as status, " \
                  "v.time as time, v.version as version" % (label, identifier)
        value_meanings = graph.run(cypher2).data()
        result = [conceptual_domain, value_meanings]
        return result
    if label == "数据元概念":
        cypher = "match(n:%s) where n.identifier='%s' " \
                 "return n.name as name, n.identifier as identifier, " \
                 "n.personId as personId, n.time as time, " \
                 "n.describe as describe, n.department as department, " \
                 "n.version as version, n.status as status" % (label, identifier)
        result = graph.run(cypher).data()
        cypher = "match(n:%s) -[:对象类]-> (m:对象类) " \
                 "where n.identifier = '%s' " \
                 "return m.name as OCLName, m.identifier as OCLIdentifier" % (label, identifier)
        temp_data = graph.run(cypher).data()
        result[0]["OCLName"] = temp_data[0]["OCLName"]
        result[0]["OCLIdentifier"] = temp_data[0]["OCLIdentifier"]

        cypher = "match(n:%s) -[:属性]-> (m:属性) " \
                 "where n.identifier = '%s' " \
                 "return m.name as PRPName, m.identifier as PRPIdentifier" % (label, identifier)
        temp_data = graph.run(cypher).data()
        result[0]["PRPName"] = temp_data[0]["PRPName"]
        result[0]["PRPIdentifier"] = temp_data[0]["PRPIdentifier"]

        cypher = "match(n:%s) -[:概念域]-> (m:概念域) " \
                 "where n.identifier = '%s' " \
                 "return m.name as CDMName, m.identifier as CDMIdentifier" % (label, identifier)
        temp_data = graph.run(cypher).data()
        result[0]["CDMName"] = temp_data[0]["CDMName"]
        result[0]["CDMIdentifier"] = temp_data[0]["CDMIdentifier"]
        return result
    if label == "值域":
        cypher = "match(n:%s) where n.identifier='%s' " \
                 "return n.name as name, n.identifier as identifier, " \
                 "n.personId as personId, n.time as time, " \
                 "n.describe as describe, n.department as department, " \
                 "n.version as version, n.status as status, n.indefinite as indefinite" % (label, identifier)
        value_domain = graph.run(cypher).data()
        if value_domain[0]["indefinite"] == "null":
            value_domain[0]["indefinite"] = "暂无信息"
        cypher = "match(n:%s) -[:概念域]-> (m:概念域) " \
                 "where n.identifier = '%s' " \
                 "return m.name as CDMName, m.identifier as CDMIdentifier" % (label, identifier)
        temp_data = graph.run(cypher).data()
        value_domain[0]["CDMName"] = temp_data[0]["CDMName"]
        value_domain[0]["CDMIdentifier"] = temp_data[0]["CDMIdentifier"]
        cypher = "match(n:%s) -[:组]-> (g:值域组) -[:可允许值]-> (p:可允许值) -[:值含义]-> (v:值含义) " \
                 "where n.identifier = '%s' return p.name as PEVName, " \
                 "p.identifier as PEVIdentifier, v.name as VLMName, v.identifier as VLMIdentifier" % (label, identifier)
        permissible_values = graph.run(cypher).data()
        result = [value_domain, permissible_values]

        return result
    if label == "数据元":
        cypher = "match(n:%s) where n.identifier='%s' " \
                 "return n.name as name, n.identifier as identifier, " \
                 "n.personId as personId, n.time as time, " \
                 "n.describe as describe, n.department as department, " \
                 "n.version as version, n.status as status" % (label, identifier)
        result = graph.run(cypher).data()

        cypher = "match(n:%s) -[:数据元概念]-> (m:数据元概念) " \
                 "where n.identifier = '%s' " \
                 "return m.name as DECName, m.identifier as DECIdentifier" % (label, identifier)
        temp_data = graph.run(cypher).data()
        result[0]["DECName"] = temp_data[0]["DECName"]
        result[0]["DECIdentifier"] = temp_data[0]["DECIdentifier"]

        cypher = "match(n:%s) -[:值域]-> (m:值域) " \
                 "where n.identifier = '%s' " \
                 "return m.name as VDMName, m.identifier as VDMIdentifier" % (label, identifier)
        temp_data = graph.run(cypher).data()
        result[0]["VDMName"] = temp_data[0]["VDMName"]
        result[0]["VDMIdentifier"] = temp_data[0]["VDMIdentifier"]
        return result


def get_json_data(data_of_graph):
    """
    将数据库中查询到的图谱数据进行处理
    :param data_of_graph:
    :return:
    """
    json_data = {'data': [], "links": []}
    # name_to_id = {}
    id_to_id = {}
    id_to_identifier = {}
    for i in data_of_graph:
        _i = i["start_id"]
        if not (_i in id_to_identifier):
            id_to_identifier[_i] = i["start_identifier"]

        _i = i["end_id"]
        if not (_i in id_to_identifier):
            id_to_identifier[_i] = i["end_identifier"]
    count = 0
    for i in data_of_graph:
        _i = i["start_id"]
        if not (_i in id_to_id):
            id_to_id[_i] = count
            count += 1
            node = {"name": i["start_name"], "category": CLASS_LIST_MDR[i["start_labels"]],
                    "identifier": id_to_identifier[_i]}
            json_data["data"].append(node)

        _i = i["end_id"]
        if not (_i in id_to_id):
            id_to_id[_i] = count
            count += 1
            node = {"name": i["end_name"], "category": CLASS_LIST_MDR[i["end_labels"]],
                    "identifier": id_to_identifier[_i]}
            json_data["data"].append(node)
    # for i in data_of_graph:
    #     _name = i["start_name"]
    #     if not (_name in name_to_id):
    #         name_to_id[_name] = count
    #         count += 1
    #         node = {"name": i["start_name"], "category": CLASS_LIST_MDR[i["start_labels"]]}
    #         json_data["data"].append(node)
    #
    #     _name = i["end_name"]
    #     if not (_name in name_to_id):
    #         name_to_id[_name] = count
    #         count += 1
    #         node = {"name": i["end_name"], "category": CLASS_LIST_MDR[i["end_labels"]]}
    #         json_data["data"].append(node)

    # for i in data_of_graph:
    #     edge = {"source": name_to_id[i["start_name"]], "target": name_to_id[i["end_name"]],
    #             "value": i["relationship"]}
    #     json_data['links'].append(edge)

    for i in data_of_graph:
        edge = {"source": id_to_id[i["start_id"]], "target": id_to_id[i["end_id"]],
                "value": i["relationship"]}
        json_data['links'].append(edge)

    nodes = calculate_x_and_y(json_data["data"], json_data["links"])
    json_data["data"] = []
    for k, v in nodes.items():
        json_data["data"].append(v)

    return json_data


def calculate_x_and_y(data_nodes, data_links):
    nodes = {}
    count = 0
    for line in data_nodes:
        line["id"] = count
        nodes[count] = line
        count += 1
    value_meanings = []
    groups = []
    for k, v in nodes.items():
        if v["category"] == 0:
            nodes[k]["x"] = 100
            nodes[k]["y"] = 50
            nodes[k]["symbol"] = "roundRect"
        elif v["category"] == 1:
            nodes[k]["x"] = 200
            nodes[k]["y"] = 50
            nodes[k]["symbol"] = "roundRect"
        elif v["category"] == 2:
            nodes[k]["x"] = 400
            nodes[k]["y"] = 100
            nodes[k]["symbol"] = "roundRect"
        elif v["category"] == 3:
            nodes[k]["x"] = 150
            nodes[k]["y"] = 100
            nodes[k]["symbol"] = "roundRect"
        elif v["category"] == 4:
            nodes[k]["x"] = 400
            nodes[k]["y"] = 350
            nodes[k]["symbol"] = "roundRect"
        elif v["category"] == 5:
            nodes[k]["x"] = 150
            nodes[k]["y"] = 350
            nodes[k]["symbol"] = "roundRect"
        elif v["category"] == 7:
            value_meanings.append(k)
        elif v["category"] == 8:
            groups.append(k)

    y_vlm = 130
    y_groups = 280
    y_pev = 200
    x_offset = 500
    for temp in value_meanings:
        nodes[temp]["x"] = x_offset
        nodes[temp]["y"] = y_vlm
        nodes[temp]["symbol"] = "roundRect"
        nodes[temp]["symbolSize"] = 50
        x_offset += 200

    x_offset_1 = 480
    x_offset_2 = 420
    for temp in groups:
        nodes[temp]["x"] = x_offset_1
        nodes[temp]["y"] = y_groups
        nodes[temp]["symbol"] = "roundRect"
        nodes[temp]["symbolSize"] = 50
        x_offset_1 += 100
        permissible_values = get_permissible_values_id_groups(temp, data_links)
        for value in permissible_values:
            nodes[value]["x"] = x_offset_2
            nodes[value]["y"] = y_pev
            nodes[value]["symbol"] = "roundRect"
            nodes[value]["symbolSize"] = 40
            x_offset_2 += 50

    return nodes


def get_permissible_values_id_groups(source, links):
    result = []
    for link in links:
        if link["source"] == source and link["value"] == "可允许值":
            result.append(link["target"])

    return result


def get_graph_of_mdr_info(identifier_data_element):
    """
    获取MDR图谱，通过数据元标识符，获取与在共享域内与该数据元相关的其他MDR信息，并以图谱的形式返回
    :param identifier_data_element:
    :return:
    """
    cypher1 = "match(a1:数据元) -[r1:数据元概念]-> (a2:数据元概念) " \
              "where a1.identifier = '{0}'" \
              "return a1.name as start_name, id(a1) as start_id, a1.identifier as start_identifier, " \
              "type(r1) as relationship, " \
              "a2.name as end_name, id(a2) as end_id, a2.identifier as end_identifier," \
              "labels(a1)[0] as start_labels, labels(a2)[0] as end_labels " \
              "union all " \
              "match(a1:数据元) -[:数据元概念]-> (a2:数据元概念) -[r2:对象类]-> (a3:对象类) " \
              "where a1.identifier = '{0}' " \
              "return a2.name as start_name, id(a2) as start_id, a2.identifier as start_identifier," \
              "type(r2) as relationship, " \
              "a3.name as end_name, id(a3) as end_id, a3.identifier as end_identifier," \
              "labels(a2)[0] as start_labels, labels(a3)[0] as end_labels " \
              "union all " \
              "match(a1:数据元) -[:数据元概念]-> (a2:数据元概念) -[r3:属性]-> (a3:属性)" \
              "where a1.identifier = '{0}' " \
              "return a2.name as start_name, id(a2) as start_id, a2.identifier as start_identifier," \
              "type(r3) as relationship, " \
              "a3.name as end_name, id(a3) as end_id, a3.identifier as end_identifier," \
              "labels(a2)[0] as start_labels, labels(a3)[0] as end_labels " \
              "union all " \
              "match(a1:数据元) -[:数据元概念]-> (a2:数据元概念) -[r4:概念域]-> (a3:概念域)" \
              "where a1.identifier = '{0}'  " \
              "return a2.name as start_name, id(a2) as start_id, a2.identifier as start_identifier," \
              "type(r4) as relationship, " \
              "a3.name as end_name, id(a3) as end_id, a3.identifier as end_identifier," \
              "labels(a2)[0] as start_labels, labels(a3)[0] as end_labels " \
              "union all " \
              "match(a1:数据元) -[:数据元概念]-> (a2:数据元概念) -[:概念域]-> (a3:概念域) -[r5:值含义]-> (a4:值含义) " \
              "where a1.identifier = '{0}' " \
              "return a3.name as start_name, id(a3) as start_id, a3.identifier as start_identifier," \
              "type(r5) as relationship, " \
              "a4.name as end_name, id(a4) as end_id, a4.identifier as end_identifier," \
              "labels(a3)[0] as start_labels, labels(a4)[0] as end_labels " \
              "union all " \
              "match(a1:数据元) -[r6:值域]-> (a2:值域) " \
              "where a1.identifier = '{0}'  " \
              "return a1.name as start_name, id(a1) as start_id, a1.identifier as start_identifier," \
              "type(r6) as relationship, " \
              "a2.name as end_name, id(a2) as end_id, a2.identifier as end_identifier," \
              "labels(a1)[0] as start_labels, labels(a2)[0] as end_labels " \
              "union all " \
              "match(a1:数据元) -[:值域]-> (a2:值域) -[r7:概念域]-> (a3:概念域)" \
              "where a1.identifier = '{0}'  " \
              "return a2.name as start_name, id(a2) as start_id, a2.identifier as start_identifier," \
              "type(r7) as relationship, " \
              "a3.name as end_name, id(a3) as end_id, a3.identifier as end_identifier," \
              "labels(a2)[0] as start_labels, labels(a3)[0] as end_labels " \
              "union all " \
              "match(a1:数据元) -[:值域]-> (a2:值域) -[r8:组]-> (a3:值域组) " \
              "where a1.identifier = '{0}'  " \
              "return a2.name as start_name, id(a2) as start_id, a2.identifier as start_identifier," \
              "type(r8) as relationship, " \
              "a3.name as end_name, id(a3) as end_id, a3.identifier as end_identifier," \
              "labels(a2)[0] as start_labels, labels(a3)[0] as end_labels " \
              "union all " \
              "match(a1:数据元) -[:值域]-> (a2:值域) -[:组]-> (a3:值域组) -[r9:可允许值]-> (a4:可允许值) " \
              "where a1.identifier = '{0}'   " \
              "return a3.name as start_name, id(a3) as start_id, a3.identifier as start_identifier," \
              "type(r9) as relationship, " \
              "a4.name as end_name, id(a4) as end_id, a4.identifier as end_identifier," \
              "labels(a3)[0] as start_labels, labels(a4)[0] as end_labels " \
              "union all " \
              "match(a1:数据元) -[:值域]-> (a2:值域) -[:组]-> (a3:值域组) -[:可允许值]-> (a4:可允许值) -[r10:值含义]-> (a5:值含义)" \
              "where a1.identifier = '{0}'   " \
              "return a4.name as start_name, id(a4) as start_id, a4.identifier as start_identifier," \
              "type(r10) as relationship, " \
              "a5.name as end_name, id(a5) as end_id, a5.identifier as end_identifier," \
              "labels(a4)[0] as start_labels, labels(a5)[0] as end_labels ".format(identifier_data_element)
    print(cypher1)
    data1 = graph.run(cypher1)
    data_of_graph = list(data1)
    return get_json_data(data_of_graph)
