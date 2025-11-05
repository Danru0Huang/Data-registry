<template>
    <div class="box">
        <el-main>
            <el-card class="box-card">

                <!-- 选择查询模型 -->
                <div slot="header" class="clearfix input-container" style="text-align: center;">
                    <el-select v-model="selectedModelName" filterable @change="search" placeholder="请选择查询模型">
                        <el-option v-for="item in optionsOfModelName" :key="item.value" :label="item.label"
                            :value="item.value"></el-option>
                    </el-select>
                </div>

                <el-row :gutter="5">
                    <el-col :span="15">
                        <div class="chat-container" :id="chartId"></div>
                    </el-col>

                    <!-- 暂时未知 -->
                    <el-col :span="9">
                        <el-form label-position="left" inline class="demo-table-expand" v-show="showDescriptions">
                            <el-form-item v-for="(item, index) in descriptionsData" :key="index">
                                <el-descriptions :column="1" border>
                                    <el-descriptions-item label="类">
                                        <el-tag>
                                            {{ item.name }}
                                        </el-tag>
                                    </el-descriptions-item>
                                    <el-divider content-position="center">属性</el-divider>
                                </el-descriptions>
                                <el-divider content-position="center">属性</el-divider>
                                <el-descriptions :column="2">
                                    <el-descriptions-item v-for="(itemValue, indexValue) in item.values" :key="indexValue">
                                        <template slot="label">
                                            <i class="el-icon-s-data"></i>
                                        </template>
                                        {{ itemValue.value }}
                                    </el-descriptions-item>
                                </el-descriptions>
                                <el-divider><i class="el-icon-crop"></i></el-divider>
                            </el-form-item>
                        </el-form>
                    </el-col>
                </el-row>
            </el-card>
        </el-main>
    </div>
</template>

