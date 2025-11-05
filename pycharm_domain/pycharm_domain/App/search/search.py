from ..config import graph, CLASS_LIST_Model
from py2neo import NodeMatcher


def match_node(label, names):
    matcher = NodeMatcher(graph)
    return matcher.match(label, name=names).first()


def query(name, label):
    cypher = "MATCH (p:%s)-[r]->(n) " \
             "WHERE p.name = '%s' " \
             "RETURN p.name AS start_name, " \
             "type(r) AS relationship, " \
             "n.name AS end_name, " \
             "labels(p)[0] AS start_labels, " \
             "labels(n)[0] AS end_labels " \
             "UNION ALL " \
             "MATCH (p:%s)-[r1]->(n)-[r2]->(m) " \
             "WHERE p.name = '%s' " \
             "RETURN n.name AS start_name, " \
             "type(r2) AS relationship, " \
             "m.name AS end_name, " \
             "labels(n)[0] AS start_labels, " \
             "labels(m)[0] AS end_labels " % (label, name, label, name)

    # cypher = "MATCH (p:Gene)-[r]->(n) " \
    #          "WHERE p.name = '%s' " \
    #          "RETURN p.name AS start_name, " \
    #          "type(r) AS relationship, " \
    #          "n.name AS end_name, " \
    #          "labels(p)[0] AS start_labels, " \
    #          "labels(n)[0] AS end_labels, " \
    #          "id(p) AS start_id, id(n) as end_id" % (name)
    data = graph.run(cypher)
    data = list(data)
    return get_json_data(data)

def search_domain_form_data(name, param):
    """
    根据子域名称和表的标识符，查询子域和表格之间各种节点的关系
    :param name: 子域名称
    :param param: 表的标识符
    """
    query = """
    MATCH (sub_domain:子域 {name: $sub_domain_name})-[:拥有]->(table:表 {identifier: $table_identifier})
    OPTIONAL MATCH (table)-[:由组成]->(attribute:表属性)
    OPTIONAL MATCH (attribute)-[:约束值]->(value:表属性值)
    WITH table, 
         collect(DISTINCT attribute) AS attributes, 
         collect(DISTINCT value) AS values
    WITH collect(DISTINCT {table_name: table.name, table_identifier: table.identifier, attributes: attributes, values: values}) AS tables
    RETURN $sub_domain_name AS sub_domain_name, tables
    """
    data = graph.run(query, sub_domain_name=name, table_identifier=param).data()
    return get_json_data(data)


def get_json_data(data):
    json_data = {'data': [], "links": [], "tableData": []}
    id_to_id = {}
    name_to_id = {}
    count = 0
    for i in data:
        _name = i["start_name"]
        if not (_name in name_to_id):
            name_to_id[_name] = count
            count += 1
            node = {"name": i["start_name"], "category": CLASS_LIST[i["start_labels"]]}
            json_data["data"].append(node)

        _name = i["end_name"]
        if not (_name in name_to_id):
            name_to_id[_name] = count
            count += 1
            node = {"name": i["end_name"], "category": CLASS_LIST[i["end_labels"]]}
            json_data["data"].append(node)

    for i in data:
        edge = {"source": name_to_id[i["start_name"]], "target": name_to_id[i["end_name"]], "value": i["relationship"]}
        json_data['links'].append(edge)

    for i in data:
        table_item = {"start": i["start_name"], "relation": i["relationship"], "end": i["end_name"]}
        json_data["tableData"].append(table_item)
    # print(json_data)
    return json_data


def get_node_message(category, name):
    nodeDetails = {"category": category}
    node_props = {}
    # cypher = "MATCH (p:%s) WHERE p.name = '%s' RETURN p" % (category, name)
    # data = graph.run(cypher)
    data = match_node(category, name)
    for key, value in data.items():
        if key == "name":
            node_props["identifier"] = value
        else:
            node_props[key] = value
    nodeDetails["properties"] = node_props
    return nodeDetails

