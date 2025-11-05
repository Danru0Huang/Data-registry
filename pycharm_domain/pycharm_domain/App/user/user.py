from ..config import graph, LABEL_CHANGE_1, LABEL_CHANGE_2, CLASS_LIST_Attribute_AND_Data_Element, LABEL_CHANGE_3, \
    CLASS_LIST_Attribute_Value_AND_Permissible_Value
from ..search.search_mdr import get_graph_of_mdr_info


def get_model_and_model_class_options_list():
    """
    获取模型及模型类选项列表
    :return:
    """
    cypher = "match(n:模型) optional match(n) -[:类]-> (m:模型类) " \
             "return n.name as model_name, m.name as class_name"
    data = graph.run(cypher).data()
    model = {}
    for line in data:
        if line["model_name"] in model:
            model[line["model_name"]]["children"].append({"value": line["class_name"], "label": line["class_name"]})
        else:
            model[line["model_name"]] = {"value": line["model_name"], "label": line["model_name"],
                                         "children": [{"value": line["class_name"], "label": line["class_name"]}]
                                         }

    result = []
    for k, v in model.items():
        result.append(v)

    return result


def get_data_element_of_model_class_options_list(model_class):
    """
    通过模型对象类获取数据元列表
    :param model_class:
    :return:
    """
    cypher = "match(a:数据元) -[:数据元概念]-> (b:数据元概念) -[:对象类]-> (c:对象类)" \
             " where c.name = '{0}' " \
             "return a.identifier as identifier, a.name as name, a.describe as describe".format(model_class)
    data = graph.run(cypher).data()
    return data


def get_data_element_info(identifier):
    """
    获取MDR的注册信息
    :param identifier:
    :return:
    """
    cypher = "match(n:数据元) where n.identifier = '{0}' " \
             "return n.identifier as identifier, n.name as name, " \
             "n.personId as personId, n.time as time, n.describe as describe, " \
             "n.department as department, n.version as version, n.status as status, " \
             "n.evolution as evolution".format(identifier)
    data = graph.run(cypher).data()
    return data


def get_sub_domain_info(identifier):
    cypher = "match(a:子域) -[:拥有]-> (b:表) -[:由组成]-> (c:表属性) -[:数据元]-> (d:数据元) " \
             "where d.identifier = '{0}' " \
             "with a,b,c optional " \
             "match(c) -[:约束值]-> (e:表属性值) -[:可允许值]-> (f:可允许值) -[:值含义]-> (g:值含义)  " \
             "return a.describe as sub_domain_describe, " \
             "b.name as table_name, b.identifier as table_identifier, " \
             "c.name as column_name, c.identifier as column_identifier, c.evolution as column_evolution, " \
             "e.name as value_name, e.identifier as value_identifier," \
             "g.name as value_meaning".format(identifier)
    data = graph.run(cypher).data()
    column = {}
    for line in data:
        if line["column_identifier"] in column:
            column[line["column_identifier"]]["value"].append({"value_name": line["value_name"],
                                                               "value_identifier": line["value_identifier"],
                                                               "value_meaning": line["value_meaning"]})
        else:
            if len(line["column_evolution"]) == 0:
                line["column_evolution"] = "暂无演化数据"
                column[line["column_identifier"]] = {"column_name": line["column_name"],
                                                     "column_identifier": line["column_identifier"],
                                                     "table_name": line["table_name"],
                                                     "evolution": line["column_evolution"],
                                                     "sub_domain_describe": line["sub_domain_describe"]
                                                     }
            else:
                evolution = []
                data = line["column_evolution"].split("???")[1:]
                for temps in data:
                    temps = temps.split(";")[:-1]
                    evolution_item = {}
                    for temp in temps:
                        if temp[:4] == "操作时间":
                            key = "操作时间"
                            value = temp[4:]
                            evolution_item[key] = value
                        else:
                            temp = temp.split(":")
                            evolution_item[temp[0]] = temp[1]
                    evolution.append(evolution_item)

                column[line["column_identifier"]] = {"column_name": line["column_name"],
                                                     "column_identifier": line["column_identifier"],
                                                     "table_name": line["table_name"],
                                                     "evolution": evolution,
                                                     "sub_domain_describe": line["sub_domain_describe"]
                                                     }
            if line["value_name"] is not None:
                column[line["column_identifier"]]["value"] = [{"value_name": line["value_name"],
                                                               "value_identifier": line["value_identifier"],
                                                               "value_meaning": line["value_meaning"]}]
            else:
                column[line["column_identifier"]]["value"] = None

    result = []
    for k, v in column.items():
        result.append(v)
    return result


