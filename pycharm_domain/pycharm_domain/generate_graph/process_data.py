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
    with open(file_name) as f:
        data_lines = f.readlines()
        datas = []
        for line in data_lines:
            line = line.strip()
            datas.append(line)

    return datas


def match_node(graph, label, name):
    matcher = NodeMatcher(graph)
    return matcher.match(label, name=name).first()


def match_node_of_permissible_value(graph, label, name, Domain):
    matcher = NodeMatcher(graph)
    return matcher.match(label, name=name, Domain=Domain).first()


def create_node(graph, label, node_props):
    # 先判断该节点是否存在，若不存在则创建新的节点
    value = match_node(graph, label, node_props["name"])
    if value is None:
        node = Node(label, **node_props)
        graph.create(node)
    print("create a node ---")


def create_node_of_permissible_value(graph, label, node_props):
    # 先判断该节点是否存在，若不存在则创建新的节点
    value = match_node_of_permissible_value(graph, label, node_props["name"], node_props["Domain"])
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


def create_relationship_of_permissible_value_1(graph, label1, name1, Domain1,
                                               label2, name2, relation):
    value1 = match_node_of_permissible_value(graph, label1, name1, Domain1)
    value2 = match_node(graph, label2, name2)
    if value1 is None or value2 is None:
        return False
    r = Relationship(value1, relation, value2)
    graph.create(r)
    print("create a relation ---")


def create_relationship_of_permissible_value(graph, label1, name1, Domain1, label2, name2, Domain2, relation):
    value1 = match_node_of_permissible_value(graph, label1, name1, Domain1)
    value2 = match_node_of_permissible_value(graph, label2, name2, Domain2)
    if value1 is None or value2 is None:
        return False
    r = Relationship(value1, relation, value2)
    graph.create(r)
    print("create a relation ---")


def process_context(data, subDomain_mdr_name):
    graph = Graph(NEO4J_URI, user=NEO4J_USER, password=NEO4J_PASSWORD)
    node_props = {}
    edge_flag = 0
    for line in data:
        if line == "Relationships":
            edge_flag = 1
        else:
            if edge_flag == 0:
                line = line.split("===")
                key = line[0].strip()
                value = line[1].strip()
                node_props[key] = value
            else:
                create_node(graph, "Context", node_props)
                line = line.split("===")
                if len(line) == 2:
                    label1 = "MDR_Registry"
                    name1 = subDomain_mdr_name
                    label2 = line[0].strip()
                    name2 = line[1].strip()
                    relation = "has_a_context"
                    create_relationship(graph, label1, name1, label2, name2, relation)
                    label1 = "Context"
                    name1 = line[1].strip()
                    label2 = "Context"
                    name2 = line[1].strip()
                    relation = "Context"
                    create_relationship(graph, label1, name1, label2, name2, relation)
                else:
                    label1 = "Context"
                    name1 = node_props["name"]
                    label2 = "Context"
                    name2 = line[1].strip()
                    relation = line[0].strip()
                    create_relationship(graph, label1, name1, label2, name2, relation)

    print(node_props)


def process_object_class(data):
    graph = Graph(NEO4J_URI, user=NEO4J_USER, password=NEO4J_PASSWORD)
    node_props = {}
    edge_flag = 0
    node_flag = 0
    for line in data:
        if line == "end":
            edge_flag = 0
            node_flag = 0
            node_props = {}
        elif line == "Relationships":
            edge_flag = 1
        else:
            if edge_flag == 0:
                line = line.split("===")
                key = line[0].strip()
                value = line[1].strip()
                node_props[key] = value
            else:
                if node_flag == 0:
                    create_node(graph, "Object_Class", node_props)
                    node_flag = 1
                line = line.split("===")
                if len(line) == 2:
                    label1 = "Object_Class"
                    name1 = node_props["name"]
                    label2 = line[0].strip()
                    name2 = line[1].strip()
                    relation = line[0].strip()
                    create_relationship(graph, label1, name1, label2, name2, relation)
                else:
                    label1 = "Object_Class"
                    name1 = node_props["name"]
                    label2 = line[2].strip()
                    name2 = line[1].strip()
                    relation = line[0].strip()
                    create_relationship(graph, label1, name1, label2, name2, relation)


