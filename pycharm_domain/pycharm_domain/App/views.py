import json

from flask import Blueprint, render_template, request, jsonify
from werkzeug.utils import secure_filename

# 以下废弃
# from .search.search import query, get_node_message
# 以下代码完成的功能为：当前端生成图谱时，点击该图谱的某节点会调用此函数查询该节点的信息，并在前端以对话框的形式展示
# 暂时废弃，后续引入该功能时可以参考
# from .search.search1 import get_mdr_object_class_node_info

# 本文文件用于完成系统的路由接收，并引入相关文件的函数完成功能
# 代码将安装三部分存放，分别为信息模型、MDR、子域（MFI）
# 每一部分又将分为三个模块存放：页面 注册 查询
# 页面：返回对应的页面
# 注册：完成各部分的注册功能，即每一部分对数据库的写入操作，该部分的路由规范为/register/()/methods
#   /register -> 表示该功能为注册功能，将由register目录下的对应py文件完成
#   () -> 本次要注册的部分，取值为model/mdr/subDomain,分别表示对信息模型、MDR以及子域的注册操作
#   methods -> 本次要注册的内容
# 查询：完成对各部分的查询功能，即每一部分对数据库的读操作，该部分的路由规范为/search/()/methods
#   /search -> 表示该功能为查询功能，将由search目录下对应的py文件完成
#   () -> 本次要查询的部分，取值为model/mdr/subDomain,分别表示对信息模型、MDR以及子域的查询操作
#   methods -> 本次要查询的内容

# 后续补充新功能请遵循上述规范，方便代码逻辑梳理

# 导入配置
from .config import graph

# 信息模型/注册
from .register.information_model import add_property_of_name, add_class_of_name, add_relation_info, add_model_info, \
    register_model_of_file
# 信息模型/查询
from .search.search_information_model import get_model_class_name_options_list, get_model_type_options_list, \
    query_graph_of_model, get_all_class_number, get_sub_domain_lists, get_sub_domain_table_relations, \
    get_class_name_and_property_name_options_list
# 信息模型/演化
from .evolution.evolution_information_model import delete_property_of_name_info
# mdr/注册
from .register.register_mdr import register_object_class, register_property, register_conceptual_domain, \
    register_data_element_concept, register_mdr_value_domain_list, register_data_element
# mdr/智能体注册
from .register.agent_register import register_mdr_with_agent, get_agent_status
# mdr/查询
from .search.search_mdr import get_object_class_option_list, get_property_option_list, \
    get_conceptual_domain_option_list, get_value_meanings_option_list, get_data_element_concept_option_list, \
    get_value_domain_option_list, get_data_element_option_list, get_value_domain_and_permissible_values_option_list, \
    get_mdr_table_list_info, get_mdr_table_info, get_graph_of_mdr_info
# mdr/演化
from .evolution.evolution_mdr import update_mdr_info, add_value_meanings_info, add_permissible_values_info
# 子域/注册
from .register.register_sub_domain import add_sub_domain_info, register_sub_domain_of_file, \
    add_relation_between_table_and_sub_domain_info, add_relation_between_attribute_and_data_element_info, \
    add_relation_between_attribute_and_value_domain_info, \
    add_relation_between_attribute_value_and_permissible_values_info
# 子域/查询
from .search.search_sub_domain import get_sub_domain_options_list, get_graph_of_table_info, \
    get_sub_domain_and_table_options_list, get_mdr_table_through_sub_domain_info, get_sub_domain_properties_list, \
    get_graph_of_attribute_info, get_sub_domain_table_options_list, get_sub_domain_exist_attribute_value_options_list
# 子域/演化
from .evolution.evolution_sub_domain import delete_attribute_value_info, delete_attribute_info, delete_table_info, \
    update_sub_domain_info
# 子域/自动映射
import sys
import os
# 添加mapping模块路径
mapping_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))), 'mapping')
if mapping_path not in sys.path:
    sys.path.insert(0, mapping_path)
# 用户
from .user.user import get_model_and_model_class_options_list, get_data_element_of_model_class_options_list, \
    get_data_share_info_json, get_model_evolution_info_json, get_sub_domain_evolution_info_json, \
    get_model_evolution_tables_list, get_sub_domain_evolution_tables_list, \
    get_data_element_identifier_info_through_object_class_and_property
# 首页信息
from .index.index import get_graph_index_info, get_index_sub_domain_info

# 蓝图
blue = Blueprint('graph', __name__)


# 系统首页
@blue.route('/')
def index():
    return render_template("index.html")


# 数据可视化展示页面
@blue.route('/index2')
def index2():
    return render_template("index2.html")


@blue.route('/index_show')
def index_show():
    data = get_all_class_number()
    return jsonify({"message": data})


# 往下的注释的页面和功能为曾经为完成功能新建的测试，由于之前逻辑过于混乱，现废弃

# @blue.route('/register', methods=['GET', 'POST'])
# def register():
#     return render_template("register.html")


