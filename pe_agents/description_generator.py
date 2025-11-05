"""
智能描述生成器
使用LLM为MDR节点生成丰富、语义化的描述信息
"""
import os
from typing import Optional, Dict, Any
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from dotenv import load_dotenv

load_dotenv()


class DescriptionGenerator:
    """
    使用LLM生成MDR节点的智能描述
    """

    def __init__(self):
        """初始化LLM"""
        self.llm = ChatOpenAI(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            temperature=float(os.getenv("OPENAI_TEMPERATURE", "0.7")),
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            openai_api_base=os.getenv("OPENAI_BASE_URL"),
            max_retries=int(os.getenv("OPENAI_MAX_RETRIES", "3")),
            max_tokens=int(os.getenv("OPENAI_MAX_TOKENS", "500"))
        )

    def generate_object_class_description(self, object_class: str, context: Optional[Dict] = None) -> str:
        """
        生成对象类的智能描述

        Args:
            object_class: 对象类名称
            context: 上下文信息（可选）

        Returns:
            生成的描述文本
        """
        system_prompt = """你是一个专业的数据治理专家，擅长ISO/IEC 11179元数据注册标准。
你的任务是为对象类生成简洁、专业、语义丰富的描述。

描述要求：
1. 简洁明了（1-2句话，不超过100字）
2. 说明对象类代表的实体类型和业务含义
3. 突出其在数据模型中的作用
4. 使用专业术语但保持易懂
5. 不要使用"表示...的对象类"这样模板化的开头"""

        user_prompt = f"""请为以下对象类生成专业描述：

对象类名称：{object_class}

{f"上下文信息：{context}" if context else ""}

请直接给出描述文本，不要包含其他说明。"""

        try:
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt)
            ]
            response = self.llm(messages)
            description = response.content.strip()

            # 如果生成失败或太短，使用默认模板
            if not description or len(description) < 10:
                return f"表示{object_class}的对象类，用于数据元的分类和组织"

            return description
        except Exception as e:
            print(f"生成描述失败，使用默认模板: {str(e)}")
            return f"表示{object_class}的对象类，用于数据元的分类和组织"

    def generate_property_description(self, property_name: str, object_class: Optional[str] = None) -> str:
        """
        生成属性的智能描述

        Args:
            property_name: 属性名称
            object_class: 关联的对象类（可选）

        Returns:
            生成的描述文本
        """
        system_prompt = """你是一个专业的数据治理专家，擅长ISO/IEC 11179元数据注册标准。
你的任务是为属性生成简洁、专业、语义丰富的描述。

描述要求：
1. 简洁明了（1-2句话，不超过100字）
2. 说明属性的业务含义和用途
3. 如果知道对象类，说明该属性描述了对象的哪个方面
4. 使用专业术语但保持易懂
5. 不要使用"...属性，用于描述对象的特征"这样模板化的表达"""

        user_prompt = f"""请为以下属性生成专业描述：

属性名称：{property_name}
{f"所属对象类：{object_class}" if object_class else ""}

请直接给出描述文本，不要包含其他说明。"""

        try:
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt)
            ]
            response = self.llm(messages)
            description = response.content.strip()

            if not description or len(description) < 10:
                return f"{property_name}属性，用于描述对象的特征"

            return description
        except Exception as e:
            print(f"生成描述失败，使用默认模板: {str(e)}")
            return f"{property_name}属性，用于描述对象的特征"

    def generate_concept_domain_description(
        self,
        concept_domain: str,
        property_name: Optional[str] = None,
        value_meanings: Optional[list] = None
    ) -> str:
        """
        生成概念域的智能描述

        Args:
            concept_domain: 概念域名称
            property_name: 关联的属性名（可选）
            value_meanings: 值含义列表（可选）

        Returns:
            生成的描述文本
        """
        system_prompt = """你是一个专业的数据治理专家，擅长ISO/IEC 11179元数据注册标准。
你的任务是为概念域生成简洁、专业、语义丰富的描述。

描述要求：
1. 简洁明了（1-2句话，不超过120字）
2. 说明概念域定义的语义范围和业务含义
3. 如果有值含义信息，可以举例说明包含的值类型
4. 使用专业术语但保持易懂
5. 不要使用"...的概念域，定义了属性值的语义范围"这样模板化的表达"""

        value_info = ""
        if value_meanings and len(value_meanings) > 0:
            value_info = f"\n可能的值类型：{', '.join(value_meanings[:5])}{' 等' if len(value_meanings) > 5 else ''}"

        user_prompt = f"""请为以下概念域生成专业描述：

概念域名称：{concept_domain}
{f"关联属性：{property_name}" if property_name else ""}
{value_info}

请直接给出描述文本，不要包含其他说明。"""

        try:
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt)
            ]
            response = self.llm(messages)
            description = response.content.strip()

            if not description or len(description) < 10:
                return f"{concept_domain}的概念域，定义了属性值的语义范围"

            return description
        except Exception as e:
            print(f"生成描述失败，使用默认模板: {str(e)}")
            return f"{concept_domain}的概念域，定义了属性值的语义范围"

    def generate_data_element_concept_description(
        self,
        object_class: str,
        property_name: str,
        concept_domain: Optional[str] = None
    ) -> str:
        """
        生成数据元概念的智能描述

        Args:
            object_class: 对象类名称
            property_name: 属性名称
            concept_domain: 概念域名称（可选）

        Returns:
            生成的描述文本
        """
        system_prompt = """你是一个专业的数据治理专家，擅长ISO/IEC 11179元数据注册标准。
你的任务是为数据元概念生成简洁、专业、语义丰富的描述。

描述要求：
1. 简洁明了（1-2句话，不超过120字）
2. 说明数据元概念的业务含义，体现"对象类+属性"的组合语义
3. 强调在实际业务中的应用场景或作用
4. 使用专业术语但保持易懂
5. 不要使用"数据元概念，表示...的...特性"这样模板化的表达"""

        user_prompt = f"""请为以下数据元概念生成专业描述：

对象类：{object_class}
属性：{property_name}
{f"概念域：{concept_domain}" if concept_domain else ""}

数据元概念名称：{object_class}{property_name}

请直接给出描述文本，不要包含其他说明。"""

        try:
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt)
            ]
            response = self.llm(messages)
            description = response.content.strip()

            if not description or len(description) < 10:
                return f"数据元概念，表示{object_class}的{property_name}特性"

            return description
        except Exception as e:
            print(f"生成描述失败，使用默认模板: {str(e)}")
            return f"数据元概念，表示{object_class}的{property_name}特性"

    def generate_value_domain_description(
        self,
        value_domain: str,
        concept_domain: Optional[str] = None,
        has_enumeration: bool = False,
        value_examples: Optional[list] = None
    ) -> str:
        """
        生成值域的智能描述

        Args:
            value_domain: 值域名称
            concept_domain: 概念域名称（可选）
            has_enumeration: 是否有可枚举值
            value_examples: 值示例列表（可选）

        Returns:
            生成的描述文本
        """
        system_prompt = """你是一个专业的数据治理专家，擅长ISO/IEC 11179元数据注册标准。
你的任务是为值域生成简洁、专业、语义丰富的描述。

描述要求：
1. 简洁明了（1-2句话，不超过120字）
2. 说明值域定义的数据类型和取值范围
3. 区分可枚举值域和不可枚举值域
4. 如果有具体值，可以举例说明
5. 使用专业术语但保持易懂
6. 不要使用"...值域，定义了...的可允许值"这样模板化的表达"""

        enum_info = "可枚举" if has_enumeration else "不可枚举"
        value_info = ""
        if value_examples and len(value_examples) > 0:
            value_info = f"\n示例值：{', '.join(value_examples[:5])}{' 等' if len(value_examples) > 5 else ''}"

        user_prompt = f"""请为以下值域生成专业描述：

值域名称：{value_domain}
{f"概念域：{concept_domain}" if concept_domain else ""}
值域类型：{enum_info}
{value_info}

请直接给出描述文本，不要包含其他说明。"""

        try:
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt)
            ]
            response = self.llm(messages)
            description = response.content.strip()

            if not description or len(description) < 10:
                enum_suffix = "（可枚举）" if has_enumeration else "（不可枚举）"
                return f"{value_domain}值域，定义了{concept_domain if concept_domain else '数据'}的可允许值{enum_suffix}"

            return description
        except Exception as e:
            print(f"生成描述失败，使用默认模板: {str(e)}")
            enum_suffix = "（可枚举）" if has_enumeration else "（不可枚举）"
            return f"{value_domain}值域，定义了{concept_domain if concept_domain else '数据'}的可允许值{enum_suffix}"

    def generate_data_element_description(
        self,
        data_element: str,
        object_class: str,
        property_name: str,
        value_domain: Optional[str] = None
    ) -> str:
        """
        生成数据元的智能描述

        Args:
            data_element: 数据元名称
            object_class: 对象类名称
            property_name: 属性名称
            value_domain: 值域名称（可选）

        Returns:
            生成的描述文本
        """
        system_prompt = """你是一个专业的数据治理专家，擅长ISO/IEC 11179元数据注册标准。
你的任务是为数据元生成简洁、专业、语义丰富的描述。

描述要求：
1. 简洁明了（1-2句话，不超过150字）
2. 说明数据元的完整业务含义和技术定义
3. 体现"对象类+属性+值域"的完整语义
4. 强调在数据交换和共享中的作用
5. 使用专业术语但保持易懂
6. 不要使用"数据元，基于...和...的完整数据定义"这样模板化的表达"""

        user_prompt = f"""请为以下数据元生成专业描述：

数据元名称：{data_element}
对象类：{object_class}
属性：{property_name}
{f"值域：{value_domain}" if value_domain else ""}

请直接给出描述文本，不要包含其他说明。"""

        try:
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt)
            ]
            response = self.llm(messages)
            description = response.content.strip()

            if not description or len(description) < 10:
                return f"数据元，定义了{object_class}的{property_name}的完整数据规范"

            return description
        except Exception as e:
            print(f"生成描述失败，使用默认模板: {str(e)}")
            return f"数据元，定义了{object_class}的{property_name}的完整数据规范"


# 单例模式
_generator = None

def get_description_generator() -> DescriptionGenerator:
    """获取描述生成器实例"""
    global _generator
    if _generator is None:
        _generator = DescriptionGenerator()
    return _generator
