<template>
  <div class="box-contain">
    <el-row>
      <el-col :span="2" style="height: 100%">
        <div id="showname">
          <p>共</p>
          <p>享</p>
          <p>域</p>
        </div>
      </el-col>
      <el-col :span="22">
        <div id="chartIdAllGraph" style="height: 100vh; width: 100%"></div>
      </el-col>
    </el-row>
    <div
      class="searchline"
      style="
        height: 60px;
        background-color: #a6d9f4;
        border-radius: 15px;
        padding: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-top: 8px;
      "
    >
      <i
        class="el-icon-top"
        style="font-size: 4vw; width: 30%; color: white"
      ></i>
      <i
        class="el-icon-top"
        style="font-size: 4vw; width: 30%; color: white"
      ></i>
      <i class="el-icon-top" style="font-size: 4vw; color: white"></i>
    </div>
    <!-- <el-row>
        <el-col :span="24">
           
        </el-col>
      </el-row> -->
    <el-row>
      <el-col :span="2" style="height: 100%">
        <div id="showinfo">
          <p>子</p>
          <p>域</p>
        </div>
      </el-col>
      <el-col :span="22">
        <div style="height: 50vh; width: 100%; overflow-y: auto">
          <div
            class="sub_Domain"
            v-for="(item1, index1) in sub_Domain_value"
            :key="index1"
          >
            <el-card
              class="card"
              style="height: 300px; width: 30%"
              v-for="(item, index) in item1"
              :key="index"
            >
              <el-descriptions
                :title="item.title"
                direction="vertical"
                :column="4"
                border
              >
                <el-descriptions-item label="属性数">{{
                  item.num_attribute
                }}</el-descriptions-item>
                <el-descriptions-item label="属性值数">{{
                  item.num_attribute_value
                }}</el-descriptions-item>
                <el-descriptions-item label="演化数">{{
                  item.num_evolution
                }}</el-descriptions-item>
                <el-descriptions-item label="表数量">{{
                  item.num_table
                }}</el-descriptions-item>
                <el-descriptions-item label="描述">
                  {{ item.describe }}
                </el-descriptions-item>
              </el-descriptions>
            </el-card>
          </div>
        </div>
      </el-col>
    </el-row>
    <el-divider></el-divider>
    <el-row>
      <el-col :span="24">
        <div id="chartIdModelGraph" style="height: 60vh; width: 100%"></div>
      </el-col>
    </el-row>
    <el-divider></el-divider>
    <el-row>
      <el-col :span="24">
        <div id="chartIdModelGraph1" style="height: 60vh; width: 100%"></div>
      </el-col>
    </el-row>
    <el-divider></el-divider>
    <el-row>
      <el-col :span="24">
        <div id="chartIdModelData" style="height: 60vh; width: 100%"></div>
      </el-col>
    </el-row>
    <el-divider direction="vertical"></el-divider>
    <el-row>
      <el-col :span="24">
        <div id="chartIdModelData1" style="height: 60vh; width: 100%"></div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import * as echarts from "echarts";
