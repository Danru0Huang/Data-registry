<template>
  <div class="box666">
    <div class="searchline" style="
        height: 60px;
        background-color: #a6d9f4;
        border-radius: 15px;
        padding: 10px;
        display: flex;
        align-items: center;
      ">
      <div class="namebox" style="min-width: 100px">业务领域</div>
      <el-button @click="backsearch" type="primary">返回查询</el-button>
    </div>
    <div id="chart_graph3" v-show="showchart_graph3"></div>
    <!-- 信息模型演化图谱 -->
    <div>
      <div class="Modeltable" v-show="showModeltable">
        <div class="searchline" style="
            height: 60px;
            background-color: #a6d9f4;
            border-radius: 15px;
            padding: 10px;
            display: flex;
            align-items: center;
          " v-show="showtableline">
          <div style="margin-left: 42%;color: white;font-size: large;">共享域演化信息溯源</div>
        </div>
        <el-table :data="model_message" style="width: 100%">>
          <el-table-column label="变更类型" prop="变更类型"> </el-table-column>
          <el-table-column label="变更原因" prop="变更原因"> </el-table-column>
          <el-table-column label="变更结果" prop="变更结果"> </el-table-column>
          <el-table-column label="操作人员" prop="操作人员"> </el-table-column>
          <el-table-column label="操作时间" prop="操作时间"> </el-table-column>
        </el-table>
      </div>
      <div class="subDomaintable" v-show="showsubDomaintable" style="display: inline-block; width: 100%">
        <el-table :data="sub_domain_message" style="width: 100%">
          <el-table-column type="expand">
            <template slot-scope="props">
              <el-form label-position="left" inline class="demo-table-expand">
                <el-form-item>
                  <el-descriptions :column="2" border>
                    <el-descriptions-item v-if="props.evolution != '暂无演化数据'" label="演化信息">
                      <el-form-item v-for="(evolutionItem, index) in props.row.evolution" :key="index">
                        <el-descriptions :column="1" border>
                          <el-descriptions-item label="变更类型">{{
                            evolutionItem.变更类型
                          }}</el-descriptions-item>
                          <el-descriptions-item label="变更原因">{{
                            evolutionItem.变更原因
                          }}</el-descriptions-item>
                          <el-descriptions-item label="变更结果">{{
                            evolutionItem.变更结果
                          }}</el-descriptions-item>
                          <el-descriptions-item label="操作人员">{{
                            evolutionItem.操作人员
                          }}</el-descriptions-item>
                          <el-descriptions-item label="操作时间">{{
                            evolutionItem.操作时间
                          }}</el-descriptions-item>
                        </el-descriptions>
                        <el-divider><i class="el-icon-crop"></i></el-divider>
                      </el-form-item>
                    </el-descriptions-item>
                  </el-descriptions>
                  <el-divider><i class="el-icon-crop"></i></el-divider>
                </el-form-item>
              </el-form>
            </template>
          </el-table-column>
          <el-table-column label="表名" prop="table_name"> </el-table-column>
          <el-table-column label="表标识符" prop="table_identifier">
          </el-table-column>
          <el-table-column align="right">
            <!-- eslint-disable -->
          </el-table-column>
        </el-table>
      </div>
      <div class="chart_graph4box" v-show="showchart_graph4">
        <div class="searchline" style="
            height: 60px;
            background-color: #a6d9f4;
            border-radius: 15px;
            padding: 10px;
            display: flex;
            align-items: center;
          ">
          <div style="margin-left: 42%;color: white;font-size: large;">共享域演化信息溯源</div>
        </div>
        <div id="chart_graph4"></div>
      </div>
      <!-- 子域演化图谱 -->
      <div class="chart_graph5box" v-show="showchart_graph5">
        <div class="searchline" style="
            height: 60px;
            background-color: #a6d9f4;
            border-radius: 15px;
            padding: 10px;
            display: flex;
            align-items: center;
          ">
          <div style="margin-left: 42%;color: white;font-size: large;">子域演化信息溯源</div>
        </div>
        <div id="chart_graph5"></div>
      </div>
    </div>
  </div>
</template>