# @blue.route('/search', methods=['GET', 'POST'])
# def search():
#     return render_template("search.html")


# @blue.route('/information_model', methods=['GET', 'POST'])
# def information_model():
#     return render_template("information_model.html")


# @blue.route('/ontologysearch', methods=['GET', 'POST'])
# def ontologyreasch():
#     return render_template("ontologysearch.html")


# @blue.route('/test')
# def test():
#     return render_template("test.html")


# @blue.route('/search_name', methods=['GET', 'POST'])
# def search_name():
#     name = request.args.get('name')
#     label = request.args.get('label')
#     json_data = query(str(name), str(label))
#     return jsonify(json_data)


# @blue.route('/search_node', methods=['GET', 'POST'])
# def search_node():
#     name = request.args.get('name')
#     category = request.args.get('category')
#     data = get_node_message(category, name)
#     return jsonify(data)


# @blue.route('/register_model_class', methods=['GET', 'POST'])
# def register_model_class():
#     model_name = request.json.get("model_name")
#     class_name = request.json.get("class_name")
#     data = register_class(model_name, class_name)
#     return jsonify({'message': data})


# @blue.route('/register_model_property', methods=['GET', 'POST'])
# def register_model_property():
#     class_name = request.json.get('class_name')
#     property_names = request.json.get('properties')
#     data = register_property(class_name, property_names)
#     return jsonify({"message": data})


# @blue.route("/register_model_relation", methods=['GET', 'POST'])
# def register_model_relation():
#     class1_name = request.json.get('class1')
#     class2_name = request.json.get('class2')
#     relation_name = request.json.get('relation')
#     data = register_relation(class1_name, class2_name, relation_name)
#     return jsonify({"message": data})


# @blue.route("/get_model_class_options", methods=['GET', 'POST'])
# def get_model_class_options():
#     print(request.json)
#     name = request.json.get("selectedValue")
#     # name = "测试模型1"
#     print(name)
#     data = get_model_class_options_list(name)
#     return jsonify({"data": data})


# @blue.route("/get_mdr_object_class_node", methods=['GET', 'POST'])
# def get_mdr_object_class_node():
#     id = request.args.get('name')
#     data = get_mdr_object_class_node_info(id)
#     return jsonify({"data": data})


# 信息模型
#   页面
#       注册页面
@blue.route('/information_model2', methods=['GET', 'POST'])
def information_model2():
    """
    返回信息模型注册页面
    :return:
    """
    return render_template("information_model2.html")


#       查询页面
@blue.route('/search2', methods=['GET', 'POST'])
def search2():
    """
    返回信息模型查询页面
    :return:
    """
    return render_template("search2.html")


#   功能
#       注册
@blue.route('/register/model/addProperty', methods=['GET', 'POST'])
def add_property():
    """
    注册信息模型中的模型属性
    :return:
    """
    property_names = request.json.get('property_names')
    model_name = request.json.get('model_name')
    class_name = request.json.get('class_name')
    evolution = request.json.get('evolution')
    if evolution == "yes":
        attribute_name = request.json.get('attributeName')
        attribute_identifier = request.json.get('attributeIdentifier')
    else:
        attribute_name = "-1"
        attribute_identifier = '-1'
    data = add_property_of_name(property_names, model_name, class_name, evolution, attribute_name, attribute_identifier)
    return jsonify({"message": data})


@blue.route('/register/model/addClass', methods=['GET', 'POST'])
def add_class():
    """
    注册信息模型中的模型类
    :return:
    """
    model_name = request.json.get("params")["model_name"]
    class_name = request.json.get("params")["class_name"]
    evolution = request.json.get("params")["evolution"]
    print(evolution)
    if evolution == "yes":
        attribute_name = request.json.get("params")["attributeName"]
        attribute_identifier = request.json.get("params")["attributeIdentifier"]
    else:
        attribute_name = "-1"
        attribute_identifier = "-1"
    data = add_class_of_name(class_name, model_name, evolution, attribute_name, attribute_identifier)
    return jsonify({"message": data})


@blue.route('/register/model/addRelation', methods=['GET', 'POST'])
def add_relation():
    """
    注册信息模型中两个类之间关系
    :return:
    """
    model_name = request.args.get("model_name")
    class_name1 = request.args.get("class_name1")
    class_name2 = request.args.get("class_name2")
    relation = request.args.get("relation")
    data = add_relation_info(model_name, class_name1, class_name2, relation)
    return jsonify({"message": data})


@blue.route('/register/model/addModel', methods=['GET', 'POST'])
def add_model():
    """
    注册新的信息模型，注册时要求必须为该模型新建一个类
    :return:
    """
    model_name = request.args.get("model_name")
    class_name = request.args.get("class_name")
    data = add_model_info(model_name, class_name)
    return jsonify({'message': data})


