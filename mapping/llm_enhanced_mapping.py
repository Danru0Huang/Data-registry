import os
from dotenv import load_dotenv
from py2neo import Graph
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage
import time
import json
from datetime import datetime

# 加载环境变量
load_dotenv()

# Neo4j连接配置（从环境变量读取）
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "123456")
graph = Graph(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

# 初始化LLM (使用DeepSeek或OpenAI，从环境变量读取API密钥)
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_BASE_URL"] = os.getenv("OPENAI_BASE_URL", "https://api.deepseek.com/v1")

llm = ChatOpenAI(
    model="deepseek-chat",
    temperature=0.1,  # 低温度保证稳定性
    max_retries=3,
    max_tokens=1000
)

# 映射结果存储文件
MAPPING_RESULTS_FILE = "mapping_results.json"
MAPPING_LOG_FILE = "mapping_log.txt"

# ==================== 数据获取函数 ====================

def get_subdomain_data():
    """获取所有子域数据(数据节点)"""
    query = "MATCH (s:数据) RETURN s.id as id, s.value as name"
    return graph.run(query).data()

def get_subdomain_values(subdomain_name):
    """获取子域数据的所有数据值"""
    query = f"""
    MATCH (s:数据 {{value: '{subdomain_name}'}})-[:包含值]->(v:数据值)
    RETURN v.id as id, v.value as name
    """
    return graph.run(query).data()

def get_shared_data_elements():
    """获取所有MDR共享域数据元"""
    query = "MATCH (d:DataElement) RETURN d.id as id, d.name as name"
    return graph.run(query).data()

def get_value_domain_for_data_element(data_element_name):
    """获取数据元对应的值域"""
    query = f"""
    MATCH (d:DataElement {{name: '{data_element_name}'}})-[:HAS_VALUE_DOMAIN]->(vd:ValueDomain)
    RETURN vd.id as id, vd.name as name
    """
    return graph.run(query).data()

def get_values_for_value_domain(value_domain_name):
    """获取值域的所有可枚举值"""
    query = f"""
    MATCH (vd:ValueDomain {{name: '{value_domain_name}'}})-[:INCLUDE]->(v:Value)
    RETURN v.id as id, v.name as name
    """
    return graph.run(query).data()

# ==================== LLM映射函数 ====================

def llm_match_data_element(subdomain_name, candidate_data_elements, context=""):
    """
    使用LLM进行第一层映射:子域数据 -> 数据元

    Args:
        subdomain_name: 子域数据名称
        candidate_data_elements: 候选数据元列表
        context: 额外上下文信息

    Returns:
        dict: {
            'matched_name': 匹配的数据元名称,
            'confidence': 置信度(high/medium/low),
            'reasoning': 匹配理由
        }
    """
    if not candidate_data_elements:
        return None

    # 构建候选列表
    candidates_str = "\n".join([f"{i+1}. {de['name']}" for i, de in enumerate(candidate_data_elements)])

    prompt = f"""你是一个专业的数据语义匹配专家。你的任务是为子域数据找到最匹配的MDR数据元。

**子域数据**: {subdomain_name}
{f"**上下文**: {context}" if context else ""}

**候选MDR数据元列表**:
{candidates_str}

请按照以下步骤分析:
1. 理解子域数据"{subdomain_name}"的语义含义
2. 分析每个候选数据元的语义
3. 选择最匹配的数据元

请以JSON格式返回结果:
{{
    "matched_name": "最匹配的数据元名称",
    "confidence": "high/medium/low",
    "reasoning": "选择这个数据元的理由(简洁说明)"
}}

如果没有合适的匹配,返回:
{{
    "matched_name": null,
    "confidence": "low",
    "reasoning": "未找到合适匹配的原因"
}}
"""

    try:
        response = llm.invoke([HumanMessage(content=prompt)])
        result_text = response.content.strip()

        # 提取JSON
        if "```json" in result_text:
            result_text = result_text.split("```json")[1].split("```")[0].strip()
        elif "```" in result_text:
            result_text = result_text.split("```")[1].split("```")[0].strip()

        result = json.loads(result_text)
        return result

    except Exception as e:
        print(f"LLM匹配出错: {e}")
        return None

def llm_match_value(subdomain_value, candidate_values, data_element_context=""):
    """
    使用LLM进行第二层映射:子域数据值 -> 可枚举值

    Args:
        subdomain_value: 子域数据值
        candidate_values: 候选可枚举值列表
        data_element_context: 所属数据元的上下文

    Returns:
        dict: 匹配结果
    """
    if not candidate_values:
        return None

    # 构建候选列表
    candidates_str = "\n".join([f"{i+1}. {v['name']}" for i, v in enumerate(candidate_values)])

    prompt = f"""你是一个专业的数据值语义匹配专家。你的任务是为子域数据值找到最匹配的MDR可枚举值。

**子域数据值**: {subdomain_value}
{f"**所属数据元**: {data_element_context}" if data_element_context else ""}

**候选MDR可枚举值列表**:
{candidates_str}

请按照以下步骤分析:
1. 理解子域数据值"{subdomain_value}"的语义含义
2. 考虑数据元上下文
3. 分析每个候选值的语义
4. 选择最匹配的可枚举值

请以JSON格式返回结果:
{{
    "matched_name": "最匹配的可枚举值名称",
    "confidence": "high/medium/low",
    "reasoning": "选择这个值的理由(简洁说明)"
}}

如果没有合适的匹配,返回:
{{
    "matched_name": null,
    "confidence": "low",
    "reasoning": "未找到合适匹配的原因"
}}
"""

    try:
        response = llm.invoke([HumanMessage(content=prompt)])
        result_text = response.content.strip()

        # 提取JSON
        if "```json" in result_text:
            result_text = result_text.split("```json")[1].split("```")[0].strip()
        elif "```" in result_text:
            result_text = result_text.split("```")[1].split("```")[0].strip()

        result = json.loads(result_text)
        return result

    except Exception as e:
        print(f"LLM值匹配出错: {e}")
        return None

# ==================== 映射关系创建 ====================

def create_data_element_mapping(subdomain_name, data_element_name, confidence, reasoning):
    """创建子域数据与数据元之间的映射关系"""
    query = f"""
    MATCH (sub:数据 {{value: '{subdomain_name}'}})
    MATCH (de:DataElement {{name: '{data_element_name}'}})
    MERGE (sub)-[r:MAPPED_TO]->(de)
    SET r.confidence = '{confidence}',
        r.reasoning = '{reasoning}',
        r.created_at = datetime()
    """
    try:
        graph.run(query)
        print(f"✓ 创建数据元映射: {subdomain_name} -> {data_element_name} (置信度: {confidence})")
        log_mapping("data_element", subdomain_name, data_element_name, confidence, reasoning)
        return True
    except Exception as e:
        print(f"✗ 创建数据元映射失败: {e}")
        return False

def create_value_mapping(subdomain_value, enumerable_value, confidence, reasoning):
    """创建子域数据值与可枚举值之间的映射关系"""
    query = f"""
    MATCH (sv:数据值 {{value: '{subdomain_value}'}})
    MATCH (ev:Value {{name: '{enumerable_value}'}})
    MERGE (sv)-[r:MAPPED_TO]->(ev)
    SET r.confidence = '{confidence}',
        r.reasoning = '{reasoning}',
        r.created_at = datetime()
    """
    try:
        graph.run(query)
        print(f"  ✓ 创建值映射: {subdomain_value} -> {enumerable_value} (置信度: {confidence})")
        log_mapping("value", subdomain_value, enumerable_value, confidence, reasoning)
        return True
    except Exception as e:
        print(f"  ✗ 创建值映射失败: {e}")
        return False

# ==================== 映射流程 ====================

def first_level_mapping(subdomain_data_list, shared_data_elements, min_confidence="medium"):
    """
    第一层映射:子域数据 -> MDR数据元

    Args:
        subdomain_data_list: 子域数据列表
        shared_data_elements: 共享域数据元列表
        min_confidence: 最低置信度阈值
    """
    print("\n" + "="*80)
    print("开始第一层映射: 子域数据 -> MDR数据元")
    print("="*80)

    total = len(subdomain_data_list)
    success_count = 0
    skip_count = 0

    confidence_levels = {"high": 3, "medium": 2, "low": 1}
    min_level = confidence_levels.get(min_confidence, 2)

    for idx, subdomain_data in enumerate(subdomain_data_list, 1):
        subdomain_name = subdomain_data['name']
        print(f"\n[{idx}/{total}] 处理子域数据: {subdomain_name}")

        # 使用LLM进行智能匹配
        match_result = llm_match_data_element(subdomain_name, shared_data_elements)

        if match_result and match_result.get('matched_name'):
            confidence = match_result.get('confidence', 'low')
            reasoning = match_result.get('reasoning', '')
            matched_name = match_result['matched_name']

            # 检查置信度
            if confidence_levels.get(confidence, 0) >= min_level:
                # 创建映射关系
                if create_data_element_mapping(subdomain_name, matched_name, confidence, reasoning):
                    success_count += 1
                    # 继续进行第二层映射
                    second_level_mapping(subdomain_name, matched_name)
            else:
                print(f"  ⚠ 置信度过低({confidence}),跳过映射")
                skip_count += 1
        else:
            print(f"  ⚠ 未找到匹配的数据元")
            skip_count += 1

        # 避免API限流
        time.sleep(0.5)

    print(f"\n第一层映射完成: 成功{success_count}, 跳过{skip_count}, 总计{total}")
    return success_count

def second_level_mapping(subdomain_name, data_element_name):
    """
    第二层映射:子域数据值 -> MDR可枚举值

    Args:
        subdomain_name: 子域数据名称
        data_element_name: 已匹配的数据元名称
    """
    print(f"  → 开始第二层映射: {subdomain_name} 的数据值")

    # 获取子域数据的所有数据值
    subdomain_values = get_subdomain_values(subdomain_name)

    if not subdomain_values:
        print(f"    ⚠ 子域数据 '{subdomain_name}' 没有数据值,跳过第二层映射")
        return 0

    # 获取数据元对应的值域
    value_domains = get_value_domain_for_data_element(data_element_name)

    if not value_domains:
        print(f"    ⚠ 数据元 '{data_element_name}' 没有值域,跳过第二层映射")
        return 0

    success_count = 0

    # 遍历每个值域
    for value_domain in value_domains:
        value_domain_name = value_domain['name']
        print(f"    处理值域: {value_domain_name}")

        # 获取值域的所有可枚举值
        enumerable_values = get_values_for_value_domain(value_domain_name)

        if not enumerable_values:
            print(f"      ⚠ 值域 '{value_domain_name}' 没有可枚举值")
            continue

        # 对每个子域数据值进行匹配
        for sub_value in subdomain_values:
            subdomain_value_name = sub_value['name']

            # 使用LLM进行智能值匹配
            match_result = llm_match_value(
                subdomain_value_name,
                enumerable_values,
                data_element_context=data_element_name
            )

            if match_result and match_result.get('matched_name'):
                confidence = match_result.get('confidence', 'low')
                reasoning = match_result.get('reasoning', '')
                matched_value = match_result['matched_name']

                # 创建值映射关系
                if create_value_mapping(subdomain_value_name, matched_value, confidence, reasoning):
                    success_count += 1

            # 避免API限流
            time.sleep(0.3)

    print(f"    第二层映射完成: 成功映射 {success_count} 个数据值")
    return success_count

# ==================== 日志和报告 ====================

def log_mapping(mapping_type, source, target, confidence, reasoning):
    """记录映射结果到日志文件"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {mapping_type.upper()}: {source} -> {target} | 置信度: {confidence} | 理由: {reasoning}\n"

    with open(MAPPING_LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(log_entry)

def save_mapping_report():
    """生成映射报告"""
    report = {
        "generated_at": datetime.now().isoformat(),
        "statistics": get_mapping_statistics()
    }

    with open(MAPPING_RESULTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print(f"\n映射报告已保存到: {MAPPING_RESULTS_FILE}")

def get_mapping_statistics():
    """获取映射统计信息"""
    stats = {}

    # 统计数据元映射
    query_de = """
    MATCH (s:数据)-[r:MAPPED_TO]->(de:DataElement)
    RETURN count(r) as total,
           sum(CASE WHEN r.confidence = 'high' THEN 1 ELSE 0 END) as high_confidence,
           sum(CASE WHEN r.confidence = 'medium' THEN 1 ELSE 0 END) as medium_confidence,
           sum(CASE WHEN r.confidence = 'low' THEN 1 ELSE 0 END) as low_confidence
    """
    de_stats = graph.run(query_de).data()[0]
    stats['data_element_mappings'] = de_stats

    # 统计值映射
    query_val = """
    MATCH (sv:数据值)-[r:MAPPED_TO]->(ev:Value)
    RETURN count(r) as total,
           sum(CASE WHEN r.confidence = 'high' THEN 1 ELSE 0 END) as high_confidence,
           sum(CASE WHEN r.confidence = 'medium' THEN 1 ELSE 0 END) as medium_confidence,
           sum(CASE WHEN r.confidence = 'low' THEN 1 ELSE 0 END) as low_confidence
    """
    val_stats = graph.run(query_val).data()[0]
    stats['value_mappings'] = val_stats

    return stats

# ==================== 主函数 ====================

def main():
    """主函数:执行完整的两层映射流程"""
    print("="*80)
    print("MDR-子域智能映射系统 (基于LLM)")
    print("="*80)

    start_time = time.time()

    try:
        # 1. 获取所有数据
        print("\n正在加载数据...")
        subdomain_data_list = get_subdomain_data()
        shared_data_elements = get_shared_data_elements()

        print(f"子域数据数量: {len(subdomain_data_list)}")
        print(f"共享域数据元数量: {len(shared_data_elements)}")

        if not subdomain_data_list or not shared_data_elements:
            print("错误: 没有找到待映射的数据")
            return

        # 2. 执行第一层映射(会自动触发第二层映射)
        success_count = first_level_mapping(
            subdomain_data_list,
            shared_data_elements,
            min_confidence="medium"  # 可调整置信度阈值
        )

        # 3. 生成映射报告
        save_mapping_report()

        # 4. 显示统计信息
        stats = get_mapping_statistics()
        print("\n" + "="*80)
        print("映射统计摘要")
        print("="*80)
        print(f"数据元映射总数: {stats['data_element_mappings']['total']}")
        print(f"  - 高置信度: {stats['data_element_mappings']['high_confidence']}")
        print(f"  - 中置信度: {stats['data_element_mappings']['medium_confidence']}")
        print(f"  - 低置信度: {stats['data_element_mappings']['low_confidence']}")
        print(f"\n数据值映射总数: {stats['value_mappings']['total']}")
        print(f"  - 高置信度: {stats['value_mappings']['high_confidence']}")
        print(f"  - 中置信度: {stats['value_mappings']['medium_confidence']}")
        print(f"  - 低置信度: {stats['value_mappings']['low_confidence']}")

        elapsed_time = time.time() - start_time
        print(f"\n总耗时: {elapsed_time:.2f} 秒")
        print("="*80)

    except Exception as e:
        print(f"\n错误: {e}")
        import traceback
        traceback.print_exc()

    finally:
        print("\n映射任务结束")

if __name__ == "__main__":
    main()
