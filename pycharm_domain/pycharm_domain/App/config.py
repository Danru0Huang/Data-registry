from py2neo import Graph
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 从环境变量读取 Neo4j 配置
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "123456")

graph = Graph(
    NEO4J_URI,
    user=NEO4J_USER,
    password=NEO4J_PASSWORD
)

# CLASS_LIST = {"Chromosome": 0,
#               "FPKM": 1,
#               "Function": 2,
#               "Gene": 3,
#               "Mutant": 4,
#               "OGI": 5,
#               "Position": 6,
#               "Protein": 7,
#               "Strand": 8,
#               "mRNA": 9
#               }

CLASS_LIST_Model = {
    "模型": 0,
    "模型类": 1,
    "模型属性": 2,
}

CLASS_LIST_SubDomain = {
    "子域": 0,
    "表": 1,
    "表属性": 2,
    "表属性值": 3,
    "数据元": 4,
    "值域": 5,
    "值域组": 6,
    "可允许值": 7
}

CLASS_LIST_Attribute = {
    "表属性": 0,
    "表属性值": 1,
    "数据元": 2,
    "值域": 3,
    "值域组": 4,
    "可允许值": 5,
    "值含义": 6
}

CLASS_LIST_MDR = {
    "对象类": 0,
    "属性": 1,
    "概念域": 2,
    "数据元概念": 3,
    "值域": 4,
    "数据元": 5,
    "可允许值": 6,
    "值含义": 7,
    "值域组": 8,
    "子域": 9,
    "表": 10,
    "表属性": 11,
    "表属性值": 12,
}

LABEL_CHANGE_1 = {
    "数据元": "概念",
    "表属性": "列",
    "表": "表",
    "子域": "子域"
}

CLASS_LIST_Attribute_AND_Data_Element = {
    "概念": 0,
    "列": 1,
    "表": 2,
    "子域": 3
}

LABEL_CHANGE_2 = {
    "数据元": "含义",
    "由组成": "由组成",
    "拥有": "拥有"
}

LABEL_CHANGE_3 = {
    "表属性": "列",
    "表属性值": "可枚举取值",
    "值含义": "值含义"
}

CLASS_LIST_Attribute_Value_AND_Permissible_Value = {
    "列": 0,
    "可枚举取值": 1,
    "值含义": 2
}