#   查询
@blue.route('/search/model/graphOfName', methods=['GET', 'POST'])
def search_model_graph_of_name():
    """
    获得信息模型的图谱数据，同时将该图谱信息相关的表格信息一起返回
    :return:
    """
    name = request.args.get('name')
    # label = request.args.get('label')
    json_data = query_graph_of_model(str(name))
    return jsonify(json_data)


@blue.route("/search/model/getModelClassNameOptions", methods=['GET', 'POST'])
def get_model_class_name_options():
    """
    获得信息模型类名称列表，便于前端注册时，通过下拉列表选中
    :return:
    """
    mode_name = request.args.get("model_name")
    data = get_model_class_name_options_list(mode_name)
    return jsonify({"data": data})


@blue.route("/search/model/getModelTypeOptions", methods=['GET', 'POST'])
def get_model_type_options():
    """
    获取模型名称列表，支持前端模型名称下拉列表的选择
    :return:
    """
    data = get_model_type_options_list()
    return jsonify({"data": data})


@blue.route("/search/model/getClassNameAndPropertyNameOptions", methods=['GET', 'POST'])
def get_class_name_and_property_name_options():
    """
    通过模型名称获得该模型下的类及属性选项
    :return:
    """
    model_name = request.args.get("model_name")
    data = get_class_name_and_property_name_options_list(model_name)
    return jsonify(data)


@blue.route("/search/getSubDomainList", methods=['GET', 'POST'])
def get_sub_domain_list():
    """
    获取子域列表，支持前端子域名称下拉列表的选择
    :return:
    """
    data = get_sub_domain_lists()
    return jsonify({"data": data})


@blue.route("/search/model/getFormList", methods=['GET', 'POST'])
def get_sub_form_list():
    """
    获取子域列表，支持前端子域名称下拉列表的选择
    :return:
    """
    sub_domain_name = request.json.get("name")
    data = get_sub_domain_table_relations(sub_domain_name)
    return jsonify({"data": data})


#       演化
@blue.route("/evolution/model/deletePropertyOfName", methods=['GET', 'POST'])
def delete_property_of_name():
    model_name = request.json.get("params")["model_name"]
    class_name = request.json.get("params")["class_name"]
    property_name = request.json.get("params")["property_name"]
    data = delete_property_of_name_info(model_name, class_name, property_name)
    return jsonify({'message': data})


# MDR
#   页面
@blue.route('/mdr', methods=['GET', 'POST'])
def mdr():
    """
    返回MDR注册页面
    :return:
    """
    return render_template("mdr.html")


@blue.route('/search1', methods=['GET', 'POST'])
def search1():
    """
    返回MDR查询页面
    :return:
    """
    return render_template("search1.html")


#   功能
#       注册
@blue.route("/register/mdr/objectClass", methods=['GET', 'POST'])
def register_mdr_object_class():
    """
    注册MDR对象类
    :return:
    """
    name = request.json.get("name")
    describe = request.json.get("describe")
    personId = request.json.get("personId")
    department = request.json.get("department")
    data = register_object_class(name, describe, personId, department)
    return jsonify({"message": data})


@blue.route("/register/mdr/property", methods=['GET', 'POST'])
def register_mdr_property():
    """
    注册MDR属性
    :return:
    """
    name = request.json.get("name")
    describe = request.json.get("describe")
    personId = request.json.get("personId")
    department = request.json.get("department")
    data = register_property(name, describe, personId, department)
    return jsonify({"message": data})


@blue.route("/register/mdr/conceptualDomain", methods=['GET', 'POST'])
def register_mdr_conceptual_domain():
    """
    注册MDR概念域
    :return:
    """
    name = request.json.get("name")
    describe = request.json.get("describe")
    personId = request.json.get("personId")
    department = request.json.get("department")
    valueMeanings = request.json.get("valueMeanings")
    data = register_conceptual_domain(name, describe, personId, department, valueMeanings)
    return jsonify({"message": data})


@blue.route("/register/mdr/dataElementConcept", methods=['GET', 'POST'])
def register_mdr_data_element_concept():
    """
    注册MDR数据元概念
    :return:
    """
    name = request.json.get("name")
    describe = request.json.get("describe")
    personId = request.json.get("personId")
    department = request.json.get("department")
    object_class = request.json.get("objectClass")
    property = request.json.get("property")
    conceptual_domain = request.json.get("conceptualDomain")
    data = register_data_element_concept(name, describe, personId, department,
                                         object_class, property, conceptual_domain)
    return jsonify({"message": data})


@blue.route("/register/mdr/valueDomain", methods=['GET', 'POST'])
def register_mdr_value_domain():
    """
    MDR值域注册
    :return:
    """
    name = request.json.get("name")
    describe = request.json.get("describe")
    personId = request.json.get("personId")
    department = request.json.get("department")
    conceptual_domain = request.json.get("conceptualDomain")
    indefinite = request.json.get("indefinite")
    enumerable = request.json.get("enumerable")
    data = register_mdr_value_domain_list(name, describe, personId, department,
                                          conceptual_domain, indefinite, enumerable)
    return jsonify({"message": data})