<script>
import * as echarts from "echarts";
export default {
  props: {
    parentData1: "",
    parentData2: "",
  },
  data() {
    return {
      nodeidentifier: '',
      // showSubdomain:true,
      showValue: false,
      showGraph2: true,
      dialogobject_class: [],
      sub_domain_info: [],

      // 演化的数据
      // 模型演化表格列表
      model_evolution_tables: [],
      //模型
      model_tree_data: [],
      model_tree_evolution_data: [],
      model_message: [],
      // 子域
      // 子域演化信息表格列表
      sub_domain_message: [],
      sub_domain_evolution_tables: [],
      sub_domain_tree_evolution: [],
      shownone: false,
      showModeltable: true,
      showsubDomaintable: false,
      showchart_graph3: true,
      showchart_graph4: true,
      showchart_graph5: true,
      showtableline: true,
    };
  },
  mounted() {
    if (this.parentData2 == "model") {
      this.getModelEvolutionInfo();
    } else {
      this.getSubDomainEvolutionInfo();
    }
    this.disposeAllEchartsInstances();
  },
  beforeDestroy() {
    // 获取当前组件中所有 echarts 实例并销毁它们
    this.disposeAllEchartsInstances();
  },
  methods: {
    sendData2() {
      this.$emit('send-data2', this.nodeidentifier, '这是从子组件发送的数据');
    },
    backsearch() {
      this.$emit("backsearch");
    },
    // 演化的函数
    disposeAllEchartsInstances() {
      // 获取当前组件中所有带有 `echarts-chart` 类名的元素
      const allCharts = document.querySelectorAll(".echarts-chart");
      allCharts.forEach((chartElement) => {
        // 获取与该元素关联的 echarts 实例
        const chartInstance = echarts.getInstanceByDom(chartElement);
        if (chartInstance) {
          // 销毁该图表实例
          chartInstance.dispose();
        }
      });
    },
    // 获取模型演化信息
    getModelEvolutionInfoNull() {
      this.$axios
        .get("http://localhost:5000/user/getModelEvolutionInfo", {
          params: {
            model_name: this.parentData1,
          },
        })
        .then((Response) => {
          this.model_tree_data = Response.data.data.model_tree;
          this.updateChart3(this.model_tree_data);
          this.showchart_graph4 = false;
          this.showchart_graph5 = false;
        });
    },
    getModelEvolutionInfo() {
      this.$axios
        .get(`${this.$apiBaseUrl}/user/getModelEvolutionInfo`, {
          params: {
            model_name: this.parentData1,
          },
        })
        .then((Response) => {
          console.log(Response);
          if (Response.data.data.model_message == "暂无演化信息") {
            this.getModelEvolutionInfoNull();
          } else {
            this.model_message = Response.data.data.model_message;
            this.model_tree_data = Response.data.data.model_tree;
            this.updateChart3(this.model_tree_data);
            this.model_tree_evolution_data =
              Response.data.data.model_tree_evolution;
            this.updateChart4(this.model_tree_evolution_data);
            this.model_message = Response.data.data.model_message;
            this.showchart_graph5 = false;
            //   console.log("模型的演化表格信息");
            //   console.log(this.model_message);
          }
        });
    },
    updateChart3(treeData) {
      var chartDom = document.getElementById("chart_graph3");
      var myChart = echarts.init(chartDom);
      var option = {
        tooltip: {
          trigger: "item",
          triggerOn: "mousemove",
        },
        series: [
          {
            type: "tree",
            id: 0,
            name: "tree1",
            data: [treeData],
            top: "10%",
            left: "8%",
            bottom: "22%",
            right: "20%",
            symbolSize: 7,
            edgeShape: "polyline",
            edgeForkPosition: "63%",
            initialTreeDepth: 1,
            lineStyle: {
              width: 2,
            },
            label: {
              backgroundColor: "#fff",
              position: "left",
              verticalAlign: "middle",
              align: "right",
              formatter: function (params) {
                var text = params.name;
                var length = text.length;
                var maxLineLength = 12; // 每行最多显示的字符数
                var lineCount = Math.ceil(length / maxLineLength); // 计算需要几行
                var lines = [];
                for (var i = 0; i < lineCount; i++) {
                  var line = text.substr(i * maxLineLength, maxLineLength);
                  lines.push(line);
                }
                return lines.join("\n");
              },
            },
            leaves: {
              label: {
                position: "right",
                verticalAlign: "middle",
                align: "left",
              },
            },
            emphasis: {
              focus: "descendant",
            },
            expandAndCollapse: true,
            animationDuration: 550,
            animationDurationUpdate: 750,
          },
        ],
      };
      myChart.off("click");
      myChart.on("click", function (params) {
        // 获取点击节点的数据
        console.log(params);
        if (params.treeAncestors.length < 4) {
          // alert("请选择有属性值的节点查询");
        } else {
          var classname =
            params.treeAncestors[params.treeAncestors.length - 2].name;
          var property =
            params.treeAncestors[params.treeAncestors.length - 1].name;
          console.log("类名:", classname);
          console.log("属性名:", property);
          // this.gotoDatasharing();
          this.$axios
            //修改接口
            .post(
              "http://localhost:5000/user/getDataElementIdentifierThroughObjectClassAndProperty",
              {
                params: {
                  //传参名修改
                  class_name: classname,
                  property: property,
                },
              }
            )
            .then((Response) => {
              this.nodeidentifier = Response.data.data;
              console.log(this.nodeidentifier);
              this.sendData2();
            });
        }
      }.bind(this)
      );
      myChart.setOption(option, true);
    },
    updateChart4(treeData) {
      var chartDom = document.getElementById("chart_graph4");
      // 检查是否已经存在图表实例
      var existingChart = echarts.getInstanceByDom(chartDom);
      if (existingChart) {
        // 如果已经存在，销毁它
        existingChart.dispose();
      }
      var myChart = echarts.init(chartDom);
      var option = {
        tooltip: {
          trigger: "item",
          triggerOn: "mousemove",
        },
        series: [
          {
            type: "tree",
            id: 0,
            name: "tree1",
            data: [treeData],
            top: "10%",
            left: "8%",
            bottom: "22%",
            right: "20%",
            symbolSize: 7,
            edgeShape: "polyline",
            edgeForkPosition: "63%",
            initialTreeDepth: 1,
            lineStyle: {
              width: 2,
            },
            label: {
              backgroundColor: "#fff",
              position: "left",
              verticalAlign: "middle",
              align: "left",
              formatter: function (params) {
                var text = params.name;
                var length = text.length;
                var maxLineLength = 12; // 每行最多显示的字符数
                var lineCount = Math.ceil(length / maxLineLength); // 计算需要几行
                var lines = [];
                for (var i = 0; i < lineCount; i++) {
                  var line = text.substr(i * maxLineLength, maxLineLength);
                  lines.push(line);
                }
                return lines.join("\n");
              },
            },
            leaves: {
              label: {
                position: "right",
                verticalAlign: "middle",
                align: "left",
              },
            },
            emphasis: {
              focus: "descendant",
            },
            expandAndCollapse: true,
            animationDuration: 550,
            animationDurationUpdate: 750,
          },
        ],
      };
      myChart.setOption(option);
    },
    // 获取子域演化信息
    getSubDomainEvolutionInfo() {
      this.$axios
        .get("http://localhost:5000/user/getSubDomainEvolutionInfo", {
          params: {
            sub_domain_name: this.parentData1,
          },
        })
        .then((Response) => {
          console.log(Response);
          if (
            Response &&
            Response.data &&
            Response.data.data &&
            Response.data.data.sub_domain_message &&
            Response.data.data.sub_domain_message.length > 0 &&
            Response.data.data.sub_domain_message[0].evolution
          ) {
            this.sub_domain_message = Response.data.data.sub_domain_message;
            console.log(this.sub_domain_message);
          } else {
            this.sub_domain_message = null;
          }
          //   console.log("子域的演化表格信息");
          //   console.log(this.sub_domain_message);
          this.sub_domain_tree_evolution =
            Response.data.data.sub_domain_tree_evolution;
          this.updateChart5(this.sub_domain_tree_evolution);
          this.showtableline = false;
          this.showchart_graph3 = false;
          this.showchart_graph4 = false;
          this.showchart_graph5 = true;
          this.showsubDomaintable = true;
          this.showModeltable = false;
        });
    },
    updateChart5(treeData) {
      var chartDom = document.getElementById("chart_graph5");
      // 检查是否已经存在图表实例
      var existingChart = echarts.getInstanceByDom(chartDom);
      if (existingChart) {
        // 如果已经存在，销毁它
        existingChart.dispose();
      }
      var myChart = echarts.init(chartDom);
      var option = {
        tooltip: {
          trigger: "item",
          triggerOn: "mousemove",
        },
        series: [
          {
            type: "tree",
            id: 0,
            name: "tree1",
            data: [treeData],
            top: "10%",
            left: "8%",
            bottom: "22%",
            right: "20%",
            symbolSize: 7,
            edgeShape: "polyline",
            edgeForkPosition: "63%",
            initialTreeDepth: 1,
            lineStyle: {
              width: 2,
            },
            label: {
              backgroundColor: "#fff",
              position: "left",
              verticalAlign: "middle",
              align: "left",
              formatter: function (params) {
                var text = params.name;
                var length = text.length;
                var maxLineLength = 20; // 每行最多显示的字符数
                var lineCount = Math.ceil(length / maxLineLength); // 计算需要几行
                var lines = [];
                for (var i = 0; i < lineCount; i++) {
                  var line = text.substr(i * maxLineLength, maxLineLength);
                  lines.push(line);
                }
                return lines.join("\n");
              },
            },
            leaves: {
              label: {
                position: "right",
                verticalAlign: "middle",
                align: "left",
              },
            },
            emphasis: {
              focus: "descendant",
            },
            expandAndCollapse: true,
            animationDuration: 550,
            animationDurationUpdate: 750,
          },
        ],
      };
      myChart.setOption(option);
    },
  },
};
</script>

<style>
.box666 {
  margin-left: 250px;
}

.namebox {
  width: 150px;
  height: 40px;
  background-color: #0da4f6;
  border-radius: 15px;
  color: white;
  text-align: center;
  margin-left: 38%;
  width: 8%;
  padding: 8px;
  margin-right: 2%;
}

.demo-table-expand {
  font-size: 0;
}

.demo-table-expand label {
  width: 90px;
  color: #99a9bf;
}

.demo-table-expand .el-form-item {
  margin-left: 60px;
  margin-bottom: 0;
  width: 100%;
}

#chart_graph1 {
  width: 100%;
  height: 700px;
}

#chart_graph2 {
  width: 100%;
  height: 700px;
}

#chart_graph3 {
  width: 100%;
  height: 600px;
}

#chart_graph4 {
  width: 100%;
  height: 600px;
}

#chart_graph5 {
  width: 100%;
  height: 600px;
}
</style>