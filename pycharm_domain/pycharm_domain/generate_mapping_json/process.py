from py2neo import Node, Relationship, Graph
import json

graph = Graph(
    "http://localhost:7474",
    user="neo4j",
    password="123456"
)


def save_to_json_file(data):
    file_path = './data/data.json'
    # 使用json.dump()将字典保存为带缩进的JSON文件
    with open(file_path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)


def get_attribute_mapping_list():
    cypher = "match(a:表属性) -[:数据元]-> (b:数据元) " \
             "return a.identifier as attribute_identifier, b.identifier as data_element_identifier"
    data = graph.run(cypher).data()
    return data


def get_attribute_value_mapping_list():
    cypher = "match(a:表属性值) -[:可允许值]-> (b:可允许值) " \
             "return a.identifier as attribute_value_identifier, b.identifier as permissible_value_identifier"
    data = graph.run(cypher).data()
    return data


if __name__ == '__main__':
    count = 1
    mapping = []
    data_element = {}
    permissible_values = {}
    attribute_mappings = get_attribute_mapping_list()
    for line in attribute_mappings:
        if line["data_element_identifier"] in data_element:
            data_element[line["data_element_identifier"]].append(line["attribute_identifier"])
        else:
            data_element[line["data_element_identifier"]] = [line["attribute_identifier"]]

    for k, v in data_element.items():
        identifier = f"MP{str(count).zfill(3)}"
        source = {"标识符": identifier, "映射集": v}
        count += 1

        identifier = f"MP{str(count).zfill(3)}"
        target = {"标识符": identifier, "映射集": k}
        count += 1

        identifier = f"MP{str(count).zfill(3)}"
        describe = {"标识符": identifier, "标记": "属性名与数据元映射"}
        count += 1

        identifier = f"MP{str(count).zfill(3)}"
        source["映射来源"] = identifier
        target["映射目标"] = identifier
        describe["描述"] = identifier
        mapping_item = {"标识符": identifier, "源集": source, "目标集": target, "被描述": describe}
        mapping.append(mapping_item)
        count += 1

    attribute_value_mappings = get_attribute_value_mapping_list()
    for line in attribute_value_mappings:
        if line["permissible_value_identifier"] in permissible_values:
            permissible_values[line["permissible_value_identifier"]].append(line["attribute_value_identifier"])
        else:
            permissible_values[line["permissible_value_identifier"]] = [line["attribute_value_identifier"]]

    for k, v in permissible_values.items():
        identifier = f"MP{str(count).zfill(3)}"
        source = {"标识符": identifier, "映射集": v}
        count += 1

        identifier = f"MP{str(count).zfill(3)}"
        target = {"标识符": identifier, "映射集": k}
        count += 1

        identifier = f"MP{str(count).zfill(3)}"
        describe = {"标识符": identifier, "标记": "属性值与值域映射"}
        count += 1

        identifier = f"MP{str(count).zfill(3)}"
        source["映射来源"] = identifier
        target["映射目标"] = identifier
        describe["描述"] = identifier
        mapping_item = {"标识符": identifier, "源集": source, "目标集": target, "被描述": describe}
        mapping.append(mapping_item)
        count += 1

    save_to_json_file(mapping)
