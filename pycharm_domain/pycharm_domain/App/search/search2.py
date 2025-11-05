from ..config import graph, CLASS_LIST
from py2neo import NodeMatcher


def match_node_of_name(label, names):
    matcher = NodeMatcher(graph)
    return matcher.match(label, name=names).first()


def get_node_message(category, name):
    nodeDetails = {"category": category}
    node_props = {}
    # cypher = "MATCH (p:%s) WHERE p.name = '%s' RETURN p" % (category, name)
    # data = graph.run(cypher)
    data = match_node_of_name(category, name)
    for key, value in data.items():
        if key == "name":
            node_props["identifier"] = value
        else:
            node_props[key] = value
    nodeDetails["properties"] = node_props
    return nodeDetails
