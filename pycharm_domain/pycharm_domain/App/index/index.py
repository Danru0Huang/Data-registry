from ..config import graph


def get_model_index_info():
    num_all = 0
    cypher = "match(a:模型) return a.name as model_name, count(a) as model_num"
    data = graph.run(cypher).data()[0]
    model_data = {"信息模型": {"$count": data["model_num"]}}
    models = [data["model_name"]]
    num_all += len(models)
    for model in models:
        num_model = 0
        model_item = {model: {"$count": len(models), model: {"$count": 350}}}
        cypher = "match(a:模型) -[:类]-> (b:模型类) where a.name = '{0}' return b.name as class_name".format(model)
        class_list = graph.run(cypher).data()
        num_model += len(class_list)
        for class_name in class_list:
            class_name = class_name["class_name"]
            cypher = "match(a:模型类) -[:属性]-> (b:模型属性) where a.name = '{0}' " \
                     "return b.name as property_name".format(class_name)
            property_list = graph.run(cypher).data()
            num_model += len(property_list)
            temp_class_name = class_name + "_类"
            class_item = {class_name: {"$count": len(property_list), temp_class_name: {"$count": 100}}}
            for property in property_list:
                property = property["property_name"]
                class_item[class_name].update({property: {"$count": 1}})
            model_item[model].update(class_item)
            num_all += num_model
            model_item[model]["$count"] = num_model
        model_data["信息模型"].update(model_item)
        model_data["信息模型"]["$count"] = num_all

    return model_data


def get_mdr_index_info():
    num = 0
    mdr_data = {"MDR": {}}
    mdr_data["MDR"].update({"$count": 6})
    cypher = "match(a:对象类) return a.name"
    data = graph.run(cypher).data()
    object_class_item = {"对象类": {"$count": len(data), "对象类": {"$count": 50}}}
    num += len(data)
    for line in data:
        object_class_name = line["a.name"]
        object_class_item["对象类"].update({object_class_name: {"$count": 5}})
    mdr_data["MDR"].update(object_class_item)

    cypher = "match(a:属性) return a.name"
    data = graph.run(cypher).data()
    property_item = {"属性": {"$count": len(data), "属性  ": {"$count": 200}}}
    num += len(data)
    for line in data:
        property_name = line["a.name"]
        property_item["属性"].update({property_name: {"$count": 5}})
    mdr_data["MDR"].update(property_item)

    cypher = "match(a:数据元概念) return a.name"
    data = graph.run(cypher).data()
    data_element_concept_item = {"数据元概念": {"$count": len(data), "数据元概念": {"$count": 300}}}
    num += len(data)
    for line in data:
        data_element_concept_name = line["a.name"]
        data_element_concept_item["数据元概念"].update({data_element_concept_name: {"$count": 5}})
    mdr_data["MDR"].update(data_element_concept_item)

    cypher = "match(a:概念域) return a.name"
    data = graph.run(cypher).data()
    conceptual_domain_item = {"概念域": {"$count": len(data), "概念域": {"$count": 300}}}
    num += len(data)
    for line in data:
        conceptual_domain_name = line["a.name"]
        conceptual_domain_item["概念域"].update({conceptual_domain_name: {"$count": 4}})
    mdr_data["MDR"].update(conceptual_domain_item)

    cypher = "match(a:值域) return a.name"
    data = graph.run(cypher).data()
    value_domain_item = {"值域": {"$count": len(data), "值域": {"$count": 300}}}
    num += len(data)
    for line in data:
        value_domain_name = line["a.name"]
        value_domain_item["值域"].update({value_domain_name: {"$count": 5}})
    mdr_data["MDR"].update(value_domain_item)

    cypher = "match(a:数据元) return a.name"
    data = graph.run(cypher).data()
    data_element_item = {"数据元": {"$count": len(data), "数据元": {"$count": 500}}}
    num += len(data)
    for line in data:
        data_element_name = line["a.name"]
        data_element_item["数据元"].update({data_element_name: {"$count": 10}})
    mdr_data["MDR"].update(data_element_item)
    mdr_data["MDR"]["$count"] = num

    return mdr_data


def get_graph_index_info():
    data = {}
    model_data = get_model_index_info()
    data.update(model_data)
    mdr_data = get_mdr_index_info()
    data.update(mdr_data)
    return data


def get_index_sub_domain_info():
    data = []
    cypher = "match(a:子域) return a.name as sub_domain_name, a.describe as sub_domain_describe"
    sub_domains = graph.run(cypher).data()
    for sub_domain in sub_domains:
        sub_domain_name = sub_domain["sub_domain_name"]
        sub_domain_item = {sub_domain_name:
                               {"title": sub_domain_name, "describe": sub_domain["sub_domain_describe"]}}
        cypher = "match(a:子域) -[:拥有]-> (b:表) where a.name = '{0}' " \
                 "return count(b) as num_table".format(sub_domain_name)
        num_table = graph.run(cypher).data()[0]["num_table"]
        sub_domain_item[sub_domain_name].update({"num_table": num_table})
        cypher = "match(a:子域) -[:拥有]-> (b:表) -[:由组成]-> (c:表属性) where a.name = '{0}' " \
                 "return count(c) as num_attribute".format(sub_domain_name)
        num_attribute = graph.run(cypher).data()[0]["num_attribute"]
        sub_domain_item[sub_domain_name].update({"num_attribute": num_attribute})
        cypher = "match(a:子域) -[:拥有]-> (b:表) -[:由组成]-> (c:表属性) -[:约束值]-> (d:表属性值) " \
                 "where a.name = '{0}' " \
                 "return count(d) as num_attribute_value".format(sub_domain_name)
        num_attribute_value = graph.run(cypher).data()[0]["num_attribute_value"]
        sub_domain_item[sub_domain_name].update({"num_attribute_value": num_attribute_value})
        cypher = "match(a:子域) -[:演化]-> (b:演化) where a.name = '{0}' " \
                 "return b.evolution as evolution".format(sub_domain_name)
        evolutions = graph.run(cypher).data()
        num_evolution = 0
        if evolutions is not None:
            for evolution in evolutions:
                evolution = evolution["evolution"]
                evolution = evolution.strip().split("???")
                print(evolution)
                num_evolution = num_evolution + len(evolution)
        sub_domain_item[sub_domain_name].update({"num_evolution": num_evolution})
        data.append(sub_domain_item[sub_domain_name])

    return data


