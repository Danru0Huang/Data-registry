<template>
  <div class="box666">
    <div
      class="searchline"
      style="
        height: 60px;
        background-color: #a6d9f4;
        border-radius: 15px;
        padding: 10px;
        display: flex;
        align-items: center;
      "
    >
      <div class="namebox" style="min-width: 100px;margin-left: 42%;">业务领域</div>
      <el-button @click="backsearch" type="primary">返回查询</el-button>
    </div>
    <div>
      <el-table :data="dialogobject_class" style="width: 75%">
        <el-table-column type="expand">
          <template slot-scope="props">
            <el-form label-position="left" inline class="demo-table-expand">
              <el-form-item label="数据元">
                <span>{{ props.row.name }}</span>
              </el-form-item>
              <el-form-item label="标识符">
                <span>{{ props.row.identifier }}</span>
              </el-form-item>
              <el-form-item label="描述">
                <span>{{ props.row.describe }}</span>
              </el-form-item>
              <el-form-item label="注册状态">
                <span>{{ props.row.status }}</span>
              </el-form-item>
              <el-form-item label="创建时间">
                <span>{{ props.row.time }}</span>
              </el-form-item>
              <el-form-item label="版本">
                <span>{{ props.row.version }}</span>
              </el-form-item>
              <el-form-item label="创建人员ID">
                <span>{{ props.row.personId }}</span>
              </el-form-item>
              <el-form-item label="创建单位">
                <span>{{ props.row.department }}</span>
              </el-form-item>
              <el-form-item label="演化信息">
                <span>{{ props.row.evolution }}</span>
              </el-form-item>
              <el-divider content-position="center">子域信息</el-divider>
              <el-form-item
                v-for="(item, index1) in sub_domain_info"
                :key="index1"
              >
                <el-descriptions :column="2" border>
                  <el-descriptions-item label="列名">{{
                    item.column_name
                  }}</el-descriptions-item>
                  <el-descriptions-item label="表格标识符">{{
                    item.column_identifier
                  }}</el-descriptions-item>
                  <el-descriptions-item label="表格名称">{{
                    item.table_name
                  }}</el-descriptions-item>
                  <el-descriptions-item label="子域描述">{{
                    item.sub_domain_describe
                  }}</el-descriptions-item>
                  <el-descriptions-item label="取值" v-if="showValue">
                    <div>
                      <el-form-item
                        v-for="(item, index2) in item.value"
                        :key="index2"
                      >
                        <el-descriptions :column="3" border>
                          <el-descriptions-item label="值">{{
                            item.value_name
                          }}</el-descriptions-item>
                          <el-descriptions-item label="标识符">{{
                            item.value_identifier
                          }}</el-descriptions-item>
                          <el-descriptions-item label="值含义">{{
                            item.value_meaning
                          }}</el-descriptions-item>
                        </el-descriptions>
                        <el-divider><i class="el-icon-crop"></i></el-divider>
                      </el-form-item>
                    </div>
                  </el-descriptions-item>
                  <el-descriptions-item
                    v-if="item.evolution != '暂无演化数据'"
                    label="演化信息"
                  >
                    <el-form-item
                      v-for="(evolutionItem, index) in item.evolution"
                      :key="index"
                    >
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
        <el-table-column label="标识符" prop="identifier"> </el-table-column>
        <el-table-column label="标签" prop="name"> </el-table-column>
        <el-table-column label="描述" prop="describe"> </el-table-column>
        <el-table-column align="right">
          <!-- eslint-disable -->
        </el-table-column>
      </el-table>
      <div
        class="searchline"
        style="
          height: 60px;
          background-color: #a6d9f4;
          border-radius: 15px;
          padding: 10px;
          display: flex;
          align-items: center;
        "
      >
        <div style="margin-left: 45%;color: white;font-size: large;">共享域概念语义关系</div>
      </div>
      <div id="chart_graph4"></div>
      <div
        class="searchline"
        style="
          height: 60px;
          background-color: #a6d9f4;
          border-radius: 15px;
          padding: 10px;
          display: flex;
          align-items: center;
        "
        v-if="showGraph1"
      >
      <div style="margin-left: 42%;color: white;font-size: large;">子域属性向共享域的语义对齐</div>
    </div>
      <div id="chart_graph1" v-if="showGraph1"></div>
      <div>
        <div
          class="searchline"
          style="
            height: 60px;
            background-color: #a6d9f4;
            border-radius: 15px;
            padding: 10px;
            display: flex;
            align-items: center;
          "
          v-if="showGraph2"
        >
        <div style="margin-left: 42%;color: white;font-size: large;">子域属性值向共享域的语义对齐</div>
      </div>
        <div id="chart_graph5" v-if="showGraph2"></div>
      </div>
    </div>
  </div>