@blue.route("/register/mdr/dataElement", methods=['GET', 'POST'])
def register_mdr_data_element():
    """
    注册MDR数据元
    :return:
    """
    name = request.json.get("name")
    describe = request.json.get("describe")
    personId = request.json.get("personId")
    department = request.json.get("department")
    dataElementConcept = request.json.get("dataElementConcept")
    valueDomain = request.json.get("valueDomain")
    evolution = request.json.get("evolution")
    if evolution == "yes":
        attribute_name = request.json.get("attributeName")
        attribute_identifier = request.json.get("attributeIdentifier")
    else:
        attribute_name = "-1"
        attribute_identifier = "-1"
    data, identifier_data_element = register_data_element(name, describe, personId, department, dataElementConcept,
                                                          valueDomain, evolution, attribute_name, attribute_identifier)
    return jsonify({"message": data, "identifier_data_element": identifier_data_element})


#       智能体自动注册
@blue.route("/register/mdr/agent/batch", methods=['POST'])
def register_mdr_agent_batch():
    """
    使用智能体批量注册MDR
    接收Excel文件，调用pe_agents进行自动注册
    :return: 注册结果统计
    """
    try:
        # 检查是否有文件上传
        if 'file' not in request.files:
            return jsonify({
                "success": False,
                "message": "未找到上传文件"
            })

        file = request.files['file']

        # 调用智能体注册函数
        result = register_mdr_with_agent(file)

        return jsonify(result)

    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"智能体注册失败: {str(e)}",
            "error": str(e)
        })


@blue.route("/register/mdr/agent/status", methods=['GET'])
def get_mdr_agent_status():
    """
    获取智能体状态
    :return: 状态信息
    """
    result = get_agent_status()
    return jsonify(result)


#       查询
@blue.route("/search/mdr/getObjectClassOptions", methods=['GET', 'POST'])
def get_object_class_option():
    """
    获得MDR对象类列表，支持前端对象类选择器功能
    :return:
    """
    data = get_object_class_option_list()
    return jsonify({"data": data})


@blue.route("/search/mdr/getPropertyOption", methods=['GET', 'POST'])
def get_property_option():
    """
    获得属性列表，支持前端属性选择器
    :return:
    """
    data = get_property_option_list()
    return jsonify({"data": data})


@blue.route("/search/mdr/getConceptualDomainOption", methods=['GET', 'POST'])
def get_conceptual_domain_option():
    """
    获得概念域列表，支持前端概念域选择器
    :return:
    """
    data = get_conceptual_domain_option_list()
    return jsonify({"data": data})


@blue.route("/search/mdr/getValueMeaningsOption", methods=['GET', 'POST'])
def get_value_meanings_option():
    """
    获得值含义列表，支持前端值含义选择器
    :return:
    """
    data = get_value_meanings_option_list()
    return jsonify({"data": data})


@blue.route("/search/mdr/getDataElementConceptOption", methods=['GET', 'POST'])
def search_data_element_concept_option():
    """
    获得数据元概念列表，支持前端数据元概念选择器
    :return:
    """
    data = get_data_element_concept_option_list()
    return jsonify({"data": data})


@blue.route("/search/mdr/getValueDomainOption", methods=['GET', 'POST'])
def get_value_domain_option():
    """
    获取MDR值域列表，支持前端值域选择器
    :return:
    """
    data = get_value_domain_option_list()
    return jsonify({"data": data})


@blue.route("/search/mdr/getDataElementOption", methods=['GET', 'POST'])
def get_data_element_option():
    """
    获取MDR数据元列表，支持前端数据元选择器
    :return:
    """
    data = get_data_element_option_list()
    return jsonify({"data": data})


@blue.route("/search/mdr/getValueDomainAndPermissibleValuesOption", methods=['GET', 'POST'])
def get_value_domain_and_permissible_values_option():
    """
    获取MDR中值域的枚举值与不可枚举值列表，该功能主要用于子域注册时，为子域表属性值与可允许值建立关系提供级联选择器
    :return:
    """
    result = get_value_domain_and_permissible_values_option_list()
    return jsonify({"data": result})


@blue.route("/search/mdr/getMDRTableList", methods=['GET', 'POST'])
def get_mdr_table_list():
    """
    获取对应label在数据库中所有的信息，将其处理为表格列表的形式在前端展示
    label: 对象类、属性、概念域、数据元概念、值域、数据元
    :return:
    """
    label = request.args.get("label")
    # 确保label不为None
    if not label:
        return jsonify({"data": [], "tableTitle": ""})

    data = get_mdr_table_list_info(label)
    return jsonify({"data": data, "tableTitle": label})


@blue.route("/search/mdr/getMDRTable", methods=['GET', 'POST'])
def get_mdr_table():
    """
    通过指定label和标识符，获取该节点的注册信息，并返回
    :return:
    """
    identifier = request.args.get('identifier')
    label = request.args.get("label")
    data = get_mdr_table_info(label, identifier)
    return jsonify({"data": data})


