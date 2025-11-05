<template>
  <div class="box-contain">
    <el-row>
      <el-col :span="2" style="height: 100%;">
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
    <div class="searchline" style="
        height: 60px;
        background-color: #a6d9f4;
        border-radius: 15px;
        padding: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-top:8px ;
      ">
      <i class="el-icon-top" style="font-size: 4vw;width: 30%;color: white;"></i>
      <i class="el-icon-top" style="font-size: 4vw;width: 30%;color: white;"></i>
      <i class="el-icon-top" style="font-size: 4vw;color: white;"></i>
    </div>
    <el-row>
      <el-col :span="2" style="height: 100%;">
        <div id="showinfo">
          <p>子</p>
          <p>域</p>
        </div>
      </el-col>
      <el-col :span="22">
        <div style="height: 50vh; width: 100%; overflow-y: auto;">
          <div class="sub_Domain" v-for="(item1, index1) in sub_Domain_value" :key="index1">
            <el-card class="card" style="height: 300px; width: 30%" v-for="(item, index) in item1" :key="index">
              <el-descriptions :title="item.title" direction="vertical" :column="4" border>
                <el-descriptions-item label="属性数">{{ item.num_attribute }}</el-descriptions-item>
                <el-descriptions-item label="属性值数">{{ item.num_attribute_value }}</el-descriptions-item>
                <el-descriptions-item label="演化数">{{ item.num_evolution }}</el-descriptions-item>
                <el-descriptions-item label="表数量">{{ item.num_table }}</el-descriptions-item>
                <el-descriptions-item label="描述">
                  {{ item.describe }}
                </el-descriptions-item>
              </el-descriptions>
            </el-card>
          </div>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import * as echarts from "echarts";
import * as d3 from 'd3-hierarchy';
export default {
  data() {
    return {
      rawData: [],
      sub_Domain_value: [],
    }
  },
  mounted() {
    this.getAllGraph();
    this.getIndexSubDomain();
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
          index: seriesData.length
        });
        for (var key in source) {
          if (source.hasOwnProperty(key) && !key.match(/^\$/)) {
            var path = basePath + '.' + key;
            convert(source[key], path, depth + 1);
          }
        }
      }
      convert(rawData, 'option', 0);
      return {
        seriesData: seriesData,
        maxDepth: maxDepth
      };
    },
    initChart(seriesData, maxDepth) {
      var chartDom = document.getElementById('chartIdAllGraph');
      var myChart = echarts.init(chartDom);
      var option;
      var displayRoot = stratify();
      function stratify() {
        return d3
          .stratify()
          .parentId(function (d) {
            return d.id.substring(0, d.id.lastIndexOf('.'));
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
        var nodePath = api.value('id');
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
            .slice(nodePath.lastIndexOf('.') + 1)
            .split(/(?=[A-Z][^A-Z])/g)
            .join('\n')
          : '';
        var z2 = api.value('depth') * 2;

        var shape;
        if (node.depth === 0) { // 最外层节点
          var rectWidth = window.innerWidth; // 获取视窗宽度
          var rectHeight = window.innerHeight; // 获取视窗高度

          shape = {
            x: node.x - rectWidth / 2, // 根据矩形中心点计算左上角坐标
            y: node.y - rectHeight / 2,
            width: rectWidth, // 设置矩形宽度
            height: rectHeight // 设置矩形高度
          };
        } else {
          // 内部节点保持圆形
          shape = {
            cx: node.x,
            cy: node.y,
            r: node.r
          };
        }

        return {
          type: node.depth === 0 ? 'rect' : 'circle',
          focus: focus,
          shape: shape,
          transition: ['shape'],
          z2: z2,
          textContent: {
            type: 'text',
            style: {
              text: nodeName,
              fontFamily: 'Arial',
              width: node.r * 1.3,
              overflow: 'truncate',
              fontSize: node.r / 3
            },
            emphasis: {
              style: {
                overflow: null,
                fontSize: Math.max(node.r / 3, 12)
              }
            }
          },
          textConfig: {
            position: 'inside'
          },
          style: {
            fill: api.visual('color')
          },
          emphasis: {
            style: {
              fontFamily: 'Arial',
              fontSize: 12,
              shadowBlur: 20,
              shadowOffsetX: 3,
              shadowOffsetY: 5,
              shadowColor: 'rgba(0,0,0,0.3)'
            }
          }
        };
      }


      option = {
        dataset: {
          source: seriesData
        },
        tooltip: {},
        visualMap: [
          {
            show: false,
            min: 0,
            max: maxDepth,
            dimension: 'depth',
            inRange: {
              color: ['#006edd', '#e0ffff']
            }
          }
        ],
        hoverLayerThreshold: Infinity,
        series: {
          type: 'custom',
          renderItem: renderItem,
          progressive: 0,
          coordinateSystem: 'none',
          encode: {
            tooltip: 'value',
            itemName: 'id'
          }
        }
      };
      myChart.setOption(option);
      myChart.on('click', { seriesIndex: 0 }, function (params) {
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
            source: seriesData
          }
        });
      }
      // Reset: click on the blank area.
      myChart.getZr().on('click', function (event) {
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
  }
}
</script>

<style>
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