def process_property(data):
    graph = Graph(NEO4J_URI, user=NEO4J_USER, password=NEO4J_PASSWORD)
    node_props = {}
    edge_flag = 0
    node_flag = 0
    for line in data:
        if line == "end":
            edge_flag = 0
            node_flag = 0
            node_props = {}
        elif line == "Relationships":
            edge_flag = 1
        else:
            if edge_flag == 0:
                line = line.split("===")
                key = line[0].strip()
                value = line[1].strip()
                node_props[key] = value
            else:
                if node_flag == 0:
                    create_node(graph, "Property", node_props)
                    node_flag = 1
                line = line.split("===")
                if len(line) == 2:
                    label1 = "Property"
                    name1 = node_props["name"]
                    label2 = line[0].strip()
                    name2 = line[1].strip()
                    relation = line[0].strip()
                    create_relationship(graph, label1, name1, label2, name2, relation)
                else:
                    label1 = "Property"
                    name1 = node_props["name"]
                    label2 = line[2].strip()
                    name2 = line[1].strip()
                    relation = line[0].strip()
                    create_relationship(graph, label1, name1, label2, name2, relation)


def process_conceptual_domain(data):
    graph = Graph(NEO4J_URI, user=NEO4J_USER, password=NEO4J_PASSWORD)
    node_props = {}
    edge_flag = 0
    node_flag = 0
    for line in data:
        if line == "end":
            edge_flag = 0
            node_flag = 0
            node_props = {}
        elif line == "Relationships":
            edge_flag = 1
        else:
            if edge_flag == 0:
                line = line.split("===")
                key = line[0].strip()
                value = line[1].strip()
                node_props[key] = value
            else:
                if node_flag == 0:
                    create_node(graph, "Conceptual_Domain", node_props)
                    node_flag = 1
                line = line.split("===")
                if len(line) == 2:
                    label1 = "Conceptual_Domain"
                    name1 = node_props["name"]
                    label2 = line[0].strip()
                    name2 = line[1].strip()
                    relation = line[0].strip()
                    create_relationship(graph, label1, name1, label2, name2, relation)
                else:
                    label1 = "Conceptual_Domain"
                    name1 = node_props["name"]
                    label2 = line[2].strip()
                    name2 = line[1].strip()
                    relation = line[0].strip()
                    create_relationship(graph, label1, name1, label2, name2, relation)


def process_data_element_concept(data):
    graph = Graph(NEO4J_URI, user=NEO4J_USER, password=NEO4J_PASSWORD)
    node_props = {}
    edge_flag = 0
    node_flag = 0
    for line in data:
        if line == "end":
            edge_flag = 0
            node_flag = 0
            node_props = {}
        elif line == "Relationships":
            edge_flag = 1
        else:
            if edge_flag == 0:
                line = line.split("===")
                key = line[0].strip()
                value = line[1].strip()
                node_props[key] = value
            else:
                if node_flag == 0:
                    create_node(graph, "Data_Element_Concept", node_props)
                    node_flag = 1
                line = line.split("===")
                if len(line) == 2:
                    label1 = "Data_Element_Concept"
                    name1 = node_props["name"]
                    label2 = line[0].strip()
                    name2 = line[1].strip()
                    relation = line[0].strip()
                    create_relationship(graph, label1, name1, label2, name2, relation)
                else:
                    label1 = "Data_Element_Concept"
                    name1 = node_props["name"]
                    label2 = line[2].strip()
                    name2 = line[1].strip()
                    relation = line[0].strip()
                    create_relationship(graph, label1, name1, label2, name2, relation)


def process_value_meanings(data):
    graph = Graph(NEO4J_URI, user=NEO4J_USER, password=NEO4J_PASSWORD)
    node_props = {}
    edge_flag = 0
    node_flag = 0
    for line in data:
        if line == "end":
            edge_flag = 0
            node_flag = 0
            node_props = {}
        elif line == "Relationships":
            edge_flag = 1
        else:
            if edge_flag == 0:
                line = line.split("===")
                key = line[0].strip()
                value = line[1].strip()
                node_props[key] = value
            else:
                if node_flag == 0:
                    create_node(graph, "Value_Meanings", node_props)
                    node_flag = 1
                line = line.split("===")
                if len(line) == 2:
                    label1 = "Value_Meanings"
                    name1 = node_props["name"]
                    label2 = line[0].strip()
                    name2 = line[1].strip()
                    relation = line[0].strip()
                    create_relationship(graph, label1, name1, label2, name2, relation)
                else:
                    label1 = "Value_Meanings"
                    name1 = node_props["name"]
                    label2 = line[2].strip()
                    name2 = line[1].strip()
                    relation = line[0].strip()
                    create_relationship(graph, label1, name1, label2, name2, relation)