@blue.route("/search/mdr/getGraphOfMDR", methods=['GET', 'POST'])
def get_mdr_graph():
    """
    查询MDR图谱，目前只实现通过数据元的标识符获取该数据元共享域六个类别之间的信息
    :return:
    """
    identifier = request.args.get('identifier')
    data = get_graph_of_mdr_info(identifier)
    return jsonify(data)


@blue.route("/evolution/mdr/updateMDR", methods=['GET', 'POST'])
def update_mdr():
    label = request.json.get("params")["label"]
    identifier = request.json.get("params")["identifier"]
    properties = request.json.get("params")["properties"]
    print(label)
    print(identifier)
    print(properties)
    data = update_mdr_info(label, identifier, properties)
    return jsonify({"message": data})


@blue.route("/evolution/mdr/addValueMeanings", methods=['GET', 'POST'])
def add_value_meanings():
    identifier_conceptual_domain = request.json.get("params")["identifier_conceptual_domain"]
    value_meanings = request.json.get("params")["value_meanings"]
    data = add_value_meanings_info(identifier_conceptual_domain, value_meanings)
    return jsonify({"message": data})


@blue.route("/evolution/mdr/addPermissibleValues", methods=['GET', 'POST'])
def add_permissible_values():
    identifier_value_domain = request.json.get("params")["identifier_value_domain"]
    enumerable = request.json.get("params")["enumerable"]
    data = add_permissible_values_info(identifier_value_domain, enumerable)
    return jsonify({"message": data})


# 子域
#   页面
@blue.route("/register_subDomain")
def register_sub_domain():
    """
    返回子域注册页面
    :return:
    """
    return render_template("register_subDomain.html")


#   功能
@blue.route('/register/subDomain/addSubDomian', methods=['GET', 'POST'])
def add_sub_domain():
    """
    注册新的子域
    :return:
    """
    name = request.args.get("name")
    describe = request.args.get("describe")
    data = add_sub_domain_info(name, describe)
    return jsonify({"message": data})


@blue.route('/search/subDomain/getSubDomainOptions', methods=['GET', 'POST'])
def get_sub_domain_options():
    """
    获取子域名称及描述信息列表
    :return:
    """
    data = get_sub_domain_options_list()
    return jsonify({"data": data})


@blue.route('/search/subDomain/getSubDomainAndTableOptions', methods=['GET', 'POST'])
def get_sub_domain_and_table_options():
    """
    获取子域名称及表格的描述信息列表
    :return:
    """
    data = get_sub_domain_and_table_options_list()
    return jsonify({"data": data})


@blue.route('/search/subDomain/getTableOptions', methods=['GET', 'POST'])
def get_sub_domain_table_options():
    data = get_sub_domain_table_options_list()
    return jsonify({"data": data})


# @blue.route('/search/subDomain/getSubDomainToLists', methods=['GET', 'POST'])
# def get_sub_domain_optionLists():
#     """
#     获取子域名称及描述信息列表
#     :return:
#     """
#     data = get_sub_domain_options()
#     return jsonify({"data": data})

@blue.route('/upload', methods=['GET', 'POST'])
def upload():
    """
    上传子域文件，并对该文件进行注册
    :return:
    """
    file = request.files['file']
    # filename = secure_filename(file.filename)
    filename = file.filename
    identifier = register_sub_domain_of_file(file, filename)

    return jsonify({'success': True, 'name': filename, 'identifier': identifier})


@blue.route('/register/subDomain/addRelationBetweenTableAndSubDomain', methods=['GET', 'POST'])
def add_relation_between_table_and_sub_domain():
    """
    添加子域与表之间的联系
    :return:
    """
    sub_domain_name = request.args.get("sub_domain_name")
    identifier = request.args.get("identifier")
    result = add_relation_between_table_and_sub_domain_info(sub_domain_name, identifier)

    # 如果返回的是字典（新格式），直接返回
    if isinstance(result, dict):
        return jsonify(result)
    # 如果返回的是字符串（旧格式），包装成字典
    else:
        return jsonify({"success": True, "message": result})


@blue.route('/register/subDomain/addRelationBetweenAttributeAndDataElement', methods=['GET', 'POST'])
def add_relation_between_attribute_and_data_element():
    """
    添加子域表属性与MDR共享域数据元之间的联系
    :return:
    """
    print(request.args)
    # sub_domain_name = request.args.get("sub_domain_name")
    identifier_table = request.args.get("identifier_table")
    name_attribute = request.args.get("name_attribute")
    identifier_data_element = request.args.get("identifier_data_element")
    # print(sub_domain_name)
    data = add_relation_between_attribute_and_data_element_info(identifier_table,
                                                                name_attribute, identifier_data_element)
    return jsonify({"data": data})