<script>
import * as echarts from 'echarts';
export default {
    data() {
        return {
            activeMenu: '',
            selectedModelName: '',
            optionsOfModelName: [],
            graphData: [],
            graphLinks: [],
            chartId: 'guanxi',
            tableData: [],
            showTable: false,
            dialogVisible: false,
            nodeDetails: {},
            categories: ["模型", "模型类", "模型属性"],
            descriptionsData: [],
            showDescriptions: false
        }
    },

    mounted() {
        this.getOptionsOfModelName().then(() => {
            if (this.optionsOfModelName.length > 0) {
                this.selectedModelName = this.optionsOfModelName[0].value;
                this.searchfirstModel();
            }
        }).catch(error => {
            console.error(error);
        });
    },

    methods: {
        // 查询函数
        search() {
            var vm = this;
            this.$axios.get('http://localhost:5000/search/model/graphOfName', {
                params: {
                    name: this.selectedModelName,
                    label: "模型"
                }
            })
                .then(function (response) {
                    if (response.data.data.length == 0) {
                        vm.openError();
                    } else {
                        vm.graphData = response.data.data.map(function (node, idx) {
                            node.id = idx;
                            return node;
                        });
                        vm.graphLinks = response.data.links;
                        vm.updateChart(vm.chartId, vm.graphData, vm.graphLinks);
                        // vm.tableData = response.data.tableData;
                        // vm.showTable = true;
                        vm.descriptionsData = response.data.list;
                        vm.showDescriptions = true;
                    }

                })
                .catch(function (error) {
                    console.log(error);
                    // 获取失败消息提示
                    this.$message({
                        showClose: true,
                        message: "查询失败",
                        type: 'error',
                        duration: 1000
                    })
                },

                );
        },
        searchfirstModel() {
            var vm = this;
            this.$axios.get('http://localhost:5000/search/model/graphOfName', {
                params: {
                    name: this.optionsOfModelName[0].value,
                    label: "模型"
                }
            })
                .then(function (response) {
                    if (response.data.data.length == 0) {
                        vm.openError();
                    } else {
                        vm.graphData = response.data.data.map(function (node, idx) {
                            node.id = idx;
                            return node;
                        });
                        vm.graphLinks = response.data.links;
                        vm.updateChart(vm.chartId, vm.graphData, vm.graphLinks);
                        // vm.tableData = response.data.tableData;
                        // vm.showTable = true;
                        vm.descriptionsData = response.data.list;
                        vm.showDescriptions = true;
                    }

                })
                .catch(function (error) {
                    console.log(error);
                    // 获取失败消息提示
                    vm.$message({
                        showClose: true,
                        message: "查询失败",
                        type: 'error',
                        duration: 1000
                    })
                },

                );
        },
        openError() {
            this.$message.error('未查询到结果，请检查输入查询内容是否正确！');
        },
        andleClose(done) {
            this.$confirm('确认关闭？')
                .then(_ => {
                    done();
                })
                .catch(_ => { });
        },
        showNodeResult(nodeDetails) {
            this.nodeDetails = nodeDetails;
            this.dialogVisible = true;
        },
        getOptionsOfModelName() {
            return new Promise((resolve, reject) => {
                this.$axios.get('http://localhost:5000/search/model/getModelTypeOptions')
                    .then(response => {
                        this.optionsOfModelName = response.data.data;
                        resolve(); // 表示异步请求成功
                    })
                    .catch(error => {
                        console.error(error);
                        reject(error); // 表示异步请求失败
                    });
            });
        },
        updateChart(chartId, graphData, graphLinks) {
            var myChart = echarts.init(document.getElementById(chartId));
            var option = {
                title: {
                    textStyle: {
                        fontWeight: "lighter"
                    }
                },
                // animationDurationUpdate 设置图表更新动画的持续时间
                animationDurationUpdate: 1500,
                // animationEasingUpdate 设置图表更新动画的缓动效果
                animationEasingUpdate: 'quinticInOut',
                legend: {
                    x: "center",
                    show: true,
                    data: ["模型", "模型类", "模型属性"]
                },
                series: [{
                    type: 'graph',
                    layout: 'force',
                    symbolSize: 60,
                    edgeSymbol: ['circle', 'arrow'],
                    edgeSymbolSize: [4, 4],
                    edgeLabel: {
                        normal: {
                            show: true,
                            textStyle: {
                                fontSize: 12
                            },
                            formatter: "{c}"
                        }
                    },
                    force: {
                        repulsion: 2500,
                        edgeLength: [10, 100]
                    },
                    focusNodeAdjacency: true,
                    draggable: true,
                    roam: true,
                    categories: [{
                        name: '模型'
                    },
                    {
                        name: '模型类'
                    },
                    {
                        name: '模型属性'
                    }
                    ],
                    label: {
                        normal: {
                            show: true,
                            textStyle: {
                                fontSize: 15
                            },
                        }
                    },
                    lineStyle: {
                        normal: {
                            opacity: 0.9,
                            width: 1,
                            curveness: 0.3
                        }
                    },
                    nodes: graphData,
                    links: graphLinks,
                }]
            };
            myChart.setOption(option, true);
            // myChart.off('click');
            // myChart.on("click", function(params) {
            // 	var name = params.name
            // 	var category_id = params.data.category;
            // 	var category = app.categories[category_id];
            // 	axios.get('/search_node', {
            // 			params: {
            // 				category: category,
            // 				name: name
            // 			}
            // 		})
            // 		.then(function(response) {
            // 			var nodeDetails = response.data; // 实际的查询结果数据
            // 			app.showNodeResult(nodeDetails);

            // 		})
            // 		.catch(function(error) {
            // 			console.log(error);
            // 		});
            // });
        }
    }
}




</script>

<style scoped>
.box {
    margin-left: 250px;
}

.el-header {
    background-color: #B3C0D1;
    color: #333;
    line-height: 60px;
}

.el-aside {
    color: #333;
}

.chat-container {
    height: 90vh;
    padding: 5px;
    /* display: flex; */
    flex-direction: column;
}

.message-container {
    flex: 1;
    max-height: calc(100% - 60px);
    overflow-y: auto;
    padding-bottom: 10px;
}

.message {
    display: flex;
    justify-content: flex-start;
    align-items: flex-start;
    margin-bottom: 10px;
}

.message.user .message-bubble {
    margin-left: auto;
    background-color: #DCF8C6;
    color: #000;
}

.message.bot .message-bubble {
    margin-right: auto;
    background-color: #F0F0F0;
    color: #000;
}

.message-bubble {
    max-width: 70%;
    padding: 10px;
    border-radius: 10px;
    background: #fff;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.input-container {

    gap: 2px;
    /* margin-top: 10px; */
}

.input-container .el-input {
    flex: 2;
    width: 200px;
    border-radius: 20px;
    padding: 5px 5px;
}

.input-container button {
    flex: none;
    /* border-radius: 20%; */
    width: 100px;
    height: 40px;
}

.text {
    font-size: 14px;
}

.item {
    margin-bottom: 18px;
}

.clearfix:before,
.clearfix:after {
    display: table;
    content: "";
}

.clearfix:after {
    clear: both
}

.box-card {
    width: center;

}
</style>