def process_representation_class(data):
    graph = Graph(NEO4J_URI, user=NEO4J_USER, password=NEO4J_PASSWORD)
    node_props = {}
    edge_flag = 0
    node_flag = 0
    for line in data:
        if line == "end":
            edge_flag = 0
            node_flag = 0
            node_props = {}
        elif line == "Relationships":
            edge_flag = 1
        else:
            if edge_flag == 0:
                line = line.split("===")
                key = line[0].strip()
                value = line[1].strip()
                node_props[key] = value
            else:
                if node_flag == 0:
                    create_node(graph, "Representation_Class", node_props)
                    node_flag = 1
                line = line.split("===")
                if len(line) == 2:
                    label1 = "Representation_Class"
                    name1 = node_props["name"]
                    label2 = line[0].strip()
                    name2 = line[1].strip()
                    relation = line[0].strip()
                    create_relationship(graph, label1, name1, label2, name2, relation)
                else:
                    label1 = "Representation_Class"
                    name1 = node_props["name"]
                    label2 = line[2].strip()
                    name2 = line[1].strip()
                    relation = line[0].strip()
                    create_relationship(graph, label1, name1, label2, name2, relation)


def process_value_domain(data):
    graph = Graph(NEO4J_URI, user=NEO4J_USER, password=NEO4J_PASSWORD)
    node_props = {}
    edge_flag = 0
    node_flag = 0
    for line in data:
        if line == "end":
            edge_flag = 0
            node_flag = 0
            node_props = {}
        elif line == "Relationships":
            edge_flag = 1
        else:
            if edge_flag == 0:
                line = line.split("===")
                key = line[0].strip()
                value = line[1].strip()
                node_props[key] = value
            else:
                if node_flag == 0:
                    create_node(graph, "Value_Domain", node_props)
                    node_flag = 1
                line = line.split("===")
                if len(line) == 2:
                    label1 = "Value_Domain"
                    name1 = node_props["name"]
                    label2 = line[0].strip()
                    name2 = line[1].strip()
                    relation = line[0].strip()
                    create_relationship(graph, label1, name1, label2, name2, relation)
                else:
                    label1 = "Value_Domain"
                    name1 = node_props["name"]
                    label2 = line[2].strip()
                    name2 = line[1].strip()
                    relation = line[0].strip()
                    create_relationship(graph, label1, name1, label2, name2, relation)


def process_permissible_values(data):
    graph = Graph(NEO4J_URI, user=NEO4J_USER, password=NEO4J_PASSWORD)
    node_props = {}
    edge_flag = 0
    node_flag = 0
    for line in data:
        if line == "end":
            edge_flag = 0
            node_flag = 0
            node_props = {}
        elif line == "Relationships":
            edge_flag = 1
        else:
            if edge_flag == 0:
                line = line.split("===")
                key = line[0].strip()
                value = line[1].strip()
                node_props[key] = value
            else:
                if node_flag == 0:
                    create_node_of_permissible_value(graph, "Permissible_Values", node_props)
                    node_flag = 1
                line = line.split("===")
                if len(line) == 2:
                    label1 = "Permissible_Values"
                    name1 = node_props["name"]
                    Domain1 = node_props["Domain"]
                    label2 = line[0].strip()
                    name2 = line[1].strip()
                    relation = line[0].strip()
                    create_relationship_of_permissible_value_1(graph, label1, name1, Domain1,
                                                               label2, name2, relation)
                else:
                    label1 = "Permissible_Values"
                    name1 = node_props["name"]
                    Domain1 = node_props["Domain"]
                    label2 = line[2].strip()
                    name2 = line[1].strip()
                    Domain2 = line[0].strip()
                    relation = line[0].strip()
                    create_relationship_of_permissible_value(graph, label1, name1, Domain1,
                                                             label2, name2, Domain2, relation)


def process_data_element(data):
    graph = Graph(NEO4J_URI, user=NEO4J_USER, password=NEO4J_PASSWORD)
    node_props = {}
    edge_flag = 0
    node_flag = 0
    for line in data:
        if line == "end":
            edge_flag = 0
            node_flag = 0
            node_props = {}
        elif line == "Relationships":
            edge_flag = 1
        else:
            if edge_flag == 0:
                line = line.split("===")
                key = line[0].strip()
                value = line[1].strip()
                node_props[key] = value
            else:
                if node_flag == 0:
                    create_node(graph, "Data_Element", node_props)
                    node_flag = 1
                line = line.split("===")
                if len(line) == 2:
                    label1 = "Data_Element"
                    name1 = node_props["name"]
                    label2 = line[0].strip()
                    name2 = line[1].strip()
                    relation = line[0].strip()
                    create_relationship(graph, label1, name1, label2, name2, relation)
                else:
                    label1 = "Data_Element"
                    name1 = node_props["name"]
                    label2 = line[2].strip()
                    name2 = line[1].strip()
                    relation = line[0].strip()
                    create_relationship(graph, label1, name1, label2, name2, relation)


