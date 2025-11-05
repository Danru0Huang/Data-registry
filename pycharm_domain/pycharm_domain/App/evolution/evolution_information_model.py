from ..config import graph


def delete_property_of_name_info(model_name, class_name, property_name):
    """
    删除模型属性
    :param model_name: 模型名称
    :param class_name: 模型类名称
    :param property_name: 属性名称
    :return:
    """
    cypher = "match(a:模型) -[:类]-> (b:模型类) -[:属性]-> (c:模型属性) " \
             "where a.name='{0}' and b.name='{1}' and c.name='{2}' " \
             "detach delete c".format(model_name, class_name, property_name)
    graph.run(cypher)
    return "属性删除成功"
