from ..config import graph, CLASS_LIST_Model
from py2neo import NodeMatcher


def get_mdr_object_class_node_info(id):
    cypher = "match(n:ObjectClass) where n.identifier='%s' " \
             "return n.name as name, n.identifier as identifier, " \
             "n.personId as personId, n.time as time, " \
             "n.describe as describe, n.department as department, " \
             "n.version as version, n.status as status" % id
    result = graph.run(cypher).data()
    return result