import * as d3 from "d3-hierarchy";
export default {
  data() {
    return {
      graphData: [],
      graphLinks: [],
      graphData2: [],
      graphLinks2: [],
      categories: ["模型", "模型类", "模型属性"],
      graphData1: [],
      rawData: [],
      sub_Domain_value: [],
    };
  },
  mounted() {
    this.getAllGraph();
    this.getIndexSubDomain();
    this.search1();
    this.updateChartOfModelGraph(this.graphData, this.graphLinks);
    this.search2();
    this.updateChartOfModelGraph1(this.graphData2, this.graphLinks2);
    this.search3();
    // this.updateBarChart();
    this.updatePieChart();
  },
  methods: {
    updataChartAllGraph() {
      const dataWrap = this.prepareData(this.rawData);
      this.initChart(dataWrap.seriesData, dataWrap.maxDepth);
      option && myChart.setOption(option);
    },
    prepareData(rawData) {
      const seriesData = [];
      let maxDepth = 0;
      function convert(source, basePath, depth) {
        if (source == null) {
          return;
        }
        if (maxDepth > 5) {
          return;
        }
        maxDepth = Math.max(depth, maxDepth);
        seriesData.push({
          id: basePath,
          value: source.$count,
          depth: depth,
          index: seriesData.length,
        });
        for (var key in source) {
          if (source.hasOwnProperty(key) && !key.match(/^\$/)) {
            var path = basePath + "." + key;
            convert(source[key], path, depth + 1);
          }
        }
      }
      convert(rawData, "option", 0);
      return {
        seriesData: seriesData,
        maxDepth: maxDepth,
      };
    },
    initChart(seriesData, maxDepth) {
      var chartDom = document.getElementById("chartIdAllGraph");
      var myChart = echarts.init(chartDom);
      var option;
      var displayRoot = stratify();
      function stratify() {
        return d3
          .stratify()
          .parentId(function (d) {
            return d.id.substring(0, d.id.lastIndexOf("."));
          })(seriesData)
          .sum(function (d) {
            return d.value || 0;
          })
          .sort(function (a, b) {
            return b.value - a.value;
          });
      }
      function overallLayout(params, api) {
        var context = params.context;
        d3
          .pack()
          .size([api.getWidth() - 2, api.getHeight() - 2])
          .padding(3)(displayRoot);
        context.nodes = {};
        displayRoot.descendants().forEach(function (node, index) {
          context.nodes[node.id] = node;
        });
      }
      function renderItem(params, api) {
        var context = params.context;
        // Only do that layout once in each time `setOption` called.
        if (!context.layout) {
          context.layout = true;
          overallLayout(params, api);
        }
        var nodePath = api.value("id");
        var node = context.nodes[nodePath];
        if (!node) {
          // Reder nothing.
          return;
        }

        var isLeaf = !node.children || !node.children.length;
        var focus = new Uint32Array(
          node.descendants().map(function (node) {
            return node.data.index;
          })
        );
        var nodeName = isLeaf
          ? nodePath
              .slice(nodePath.lastIndexOf(".") + 1)
              .split(/(?=[A-Z][^A-Z])/g)
              .join("\n")
          : "";
        var z2 = api.value("depth") * 2;

        var shape;
        if (node.depth === 0) {
          // 最外层节点
          var rectWidth = window.innerWidth; // 获取视窗宽度
          var rectHeight = window.innerHeight; // 获取视窗高度

          shape = {
            x: node.x - rectWidth / 2, // 根据矩形中心点计算左上角坐标
            y: node.y - rectHeight / 2,
            width: rectWidth, // 设置矩形宽度
            height: rectHeight, // 设置矩形高度
          };
        } else {
          // 内部节点保持圆形
          shape = {
            cx: node.x,
            cy: node.y,
            r: node.r,
          };
        }

        return {
          type: node.depth === 0 ? "rect" : "circle",
          focus: focus,
          shape: shape,
          transition: ["shape"],
          z2: z2,
          textContent: {
            type: "text",
            style: {
              text: nodeName,
              fontFamily: "Arial",
              width: node.r * 1.3,
              overflow: "truncate",
              fontSize: node.r / 3,
            },
            emphasis: {
              style: {
                overflow: null,
                fontSize: Math.max(node.r / 3, 12),
              },
            },
          },
          textConfig: {
            position: "inside",
          },
          style: {
            fill: api.visual("color"),
          },
          emphasis: {
            style: {
              fontFamily: "Arial",
              fontSize: 12,
              shadowBlur: 20,
              shadowOffsetX: 3,
              shadowOffsetY: 5,
              shadowColor: "rgba(0,0,0,0.3)",
            },
          },
        };
      }

      option = {
        dataset: {
          source: seriesData,
        },
        tooltip: {},
        visualMap: [
          {
            show: false,
            min: 0,
            max: maxDepth,
            dimension: "depth",
            inRange: {
              color: ["#006edd", "#e0ffff"],
            },
          },
        ],
        hoverLayerThreshold: Infinity,
        series: {
          type: "custom",
          renderItem: renderItem,
          progressive: 0,
          coordinateSystem: "none",
          encode: {
            tooltip: "value",
            itemName: "id",
          },
        },
      };
      myChart.setOption(option);
      myChart.on("click", { seriesIndex: 0 }, function (params) {
        drillDown(params.data.id);
      });
      function drillDown(targetNodeId) {
        displayRoot = stratify();
        if (targetNodeId != null) {
          displayRoot = displayRoot.descendants().find(function (node) {
            return node.data.id === targetNodeId;
          });
        }
        // A trick to prevent d3-hierarchy from visiting parents in this algorithm.
        displayRoot.parent = null;
        myChart.setOption({
          dataset: {
            source: seriesData,
          },
        });
      }
      // Reset: click on the blank area.
      myChart.getZr().on("click", function (event) {
        if (!event.target) {
          drillDown();
        }
      });
    },
    getAllGraph() {
      var vm = this;
      this.$axios
        .get("http://localhost:5000/index/getIndexGraph")
        .then(function (response) {
          // console.log(response.data)
          vm.rawData = response.data.data;
          vm.updataChartAllGraph();
        })
        .catch(function (error) {
          console.log(error);
        });
    },
    getIndexSubDomain() {
      var vm = this;
      this.$axios
        .get("http://localhost:5000/index/getIndexSubDomain")
        .then(function (response) {
          console.log(response.data);
          var dataArray = response.data.data;
          var tempArray = [];
          vm.sub_Domain_value = [];

          // 遍历响应数据
          for (var i = 0; i < dataArray.length; i++) {
            tempArray.push(dataArray[i]);
            // 每遍历三个对象，就将临时数组添加到 sub_Domain_value 中，并清空临时数组
            if ((i + 1) % 3 === 0 || i === dataArray.length - 1) {
              vm.sub_Domain_value.push(tempArray);
              tempArray = []; // 清空临时数组
            }
          }
        })
        .catch(function (error) {
          console.log(error);
        });
    },

    //专利信息模型图谱数据获取
    search1() {
      var vm = this;
      this.$axios
        .get("http://localhost:5000/search/model/graphOfName", {
          params: {
            // name: this.searchInput,
            name: "专利信息模型",
            label: "模型",
          },
        })
        .then(function (response) {
          // console.log(response)
          if (response.data.data.length == 0) {
            vm.openError();
          } else {
            vm.graphData = response.data.data.map(function (node, idx) {
              node.id = idx;
              return node;
            });
            vm.graphLinks = response.data.links;
            vm.updateChartOfModelGraph(vm.graphData, vm.graphLinks);
          }
        })
        .catch(function (error) {
          console.log(error);
        });
    },
    //专利法律状态案例图谱数据获取
    search2() {
      var vm = this;
      this.$axios
        .get("http://localhost:5000/search/mdr/getGraphOfMDR", {
          params: {
            identifier: "DEL029",
          },
        })
        .then(function (response) {
          if (response.data.data.length == 0) {
            vm.openError();
          } else {
            // console.log(response.data.data);
            vm.graphData2 = response.data.data.map(function (node, idx) {
              node.id = idx;
              return node;
            });
            vm.graphLinks2 = response.data.links;
            vm.updateChartOfModelGraph1(vm.graphData2, vm.graphLinks2);
          }
        })
        .catch(function (error) {
          console.log(error);
        });
    },
    //模型数量数据获取
    search3() {
      var vm = this;
      this.$axios
        .get("http://localhost:5000/index_show")
        .then(function (response) {
          // console.log(response)
          if (
            response.data &&
            response.data.data &&
            response.data.data.length > 0
          ) {
            vm.openError();
          } else {
            // 处理数据
            vm.processData(response.data.message);
          }
        })
        .catch(function (error) {
          console.log(error);
        });
    },
    openError() {
      this.$message.error("未查询到结果，请检查输入查询内容是否正确！");
    },
    //数据处理
    processData(data) {
      this.graphData1 = data
        .filter((item) => {
          // 选择要展示的标签
          const selectedLabels = [
            "模型",
            "模型类",
            "对象类",
            "属性",
            "模型属性",
            "概念域",
            "值域",
            "子域",
            "数据元",
            "数据元概念",
          ]; // 替换为您想要展示的标签数组
          // 过滤数据，只保留具有选定标签的项
          return selectedLabels.includes(item.label);
        })
        .map((item) => ({
          name: item.label,
          value: item.node_count,
        }));

      // 调用更新图表的方法
      this.updateBarChart(this.graphData1);
      this.updatePieChart(this.graphData1);
    },

    updateChartOfModelGraph(graphData, graphLinks) {
      var divModelGraph = document.getElementById("chartIdModelGraph");
      // 使用 echarts 初始化图表
      divModelGraph?.removeAttribute("_echarts_instance_");
      var chartOfModelGraph = echarts.init(divModelGraph);
      // var chartOfModelGraph = echarts.init(divModelGraph);
      var optionOfModelGraph = {
        title: {
          text: "专利信息模型",
          left: "center",
          top: "bottom",
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
          data: ["模型", "模型类", "模型属性"],
        },
        series: [
          {
            type: "graph",
            layout: "force",
            symbolSize: 60,
            edgeSymbol: ["circle", "arrow"],
            edgeSymbolSize: [4, 4],
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
                name: "模型",
              },
              {
                name: "模型类",
              },
              {
                name: "模型属性",
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
                curveness: 0.3,
              },
            },
            nodes: graphData,
            links: graphLinks,
          },
        ],
      };
      chartOfModelGraph.setOption(optionOfModelGraph, true);
    },
    updateChartOfModelGraph1(graphData2, graphLinks2) {
      // Box 2 Graph
      var divModelGraph = document.getElementById("chartIdModelGraph1");
      // 使用 echarts 初始化图表
      divModelGraph?.removeAttribute("_echarts_instance_");
      var chartOfModelGraph = echarts.init(divModelGraph);
      // var chartOfModelGraph = echarts.init(divModelGraph);
      var optionOfModelGraph = {
        title: {
          text: "专利法律状态案例",
          left: "center",
          top: "bottom",
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
            edgeSymbolSize: [4, 4],
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
                curveness: 0.01,
              },
            },
            nodes: graphData2,
            links: graphLinks2,
          },
        ],
      };
      chartOfModelGraph.setOption(optionOfModelGraph, true);
    },
    updateBarChart(data) {
      // 获取柱状图的 DOM 元素
      var barChartElement = document.getElementById("chartIdModelData");
      // console.log(data)
      // 使用 echarts 初始化柱状图
      var barChart = echarts.init(barChartElement);
      //颜色数组
      var colorArray = [
        "#5470C6",
        "#91CC75",
        "#EE6666",
        "#EE9966",
        "#73C0DE",
        "#3BA272",
        "#FCCE10",
        "#E87C25",
        "#B5C334",
        "#FE8463",
      ];
      // 柱状图的配置项
      var option = {
        title: {
          text: "数据总量柱状图(部分)",
          left: "center",
          top: "bottom",
          textStyle: {
            fontWeight: "lighter",
          },
        },
        xAxis: {
          type: "category",
          data: data.map((item) => item.name),
        },
        yAxis: {
          type: "value",
        },
        tooltip: {
          // 添加 tooltip 配置
          trigger: "axis",
          axisPointer: {
            type: "shadow",
          },
          formatter: function (params) {
            return `${params[0].name}: ${params[0].value}`;
          },
        },
        series: [
          {
            data: data.map((item, index) => ({
              value: item.value,
              itemStyle: {
                color: colorArray[index % colorArray.length], // 根据索引选择颜色
              },
            })),
            type: "bar",
          },
        ],
      };

      // 设置柱状图的配置项并渲染图表
      barChart.setOption(option);
    },

    updatePieChart(data) {
      // 获取饼状图的 DOM 元素
      var pieChartElement = document.getElementById("chartIdModelData1");

      // 使用 echarts 初始化饼状图
      var pieChart = echarts.init(pieChartElement);

      // 饼状图的配置项
      var option = {
        title: {
          text: "数据总量扇形图",
          left: "center",
          top: "bottom",
          textStyle: {
            fontWeight: "lighter",
          },
        },
        tooltip: {
          trigger: "item",
          formatter: "{a} <br/>{b}: {c} ({d}%)",
        },
        series: [
          {
            name: "访问来源",
            type: "pie",
            radius: ["40%", "70%"],
            avoidLabelOverlap: false,
            label: {
              show: false,
              position: "center",
            },
            emphasis: {
              label: {
                show: true,
                fontSize: "30",
                fontWeight: "bold",
              },
            },
            labelLine: {
              show: false,
            },
            data: data.map((item) => ({
              name: item.name,
              value: item.value,
            })),
          },
        ],
      };

      // 设置饼状图的配置项并渲染图表
      pieChart.setOption(option);
    },
  },
};
</script>



<style scoped>
.box-contain {
  margin-left: 250px;
}
.sub_Domain {
  display: flex;
  align-items: center;
  justify-content: center;
}
.card {
  margin: 1%;
}
#showname {
  width: 100%;
  height: 100vh;
  background-color: #a6d9f4;
  color: white;
  font-size: 2vw;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
}
#showinfo {
  margin-top: 8px;
  width: 100%;
  height: 306px;
  background-color: #a6d9f4;
  color: white;
  font-size: 2vw;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
}
</style>