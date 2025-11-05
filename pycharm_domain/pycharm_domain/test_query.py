#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试MDR查询
"""
from py2neo import Graph
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 从环境变量读取 Neo4j 配置并连接数据库
NEO4J_URI = os.getenv("NEO4J_URI", "http://localhost:7474")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "123456")

graph = Graph(NEO4J_URI, user=NEO4J_USER, password=NEO4J_PASSWORD)

# 测试查询对象类
label = "对象类"
cypher = "match(n:%s) return n.name as name, n.identifier as identifier, " \
         "n.personId as personId, n.time as time, " \
         "n.describe as describe, n.department as department, " \
         "n.version as version, n.status as status" % label

print(f"执行查询: {cypher}")
print()

result = graph.run(cypher).data()
print(f"查询结果类型: {type(result)}")
print(f"查询结果长度: {len(result)}")
print(f"查询结果: {result}")