def get_graph_of_data_element_and_attribute(identifier):
    cypher = "match(a1:表属性) -[r:数据元]-> (a2:数据元) " \
             "where a2.identifier = '{0}' " \
             "return a1.name as start_name, id(a1) as start_id, " \
             "type(r) as relationship, " \
             "a2.name as end_name, id(a2) as end_id, " \
             "labels(a1)[0] as start_labels, labels(a2)[0] as end_labels " \
             "union all " \
             "match(a1:表) -[r:由组成]-> (a2:表属性) -[:数据元]-> (a3:数据元) " \
             "where a3.identifier = '{0}' " \
             "return a1.name as start_name, id(a1) as start_id, " \
             "type(r) as relationship, " \
             "a2.name as end_name, id(a2) as end_id, " \
             "labels(a1)[0] as start_labels, labels(a2)[0] as end_labels " \
             "union all" \
             " match(a1:子域) -[r:拥有]-> (a2:表) -[:由组成]-> (a3:表属性) -[:数据元]-> (a4:数据元) " \
             "where a4.identifier = '{0}' " \
             "return a1.describe as start_name, id(a1) as start_id, " \
             "type(r) as relationship, " \
             "a2.name as end_name, id(a2) as end_id, " \
             "labels(a1)[0] as start_labels, labels(a2)[0] as end_labels".format(identifier)
    data = graph.run(cypher).data()

    graph_data = {"data": [], "links": []}
    id_to_id = {}
    count = 0
    for i in data:
        _i = i["start_id"]
        if not (_i in id_to_id):
            id_to_id[_i] = count
            count += 1
            label = LABEL_CHANGE_1[i["start_labels"]]
            node = {"name": i["start_name"], "category": CLASS_LIST_Attribute_AND_Data_Element[label]}
            graph_data["data"].append(node)

        _i = i["end_id"]
        if not (_i in id_to_id):
            id_to_id[_i] = count
            count += 1
            label = LABEL_CHANGE_1[i["end_labels"]]
            node = {"name": i["end_name"], "category": CLASS_LIST_Attribute_AND_Data_Element[label]}
            graph_data["data"].append(node)

    for i in data:
        edge = {"source": id_to_id[i["start_id"]], "target": id_to_id[i["end_id"]],
                "value": LABEL_CHANGE_2[i["relationship"]]}
        graph_data['links'].append(edge)

    nodes = calculate_x_and_y_1(graph_data["data"], graph_data["links"])
    graph_data["data"] = []
    for k, v in nodes.items():
        graph_data["data"].append(v)

    return graph_data


def get_graph_of_permissible_values_and_attribute_value(identifier):
    cypher = "match(a1:表属性) -[:数据元]-> (a2:数据元) " \
             "where a2.identifier = '{0}'  " \
             "with a1, a2 " \
             "match(a1) -[r:约束值]->(a3:表属性值)  " \
             "return a1.name as start_name, id(a1) as start_id, " \
             "type(r) as relationship, " \
             "a3.name as end_name, id(a3) as end_id, " \
             "labels(a1)[0] as start_labels, labels(a3)[0] as end_labels " \
             "union all " \
             "match(a1:表属性) -[:数据元]-> (a2:数据元) " \
             "where a2.identifier = '{0}'  " \
             "with a1, a2 " \
             "match(a1) -[:约束值]->(a3:表属性值) -[:可允许值]-> (a4:可允许值) -[r:值含义]-> (a5:值含义) " \
             "return a3.name as start_name, id(a3) as start_id, " \
             "type(r) as relationship, " \
             "a5.name as end_name, id(a5) as end_id, " \
             "labels(a3)[0] as start_labels, labels(a5)[0] as end_labels".format(identifier)
    data = graph.run(cypher).data()

    graph_data = {"data": [], "links": []}
    id_to_id = {}
    count = 0
    for i in data:
        _i = i["start_id"]
        if not (_i in id_to_id):
            id_to_id[_i] = count
            count += 1
            label = LABEL_CHANGE_3[i["start_labels"]]
            node = {"name": i["start_name"], "category": CLASS_LIST_Attribute_Value_AND_Permissible_Value[label]}
            graph_data["data"].append(node)

        _i = i["end_id"]
        if not (_i in id_to_id):
            id_to_id[_i] = count
            count += 1
            label = LABEL_CHANGE_3[i["end_labels"]]
            node = {"name": i["end_name"], "category": CLASS_LIST_Attribute_Value_AND_Permissible_Value[label]}
            graph_data["data"].append(node)

    for i in data:
        edge = {"source": id_to_id[i["start_id"]], "target": id_to_id[i["end_id"]],
                "value": i["relationship"]}
        graph_data['links'].append(edge)

    nodes = calculate_x_and_y_2(graph_data["data"], graph_data["links"])
    graph_data["data"] = []
    for k, v in nodes.items():
        graph_data["data"].append(v)
    return graph_data


