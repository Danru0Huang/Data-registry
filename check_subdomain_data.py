"""
检查子域数据库中的表和数据
"""
from py2neo import Graph
from config import Config
import sys
import io

# 设置UTF-8编码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 连接数据库
config = Config.get_neo4j_config()
graph = Graph(config['uri'], auth=(config['user'], config['password']))

def check_subdomain_tables(subdomain_name):
    """检查指定子域的表结构和数据"""
    print("=" * 80)
    print(f"检查子域 '{subdomain_name}' 的数据")
    print("=" * 80)

    # 查询子域的表
    query = """
    MATCH (d:子域 {name: $subdomain_name})-[:拥有]->(t:表)
    RETURN t.name as table_name, t.identifier as table_id
    """
    tables = graph.run(query, subdomain_name=subdomain_name).data()

    if not tables:
        print(f"❌ 找不到子域 '{subdomain_name}' 的表")
        return

    print(f"\n找到 {len(tables)} 个表：\n")

    for table in tables:
        table_name = table['table_name']
        table_id = table['table_id']

        print(f"表: {table_name} (ID: {table_id})")

        # 查询表的属性
        attr_query = """
        MATCH (t:表 {identifier: $table_id})-[:由组成]->(a:表属性)
        RETURN a.name as attr_name, a.identifier as attr_id
        ORDER BY a.identifier
        """
        attributes = graph.run(attr_query, table_id=table_id).data()

        for attr in attributes:
            attr_name = attr['attr_name']
            attr_id = attr['attr_id']

            # 查询该属性的值（最多显示10个）
            value_query = """
            MATCH (a:表属性 {identifier: $attr_id})-[:约束值]->(v:表属性值)
            RETURN DISTINCT v.name as value_name
            LIMIT 10
            """
            values = graph.run(value_query, attr_id=attr_id).data()

            value_list = [v['value_name'] for v in values]
            value_count = len(value_list)

            print(f"  └─ 表属性: {attr_name} (ID: {attr_id})")
            print(f"      └─ 数据值 ({value_count}个): {', '.join(map(str, value_list))}")

        print()


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        subdomain_name = sys.argv[1]
    else:
        subdomain_name = "测试子域1"

    check_subdomain_tables(subdomain_name)
