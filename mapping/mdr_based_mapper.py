"""
基于 MDR 的映射系统 - 替代 DBpedia 使用 Neo4j MDR 数据
修改自 ctaceallm/react0211nam.py
"""
import os
import sys
import csv
import json
import logging
import tempfile
from datetime import datetime
import pandas as pd
from typing import Dict, List, Tuple, Optional
from collections import defaultdict, Counter
from dotenv import load_dotenv
from py2neo import Graph

# 添加项目路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 导入配置
from config import Config

# LangChain 相关
from langchain_openai import ChatOpenAI
from langchain.tools import Tool
from langchain.agents import create_react_agent, AgentExecutor
from langchain.prompts import PromptTemplate
from langchain.schema import HumanMessage

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 加载环境变量
load_dotenv()


class MDRBasedMapper:
    """基于 MDR 的映射器 - 替代 DBpedia"""

    def __init__(self):
        """初始化映射器"""
        # Neo4j 连接
        neo4j_config = Config.get_neo4j_config()
        self.graph = Graph(neo4j_config["uri"], auth=(neo4j_config["user"], neo4j_config["password"]))

        # LLM 初始化
        openai_config = Config.get_openai_config()
        self.llm = ChatOpenAI(
            model=openai_config["model"],  # 从 .env 读取
            temperature=openai_config["temperature"],  # 从 .env 读取
            openai_api_key=openai_config["api_key"],
            openai_api_base=openai_config["base_url"],
            max_retries=openai_config["max_retries"],
            max_tokens=openai_config["max_tokens"]  # 从 .env 读取
        )

        # 初始化工具和 Agent
        self._init_tools()
        self._init_agent()

        logger.info("MDR 映射器初始化完成")

    # ==================== 工具1: 查询 MDR DataElement 候选（替代 DBpedia Lookup for CTA） ====================
    def query_mdr_data_elements(self, keyword: str, max_results: int = 5) -> Dict[str, float]:
        """
        利用 MDR 完整语义结构查询 DataElement 候选

        多层语义匹配策略（从高到低）：
        1. 数据元.name 精确匹配 (1.0)
        2. 数据元.name 包含匹配 (0.9)
        3. 属性.name 精确匹配 (0.85) - 属性语义
        4. 对象类.name 精确匹配 (0.8) - 对象类语义
        5. 属性.name 包含匹配 (0.75)
        6. 对象类.name 包含匹配 (0.7)
        7. 概念域.name 匹配 (0.65) - 概念域语义
        8. 值含义.name 匹配 (0.6) - 值含义语义

        Args:
            keyword: 关键词（子域数据名称）
            max_results: 最大返回结果数

        Returns:
            {data_element_name: semantic_score} 字典
        """
        try:
            logger.debug(f"查询 数据元 候选: '{keyword}'")

            # 多层语义匹配查询（使用中文标签和关系）
            query = """
            MATCH (de:数据元)
            OPTIONAL MATCH (de)-[:数据元概念]->(dec:数据元概念)
            OPTIONAL MATCH (dec)-[:属性]->(p:属性)
            OPTIONAL MATCH (dec)-[:对象类]->(oc:对象类)
            OPTIONAL MATCH (dec)-[:概念域]->(cd:概念域)
            OPTIONAL MATCH (de)-[:值域]->(vd:值域)-[:组]->(vdg:值域组)
            OPTIONAL MATCH (vdg)-[:可允许值]->(v:可允许值)-[:值含义]->(vm:值含义)

            // 计算多层语义匹配分数
            WITH de, p, oc, cd, vm,
                 CASE
                     // 1级：数据元 精确匹配（最高优先级）
                     WHEN de.name = $keyword THEN 1.0

                     // 2级：数据元 包含匹配
                     WHEN de.name CONTAINS $keyword OR $keyword CONTAINS de.name THEN 0.9

                     // 3级：属性 精确匹配（属性语义）
                     WHEN p.name = $keyword THEN 0.85

                     // 4级：对象类 精确匹配（对象类语义）
                     WHEN oc.name = $keyword THEN 0.8

                     // 5级：属性 包含匹配
                     WHEN p.name CONTAINS $keyword OR $keyword CONTAINS p.name THEN 0.75

                     // 6级：对象类 包含匹配
                     WHEN oc.name CONTAINS $keyword OR $keyword CONTAINS oc.name THEN 0.7

                     // 7级：概念域 匹配（概念域语义）
                     WHEN cd.name CONTAINS $keyword OR $keyword CONTAINS cd.name THEN 0.65

                     // 8级：值含义 匹配（值含义语义）
                     WHEN vm.name CONTAINS $keyword OR $keyword CONTAINS vm.name THEN 0.6

                     ELSE 0.0
                 END as semantic_score

            WHERE semantic_score > 0

            // 聚合：同一个 数据元 可能通过多个路径匹配，取最高分
            WITH de, MAX(semantic_score) as final_score,
                 COLLECT(DISTINCT p.name) as properties,
                 COLLECT(DISTINCT oc.name) as object_classes,
                 COLLECT(DISTINCT cd.name) as concept_domains

            RETURN de.name as name,
                   final_score as score,
                   properties[0] as property_name,
                   object_classes[0] as object_class_name,
                   concept_domains[0] as concept_domain_name
            ORDER BY final_score DESC
            LIMIT $max_results
            """

            results = self.graph.run(query, keyword=keyword, max_results=max_results).data()

            # 构建返回结果
            candidates = {}
            for r in results:
                name = r['name']
                score = r['score']
                candidates[name] = score

                # 记录匹配路径（用于调试）
                match_info = []
                if r.get('property_name'):
                    match_info.append(f"属性: {r['property_name']}")
                if r.get('object_class_name'):
                    match_info.append(f"对象类: {r['object_class_name']}")
                if r.get('concept_domain_name'):
                    match_info.append(f"概念域: {r['concept_domain_name']}")

                if match_info:
                    logger.debug(f"  - {name} (score: {score:.2f}) via {', '.join(match_info)}")
                else:
                    logger.debug(f"  - {name} (score: {score:.2f}) via direct match")

            logger.info(f"✓ 找到 {len(candidates)} 个 数据元 候选: {list(candidates.keys())}")
            return candidates

        except Exception as e:
            logger.error(f"查询 MDR 数据元 失败: {str(e)}")
            import traceback
            traceback.print_exc()
            return {}
    
    # ==================== 工具2: 查询 MDR Value 候选（替代 DBpedia Lookup for CEA） ====================
    def query_mdr_values(self, keyword: str, column_type: str = None, max_results: int = 10) -> List[Tuple[str, float]]:
        """
        利用 MDR 完整语义结构查询 可允许值 候选（for CEA）

        多层语义匹配策略（从高到低）：
        1. 可允许值.name 精确匹配 (1.0)
        2. 可允许值.name 包含匹配 (0.9)
        3. 值含义.name 精确匹配 (0.85) - 值含义语义
        4. 值含义.name 包含匹配 (0.75)
        5. 关联 数据元 的 属性 匹配 (0.7) - 通过值域关联
        6. 关联 值域 的描述匹配 (0.65)

        Args:
            keyword: 关键词（子域数据值）
            column_type: 列类型（数据元 name，如果已经完成 CTA）
            max_results: 最大返回结果数

        Returns:
            [(value_name, semantic_score), ...] 列表
        """
        try:
            logger.debug(f"查询 可允许值 候选: '{keyword}'" + (f" (限定于 {column_type})" if column_type else ""))

            if column_type:
                # 模式 A：已知列类型，在对应的 值域 中搜索
                query = """
                MATCH (de:数据元 {name: $column_type})-[:值域]->(vd:值域)
                MATCH (vd)-[:组]->(vdg:值域组)-[:可允许值]->(v:可允许值)
                OPTIONAL MATCH (v)-[:值含义]->(vm:值含义)

                // 计算语义匹配分数
                WITH v, vm,
                     CASE
                         // 1级：可允许值 精确匹配
                         WHEN v.name = $keyword THEN 1.0

                         // 2级：可允许值 包含匹配
                         WHEN v.name CONTAINS $keyword OR $keyword CONTAINS v.name THEN 0.9

                         // 3级：值含义 精确匹配
                         WHEN vm.name = $keyword THEN 0.85

                         // 4级：值含义 包含匹配
                         WHEN vm.name CONTAINS $keyword OR $keyword CONTAINS vm.name THEN 0.75

                         ELSE 0.0
                     END as semantic_score

                WHERE semantic_score > 0

                // 聚合：同一个 可允许值 可能有多个 值含义，取最高分
                WITH v, MAX(semantic_score) as final_score,
                     COLLECT(DISTINCT vm.name) as value_meanings

                RETURN v.name as name,
                       final_score as score,
                       value_meanings[0] as value_meaning
                ORDER BY final_score DESC
                LIMIT $max_results
                """
                results = self.graph.run(query, column_type=column_type, keyword=keyword, max_results=max_results).data()

            else:
                # 模式 B：未知列类型，在所有 可允许值 中搜索
                query = """
                MATCH (v:可允许值)
                OPTIONAL MATCH (v)-[:值含义]->(vm:值含义)
                OPTIONAL MATCH (v)<-[:可允许值]-(vdg:值域组)<-[:组]-(vd:值域)<-[:值域]-(de:数据元)
                OPTIONAL MATCH (de)-[:数据元概念]->(dec:数据元概念)-[:属性]->(p:属性)

                // 计算语义匹配分数
                WITH v, vm, p,
                     CASE
                         // 1级：可允许值 精确匹配
                         WHEN v.name = $keyword THEN 1.0

                         // 2级：可允许值 包含匹配
                         WHEN v.name CONTAINS $keyword OR $keyword CONTAINS v.name THEN 0.9

                         // 3级：值含义 精确匹配
                         WHEN vm.name = $keyword THEN 0.85

                         // 4级：值含义 包含匹配
                         WHEN vm.name CONTAINS $keyword OR $keyword CONTAINS vm.name THEN 0.75

                         // 5级：关联的 属性 匹配（扩展语义）
                         WHEN p.name CONTAINS $keyword OR $keyword CONTAINS p.name THEN 0.7

                         ELSE 0.0
                     END as semantic_score

                WHERE semantic_score > 0

                // 聚合
                WITH v, MAX(semantic_score) as final_score,
                     COLLECT(DISTINCT vm.name) as value_meanings,
                     COLLECT(DISTINCT p.name) as properties

                RETURN v.name as name,
                       final_score as score,
                       value_meanings[0] as value_meaning,
                       properties[0] as property_name
                ORDER BY final_score DESC
                LIMIT $max_results
                """
                results = self.graph.run(query, keyword=keyword, max_results=max_results).data()

            # 构建返回结果
            candidates = []
            for r in results:
                name = r['name']
                score = r['score']

                # 只过滤空值，保留所有数据库中的可允许值（包括数字）
                if not name:
                    continue

                candidates.append((name, score))

                # 记录匹配路径（用于调试）
                match_info = []
                if r.get('value_meaning'):
                    match_info.append(f"值含义: {r['value_meaning']}")
                if r.get('property_name'):
                    match_info.append(f"属性: {r['property_name']}")

                if match_info:
                    logger.debug(f"  - {name} (score: {score:.2f}) via {', '.join(match_info)}")
                else:
                    logger.debug(f"  - {name} (score: {score:.2f}) via direct match")

            logger.info(f"✓ 找到 {len(candidates)} 个 可允许值 候选: {[c[0] for c in candidates]}")
            return candidates

        except Exception as e:
            logger.error(f"查询 MDR 可允许值 失败: {str(e)}")
            import traceback
            traceback.print_exc()
            return []
    
    # ==================== 工具3: CTA - 列类型注释（使用 LLM + MDR DataElement） ====================
    def get_column_type_with_llm(self, column_values: List[str]) -> str:
        """
        使用 LLM 从 MDR DataElement 候选中选择最佳列类型

        Args:
            column_values: 列的前几个值

        Returns:
            MDR DataElement name
        """
        try:
            # 为每个列值查询 DataElement 候选
            all_candidates = Counter()
            for value in column_values[:10]:
                if value and str(value).strip():
                    candidates = self.query_mdr_data_elements(str(value), max_results=3)
                    for name, score in candidates.items():
                        all_candidates[name] += score

            # 获取 Top 5 候选
            top_candidates = [name for name, _ in all_candidates.most_common(5)]

            if not top_candidates:
                logger.warning(f"未找到候选，列值: {column_values[:3]}")
                return ""

            # 使用 LLM 从候选中选择最佳
            prompt = f"""
            You are a data expert. Given a list of column values and MDR DataElement candidates,
            select the most suitable DataElement that represents this column.

            Column values: {column_values[:10]}
            MDR DataElement candidates: {top_candidates}

            Please select the most suitable DataElement from the candidates.
            Return ONLY the DataElement name, nothing else.
            """

            response = self.llm([HumanMessage(content=prompt)])
            result = response.content.strip()

            # 验证结果是否在候选中
            if result in top_candidates:
                logger.info(f"✓ CTA: 列值 {column_values[:3]} → {result}")
                return result
            else:
                # 返回得分最高的候选
                logger.warning(f"LLM 返回的结果不在候选中，使用得分最高的: {top_candidates[0]}")
                return top_candidates[0] if top_candidates else ""

        except Exception as e:
            logger.error(f"CTA 失败: {str(e)}")
            return ""

    # ==================== 工具4: CEA - 单元格实体注释（使用 LLM + MDR Value） ====================
    def get_cell_entity_with_llm(self, cell_value: str, column_type: str) -> str:
        """
        使用 LLM 从 MDR Value 候选中选择最佳单元格实体

        Args:
            cell_value: 单元格值
            column_type: 列类型（DataElement name）

        Returns:
            MDR Value name
        """
        try:
            # 查询 Value 候选
            candidates = self.query_mdr_values(cell_value, column_type, max_results=5)

            if not candidates:
                logger.warning(f"未找到候选，单元格: {cell_value}, 列类型: {column_type}")
                return ""

            # 使用 LLM 从候选中选择最佳
            prompt = f"""
            You are a data expert. Given a cell value, its column type, and MDR Value candidates,
            select the most suitable Value that matches this cell.

            Cell value: {cell_value}
            Column type (DataElement): {column_type}
            MDR Value candidates: {candidates}

            Please select the most suitable Value from the candidates.
            Return ONLY the Value name, nothing else.
            """

            response = self.llm([HumanMessage(content=prompt)])
            result = response.content.strip()

            # 验证结果是否在候选中
            if result in candidates:
                logger.debug(f"✓ CEA: {cell_value} → {result}")
                return result
            else:
                # 返回第一个候选
                logger.warning(f"LLM 返回的结果不在候选中，使用第一个候选: {candidates[0]}")
                return candidates[0] if candidates else ""

        except Exception as e:
            logger.error(f"CEA 失败: {str(e)}")
            return ""

    # ==================== 辅助函数 ====================
    def _calculate_scores(self, elements: List[str]) -> Dict[str, float]:
        """
        根据元素的位置分配分数

        Args:
            elements: 待评分的元素列表

        Returns:
            {element: score} 字典
        """
        scores = defaultdict(float)
        score_weights = [1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1]

        for idx, element in enumerate(elements[:10]):
            scores[element] += score_weights[idx]

        return dict(scores)

    def _init_tools(self):
        """初始化 LangChain 工具"""
        # CTA 工具
        cta_tool = Tool(
            name="GetColumnType",
            func=lambda x: self.get_column_type_with_llm(eval(x) if isinstance(x, str) else x),
            description="Get MDR DataElement type for a column based on its values. Input should be a list of column values."
        )

        # CEA 工具
        cea_tool = Tool(
            name="GetCellEntity",
            func=lambda x: self.get_cell_entity_with_llm(*eval(x) if isinstance(x, str) else x),
            description="Get MDR Value for a cell given its value and column type. Input should be (cell_value, column_type)."
        )

        self.tools = [cta_tool, cea_tool]

    def _init_agent(self):
        """初始化 ReAct Agent"""
        template = '''
        Do your best to answer the following questions. You may use the following tools.

        {tools}

        Use the following format:

        Question: the input question you must answer
        Thought: you should always think about what to do
        Action: the action to take, should be one of [{tool_names}]
        Action Input: the input to the action
        Observation: the result of the action
        ... (this Thought/Action/Action Input/Observation can repeat N times)
        Thought: I now know the final answer
        Final Answer: the final answer to the original input question

        Begin!

        Question: {input}
        Thought:{agent_scratchpad}
        '''

        prompt = PromptTemplate.from_template(template)
        agent = create_react_agent(self.llm, self.tools, prompt)

        self.agent_executor = AgentExecutor(
            agent=agent,
            tools=self.tools,
            handle_parsing_errors=True,
            verbose=True,
            max_iterations=10
        )

    # ==================== 主流程 ====================
    def export_subdomain_for_mapping(self, subdomain_name: str, output_dir: str) -> Tuple[str, str]:
        """
        从 Neo4j 导出子域数据，生成 CTA 和 CEA 映射表（适配原系统数据模型）

        Args:
            subdomain_name: 子域名称
            output_dir: 输出目录（data 文件夹）

        Returns:
            (cta_csv_path, cea_csv_path) 元组
        """
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            cta_csv_path = os.path.join(output_dir, f"CTA_mapping_{subdomain_name}_{timestamp}.csv")
            cea_csv_path = os.path.join(output_dir, f"CEA_mapping_{subdomain_name}_{timestamp}.csv")

            # 查询子域数据和数据值（适配原系统：子域 → 表 → 表属性 → 表属性值）
            query = """
            MATCH (s:子域 {name: $subdomain_name})-[:拥有]->(t:表)-[:由组成]->(a:表属性)
            OPTIONAL MATCH (a)-[:约束值]->(v:表属性值)
            RETURN a.name as data_name, collect(DISTINCT v.name) as data_values
            ORDER BY data_name
            """

            result = self.graph.run(query, subdomain_name=subdomain_name).data()

            if not result:
                logger.warning(f"未找到子域 '{subdomain_name}' 的数据")
                return None, None

            logger.info(f"查询到 {len(result)} 个表属性")

            # ========== 1. 生成 CTA 映射表（表属性 → DataElement 候选）==========
            logger.info("生成 CTA 映射表...")
            cta_rows = []

            for row in result:
                data_name = row['data_name']

                # 查询 DataElement 候选（使用多层语义匹配）
                candidates = self.query_mdr_data_elements(data_name, max_results=5)

                # 构建 CSV 行：[表属性名称, 候选1, 候选2, ...]
                cta_row = [data_name]
                # 按分数排序
                sorted_candidates = sorted(candidates.items(), key=lambda x: x[1], reverse=True)
                cta_row.extend([name for name, score in sorted_candidates])

                cta_rows.append(cta_row)
                logger.debug(f"  {data_name}: 找到 {len(candidates)} 个候选")

            # 写入 CTA CSV
            with open(cta_csv_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                # 表头
                max_candidates = max(len(row) - 1 for row in cta_rows) if cta_rows else 0
                headers = ['表属性名称'] + [f'候选数据元{i+1}' for i in range(max_candidates)]
                writer.writerow(headers)
                # 数据行（补齐空列）
                for row in cta_rows:
                    row_padded = row + [''] * (len(headers) - len(row))
                    writer.writerow(row_padded)

            logger.info(f"✓ CTA 映射表已导出: {cta_csv_path}")

            # ========== 2. 生成 CEA 映射表（表属性值 → Value 候选）==========
            logger.info("生成 CEA 映射表...")
            cea_rows = []

            for row in result:
                data_name = row['data_name']
                data_values = row['data_values']

                if not data_values:
                    continue

                for value in data_values:
                    if not value:
                        continue

                    # 查询 Value 候选（使用多层语义匹配）
                    # 注意：这里不传 column_type，因为还没有完成 CTA
                    candidates = self.query_mdr_values(value, column_type=None, max_results=5)

                    # 只过滤空值，保留所有有效候选（包括数字编码）
                    valid_candidates = [
                        (name, score) for name, score in candidates
                        if name is not None and str(name).strip()
                    ]

                    if not valid_candidates:
                        logger.debug(f"  {value} ({data_name}): 无候选，跳过")
                        continue

                    # 构建 CSV 行：[表属性值, 所属表属性, 候选1, 候选2, ...]
                    cea_row = [value, data_name]
                    # 按分数排序
                    sorted_candidates = sorted(valid_candidates, key=lambda x: x[1], reverse=True)
                    cea_row.extend([name for name, score in sorted_candidates])

                    cea_rows.append(cea_row)
                    logger.debug(f"  {value} ({data_name}): 找到 {len(valid_candidates)} 个候选")

            # 写入 CEA CSV
            with open(cea_csv_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                # 表头
                max_candidates = max(len(row) - 2 for row in cea_rows) if cea_rows else 0
                headers = ['表属性值', '所属表属性'] + [f'候选可允许值{i+1}' for i in range(max_candidates)]
                writer.writerow(headers)
                # 数据行（补齐空列）
                for row in cea_rows:
                    row_padded = row + [''] * (len(headers) - len(row))
                    writer.writerow(row_padded)

            logger.info(f"✓ CEA 映射表已导出: {cea_csv_path}")
            logger.info(f"✓ CTA 记录数: {len(cta_rows)}, CEA 记录数: {len(cea_rows)}")

            return cta_csv_path, cea_csv_path

        except Exception as e:
            logger.error(f"导出子域数据失败: {str(e)}")
            import traceback
            traceback.print_exc()
            return None, None

    def process_csv_mapping(self, csv_file_path: str) -> Dict:
        """
        处理 CSV 文件，执行 CTA 和 CEA

        Args:
            csv_file_path: CSV 文件路径

        Returns:
            映射结果
        """
        try:
            # 读取 CSV
            df = pd.read_csv(csv_file_path, encoding='utf-8')
            logger.info(f"读取到 {len(df.columns)} 列数据")

            cta_results = []  # 列类型注释
            cea_results = []  # 单元格实体注释

            # 对每一列进行 CTA
            for col_idx, column in enumerate(df.columns):
                column_values = df[column].dropna().astype(str).head(10).tolist()

                if not column_values:
                    continue

                logger.info(f"\n处理列 {col_idx}: {column}")

                # CTA: 获取列类型
                column_type = self.get_column_type_with_llm(column_values)

                if column_type:
                    cta_results.append({
                        'column_index': col_idx,
                        'column_name': column,
                        'data_element': column_type
                    })

                    # CEA: 对该列的单元格进行实体注释
                    for row_idx, value in enumerate(column_values[:5]):
                        if pd.notna(value) and str(value).strip():
                            entity = self.get_cell_entity_with_llm(str(value), column_type)

                            if entity:
                                cea_results.append({
                                    'row_index': row_idx,
                                    'column_index': col_idx,
                                    'cell_value': value,
                                    'mdr_value': entity
                                })

            logger.info(f"\n✓ CTA 完成: {len(cta_results)} 个列类型")
            logger.info(f"✓ CEA 完成: {len(cea_results)} 个单元格实体")

            return {
                'status': 'success',
                'cta_count': len(cta_results),
                'cea_count': len(cea_results),
                'cta_results': cta_results,
                'cea_results': cea_results
            }

        except Exception as e:
            logger.error(f"处理 CSV 映射失败: {str(e)}")
            return {'status': 'failed', 'error': str(e)}

    def create_mappings_in_neo4j(self, cta_results: List[Dict], cea_results: List[Dict]) -> int:
        """将映射结果写回 Neo4j（适配原系统数据模型，使用中文标签）"""
        mapping_count = 0

        try:
            # CTA 映射: 表属性 → MDR 数据元
            logger.info("写入 CTA 映射（表属性 → 数据元）...")
            for cta in cta_results:
                subdomain_data = cta['subdomain_data']  # 表属性名称
                data_element = cta['data_element']      # 数据元名称

                query = """
                MATCH (a:表属性 {name: $subdomain_data})
                MATCH (de:数据元 {name: $data_element})
                MERGE (a)-[r:数据元]->(de)
                SET r.mapping_method = 'AUTO_MDR_CTA',
                    r.confidence = 0.9,
                    r.created_at = datetime()
                RETURN count(r) as count
                """

                result = self.graph.run(query, subdomain_data=subdomain_data, data_element=data_element).data()

                if result and result[0]['count'] > 0:
                    mapping_count += result[0]['count']
                    logger.info(f"  ✓ CTA: 表属性 '{subdomain_data}' → 数据元 '{data_element}'")

            # CEA 映射: 表属性值 → MDR 可允许值
            logger.info("\n写入 CEA 映射（表属性值 → 可允许值）...")
            for cea in cea_results:
                subdomain_value = cea['subdomain_value']  # 表属性值名称
                subdomain_data = cea['subdomain_data']    # 表属性名称
                mdr_value = cea['mdr_value']              # 可允许值名称

                query = """
                MATCH (av:表属性值 {name: $subdomain_value})
                MATCH (v:可允许值 {name: $mdr_value})
                MERGE (av)-[r:映射]->(v)
                SET r.mapping_method = 'AUTO_MDR_CEA',
                    r.confidence = 0.9,
                    r.subdomain_data = $subdomain_data,
                    r.created_at = datetime()
                RETURN count(r) as count
                """

                result = self.graph.run(
                    query,
                    subdomain_value=str(subdomain_value),
                    subdomain_data=subdomain_data,
                    mdr_value=mdr_value
                ).data()

                if result and result[0]['count'] > 0:
                    mapping_count += result[0]['count']
                    logger.debug(f"  ✓ CEA: 表属性值 '{subdomain_value}' → 可允许值 '{mdr_value}'")

            logger.info(f"\n✓ 创建了 {mapping_count} 个映射关系")
            return mapping_count

        except Exception as e:
            logger.error(f"创建映射关系失败: {str(e)}")
            import traceback
            traceback.print_exc()
            return 0

    def process_mapping_tables(self, cta_csv_path: str, cea_csv_path: str) -> Dict:
        """
        处理 CTA 和 CEA 映射表，使用 LLM 从候选中选择最佳匹配

        Args:
            cta_csv_path: CTA 映射表路径
            cea_csv_path: CEA 映射表路径

        Returns:
            映射结果 {'status', 'cta_results', 'cea_results', 'cta_count', 'cea_count'}
        """
        try:
            cta_results = []
            cea_results = []

            # ========== 1. 处理 CTA 映射表 ==========
            logger.info("处理 CTA 映射表...")
            cta_df = pd.read_csv(cta_csv_path, encoding='utf-8')

            for idx, row in cta_df.iterrows():
                data_name = row['表属性名称']

                # 获取候选列表（候选数据元1, 候选数据元2, ...）
                candidates = []
                for col in cta_df.columns:
                    if col.startswith('候选数据元'):
                        candidate = row[col]
                        # 转换为字符串并检查是否有效
                        if pd.notna(candidate):
                            candidate_str = str(candidate).strip()
                            if candidate_str and candidate_str != 'nan':
                                candidates.append(candidate_str)

                if not candidates:
                    logger.warning(f"  {data_name}: 无候选，跳过")
                    continue

                logger.info(f"  处理 CTA: {data_name}")
                logger.debug(f"    候选: {candidates}")

                # 使用 LLM 从候选中选择（简化版：取候选1，实际应该用 LLM）
                # TODO: 如果需要，可以调用 get_column_type_with_llm
                best_match = candidates[0]  # 暂时取第一个候选（分数最高）

                cta_results.append({
                    'subdomain_data': data_name,
                    'data_element': best_match
                })
                logger.info(f"    ✓ 映射到: {best_match}")

            # ========== 2. 处理 CEA 映射表 ==========
            logger.info("\n处理 CEA 映射表...")
            cea_df = pd.read_csv(cea_csv_path, encoding='utf-8')

            for idx, row in cea_df.iterrows():
                data_value = row['表属性值']
                data_name = row['所属表属性']

                # 获取候选列表（候选可允许值1, 候选可允许值2, ...）
                candidates = []
                for col in cea_df.columns:
                    if col.startswith('候选可允许值'):
                        candidate = row[col]
                        # 转换为字符串并检查是否有效
                        if pd.notna(candidate):
                            candidate_str = str(candidate).strip()
                            if candidate_str and candidate_str != 'nan':
                                candidates.append(candidate_str)

                if not candidates:
                    logger.debug(f"  {data_value} ({data_name}): 无候选，跳过")
                    continue

                logger.debug(f"  处理 CEA: {data_value} ({data_name})")
                logger.debug(f"    候选: {candidates}")

                # 使用 LLM 从候选中选择（简化版：取候选1）
                # TODO: 如果需要，可以调用 get_cell_entity_with_llm
                best_match = candidates[0]  # 暂时取第一个候选（分数最高）

                cea_results.append({
                    'subdomain_value': data_value,
                    'subdomain_data': data_name,
                    'mdr_value': best_match
                })
                logger.debug(f"    ✓ 映射到: {best_match}")

            logger.info(f"\n✓ CTA 映射: {len(cta_results)} 个")
            logger.info(f"✓ CEA 映射: {len(cea_results)} 个")

            return {
                'status': 'success',
                'cta_results': cta_results,
                'cea_results': cea_results,
                'cta_count': len(cta_results),
                'cea_count': len(cea_results)
            }

        except Exception as e:
            logger.error(f"处理映射表失败: {str(e)}")
            import traceback
            traceback.print_exc()
            return {
                'status': 'failed',
                'error': str(e)
            }
    def run_complete_mapping(self, subdomain_name: str = "子域1") -> Dict:
        """执行完整的映射流程（方案 B）"""
        try:
            logger.info(f"\n{'='*80}")
            logger.info(f"开始 MDR 映射流程: {subdomain_name}")
            logger.info(f"{'='*80}\n")

            # 1. 导出子域数据，生成 CTA 和 CEA 映射表（存到 data 文件夹）
            data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
            os.makedirs(data_dir, exist_ok=True)

            logger.info("步骤 1/3: 导出子域数据并生成 CTA/CEA 映射表")
            cta_csv_path, cea_csv_path = self.export_subdomain_for_mapping(subdomain_name, data_dir)

            if not cta_csv_path or not cea_csv_path:
                return {'status': 'failed', 'error': 'Failed to export subdomain data'}

            logger.info(f"✓ CTA 映射表: {cta_csv_path}")
            logger.info(f"✓ CEA 映射表: {cea_csv_path}")

            # 2. 执行 CTA 和 CEA（使用 LLM 从候选中选择）
            logger.info("\n步骤 2/3: 使用 LLM 执行 CTA 和 CEA 映射")
            mapping_result = self.process_mapping_tables(cta_csv_path, cea_csv_path)

            if mapping_result['status'] != 'success':
                return mapping_result

            # 3. 将结果写入 Neo4j
            logger.info("\n步骤 3/3: 将映射结果写入 Neo4j")
            mapping_count = self.create_mappings_in_neo4j(
                mapping_result['cta_results'],
                mapping_result['cea_results']
            )

            logger.info(f"\n{'='*80}")
            logger.info(f"✓ MDR 映射完成！")
            logger.info(f"  - CTA (列类型): {mapping_result['cta_count']} 个")
            logger.info(f"  - CEA (单元格实体): {mapping_result['cea_count']} 个")
            logger.info(f"  - 总映射关系: {mapping_count} 个")
            logger.info(f"{'='*80}\n")

            return {
                'status': 'success',
                'total_mappings': mapping_count,
                'cta_count': mapping_result['cta_count'],
                'cea_count': mapping_result['cea_count']
            }

        except Exception as e:
            logger.error(f"MDR 映射流程失败: {str(e)}")
            import traceback
            traceback.print_exc()
            return {'status': 'failed', 'error': str(e)}


# 便捷函数
def run_mdr_mapping(subdomain_name: str = "子域1") -> Dict:
    """执行 MDR 映射的便捷函数"""
    mapper = MDRBasedMapper()
    return mapper.run_complete_mapping(subdomain_name)


if __name__ == "__main__":
    # 测试
    result = run_mdr_mapping("子域1")
    print(f"\n映射结果: {result}")