def get_target_node_id(source, label, links):
    targets = []
    for link in links:
        if link["source"] == source:
            if link["value"] == label:
                targets.append(link["target"])
    return targets


def calculate_x_and_y_2(data_nodes, data_links):
    nodes = {}
    count = 0
    for line in data_nodes:
        line["id"] = count
        nodes[count] = line
        count += 1
    columns = []
    permissible_value = []
    value_meanings = []
    for k, v in nodes.items():
        if v["category"] == 0:
            columns.append(v)
            targets = get_target_node_id(k, "约束值", data_links)
            for target in targets:
                permissible_value.append(nodes[target])
        if v["category"] == 2:
            value_meanings.append(v)

    x_offset = 100  # x 的偏移量
    len_category = len(columns)
    x_start = -x_offset * (len_category - 1) / 2  # 计算起始 x 值
    for i, temp in enumerate(columns):
        x = x_start + i * x_offset
        id = temp["id"]
        nodes[id]["x"] = x
        nodes[id]["y"] = 500

    len_category = len(permissible_value)
    x_start = -x_offset * (len_category - 1) / 2  # 计算起始 x 值
    for i, temp in enumerate(permissible_value):
        x = x_start + i * x_offset
        id = temp["id"]
        nodes[id]["x"] = x
        nodes[id]["y"] = 300

    len_category = len(value_meanings)
    x_start = -x_offset * (len_category - 1) / 2  # 计算起始 x 值
    for i, temp in enumerate(value_meanings):
        x = x_start + i * x_offset
        id = temp["id"]
        nodes[id]["x"] = x
        nodes[id]["y"] = 100

    return nodes


def calculate_x_and_y_1(data_nodes, data_links):
    nodes = {}
    count = 0
    for line in data_nodes:
        line["id"] = count
        nodes[count] = line
        count += 1
    data_elements = []
    columns = []
    sub_domains = []
    tables = []
    for k, v in nodes.items():
        if v["category"] == 3:
            sub_domains.append(v)
            target_tables = get_target_node_id(k, "拥有", data_links)
            for target_table in target_tables:
                tables.append(nodes[target_table])
                target_columns = get_target_node_id(target_table, "由组成", data_links)
                for target_column in target_columns:
                    columns.append(nodes[target_column])
        if v["category"] == 0:
            data_elements.append(v)

    x_offset = 200  # x 的偏移量
    len_category = len(sub_domains)
    x_start = -x_offset * (len_category - 1) / 2  # 计算起始 x 值
    for i, temp in enumerate(sub_domains):
        x = x_start + i * x_offset
        id = temp["id"]
        nodes[id]["x"] = x
        nodes[id]["y"] = 500

    len_category = len(tables)
    x_start = -x_offset * (len_category - 1) / 2  # 计算起始 x 值
    for i, temp in enumerate(tables):
        x = x_start + i * x_offset
        id = temp["id"]
        nodes[id]["x"] = x
        nodes[id]["y"] = 350

    len_category = len(columns)
    x_start = -x_offset * (len_category - 1) / 2  # 计算起始 x 值
    for i, temp in enumerate(columns):
        x = x_start + i * x_offset
        id = temp["id"]
        nodes[id]["x"] = x
        nodes[id]["y"] = 200

    len_category = len(data_elements)
    x_start = -x_offset * (len_category - 1) / 2  # 计算起始 x 值
    for i, temp in enumerate(data_elements):
        x = x_start + i * x_offset
        id = temp["id"]
        nodes[id]["x"] = x
        nodes[id]["y"] = 100

    return nodes


