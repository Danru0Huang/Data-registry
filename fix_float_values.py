"""
修复脚本：将数据库中的浮点数值标准化为整数
例如：0.0 -> 0, 1.0 -> 1
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

def normalize_float_values():
    """标准化所有表属性值中的浮点数"""
    print("=" * 80)
    print("开始标准化表属性值中的浮点数...")
    print("=" * 80)

    # 查询所有表属性值
    query = """
    MATCH (v:表属性值)
    RETURN v.name as value_name, v.identifier as value_id, id(v) as node_id
    """
    results = graph.run(query).data()

    updated_count = 0
    for r in results:
        value_name = r['value_name']
        value_id = r['value_id']
        node_id = r['node_id']

        # 检查是否是浮点数字符串（如"0.0", "1.0"等）
        try:
            if isinstance(value_name, str):
                float_val = float(value_name)
                # 如果能转换为浮点数，且小数部分为0
                if float_val.is_integer():
                    int_val = int(float_val)
                    new_value = str(int_val)

                    # 如果值发生了变化
                    if new_value != value_name:
                        print(f"更新: {value_name} -> {new_value} (ID: {value_id})")

                        # 更新节点
                        update_query = """
                        MATCH (v:表属性值)
                        WHERE id(v) = $node_id
                        SET v.name = $new_value
                        """
                        graph.run(update_query, node_id=node_id, new_value=new_value)
                        updated_count += 1
            elif isinstance(value_name, float):
                # 直接就是浮点数类型
                if value_name.is_integer():
                    int_val = int(value_name)
                    new_value = str(int_val)
                    print(f"更新: {value_name} -> {new_value} (ID: {value_id})")

                    # 更新节点
                    update_query = """
                    MATCH (v:表属性值)
                    WHERE id(v) = $node_id
                    SET v.name = $new_value
                    """
                    graph.run(update_query, node_id=node_id, new_value=new_value)
                    updated_count += 1
        except (ValueError, TypeError):
            # 不是数字，跳过
            pass

    print("\n" + "=" * 80)
    print(f"标准化完成！共更新了 {updated_count} 个值")
    print("=" * 80)


if __name__ == "__main__":
    try:
        normalize_float_values()
    except Exception as e:
        print(f"\n❌ 错误: {str(e)}")
        import traceback
        traceback.print_exc()
