from py2neo import Graph, Node, Relationship, NodeMatcher
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 从环境变量读取 Neo4j 配置
NEO4J_URI = os.getenv("NEO4J_URI", "http://localhost:7474")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "123456")


def read_file(file_name):
    with open(file_name, encoding='utf-8') as f:
        data_lines = f.readlines()
        datas = []
        for line in data_lines:
            line = line.strip()
            datas.append(line)

    return datas


def match_node(graph, label, name):
    matcher = NodeMatcher(graph)
    return matcher.match(label, name=name).first()


def create_node(graph, label, node_props):
    # 先判断该节点是否存在，若不存在则创建新的节点
    value = match_node(graph, label, node_props["name"])
    if value is None:
        node = Node(label, **node_props)
        graph.create(node)
    print("create a node ---")


def create_relationship(graph, label1, name1, label2, name2, relation):
    value1 = match_node(graph, label1, name1)
    value2 = match_node(graph, label2, name2)
    if value1 is None or value2 is None:
        return False
    r = Relationship(value1, relation, value2)
    graph.create(r)
    print("create a relation ---")


def process_node(data):
    graph = Graph(NEO4J_URI, user=NEO4J_USER, password=NEO4J_PASSWORD)
    node_props = {}
    label = ""
    for line in data:
        if line == "end":
            create_node(graph, label, node_props)
            node_props = {}
            label = ""
        else:
            line = line.split("===")
            key = line[0].strip()
            value = line[1].strip()
            if key == "type":
                label = value
            else:
                node_props[key] = value


def process_edge(data):
    graph = Graph(NEO4J_URI, user=NEO4J_USER, password=NEO4J_PASSWORD)
    for line in data:
        line = line.split("==")
        label1 = line[1].strip()
        name1 = line[0].strip()
        relation = line[2].strip()
        label2 = line[4].strip()
        name2 = line[3].strip()
        create_relationship(graph, label1, name1, label2, name2, relation)


if __name__ == '__main__':
    file_name = "./data/MFI/E-R_node.txt"
    data = read_file(file_name)
    process_node(data)

    file_name = "./data/MFI/mapping_node.txt"
    data = read_file(file_name)
    process_node(data)

    file_name = "./data/MFI/ontology_node.txt"
    data = read_file(file_name)
    process_node(data)

    file_name = "./data/MFI/UML_node.txt"
    data = read_file(file_name)
    process_node(data)

    file_name = "./data/MFI/relation.txt"
    data = read_file(file_name)
    process_edge(data)

