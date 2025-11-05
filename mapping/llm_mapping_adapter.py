"""
LLM 增强映射适配器 - 集成 ctaceallm 到完整流程
基于 ReAct Agent 和 DBpedia 的智能语义映射
"""
import os
import sys
import logging
import csv
import tempfile
from typing import Dict, List, Tuple, Optional
import pandas as pd
from py2neo import Graph
from dotenv import load_dotenv

# 添加项目路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 导入配置
from config import Config

# 设置日志
logger = logging.getLogger(__name__)

# 导入 LangChain 相关
try:
    from langchain_openai import ChatOpenAI
    from langchain.tools import Tool
    from langchain.agents import create_react_agent, AgentExecutor, load_tools
    from langchain.prompts import PromptTemplate
    from langchain.schema import HumanMessage
    LANGCHAIN_AVAILABLE = True
except ImportError:
    logger.warning("LangChain 未安装，将使用基础映射功能")
    LANGCHAIN_AVAILABLE = False


class LLMMappingAdapter:
    """LLM 增强映射适配器"""

    def __init__(self):
        """初始化适配器"""
        load_dotenv()

        # 初始化 Neo4j 连接
        neo4j_config = Config.get_neo4j_config()
        self.graph = Graph(neo4j_config["uri"], auth=(neo4j_config["user"], neo4j_config["password"]))

        # 初始化 LLM
        if LANGCHAIN_AVAILABLE:
            openai_config = Config.get_openai_config()
            self.llm = ChatOpenAI(
                model="gpt-3.5-turbo",
                temperature=0.5,
                openai_api_key=openai_config["api_key"],
                openai_api_base=openai_config["base_url"],
                max_retries=openai_config["max_retries"]
            )
            self._init_agent()
        else:
            self.llm = None
            logger.warning("LLM 未初始化，将使用基础映射")

        logger.info("LLM 映射适配器初始化完成")

    def _init_agent(self):
        """初始化 ReAct Agent"""
        try:
            # 定义列类型注释工具 (CTA)
            def get_column_type(column_values: str) -> str:
                """获取列的 DBpedia Ontology 类型"""
                prompt = f"""
                You are a data expert. Given a list of column values, determine the semantic type.
                Return only the DBpedia ontology URL (e.g., http://dbpedia.org/ontology/Person).

                Column values: {column_values}
                """
                response = self.llm([HumanMessage(content=prompt)])
                return response.content.strip()

            # 定义单元格实体注释工具 (CEA)
            def get_cell_entity(cell_value: str, column_type: str) -> str:
                """获取单元格的 DBpedia 实体"""
                prompt = f"""
                You are a data expert. Given a cell value and its column type, find the best matching entity.
                Return only the DBpedia resource URL (e.g., http://dbpedia.org/resource/Albert_Einstein).

                Cell value: {cell_value}
                Column type: {column_type}
                """
                response = self.llm([HumanMessage(content=prompt)])
                return response.content.strip()

            # 创建工具
            column_type_tool = Tool(
                name="GetColumnType",
                func=get_column_type,
                description="Get DBpedia ontology type for a column based on its values"
            )

            cell_entity_tool = Tool(
                name="GetCellEntity",
                func=get_cell_entity,
                description="Get DBpedia entity for a cell value given its column type"
            )

            # 加载基础工具
            base_tools = load_tools(["llm-math"], llm=self.llm)
            self.tools = base_tools + [column_type_tool, cell_entity_tool]

            # 创建 ReAct Agent
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
                verbose=True
            )

            logger.info("ReAct Agent 初始化成功")

        except Exception as e:
            logger.error(f"Agent 初始化失败: {str(e)}")
            self.agent_executor = None

    def export_subdomain_to_csv(self, subdomain_name: str, output_path: str) -> bool:
        """
        将子域数据从 Neo4j 导出到 CSV 文件

        Args:
            subdomain_name: 子域名称
            output_path: 输出 CSV 文件路径

        Returns:
            是否成功导出
        """
        try:
            # 查询子域数据
            query = """
            MATCH (s:子域 {name: $subdomain_name})-[:包含]->(d:数据)
            OPTIONAL MATCH (d)-[:包含值]->(v:数据值)
            RETURN d.value as data_name, collect(v.value) as data_values
            ORDER BY data_name
            """

            result = self.graph.run(query, subdomain_name=subdomain_name).data()

            if not result:
                logger.warning(f"未找到子域 '{subdomain_name}' 的数据")
                return False

            # 写入 CSV 文件
            with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)

                # 写入表头
                headers = [row['data_name'] for row in result]
                writer.writerow(headers)

                # 写入数据值
                max_rows = max(len(row['data_values']) for row in result)
                for i in range(max_rows):
                    row_data = []
                    for col_data in result:
                        values = col_data['data_values']
                        if i < len(values):
                            row_data.append(values[i])
                        else:
                            row_data.append('')
                    writer.writerow(row_data)

            logger.info(f"✓ 子域数据已导出到: {output_path}")
            return True

        except Exception as e:
            logger.error(f"导出子域数据失败: {str(e)}")
            return False

    def perform_llm_mapping(self, csv_file_path: str) -> Dict:
        """
        使用 LLM Agent 执行映射

        Args:
            csv_file_path: CSV 文件路径

        Returns:
            映射结果统计
        """
        if not LANGCHAIN_AVAILABLE or not self.agent_executor:
            logger.warning("LLM Agent 不可用，跳过 LLM 映射")
            return {'status': 'skipped', 'reason': 'LLM not available'}

        try:
            logger.info("开始 LLM 映射...")

            # 读取 CSV 文件
            df = pd.read_csv(csv_file_path, encoding='utf-8', errors='ignore')
            logger.info(f"读取到 {len(df.columns)} 列数据")

            cta_results = []  # 列类型注释结果
            cea_results = []  # 单元格实体注释结果

            # 对每一列进行 CTA
            for col_idx, column in enumerate(df.columns):
                column_values = df[column].dropna().head(10).tolist()

                if not column_values:
                    continue

                logger.info(f"处理列 {col_idx}: {column}")

                # 使用 Agent 获取列类型
                try:
                    response = self.agent_executor.invoke({
                        "input": f"What is the DBpedia ontology type for a column with these values: {column_values}? Give only the URL."
                    })

                    column_type = response.get('output', '')
                    cta_results.append({
                        'column_index': col_idx,
                        'column_name': column,
                        'column_type': column_type
                    })

                    logger.info(f"✓ 列类型: {column_type}")

                    # 对该列的前几个单元格进行 CEA
                    for row_idx, value in enumerate(column_values[:5]):
                        if pd.notna(value) and str(value).strip():
                            try:
                                cea_response = self.agent_executor.invoke({
                                    "input": f"What is the DBpedia entity for '{value}' of type {column_type}? Give only the URL."
                                })

                                entity_url = cea_response.get('output', '')
                                cea_results.append({
                                    'row_index': row_idx,
                                    'column_index': col_idx,
                                    'cell_value': value,
                                    'entity_url': entity_url
                                })

                                logger.debug(f"  ✓ 单元格 ({row_idx}, {col_idx}): {entity_url}")

                            except Exception as e:
                                logger.warning(f"CEA 失败: {str(e)}")

                except Exception as e:
                    logger.warning(f"CTA 失败: {str(e)}")

            return {
                'status': 'success',
                'cta_count': len(cta_results),
                'cea_count': len(cea_results),
                'cta_results': cta_results,
                'cea_results': cea_results
            }

        except Exception as e:
            logger.error(f"LLM 映射失败: {str(e)}")
            return {'status': 'failed', 'error': str(e)}

    def create_mappings_in_neo4j(self, cta_results: List[Dict], cea_results: List[Dict], subdomain_name: str) -> int:
        """
        将映射结果写入 Neo4j

        Args:
            cta_results: 列类型注释结果
            cea_results: 单元格实体注释结果
            subdomain_name: 子域名称

        Returns:
            创建的映射关系数量
        """
        mapping_count = 0

        try:
            # 创建列类型映射 (CTA)
            for cta in cta_results:
                column_name = cta['column_name']
                column_type = cta['column_type']

                if not column_type or 'dbpedia' not in column_type.lower():
                    continue

                # 查找对应的数据元
                query = """
                MATCH (sub:数据 {value: $column_name})
                MATCH (de:DataElement)
                WHERE de.name CONTAINS $column_name OR $column_name CONTAINS de.name
                MERGE (sub)-[r:MAPPED_TO]->(de)
                SET r.column_type = $column_type,
                    r.mapping_method = 'LLM_CTA',
                    r.confidence = 0.8
                RETURN count(r) as count
                """

                result = self.graph.run(query, {
                    'column_name': column_name,
                    'column_type': column_type
                }).data()

                if result and result[0]['count'] > 0:
                    mapping_count += result[0]['count']
                    logger.debug(f"✓ CTA映射: {column_name} → {column_type}")

            # 创建单元格实体映射 (CEA)
            for cea in cea_results:
                cell_value = cea['cell_value']
                entity_url = cea['entity_url']

                if not entity_url or 'dbpedia' not in entity_url.lower():
                    continue

                # 查找对应的数据值和值域
                query = """
                MATCH (subv:数据值 {value: $cell_value})
                MATCH (v:Value)
                WHERE v.name CONTAINS $cell_value OR $cell_value CONTAINS v.name
                MERGE (subv)-[r:MAPPED_TO]->(v)
                SET r.entity_url = $entity_url,
                    r.mapping_method = 'LLM_CEA',
                    r.confidence = 0.8
                RETURN count(r) as count
                """

                result = self.graph.run(query, {
                    'cell_value': str(cell_value),
                    'entity_url': entity_url
                }).data()

                if result and result[0]['count'] > 0:
                    mapping_count += result[0]['count']
                    logger.debug(f"✓ CEA映射: {cell_value} → {entity_url}")

            logger.info(f"✓ 创建了 {mapping_count} 个映射关系")
            return mapping_count

        except Exception as e:
            logger.error(f"创建映射关系失败: {str(e)}")
            return mapping_count

    def run_complete_mapping(self, subdomain_name: str = "子域1") -> Dict:
        """
        执行完整的 LLM 映射流程

        Args:
            subdomain_name: 子域名称

        Returns:
            映射结果
        """
        try:
            logger.info(f"开始 LLM 映射流程: {subdomain_name}")

            # 1. 导出子域数据到临时 CSV
            with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as tmp_file:
                csv_path = tmp_file.name

            success = self.export_subdomain_to_csv(subdomain_name, csv_path)
            if not success:
                return {'status': 'failed', 'error': 'Failed to export subdomain data'}

            # 2. 执行 LLM 映射
            mapping_result = self.perform_llm_mapping(csv_path)

            if mapping_result['status'] != 'success':
                return mapping_result

            # 3. 将结果写入 Neo4j
            mapping_count = self.create_mappings_in_neo4j(
                mapping_result['cta_results'],
                mapping_result['cea_results'],
                subdomain_name
            )

            # 清理临时文件
            try:
                os.unlink(csv_path)
            except:
                pass

            logger.info(f"✓ LLM 映射完成: 创建 {mapping_count} 个映射关系")

            return {
                'status': 'success',
                'total_mappings': mapping_count,
                'cta_count': mapping_result['cta_count'],
                'cea_count': mapping_result['cea_count']
            }

        except Exception as e:
            logger.error(f"LLM 映射流程失败: {str(e)}")
            return {'status': 'failed', 'error': str(e)}


# 便捷函数
def run_llm_mapping(subdomain_name: str = "子域1") -> Dict:
    """
    执行 LLM 增强映射的便捷函数

    Args:
        subdomain_name: 子域名称

    Returns:
        映射结果
    """
    adapter = LLMMappingAdapter()
    return adapter.run_complete_mapping(subdomain_name)


if __name__ == "__main__":
    # 配置日志
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # 执行映射
    result = run_llm_mapping("子域1")
    print(f"\n映射结果: {result}")