def get_data_share_info_json(identifier):
    data = {}
    data_element_info = get_data_element_info(identifier)
    sub_domain_info = get_sub_domain_info(identifier)
    graph1 = get_graph_of_data_element_and_attribute(identifier)
    graph2 = get_graph_of_permissible_values_and_attribute_value(identifier)
    graph3 = get_graph_of_mdr_info(identifier)
    data["data_element_info"] = data_element_info
    data["sub_domain_info"] = sub_domain_info
    data["graph1"] = graph1
    data["graph2"] = graph2
    data["graph3"] = graph3

    return data


def get_data_element_identifier_info_through_object_class_and_property(object_class, property):
    cypher = "match(a:数据元) -[:数据元概念]-> (b:数据元概念) -[:对象类]-> (c:对象类)  " \
             "match(a) -[:数据元概念]-> (b) -[:属性]-> (d:属性) where c.name = '{0}' and d.name = '{1}' " \
             "return a.identifier as identifier".format(object_class, property)
    data = graph.run(cypher).data()
    if data is None:
        return "暂无相关数据"
    identifier = data[0]["identifier"]
    return identifier


def get_tree_of_model(model_name):
    cypher = "match(a:模型) -[r:类]-> (b:模型类) " \
             "where a.name = '{0}' " \
             "return a.name as start_name, id(a) as start_id, " \
             "type(r) as relation, " \
             "b.name as end_name, id(b) as end_id, " \
             "labels(a)[0] as start_label, labels(b)[0] as end_labels " \
             "union all " \
             "match(a:模型) -[:类]-> (b:模型类) -[r:属性]-> (c:模型属性) " \
             "where a.name = '{0}' return " \
             "b.name as start_name, id(b) as start_id, " \
             "type(r) as relation, " \
             "c.name as end_name, id(c) as end_id, " \
             "labels(b)[0] as start_label, labels(c)[0] as end_labels".format(model_name)
    data = graph.run(cypher).data()
    model_id = {}
    _model_id = ""
    model_class_id = {}
    model_class_properties_id = {}
    for line in data:
        if line["relation"] == "类":
            if not (line["start_id"] in model_id):
                model_id[line["start_id"]] = line["start_name"]
                _model_id = line["start_id"]
            if not (line["end_id"] in model_class_id):
                model_class_id[line["end_id"]] = {"name": line["end_name"]}
        if line["relation"] == "属性":
            if not (line["start_id"] in model_class_properties_id):
                model_class_properties_id[line["start_id"]] = {"children": [{"name": line["end_name"]}]}
            else:
                model_class_properties_id[line["start_id"]]["children"].append({"name": line["end_name"]})

    for k, v in model_class_properties_id.items():
        model_class_id[k]["children"] = v["children"]

    tree = {"name": model_id[_model_id], "children": []}
    for k, v in model_class_id.items():
        tree["children"].append(v)

    return tree


def get_tree_of_model_evolution(model_name):
    cypher = "match(n:模型) where n.name = '{0}' return n.evolution as evolution".format(model_name)
    data = graph.run(cypher).data()[0]["evolution"]
    if data is None:
        return []
    else:
        type_one = []
        type_two = []
        data = data.split("???")[1:]
        for temp in data:
            line = temp
            temp = temp.split(";")[:-1]
            temp = temp[0].split(":")
            if temp[1] == "子域引起信息模型新增类":
                type_one.append(line)
            else:
                type_two.append(line)
        tree = {"name": model_name + "的演化信息", "children": []}
        if len(type_one) > 0:
            index = 0
            tree["children"].append({"name": "子域引起信息模型新增类", "children": []})
            for i, temp in enumerate(tree["children"]):
                if temp["name"] == "子域引起信息模型新增类":
                    index = i
            for line in type_one:
                line = line.split(";")[:-1]
                cause = line[1].split(":")
                result = line[2].split(":")
                item = {"name": cause[1], "children": [{"name": result[1]}]}
                tree["children"][index]["children"].append(item)
        if len(type_two) > 0:
            index = 0
            tree["children"].append({"name": "子域引起信息模型新增属性", "children": []})
            for i, temp in enumerate(tree["children"]):
                if temp["name"] == "子域引起信息模型新增属性":
                    index = i
            for line in type_two:
                line = line.split(";")[:-1]
                cause = line[1].split(":")
                result = line[2].split(":")
                item = {"name": cause[1], "children": [{"name": result[1]}]}
                tree["children"][index]["children"].append(item)

        return tree


