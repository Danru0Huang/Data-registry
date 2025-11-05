"""
清空Neo4j数据库脚本
安全地删除所有MDR和子域数据，并重置ID计数器
"""
import os
import sys
from py2neo import Graph
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 连接Neo4j
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "123456")

graph = Graph(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

def confirm_reset():
    """确认是否清空数据库"""
    print("=" * 60)
    print("⚠️  警告：此操作将清空所有数据库内容！")
    print("=" * 60)

    # 统计当前数据
    stats = get_database_stats()
    print("\n当前数据库统计：")
    for label, count in stats.items():
        if count > 0:
            print(f"  - {label}: {count} 个节点")

    print("\n" + "=" * 60)
    response = input("确认清空数据库？(输入 'YES' 确认): ")
    return response == "YES"

def get_database_stats():
    """获取数据库统计信息"""
    labels = [
        "对象类", "属性", "概念域", "数据元概念",
        "值域", "数据元", "值含义", "可允许值", "值域组",
        "子域", "表", "表属性", "表属性值",
        "模型", "模型类", "模型属性"
    ]

    stats = {}
    for label in labels:
        query = f"MATCH (n:{label}) RETURN count(n) as count"
        result = graph.run(query).data()
        stats[label] = result[0]['count'] if result else 0

    return stats

def delete_all_data():
    """删除所有数据节点和关系"""
    print("\n🗑️  正在删除所有数据...")

    # 删除所有关系
    print("  - 删除关系...")
    graph.run("MATCH ()-[r]->() DELETE r")

    # 删除所有数据节点（但保留ID计数器节点）
    labels_to_delete = [
        "对象类", "属性", "概念域", "数据元概念",
        "值域", "数据元", "值含义", "可允许值", "值域组",
        "子域", "表", "表属性", "表属性值",
        "模型", "模型类", "模型属性"
    ]

    for label in labels_to_delete:
        print(f"  - 删除 {label} 节点...")
        graph.run(f"MATCH (n:{label}) DELETE n")

    print("✓ 数据删除完成")

def reset_id_counters():
    """重置所有ID计数器"""
    print("\n🔄 正在重置ID计数器...")

    id_labels = [
        "对象类ID", "属性ID", "概念域ID", "数据元概念ID",
        "值域ID", "数据元ID", "值含义ID", "可允许值ID",
        "子域ID", "表ID", "表属性ID", "表属性值ID",
        "模型ID", "模型类ID", "模型属性ID"
    ]

    for id_label in id_labels:
        # 删除旧的ID计数器
        graph.run(f"MATCH (n:{id_label}) DELETE n")
        # 创建新的ID计数器（初始值为1）
        graph.run(f"CREATE (n:{id_label} {{name: 1}})")
        print(f"  - {id_label} 重置为 1")

    print("✓ ID计数器重置完成")

def verify_cleanup():
    """验证清理结果"""
    print("\n✅ 验证清理结果...")

    stats = get_database_stats()
    total = sum(stats.values())

    if total == 0:
        print("✓ 数据库已成功清空")

        # 检查ID计数器
        id_count = graph.run("MATCH (n) WHERE labels(n)[0] ENDS WITH 'ID' RETURN count(n) as count").data()[0]['count']
        print(f"✓ ID计数器节点数: {id_count}")

        return True
    else:
        print(f"⚠️  警告：仍有 {total} 个数据节点")
        return False

def main():
    """主函数"""
    print("\n" + "=" * 60)
    print("Neo4j 数据库清空工具")
    print("=" * 60)

    try:
        # 确认操作
        if not confirm_reset():
            print("\n❌ 操作已取消")
            return

        # 删除所有数据
        delete_all_data()

        # 重置ID计数器
        reset_id_counters()

        # 验证结果
        if verify_cleanup():
            print("\n" + "=" * 60)
            print("✅ 数据库清空成功！")
            print("=" * 60)
            print("\n现在可以重新开始注册数据了。")
        else:
            print("\n⚠️  清空过程可能存在问题，请手动检查")

    except Exception as e:
        print(f"\n❌ 错误：{str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