if __name__ == '__main__':
    # file_name = "./data/MDR/Ontology/Context.txt"
    # data = read_file(file_name)
    # subDomain_mdr_name = "MDR registry of ontology"
    # process_context(data, subDomain_mdr_name)
    # file_name = "./data/MDR/E-R/Context.txt"
    # data = read_file(file_name)
    # subDomain_mdr_name = "MDR registry of E-R"
    # process_context(data, subDomain_mdr_name)
    # file_name = "./data/MDR/UML/Context.txt"
    # data = read_file(file_name)
    # subDomain_mdr_name = "MDR registry of uml"
    # process_context(data, subDomain_mdr_name)
    #
    # file_name = "./data/MDR/Ontology/Object_Class .txt"
    # data = read_file(file_name)
    # process_object_class(data)
    # file_name = "./data/MDR/E-R/Object_Class .txt"
    # data = read_file(file_name)
    # process_object_class(data)
    # file_name = "./data/MDR/UML/Object_Class .txt"
    # data = read_file(file_name)
    # process_object_class(data)
    #
    # file_name = "./data/MDR/Ontology/Property.txt"
    # data = read_file(file_name)
    # process_property(data)
    # file_name = "./data/MDR/E-R/Property.txt"
    # data = read_file(file_name)
    # process_property(data)
    # file_name = "./data/MDR/UML/Property.txt"
    # data = read_file(file_name)
    # process_property(data)
    #
    # file_name = "./data/MDR/Ontology/Conceptual_Domain.txt"
    # data = read_file(file_name)
    # process_conceptual_domain(data)
    # file_name = "./data/MDR/E-R/Conceptual_Domain.txt"
    # data = read_file(file_name)
    # process_conceptual_domain(data)
    # file_name = "./data/MDR/UML/Conceptual_Domain.txt"
    # data = read_file(file_name)
    # process_conceptual_domain(data)
    #
    # file_name = "./data/MDR/Ontology/Data_Element_Concept.txt"
    # data = read_file(file_name)
    # process_data_element_concept(data)
    # file_name = "./data/MDR/E-R/Data_Element_Concept.txt"
    # data = read_file(file_name)
    # process_data_element_concept(data)
    # file_name = "./data/MDR/UML/Data_Element_Concept.txt"
    # data = read_file(file_name)
    # process_data_element_concept(data)
    #
    # file_name = "./data/MDR/Ontology/Value_Meanings.txt"
    # data = read_file(file_name)
    # process_value_meanings(data)
    # file_name = "./data/MDR/E-R/Value_Meanings.txt"
    # data = read_file(file_name)
    # process_value_meanings(data)
    # file_name = "./data/MDR/UML/Value_Meanings.txt"
    # data = read_file(file_name)
    # process_value_meanings(data)
    #
    # file_name = "./data/MDR/Ontology/Representation_Class.txt"
    # data = read_file(file_name)
    # process_representation_class(data)
    # file_name = "./data/MDR/E-R/Representation_Class.txt"
    # data = read_file(file_name)
    # process_representation_class(data)
    # file_name = "./data/MDR/UML/Representation_Class.txt"
    # data = read_file(file_name)
    # process_representation_class(data)
    #
    # file_name = "./data/MDR/Ontology/Value_Domain.txt"
    # data = read_file(file_name)
    # process_value_domain(data)
    # file_name = "./data/MDR/E-R/Value_Domain.txt"
    # data = read_file(file_name)
    # process_value_domain(data)
    # file_name = "./data/MDR/UML/Value_Domain.txt"
    # data = read_file(file_name)
    # process_value_domain(data)

    # file_name = "./data/MDR/Ontology/Permissible_Values.txt"
    # data = read_file(file_name)
    # process_permissible_values(data)
    # file_name = "./data/MDR/E-R/Permissible_Values.txt"
    # data = read_file(file_name)
    # process_permissible_values(data)
    # file_name = "./data/MDR/UML/Permissible_Values.txt"
    # data = read_file(file_name)
    # process_permissible_values(data)
    #
    # file_name = "./data/MDR/Ontology/Data_Element.txt"
    # data = read_file(file_name)
    # process_data_element(data)
    # file_name = "./data/MDR/E-R/Data_Element.txt"
    # data = read_file(file_name)
    # process_data_element(data)
    # file_name = "./data/MDR/UML/Data_Element.txt"
    # data = read_file(file_name)
    # process_data_element(data)
    pass