def get_model_message(model_name):
    cypher = "match(n:模型) where n.name = '{0}' return n.evolution as evolution".format(model_name)
    data = graph.run(cypher).data()[0]["evolution"]
    if data is None:
        return "暂无演化信息"
    else:
        data = data.split("???")[1:]
        evolution = []
        for temps in data:
            temps = temps.split(";")[:-1]
            evolution_item = {}
            for temp in temps:
                if temp[:4] == "操作时间":
                    key = "操作时间"
                    value = temp[4:]
                    evolution_item[key] = value
                else:
                    temp = temp.split(":")
                    evolution_item[temp[0]] = temp[1]
            evolution.append(evolution_item)
        return evolution


def get_model_evolution_info_json(model_name):
    data = {}
    model_tree = get_tree_of_model(model_name)
    model_tree_evolution = get_tree_of_model_evolution(model_name)
    model_message = get_model_message(model_name)
    data["model_tree"] = model_tree
    data["model_tree_evolution"] = model_tree_evolution
    data["model_message"] = model_message
    return data


def get_sub_domain_message(sub_domain_name):
    cypher = "match(a:子域) -[:演化]-> (b:演化) " \
             "where a.name = '{0}' " \
             "return b.name as table_identifier, b.table_name as table_name, " \
             "b.evolution as evolution".format(sub_domain_name)
    data = graph.run(cypher).data()
    if len(data) == 0:
        return data
    else:
        sub_domain_message = []
        for line in data:
            table_name = line["table_name"]
            table_identifier = line["table_identifier"]
            evolution_data = line["evolution"]
            evolution = []
            evolution_data = evolution_data.split("???")
            for temps in evolution_data:
                temps = temps.split(";")[:-1]
                evolution_item = {}
                for temp in temps:
                    if temp[:4] == "操作时间":
                        key = "操作时间"
                        value = temp[5:]
                        evolution_item[key] = value
                    else:
                        temp = temp.split(":")
                        evolution_item[temp[0]] = temp[1]
                evolution.append(evolution_item)
            item = {"table_name": table_name, "table_identifier": table_identifier, "evolution": evolution}
            sub_domain_message.append(item)
    return sub_domain_message


def get_tree_of_sub_domain_evolution(sub_domain_name):
    cypher = "match(a:子域) -[:演化]-> (b:演化) " \
             "where a.name = '{0}' " \
             "return b.name as table_identifier, b.table_name as table_name, " \
             "b.evolution as evolution".format(sub_domain_name)
    data = graph.run(cypher).data()
    if len(data) == 0:
        return data
    else:
        tree = {"name": sub_domain_name, "children": []}
        for line in data:
            table_name = line["table_name"]
            item_table = {"name": table_name, "children": []}
            evolution_data = line["evolution"]
            evolution_data = evolution_data.split("???")
            for temp in evolution_data:
                temp = temp.split(";")[:-1]
                item_evolution = {"name": temp[0].split(":")[1], "children": [{"name": temp[2].split(":")[1]}]}
                item_table["children"].append(item_evolution)
            tree["children"].append(item_table)
    return tree


def get_sub_domain_evolution_info_json(sub_domain_name):
    data = {}
    sub_domain_message = get_sub_domain_message(sub_domain_name)
    sub_domain_tree_evolution = get_tree_of_sub_domain_evolution(sub_domain_name)
    data["sub_domain_message"] = sub_domain_message
    data["sub_domain_tree_evolution"] = sub_domain_tree_evolution
    return data


def get_model_evolution_tables_list():
    cypher = "match(n:模型) return n.name as model_name, n.evolution as evolution"
    data = graph.run(cypher).data()
    model_tables = []
    for line in data:
        if line["evolution"] is None:
            line["evolution"] = "暂无演化数据"
            model_tables.append(line)
        else:
            temp = line["evolution"].split("???")[1:]
            num = len(temp)
            line["evolution"] = "共有" + str(num) + "条演化数据"
            model_tables.append(line)
    return model_tables


def get_sub_domain_evolution_tables_list():
    cypher = "match(n:子域) " \
             "optional match(n:子域) -[:演化]-> (m:演化) " \
             "return n.name as name, n.describe as describe, count(m) as evolution"
    data = graph.run(cypher).data()
    sub_domain_evolution_tables = []
    for line in data:
        if line["evolution"] == 0:
            line["evolution"] = "暂无演化信息"
        else:
            line["evolution"] = "共有" + str(line["evolution"]) + "张表的演化信息"
        sub_domain_evolution_tables.append(line)

    return sub_domain_evolution_tables