</template>

<script>
import * as echarts from "echarts";
export default {
  props: {
    parentData: "",
    wdf: "",
  },
  data() {
    return {
      // showSubdomain:true,
      showValue: false,
      showGraph2: true,
      showGraph1: true,
      dialogobject_class: [],
      sub_domain_info: [],
      sub_domain_infoValue: [],
      graphData1: {
        nodes: [],
        links: [],
      },
      graphData2: {
        nodes: [],
        links: [],
      },
      graphData3: {
        nodes: [],
        links: [],
      },
      // 演化的数据
      // 模型演化表格列表
      model_evolution_tables: [],
      //模型
      model_tree_data: [],
      model_tree_evolution_data: [],
      model_message: null,
      // 子域
      // 子域演化信息表格列表
      sub_domain_evolution_tables: [],
      sub_domain_message: null,
      sub_domain_tree_evolution: [],
    };
  },
  mounted() {
    this.getOptionSearchNews();
    // if (!this.timerStarted) {
    //     this.timerStarted = true;
    //     setTimeout(() => {
    //       this.updateChart3(this.graphData3);
    //     }, 500);
    //   }
    this.disposeAllEchartsInstances();
  },
  beforeDestroy() {
    // 获取当前组件中所有 echarts 实例并销毁它们
    this.disposeAllEchartsInstances();
  },
  methods: {
    disposeAllEchartsInstances() {
      const chartDom = document.getElementById("chart_graph1");
      if (chartDom) {
        const chartInstance = echarts.getInstanceByDom(chartDom);
        if (chartInstance) {
          chartInstance.dispose();
        }
      }
    },
    backsearch() {
      if (this.wdf && this.wdf === "wdf") {
        this.$router.push({ path: "/Demonstration/Co_evolution" });
      } else {
        this.$emit("backsearch");
      }
    },
    getOptionSearchNews() {
      let vm = this;
      this.$axios
        .get("http://localhost:5000/user/getDataShareInfo", {
          params: {
            identifier: this.parentData,
          },
        })
        .then((Response) => {
          // console.log(Response);
          this.dialogobject_class = Response.data.data.data_element_info;
          if (!Response.data.data.sub_domain_info) {
            this.showValue = false;
          } else {
            this.showValue = true;
            this.sub_domain_info = Response.data.data.sub_domain_info;
          }
          this.graphData1.nodes = Response.data.data.graph1.data;
          this.graphData1.links = Response.data.data.graph1.links;
          if (this.graphData1.nodes.length == 0) {
            vm.showGraph1 = false;
            this.updateChart1(this.graphData1);
          } else {
            vm.showGraph1 = true;
            this.updateChart1(this.graphData1);
          }

          // console.log(this.graphData1.nodes);
          this.graphData2.nodes = Response.data.data.graph2.data;
          this.graphData2.links = Response.data.data.graph2.links;

          this.graphData3.nodes = Response.data.data.graph3.data;
          this.graphData3.links = Response.data.data.graph3.links;

          this.updateChart3(this.graphData3);
          // setTimeout(() => {
          //   this.updateChart3(this.graphData3);
          // }, 10);
          //   console.log(this.graphData2.nodes)
          if (this.graphData2.nodes.length == 0) {
            vm.showGraph2 = false;
            this.updateChart2(this.graphData2);
          } else {
            vm.showGraph2 = true;
            this.updateChart2(this.graphData2);
          }
        });
    },
    updateChart1(graphData) {
      var chartDom = document.getElementById("chart_graph1");
      // 检查是否已经存在图表实例
      // var existingChart = echarts.getInstanceByDom(chartDom);
      // if (existingChart) {
      //   // 如果已经存在，销毁它
      //   existingChart.dispose();
      // }
      var myChart = echarts.init(chartDom);
      var option = {
        tooltip: {
          formatter: function (params) {
            const nodeData = params.data;
            let tooltipContent = `名称：${nodeData.name}<br/>`;

            // 检查描述是否存在
            if (nodeData.description) {
              tooltipContent += `描述：${nodeData.description}<br/>`;
            }

            // 检查创建人员ID是否存在
            if (nodeData.personId) {
              tooltipContent += `创建人员ID：${nodeData.personId}<br/>`;
            }
            return tooltipContent;
          },
        },
        title: {
          textStyle: {
            fontWeight: "lighter",
          },
        },
        // animationDurationUpdate 设置图表更新动画的持续时间
        animationDurationUpdate: 1500,
        // animationEasingUpdate 设置图表更新动画的缓动效果
        animationEasingUpdate: "quinticInOut",
        legend: {
          x: "center",
          show: true,
          data: ["概念", "列", "表", "子域"],
        },
        series: [
          {
            type: "graph",
            layout: "none",
            symbolSize: 60,
            edgeSymbol: ["circle", "arrow"],
            edgeSymbolSize: [6, 10],
            edgeLabel: {
              normal: {
                show: true,
                textStyle: {
                  fontSize: 12,
                },
                formatter: "{c}",
              },
            },
            force: {
              repulsion: 2500,
              edgeLength: [10, 100],
            },
            focusNodeAdjacency: true,
            draggable: true,
            roam: true,
            categories: [
              {
                name: "概念",
              },
              {
                name: "列",
              },
              {
                name: "表",
              },
              {
                name: "子域",
              },
            ],
            label: {
              normal: {
                show: true,
                textStyle: {
                  fontSize: 15,
                },
              },
            },
            lineStyle: {
              normal: {
                opacity: 0.9,
                width: 1,
                curveness: 0,
              },
            },
            nodes: graphData.nodes.map((node) => {
              if (node.category === 0) {
                return {
                  ...node,
                  symbol: "rect",
                  symbolSize: [100, 40],
                };
              }
              return node;
            }),
            links: graphData.links,
          },
        ],
      };
      myChart.setOption(option);
    },
    updateChart2(graphData) {
      var myChart = echarts.init(document.getElementById("chart_graph5"));
      var option = {
        tooltip: {
          formatter: function (params) {
            const nodeData = params.data;
            let tooltipContent = `名称：${nodeData.name}<br/>`;

            // 检查描述是否存在
            if (nodeData.description) {
              tooltipContent += `描述：${nodeData.description}<br/>`;
            }

            // 检查创建人员ID是否存在
            if (nodeData.personId) {
              tooltipContent += `创建人员ID：${nodeData.personId}<br/>`;
            }
            return tooltipContent;
          },
        },
        title: {
          textStyle: {
            fontWeight: "lighter",
          },
        },
        // animationDurationUpdate 设置图表更新动画的持续时间
        animationDurationUpdate: 1500,
        // animationEasingUpdate 设置图表更新动画的缓动效果
        animationEasingUpdate: "quinticInOut",
        legend: {
          x: "center",
          show: true,
          data: ["列", "可枚举值", "值含义"],
        },
        series: [
          {
            type: "graph",
            layout: "none",
            symbolSize: 60,
            edgeSymbol: ["circle", "arrow"],
            edgeSymbolSize: [6, 10],
            edgeLabel: {
              normal: {
                show: true,
                textStyle: {
                  fontSize: 12,
                },
                formatter: "{c}",
              },
            },
            force: {
              repulsion: 2500,
              edgeLength: [10, 100],
            },
            focusNodeAdjacency: true,
            draggable: true,
            roam: true,
            categories: [
              {
                name: "列",
              },
              {
                name: "可枚举值",
              },
              {
                name: "值含义",
              },
            ],
            label: {
              normal: {
                show: true,
                textStyle: {
                  fontSize: 15,
                },
              },
            },
            lineStyle: {
              normal: {
                opacity: 0.9,
                width: 1,
                curveness: 0,
              },
            },
            nodes: graphData.nodes.map((node) => {
              if (node.category === 2) {
                return {
                  ...node,
                  symbol: "rect",
                  symbolSize: [80, 40],
                };
              }
              return node;
            }),
            links: graphData.links,
          },
        ],
      };
      myChart.setOption(option, true);
    },
    updateChart3(graphData) {
      var chartDom = document.getElementById("chart_graph4");
      // var existingChart = echarts.getInstanceByDom(chartDom);
      // if (existingChart) {
      //     // 如果已经存在，销毁它
      //     existingChart.dispose();
      // }
      var myChart = echarts.init(chartDom);
      var option = {
        tooltip: {
          formatter: function (params) {
            const nodeData = params.data;
            let tooltipContent = `名称：${nodeData.name}<br/>`;

            // 检查描述是否存在
            if (nodeData.description) {
              tooltipContent += `描述：${nodeData.description}<br/>`;
            }

            // 检查创建人员ID是否存在
            if (nodeData.personId) {
              tooltipContent += `创建人员ID：${nodeData.personId}<br/>`;
            }
            return tooltipContent;
          },
        },
        title: {
          textStyle: {
            fontWeight: "lighter",
          },
        },
        // animationDurationUpdate 设置图表更新动画的持续时间
        animationDurationUpdate: 1500,
        // animationEasingUpdate 设置图表更新动画的缓动效果
        animationEasingUpdate: "quinticInOut",
        legend: {
          x: "center",
          show: true,
          data: [
            "对象类",
            "属性",
            "概念域",
            "数据元概念",
            "值域",
            "数据元",
            "可允许值",
            "值含义",
            "值域组",
          ],
        },
        series: [
          {
            type: "graph",
            layout: "none",
            symbolSize: 60,
            edgeSymbol: ["circle", "arrow"],
            edgeSymbolSize: [6, 10],
            edgeLabel: {
              normal: {
                show: true,
                textStyle: {
                  fontSize: 12,
                },
                formatter: "{c}",
              },
            },
            force: {
              repulsion: 2500,
              edgeLength: [10, 100],
            },
            focusNodeAdjacency: true,
            draggable: true,
            roam: true,
            categories: [
              {
                name: "对象类",
              },
              {
                name: "属性",
              },
              {
                name: "概念域",
              },
              {
                name: "数据元概念",
              },
              {
                name: "值域",
              },
              {
                name: "数据元",
              },
              {
                name: "可允许值",
              },
              {
                name: "值含义",
              },
              {
                name: "值域组",
              },
            ],
            label: {
              normal: {
                show: true,
                textStyle: {
                  fontSize: 15,
                },
              },
            },
            lineStyle: {
              normal: {
                opacity: 0.9,
                width: 1,
                curveness: 0,
              },
            },
            nodes: graphData.nodes,
            // nodes: graphData.nodes.map((node) => {
            //   if (node.category === 2) {
            //     return {
            //       ...node,
            //       symbol: "roundRect",
            //       symbolSize: [80, 40],
            //     };
            //   }
            //   return node;
            // }),
            links: graphData.links,
          },
        ],
      };
      myChart.setOption(option, true);
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
  margin-left: 45%;
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