"""
数据库初始化脚本
用于创建系统运行所需的基础节点
"""
from App.config import graph
from py2neo import Node

def init_id_counters():
    """
    初始化ID计数器节点
    这些节点用于跟踪各类实体的ID序号
    """
    print("开始初始化数据库...")

    # 定义所有需要的ID计数器及其初始值
    id_counters = {
        # 子域相关
        "表ID": 1,
        "表属性ID": 1,
        "表属性值ID": 1,

        # MDR相关
        "对象类ID": 1,
        "属性ID": 1,
        "概念域ID": 1,
        "数据元概念ID": 1,
        "值域ID": 1,
        "数据元ID": 1,
        "可允许值ID": 1,
        "值含义ID": 1,
        "值域组ID": 1,

        # 信息模型相关
        "模型ID": 1,
        "模型类ID": 1,
        "模型属性ID": 1,
    }

    # 检查并创建ID计数器节点
    for label, initial_value in id_counters.items():
        # 检查节点是否已存在
        query = f"MATCH (n:{label}) RETURN n"
        result = graph.run(query).data()

        if not result:
            # 创建新节点
            node = Node(label, name=initial_value)
            graph.create(node)
            print(f"✓ 创建 {label} 节点，初始值: {initial_value}")
        else:
            print(f"○ {label} 节点已存在")

    print("\n数据库初始化完成！")
    print("=" * 50)


def check_database_status():
    """检查数据库连接状态"""
    try:
        graph.run("RETURN 1").data()
        print("✓ Neo4j 数据库连接成功")
        # 从配置中读取连接信息
        from App.config import NEO4J_URI, NEO4J_USER
        print(f"  URI: {NEO4J_URI}")
        print(f"  用户: {NEO4J_USER}")
        return True
    except Exception as e:
        print(f"✗ Neo4j 数据库连接失败: {str(e)}")
        return False


if __name__ == "__main__":
    print("=" * 50)
    print("数据库初始化脚本")
    print("=" * 50)

    # 检查数据库连接
    if check_database_status():
        print()
        # 初始化ID计数器
        init_id_counters()

        print("\n提示：")
        print("- 如果需要重置数据库，请在Neo4j Browser中运行: MATCH (n) DETACH DELETE n")
        print("- 然后重新运行此脚本")
    else:
        print("\n请检查：")
        print("1. Neo4j 是否已启动")
        print("2. .env 文件中的配置是否正确")
        print("3. 用户名和密码是否正确")
