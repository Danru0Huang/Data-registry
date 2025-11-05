"""
智能体后端调用接口
为Flask后端提供简单的函数调用接口
"""
import os
import sys
import pandas as pd
from typing import Dict, List, Tuple, Any

# 添加项目路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from pe_agents.tools_backend_compatible import (
    register_object_class,
    register_property,
    register_concept_domain,
    register_data_element_concept_with_relationships,
    register_value_domain_with_values,
    register_value_domain_with_relationship,
    register_value_meanings_with_relationship,
    register_data_element_with_relationships,
)


class AgentRegisterAPI:
    """
    智能体注册API
    为后端提供统一的注册接口
    """

    def __init__(self):
        """初始化"""
        self.success_count = 0
        self.error_count = 0
        self.skip_count = 0
        self.errors = []

    def parse_excel_data(self, file_path: str) -> Dict[str, Dict[str, Any]]:
        """
        解析Excel数据
        :param file_path: Excel文件路径
        :return: 分组后的数据 {本体类: {属性: {value_str, meaning_str}}}
        """
        try:
            df = pd.read_excel(file_path)

            # 修复列名（处理编码问题）
            if len(df.columns) == 8:
                # 8列格式
                expected_columns = ['本体类', '属性', '值', '值含义', '代码', '数据类型', '属性描述', '来源文件']
                df.columns = expected_columns
            elif len(df.columns) == 4:
                # 4列格式
                expected_columns = ['本体类', '属性', '值', '值含义']
                df.columns = expected_columns
            else:
                raise ValueError(f"Excel列数不正确，期望4列或8列，实际{len(df.columns)}列")

            # 分组数据
            grouped_data = {}
            for _, row in df.iterrows():
                ontology_class = row["本体类"]
                attribute = row["属性"]
                value_str = row.get("值", "")
                meaning_str = row.get("值含义", "")

                # 处理空值
                if pd.isna(value_str) or value_str == "nan" or value_str == "null":
                    value_str = ""
                if pd.isna(meaning_str) or meaning_str == "nan" or meaning_str == "null":
                    meaning_str = ""

                if ontology_class not in grouped_data:
                    grouped_data[ontology_class] = {}

                grouped_data[ontology_class][attribute] = {
                    "value_str": value_str,
                    "meaning_str": meaning_str
                }

            return grouped_data

        except Exception as e:
            raise Exception(f"解析Excel文件失败: {str(e)}")

    def register_single_mdr(self, ontology_class: str, attribute: str,
                           value_str: str = "", meaning_str: str = "") -> Dict[str, Any]:
        """
        注册单个MDR数据
        :param ontology_class: 本体类
        :param attribute: 属性
        :param value_str: 值（可选）
        :param meaning_str: 值含义（可选）
        :return: 注册结果
        """
        result = {
            "success": False,
            "steps": [],
            "error": None
        }

        try:
            # 1. 注册对象类
            step1 = register_object_class.invoke({"object_class": ontology_class})
            result["steps"].append({"step": "对象类", "result": step1})

            # 2. 注册属性
            step2 = register_property.invoke({"property": attribute})
            result["steps"].append({"step": "属性", "result": step2})

            # 3. 注册概念域（使用属性名）
            concept_domain = attribute
            step3 = register_concept_domain.invoke({"concept_domain": concept_domain})
            result["steps"].append({"step": "概念域", "result": step3})

            # 4. 注册数据元概念
            data_element_concept = f"{ontology_class}{attribute}"
            step4 = register_data_element_concept_with_relationships.invoke({
                "data_element_concept": data_element_concept,
                "object_class": ontology_class,
                "property": attribute,
                "concept_domain": concept_domain
            })
            result["steps"].append({"step": "数据元概念", "result": step4})

            # 5. 注册值域
            value_domain = attribute
            if value_str and value_str.strip():
                # 先注册值含义（如果有），然后注册值域、值域组、可允许值
                if meaning_str and meaning_str.strip():
                    step5a = register_value_meanings_with_relationship.invoke({
                        "concept_domain": concept_domain,
                        "value_str": value_str,
                        "meaning_str": meaning_str
                    })
                    result["steps"].append({"step": "值含义", "result": step5a})

                # 有值，注册值域和值（包括值域组、可允许值，并关联值含义）
                step5 = register_value_domain_with_values.invoke({
                    "value_domain": value_domain,
                    "concept_domain": concept_domain,
                    "value_str": value_str,
                    "meaning_str": meaning_str if meaning_str else ""
                })
                result["steps"].append({"step": "值域(带值)", "result": step5})
            else:
                # 无值，仅注册值域
                step5 = register_value_domain_with_relationship.invoke({
                    "value_domain": value_domain,
                    "concept_domain": concept_domain
                })
                result["steps"].append({"step": "值域(无值)", "result": step5})

            # 7. 注册数据元
            data_element = f"DE{ontology_class}{attribute}"
            step7 = register_data_element_with_relationships.invoke({
                "data_element": data_element,
                "data_element_concept": data_element_concept,
                "value_domain": value_domain
            })
            result["steps"].append({"step": "数据元", "result": step7})

            result["success"] = True
            self.success_count += 1
            print(f"[SUCCESS] 注册成功 [{ontology_class}] {attribute}")

        except Exception as e:
            error_msg = f"{type(e).__name__}: {str(e)}"
            result["error"] = error_msg
            self.error_count += 1
            self.errors.append({
                "ontology_class": ontology_class,
                "attribute": attribute,
                "error": error_msg
            })
            # 打印详细错误信息用于调试
            print(f"[ERROR] 注册失败 [{ontology_class}] {attribute}: {error_msg}")
            import traceback
            traceback.print_exc()

        return result

    def register_batch(self, file_path: str, batch_size: int = 1) -> Dict[str, Any]:
        """
        批量注册MDR
        :param file_path: Excel文件路径
        :param batch_size: 批次大小
        :return: 注册结果统计
        """
        # 重置计数器
        self.success_count = 0
        self.error_count = 0
        self.skip_count = 0
        self.errors = []

        try:
            # 解析Excel数据
            grouped_data = self.parse_excel_data(file_path)

            total_count = sum(len(attributes) for attributes in grouped_data.values())
            processed_count = 0

            # 批量注册
            for ontology_class, attributes in grouped_data.items():
                for attribute, details in attributes.items():
                    # 注册单个MDR
                    self.register_single_mdr(
                        ontology_class,
                        attribute,
                        details.get("value_str", ""),
                        details.get("meaning_str", "")
                    )

                    processed_count += 1

            # 返回统计结果
            return {
                "success": True,
                "total": total_count,
                "success_count": self.success_count,
                "error_count": self.error_count,
                "skip_count": self.skip_count,
                "errors": self.errors[:10],  # 只返回前10个错误
                "message": f"注册完成：成功{self.success_count}条，失败{self.error_count}条"
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": f"批量注册失败: {str(e)}"
            }


# 单例模式
_agent_api = None

def get_agent_api() -> AgentRegisterAPI:
    """获取智能体API实例"""
    global _agent_api
    if _agent_api is None:
        _agent_api = AgentRegisterAPI()
    return _agent_api
