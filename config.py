"""
配置文件 - 集中管理所有配置参数
"""
import os
from typing import Optional
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class Config:
    """应用配置类"""

    # DeepSeek API 配置
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_BASE_URL: str = os.getenv("OPENAI_BASE_URL", "https://api.deepseek.com/v1")
    LLM_MODEL: str = os.getenv("LLM_MODEL", "deepseek-chat")

    # Neo4j 数据库配置
    NEO4J_URI: str = os.getenv("NEO4J_URI", "bolt://localhost:7687/")
    NEO4J_USER: str = os.getenv("NEO4J_USER", "neo4j")
    NEO4J_PASSWORD: str = os.getenv("NEO4J_PASSWORD", "")

    # 应用设置
    BATCH_SIZE: int = int(os.getenv("BATCH_SIZE", "1"))
    RETRY_COUNT: int = int(os.getenv("RETRY_COUNT", "3"))
    SLEEP_INTERVAL: float = float(os.getenv("SLEEP_INTERVAL", "0.3"))
    MAX_TOKENS: int = int(os.getenv("MAX_TOKENS", "2000"))
    TEMPERATURE: float = float(os.getenv("TEMPERATURE", "0"))

    # 数据库连接池配置
    DB_MAX_CONNECTION_LIFETIME: int = int(os.getenv("DB_MAX_CONNECTION_LIFETIME", "3600"))
    DB_MAX_CONNECTION_POOL_SIZE: int = int(os.getenv("DB_MAX_CONNECTION_POOL_SIZE", "50"))
    DB_CONNECTION_ACQUISITION_TIMEOUT: int = int(os.getenv("DB_CONNECTION_ACQUISITION_TIMEOUT", "60"))
    DB_MAX_TRANSACTION_RETRY_TIME: int = int(os.getenv("DB_MAX_TRANSACTION_RETRY_TIME", "30"))
    DB_CONNECTION_TIMEOUT: int = int(os.getenv("DB_CONNECTION_TIMEOUT", "30"))

    # 文件路径配置
    # 数据目录
    DATA_DIR: str = os.getenv("DATA_DIR", "../data")

    # 输入数据文件
    SUBDOMAIN_DATA_FILE: str = os.getenv("SUBDOMAIN_DATA_FILE", "../data/sub_domain_data.xlsx")  # 子域数据文件
    SHARED_DOMAIN_FILE: str = os.getenv("SHARED_DOMAIN_FILE", "../data/shared_domain.xlsx")  # 共享域数据文件
    ONTOLOGY_DATA_FILE: str = os.getenv("ONTOLOGY_DATA_FILE", "../data/ontology_data_all.xlsx")  # 本体数据文件
    DOMAIN_OUTPUT_FILE: str = os.getenv("DOMAIN_OUTPUT_FILE", "../data/domain_output.xlsx")  # 域输出文件

    # 输出结果文件
    MAPPING_RESULTS_FILE: str = os.getenv("MAPPING_RESULTS_FILE", "../data/mapping_results.xlsx")  # 映射结果文件

    # 进度跟踪文件
    PROGRESS_FILE: str = os.getenv("PROGRESS_FILE", "registration_progress.json")
    COMPLETED_FILE: str = os.getenv("COMPLETED_FILE", "registration_completed.json")

    # 兼容旧代码
    DATA_FILE_PATH: str = os.getenv("DATA_FILE_PATH", "../data/ontology_data_all.xlsx")

    @classmethod
    def validate_config(cls) -> Optional[str]:
        """
        验证配置是否完整

        Returns:
            如果有错误，返回错误信息；否则返回 None
        """
        if not cls.OPENAI_API_KEY:
            return "OPENAI_API_KEY 未设置，请在 .env 文件中配置"

        if not cls.NEO4J_PASSWORD:
            return "NEO4J_PASSWORD 未设置，请在 .env 文件中配置"

        return None

    @classmethod
    def get_neo4j_config(cls) -> dict:
        """获取 Neo4j 配置"""
        return {
            "uri": cls.NEO4J_URI,
            "user": cls.NEO4J_USER,
            "password": cls.NEO4J_PASSWORD
        }

    @classmethod
    def get_openai_config(cls) -> dict:
        """获取 OpenAI 配置"""
        return {
            "api_key": cls.OPENAI_API_KEY,
            "base_url": cls.OPENAI_BASE_URL,
            "model": cls.LLM_MODEL,
            "temperature": cls.TEMPERATURE,
            "max_tokens": cls.MAX_TOKENS,
            "max_retries": cls.RETRY_COUNT
        }
