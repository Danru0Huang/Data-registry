"""
测试智能体注册时describe字段是否正确生成
"""
import os
import sys
from dotenv import load_dotenv
from neo4j import GraphDatabase

# 添加项目路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pe_agents.tools_backend_compatible import (
    register_object_class,
    register_property,
    register_concept_domain,
    register_data_element_concept_with_relationships,
    register_value_domain_with_values,
    register_value_domain_with_relationship,
    register_data_element_with_relationships
)

# 加载环境变量
load_dotenv()

# 配置 Neo4j 驱动
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687/")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "123456")

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))


def verify_node_fields(label_cn, name):
    """
    验证节点的所有字段是否正确
    """
    with driver.session() as session:
        query = f"""
        MATCH (n:{label_cn} {{name: $name}})
        RETURN n.name AS name,
               n.describe AS describe,
               n.personId AS personId,
               n.department AS department,
               n.time AS time,
               n.identifier AS identifier,
               n.status AS status,
               n.version AS version
        """
        result = session.run(query, name=name).single()

        if result:
            print(f"\n✓ 找到节点: {label_cn} '{name}'")
            print(f"  - identifier: {result['identifier']}")
            print(f"  - describe: {result['describe']}")
            print(f"  - personId: {result['personId']}")
            print(f"  - department: {result['department']}")
            print(f"  - time: {result['time']}")
            print(f"  - status: {result['status']}")
            print(f"  - version: {result['version']}")

            # 检查必填字段
            missing_fields = []
            if not result['describe']:
                missing_fields.append('describe')
            if not result['personId']:
                missing_fields.append('personId')
            if not result['department']:
                missing_fields.append('department')
            if not result['time']:
                missing_fields.append('time')
            if not result['identifier']:
                missing_fields.append('identifier')
            if not result['status']:
                missing_fields.append('status')
            if not result['version']:
                missing_fields.append('version')

            if missing_fields:
                print(f"  ✗ 缺失或为空的字段: {', '.join(missing_fields)}")
                return False
            else:
                print(f"  ✓ 所有8个必填字段均已正确填写")
                return True
        else:
            print(f"\n✗ 未找到节点: {label_cn} '{name}'")
            return False


def test_basic_registration():
    """
    测试基本的注册功能，验证describe字段
    """
    print("=" * 80)
    print("开始测试智能体注册功能（带describe字段）")
    print("=" * 80)

    # 测试数据
    test_object_class = "测试对象类_智能体"
    test_property = "测试属性_智能体"
    test_concept_domain = "测试概念域_智能体"
    test_data_element_concept = "测试对象类_智能体测试属性_智能体"
    test_value_domain = "测试值域_智能体"
    test_data_element = "DE测试对象类_智能体测试属性_智能体"

    success_count = 0
    total_count = 0

    # 1. 测试对象类注册
    print("\n[1/6] 测试对象类注册...")
    try:
        result = register_object_class.invoke({"object_class": test_object_class})
        print(f"注册结果: {result}")
        total_count += 1
        if verify_node_fields("对象类", test_object_class):
            success_count += 1
    except Exception as e:
        print(f"✗ 注册失败: {e}")
        total_count += 1

    # 2. 测试属性注册
    print("\n[2/6] 测试属性注册...")
    try:
        result = register_property.invoke({"property": test_property})
        print(f"注册结果: {result}")
        total_count += 1
        if verify_node_fields("属性", test_property):
            success_count += 1
    except Exception as e:
        print(f"✗ 注册失败: {e}")
        total_count += 1

    # 3. 测试概念域注册
    print("\n[3/6] 测试概念域注册...")
    try:
        result = register_concept_domain.invoke({"concept_domain": test_concept_domain})
        print(f"注册结果: {result}")
        total_count += 1
        if verify_node_fields("概念域", test_concept_domain):
            success_count += 1
    except Exception as e:
        print(f"✗ 注册失败: {e}")
        total_count += 1

    # 4. 测试数据元概念注册
    print("\n[4/6] 测试数据元概念注册...")
    try:
        result = register_data_element_concept_with_relationships.invoke({
            "data_element_concept": test_data_element_concept,
            "object_class": test_object_class,
            "property": test_property,
            "concept_domain": test_concept_domain
        })
        print(f"注册结果: {result}")
        total_count += 1
        if verify_node_fields("数据元概念", test_data_element_concept):
            success_count += 1
    except Exception as e:
        print(f"✗ 注册失败: {e}")
        total_count += 1

    # 5. 测试值域注册（不可枚举）
    print("\n[5/6] 测试值域注册（不可枚举）...")
    try:
        result = register_value_domain_with_relationship.invoke({
            "value_domain": test_value_domain,
            "concept_domain": test_concept_domain
        })
        print(f"注册结果: {result}")
        total_count += 1
        if verify_node_fields("值域", test_value_domain):
            success_count += 1
    except Exception as e:
        print(f"✗ 注册失败: {e}")
        total_count += 1

    # 6. 测试数据元注册
    print("\n[6/6] 测试数据元注册...")
    try:
        result = register_data_element_with_relationships.invoke({
            "data_element": test_data_element,
            "data_element_concept": test_data_element_concept,
            "value_domain": test_value_domain
        })
        print(f"注册结果: {result}")
        total_count += 1
        if verify_node_fields("数据元", test_data_element):
            success_count += 1
    except Exception as e:
        print(f"✗ 注册失败: {e}")
        total_count += 1

    # 打印测试结果
    print("\n" + "=" * 80)
    print(f"测试完成: {success_count}/{total_count} 个测试通过")
    print("=" * 80)

    if success_count == total_count:
        print("\n✓ 所有测试通过！智能体注册的describe字段已正确实现。")
    else:
        print(f"\n✗ 有 {total_count - success_count} 个测试失败，请检查代码。")

    return success_count == total_count


def cleanup_test_data():
    """
    清理测试数据
    """
    print("\n是否清理测试数据？(y/n): ", end='')
    choice = input().strip().lower()

    if choice == 'y':
        with driver.session() as session:
            # 删除测试节点
            test_names = [
                ("对象类", "测试对象类_智能体"),
                ("属性", "测试属性_智能体"),
                ("概念域", "测试概念域_智能体"),
                ("数据元概念", "测试对象类_智能体测试属性_智能体"),
                ("值域", "测试值域_智能体"),
                ("数据元", "DE测试对象类_智能体测试属性_智能体")
            ]

            for label, name in test_names:
                query = f"MATCH (n:{label} {{name: $name}}) DETACH DELETE n"
                session.run(query, name=name)

            print("✓ 测试数据已清理")
    else:
        print("保留测试数据")


if __name__ == "__main__":
    try:
        # 运行测试
        test_result = test_basic_registration()

        # 清理测试数据
        cleanup_test_data()

    finally:
        # 关闭数据库连接
        driver.close()
        print("\n数据库连接已关闭")