@blue.route('/register/subDomain/addRelationBetweenAttributeAndValueDomain', methods=['GET', 'POST'])
def add_relation_between_attribute_and_value_domain():
    """
    添加表属性与值域之间的联系
    :return:
    """
    sub_domain_name = request.args.get("sub_domain_name")
    identifier_table = request.args.get("identifier_table")
    name_attribute = request.args.get("name_attribute")
    identifier_value_domain = request.args.get("identifier_value_domain")
    data = add_relation_between_attribute_and_value_domain_info(sub_domain_name, identifier_table,
                                                                name_attribute, identifier_value_domain)
    return jsonify({"data": data})


@blue.route('/register/subDomain/addRelationBetweenAttributeValueAndPermissibleValues', methods=['GET', 'POST'])
def add_relation_between_attribute_value_and_permissible_values():
    """
    添加表属性值与可允许值之间的关系
    :return:
    """
    sub_domain_name = request.args.get("sub_domain_name")
    identifier_table = request.args.get("identifier_table")
    name_attribute_value = request.args.get("name_attribute_value")
    identifier_permissible_values = request.args.get("identifier_permissible_values")
    data = add_relation_between_attribute_value_and_permissible_values_info(sub_domain_name, identifier_table,
                                                                            name_attribute_value,
                                                                            identifier_permissible_values)

    return jsonify({"data": data})


# ==== 子域自动映射路由（两阶段流程） ====

@blue.route('/register/subDomain/getMappingCandidates', methods=['GET', 'POST'])
def get_mapping_candidates():
    """
    阶段1：获取自动映射的候选结果（不写入数据库）
    用户可以在前端审核和修改这些候选
    :return: 候选映射结果
    """
    try:
        subdomain_name = request.args.get("subdomain_name")

        if not subdomain_name:
            return jsonify({
                "success": False,
                "message": "未提供子域名称"
            })

        # 延迟导入
        from mdr_based_mapper import MDRBasedMapper
        import os

        mapper = MDRBasedMapper()

        # 导出子域数据并生成候选映射表
        data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))), "data")
        os.makedirs(data_dir, exist_ok=True)

        cta_csv_path, cea_csv_path = mapper.export_subdomain_for_mapping(subdomain_name, data_dir)

        if not cta_csv_path or not cea_csv_path:
            return jsonify({
                "success": False,
                "message": "生成候选失败：未找到子域数据"
            })

        # 处理映射表，获取候选结果
        mapping_result = mapper.process_mapping_tables(cta_csv_path, cea_csv_path)

        if mapping_result['status'] != 'success':
            return jsonify({
                "success": False,
                "message": f"处理映射表失败: {mapping_result.get('error', '未知错误')}"
            })

        # 返回候选结果供前端展示和修改
        return jsonify({
            "success": True,
            "message": "候选生成成功",
            "data": {
                "cta_candidates": mapping_result['cta_results'],  # [{subdomain_data, data_element}, ...]
                "cea_candidates": mapping_result['cea_results'],  # [{subdomain_value, subdomain_data, mdr_value}, ...]
                "cta_count": mapping_result['cta_count'],
                "cea_count": mapping_result['cea_count']
            }
        })

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({
            "success": False,
            "message": f"生成候选时发生错误: {str(e)}"
        })


@blue.route('/register/subDomain/confirmMapping', methods=['POST'])
def confirm_mapping():
    """
    阶段2：用户确认后，将映射结果写入数据库
    接收前端审核/修改后的映射结果
    :return: 写入结果
    """
    try:
        # 获取前端传来的映射结果（JSON格式）
        data = request.get_json()

        if not data:
            return jsonify({
                "success": False,
                "message": "未提供映射数据"
            })

        cta_results = data.get('cta_results', [])
        cea_results = data.get('cea_results', [])

        if not cta_results and not cea_results:
            return jsonify({
                "success": False,
                "message": "映射数据为空"
            })

        # 延迟导入
        from mdr_based_mapper import MDRBasedMapper

        mapper = MDRBasedMapper()

        # 写入数据库
        mapping_count = mapper.create_mappings_in_neo4j(cta_results, cea_results)

        return jsonify({
            "success": True,
            "message": "映射关系创建成功",
            "data": {
                "total_mappings": mapping_count,
                "cta_count": len(cta_results),
                "cea_count": len(cea_results)
            }
        })

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({
            "success": False,
            "message": f"创建映射时发生错误: {str(e)}"
        })


