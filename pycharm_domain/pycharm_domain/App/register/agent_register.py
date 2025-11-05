"""
智能体自动注册模块
为后端提供智能体批量注册MDR的功能
"""
import os
import sys
from werkzeug.utils import secure_filename

# 添加pe_agents路径
# 从当前文件向上5层到达data_share目录
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
pe_agents_path = os.path.join(project_root, 'pe_agents')
if pe_agents_path not in sys.path:
    sys.path.insert(0, pe_agents_path)

# 导入backend_api
from backend_api import get_agent_api


# 上传文件配置
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'uploads')
ALLOWED_EXTENSIONS = {'xlsx', 'xls'}

# 确保上传目录存在
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


def allowed_file(filename):
    """
    检查文件扩展名是否允许
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def register_mdr_with_agent(file):
    """
    使用智能体批量注册MDR
    :param file: 上传的Excel文件对象
    :return: 注册结果
    """
    try:
        # 检查文件
        if not file:
            return {
                "success": False,
                "message": "未提供文件"
            }

        if file.filename == '':
            return {
                "success": False,
                "message": "文件名为空"
            }

        if not allowed_file(file.filename):
            return {
                "success": False,
                "message": f"不支持的文件类型，仅支持: {', '.join(ALLOWED_EXTENSIONS)}"
            }

        # 保存文件
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        # 调用智能体API进行批量注册
        agent_api = get_agent_api()
        result = agent_api.register_batch(filepath, batch_size=1)

        # 删除临时文件
        try:
            os.remove(filepath)
        except:
            pass

        return result

    except Exception as e:
        return {
            "success": False,
            "message": f"注册过程出错: {str(e)}",
            "error": str(e)
        }


def get_agent_status():
    """
    获取智能体状态
    :return: 状态信息
    """
    return {
        "success": True,
        "status": "online",
        "message": "智能体注册服务运行中"
    }
