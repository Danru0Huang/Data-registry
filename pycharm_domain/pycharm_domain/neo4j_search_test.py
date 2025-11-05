from py2neo import Node, Relationship, Graph
import json
from App.index.index import get_index_sub_domain_info

graph = Graph(
    "http://localhost:7474",
    user="neo4j",
    password="123456"
)


def save_to_json_file(data):
    file_path = 'info.json'
    # 使用json.dump()将字典保存为带缩进的JSON文件
    with open(file_path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    data = get_index_sub_domain_info()
    print(data)



    # data = {"专利信息模型":
    #             {"$count": 50,
    #              "专利": {"$count": 20,
    #                     "专利来源": {"$count": 5},
    #                     "被引频次": {"$count": 5},
    #                     "发布路径": {"$count": 5},
    #                     "具体法律状态": {"$count": 5},
    #                     "发表时间": {"$count": 5},
    #                     "公开号": {"$count": 5},
    #                     "申请号": {"$count": 5},
    #                     "主分类号": {"$count": 5},
    #                     "属性": {"$count": 5},
    #                     "名称": {"$count": 5},
    #                     "授权公告日": {"$count": 5},
    #                     "他引频次": {"$count": 5},
    #                     "下载频次": {"$count": 5},
    #                     "更新日期": {"$count": 5},
    #                     "公开日": {"$count": 5},
    #                     "申请日": {"$count": 5},
    #                     "密级": {"$count": 5},
    #                     "IPC分类号": {"$count": 5},
    #                     "类别": {"$count": 5},
    #                     },
    #              "文件": {"$count": 20,
    #                     "权力要求书": {"$count": 5},
    #                     "说明书附图": {"$count": 5},
    #                     "申请书": {"$count": 5},
    #                     "说明书页数": {"$count": 5},
    #                     "说明书": {"$count": 5},
    #                     "摘要": {"$count": 5}
    #                     },
    #              "人员": {"$count": 20,
    #                     "联系人": {"$count": 5},
    #                     "电话": {"$count": 5},
    #                     "邮编": {"$count": 5},
    #                     "权力要求人": {"$count": 5},
    #                     "审查人": {"$count": 5},
    #                     "类型": {"$count": 5},
    #                     "地址": {"$count": 5},
    #                     "申请人": {"$count": 5},
    #                     "发明人": {"$count": 5}
    #                     },
    #              "代理": {"$count": 2,
    #                     "电话": {"$count": 5},
    #                     "地址": {"$count": 5},
    #                     "邮编": {"$count": 5},
    #                     "代理人": {"$count": 5},
    #                     "代理机机构": {"$count": 5}
    #                     },
    #              "单位": {"$count": 20,
    #                     "地址": {"$count": 5},
    #                     "类型": {"$count": 5},
    #                     "地区": {"$count": 5},
    #                     "上级主管单位": {"$count": 5},
    #                     "单位编号": {"$count": 5},
    #                     "单位名称": {"$count": 5}
    #                     },
    #              }
    #         }
    # save_to_json_file(data)
    #
    # data2 = {"数据元":
    #              {"$count": 6,
    #               "DE 专利法律状态1": {"$count": 1},
    #               "DE 专利法律状态2": {"$count": 1},
    #               "DE 专利法律状态3": {"$count": 1},
    #               "DE 专利法律状态4": {"$count": 1},
    #               "DE 专利法律状态5": {"$count": 1},
    #               "DE 专利法律状态6": {"$count": 1},
    #               },
    #          "数据元2":
    #              {"$count": 8,
    #               "DE 专利法律状态1": {"$count": 1},
    #               "DE 专利法律状态2": {"$count": 1},
    #               "DE 专利法律状态3": {"$count": 1},
    #               "DE 专利法律状态4": {"$count": 1},
    #               "DE 专利法律状态5": {"$count": 1},
    #               "DE 专利法律状态6": {"$count": 1},
    #               "DE 专利法律状态7": {"$count": 1},
    #               "DE 专利法律状态8": {"$count": 1},
    #               },
    #          }