@blue.route('/search/mdr/getAllDataElements', methods=['GET'])
def get_all_data_elements():
    """
    获取所有数据元（用于映射审核时的下拉选择）
    支持根据子域筛选相关的数据元
    :return:
    """
    try:
        subdomain_name = request.args.get("subdomain_name")

        if subdomain_name:
            # 获取与子域表属性相关的数据元（通过语义相似度）
            query = """
            MATCH (s:子域 {name: $subdomain_name})-[:拥有]->(t:表)-[:由组成]->(a:表属性)
            WITH COLLECT(DISTINCT a.name) as attr_names

            // 查询所有数据元及其语义信息
            MATCH (de:DataElement)
            OPTIONAL MATCH (de)-[:BASED_ON]->(dec:DataElementConcept)
            OPTIONAL MATCH (dec)-[:HAS_PROPERTY]->(p:Property)
            OPTIONAL MATCH (dec)-[:HAS_OBJECT_CLASS]->(oc:ObjectClass)

            // 计算与表属性的相关性
            WITH de, attr_names, p, oc,
                 REDUCE(score = 0, attr IN attr_names |
                   score +
                   CASE
                     WHEN de.name CONTAINS attr OR attr CONTAINS de.name THEN 1.0
                     WHEN p.name CONTAINS attr OR attr CONTAINS p.name THEN 0.8
                     WHEN oc.name CONTAINS attr OR attr CONTAINS oc.name THEN 0.6
                     ELSE 0.0
                   END
                 ) as relevance_score

            WHERE relevance_score > 0 OR SIZE(attr_names) = 0

            RETURN DISTINCT de.name as name
            ORDER BY relevance_score DESC, de.name
            LIMIT 100
            """
            results = graph.run(query, subdomain_name=subdomain_name).data()
        else:
            # 未指定子域，返回所有数据元
            query = """
            MATCH (de:DataElement)
            RETURN de.name as name
            ORDER BY de.name
            """
            results = graph.run(query).data()

        return jsonify({
            "success": True,
            "data": results
        })
    except Exception as e:
        print(f"获取数据元列表失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            "success": False,
            "message": f"获取数据元列表失败: {str(e)}"
        })


@blue.route('/search/mdr/getAllPermissibleValues', methods=['GET'])
def get_all_permissible_values():
    """
    获取所有可允许值（用于映射审核时的下拉选择）
    支持根据子域筛选相关的可允许值
    :return:
    """
    try:
        subdomain_name = request.args.get("subdomain_name")

        if subdomain_name:
            # 获取与子域表属性值相关的可允许值（通过语义相似度）
            query = """
            MATCH (s:子域 {name: $subdomain_name})-[:拥有]->(t:表)-[:由组成]->(a:表属性)-[:约束值]->(av:表属性值)
            WITH COLLECT(DISTINCT av.name) as value_names

            // 查询所有可允许值及其语义信息
            MATCH (v:Value)
            OPTIONAL MATCH (v)-[:REPRESENTS]->(vm:ValueMeaning)

            // 计算与表属性值的相关性
            WITH v, value_names, vm,
                 REDUCE(score = 0, val IN value_names |
                   score +
                   CASE
                     WHEN v.name = val THEN 1.0
                     WHEN v.name CONTAINS val OR val CONTAINS v.name THEN 0.9
                     WHEN vm.name CONTAINS val OR val CONTAINS vm.name THEN 0.7
                     ELSE 0.0
                   END
                 ) as relevance_score

            WHERE relevance_score > 0 OR SIZE(value_names) = 0

            RETURN DISTINCT v.name as name
            ORDER BY relevance_score DESC, v.name
            LIMIT 200
            """
            results = graph.run(query, subdomain_name=subdomain_name).data()
        else:
            # 未指定子域，返回所有可允许值
            query = """
            MATCH (v:Value)
            RETURN v.name as name
            ORDER BY v.name
            """
            results = graph.run(query).data()

        return jsonify({
            "success": True,
            "data": results
        })
    except Exception as e:
        print(f"获取可允许值列表失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            "success": False,
            "message": f"获取可允许值列表失败: {str(e)}"
        })


@blue.route('/search/subDomain/getGraphOfTable')
def get_graph_of_table():
    """
    获取子域图谱数据
    :return:
    """
    sub_domain_name = request.args.get("sub_domain_name")
    identifier_table = request.args.get("identifier_table")
    data = get_graph_of_table_info(sub_domain_name, identifier_table)
    return jsonify(data)


# @blue.route('/search/subDomain/getMDR', methods=['GET', 'POST'])
# def get_MDR_by_subDomain():
#     """
#     通过子域名字获取MDR信息
#     :return:
#     """
#     sub_domain_name = request.args.get("sub_domain_name")
#     data = get_graph_of_domian_info(sub_domain_name)
#     return jsonify(data)

@blue.route('/search/subDomain/getMDRTableThroughSubDomain', methods=['GET', 'POST'])
def get_mdr_table_through_sub_domain():
    """
    通过子域名字获取MDR信息
    :return:
    """
    identifier_attribute = request.args.get("identifier_attribute")
    data = get_mdr_table_through_sub_domain_info(identifier_attribute)
    return jsonify(data)


@blue.route('/search/subDomain/getSubDomainProperties', methods=['GET', 'POST'])
def get_sub_domain_properties():
    """
    通过表格标识符获取该表下的属性与属性值列表
    :return:
    """
    identifier_table = request.args.get("identifier_table")
    data = get_sub_domain_properties_list(identifier_table)
    return jsonify(data)


@blue.route('/search/subDomain/getSubDomainExistAttributeValueOptions', methods=['GET', 'POST'])
def get_sub_domain_exist_attribute_value_options():
    identifier_table = request.args.get("identifier_table")
    # print(identifier_table)
    data = get_sub_domain_exist_attribute_value_options_list(identifier_table)
    return jsonify({"data": data})


@blue.route('/search/subDomain/getGraphOfAttribute', methods=['GET', 'POST'])
def get_graph_of_attribute():
    """
    通过表属性标识符查询表属性相关的子图谱
    :return:
    """
    identifier_attribute = request.args.get("identifier_attribute")
    data = get_graph_of_attribute_info(identifier_attribute)
    print(data)
    return jsonify(data)


#       演化
@blue.route('/evolution/subDomain/deleteAttributeValue', methods=['GET', 'POST'])
def delete_attribute_value():
    """
    删除表属性值
    :return:
    """
    identifier_attribute_value = request.json.get("params")["identifier_attribute_value"]
    data = delete_attribute_value_info(identifier_attribute_value)
    return jsonify({"message": data})


@blue.route('/evolution/subDomain/deleteAttribute', methods=['GET', 'POST'])
def delete_attribute():
    """
    删除表属性
    :return:
    """
    identifier_attribute = request.json.get("params")["identifier_attribute"]
    data = delete_attribute_info(identifier_attribute)
    return jsonify({"message": data})


@blue.route('/evolution/subDomain/deleteTable', methods=['GET', 'POST'])
def delete_table():
    """
    通过表标识符删除表
    :return:
    """

    identifier_table = request.json.get("params")["identifier_table"]
    print(identifier_table)
    # print(request.json.get("params")["identifier_table"])
    data = delete_table_info(identifier_table)
    return jsonify({"message": data})


@blue.route('/evolution/subDomain/updateSubDomain', methods=['GET', 'POST'])
def update_sub_domain():
    """
    更新子域节点信息
    :return:
    """
    label = request.args.get("label")
    identifier = request.args.get("identifier")
    name = request.args.get("name")
    data = update_sub_domain_info(label, identifier, name)
    return jsonify({"message": data})


@blue.route('/upload_json_file', methods=['POST', 'GET'])
def upload_json_file():
    """
        上传json文件接口
        :return:
        """
    if request.method == 'POST':
        file = request.files['file']
        if file.filename.endswith('.json'):
            # 读取上传的 JSON 文件并输出内容到控制台
            data = json.load(file.stream)
            message = register_model_of_file(data)
            return jsonify({"message": message})
    return "导入失败"


# 用户
@blue.route('/user/getModelAndModelClassOptions', methods=['POST', 'GET'])
def get_model_and_model_class_options():
    data = get_model_and_model_class_options_list()
    return jsonify({"data": data})


@blue.route('/user/getDataElementOfModelClassOptions', methods=['POST', 'GET'])
def get_data_element_of_model_class_options():
    model_class = request.args.get("model_class")
    print(model_class)
    data = get_data_element_of_model_class_options_list(model_class)
    return jsonify({"data": data})


@blue.route('/user/getDataElementIdentifierThroughObjectClassAndProperty', methods=['POST', 'GET'])
def get_data_element_identifier_through_object_class_and_property():
    class_name = request.json.get("params")["class_name"]
    property = request.json.get("params")["property"]
    data = get_data_element_identifier_info_through_object_class_and_property(class_name, property)
    return jsonify({"data": data})


@blue.route('/user/getDataShareInfo', methods=['POST', 'GET'])
def get_data_share_info():
    identifier = request.args.get("identifier")
    data = get_data_share_info_json(identifier)
    print(data)
    return jsonify({"data": data})


@blue.route('/user/getModelEvolutionInfo', methods=['POST', 'GET'])
def get_model_evolution_info():
    model_name = request.args.get("model_name")
    data = get_model_evolution_info_json(model_name)
    print(data)
    return jsonify({"data": data})


@blue.route('/user/getSubDomainEvolutionInfo', methods=['POST', 'GET'])
def get_sub_domain_evolution_info():
    sub_domain_name = request.args.get("sub_domain_name")
    data = get_sub_domain_evolution_info_json(sub_domain_name)
    return jsonify({"data": data})


@blue.route('/user/getModelEvolutionTables', methods=['POST', 'GET'])
def get_model_evolution_tables():
    data = get_model_evolution_tables_list()
    return jsonify({"data": data})


@blue.route('/user/getSubDomainEvolutionTables', methods=['POST', 'GET'])
def get_sub_domain_evolution_tables():
    data = get_sub_domain_evolution_tables_list()
    return jsonify({"data": data})


# index
@blue.route('/index/getIndexGraph', methods=['POST', 'GET'])
def get_index_graph():
    data = get_graph_index_info()
    return jsonify({"data": data})


@blue.route('/index/getIndexSubDomain', methods=['POST', 'GET'])
def get_index_sub_domain():
    data = get_index_sub_domain_info()
    return jsonify({"data": data})
