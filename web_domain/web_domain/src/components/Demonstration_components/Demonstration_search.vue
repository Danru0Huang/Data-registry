<template>
    <div class="mainpage">
        <div class="modeltree" style="margin-left: 250px;">
            <div slot="header" class="clearfix input-container" style="text-align: center ;height: 60px;background-color:#a6d9f4; border-radius: 15px;
                padding: 10px; display: flex;">
                <el-select v-model="selectedModelName[0]" style="margin-left: 45%;" filterable @change="search"
                    placeholder="请选择查询模型">
                    <el-option v-for="item in optionsOfModelName" :key="item.value" :label="item.label"
                        :value="item.value"></el-option>
                </el-select>
            </div>
            <div class="tree">
                <div id="chart_graph1"></div>
                <!-- 信息模型演化图谱 -->
            </div>
        </div>
        <div class="search" style="margin-left: 250px;">
            <div class="searchline" style="height: 60px;background-color:#a6d9f4; border-radius: 15px;
                padding: 10px; display: flex; align-items: center;">
                <div class="namebox" style="min-width: 100px;">业务领域</div>
                <el-cascader v-model="selectedModelName" :options="optionsOfModelName" filterable clearable @change="search"
                    placeholder="请选择查询模型类名称" style="width:250px">
                </el-cascader>
            </div>
            <div class="showbox" style="margin-left: 20px;">
                <el-table :data="tableDataOfmodel" style="width: 100%">>
                    <el-table-column label="标识符" prop="identifier">
                    </el-table-column>
                    <el-table-column label="概念" prop="name">
                    </el-table-column>
                    <el-table-column label="描述" prop="describe">
                    </el-table-column>
                    <el-table-column align="right">
                        <template slot-scope="scope">
                            <el-button type="primary" icon="el-icon-search" @click="handleClick(scope.row)">查看</el-button>
                            <el-button type="danger" icon="el-icon-delete"
                                @click.native.prevent="deleteRow(scope.$index, tableDataOfmodel)"></el-button>
                        </template>
                    </el-table-column>
                </el-table>
            </div>
        </div>
    </div>
</template>

<script>
import * as echarts from "echarts";
export default {
    data() {
        return {
            nodeidentifier: '',
            // showchart_graph3: true,
            selectedModelName: '',
            tableDataOfmodel: [],
            optionsOfModelName: [],
            this_row: '',
        }
    },
    mounted() {
        this.getOptionsOfModelName().then(() => {
            if (this.optionsOfModelName.length > 0) {
                this.selectedModelName = [this.optionsOfModelName[0].value, this.optionsOfModelName[0].children[0].value];
                this.search()
                this.getModelEvolutionInfo();
                // console.log(this.graphData2.nodes)
                // console.log(this.selectedModelName[0])
            }
        }).catch(error => {
            console.error(error);
        });
        // this.disposeAllEchartsInstances();
    },
    beforeDestroy() {
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
        search() {
            var vm = this;
            this.$axios.get('http://localhost:5000/user/getDataElementOfModelClassOptions', {
                params: {
                    model_class: this.selectedModelName[1],
                }
            })
                .then(function (response) {
                    // console.log(response)
                    if (response.data.data.length == 0) {
                        vm.openError();
                    } else {
                        vm.tableDataOfmodel = response.data.data;
                    }
                })
                .catch(function (error) {
                    console.log(error);
                    // 获取失败消息提示
                    // this.$message({
                    //     showClose: true,
                    //     message: "查询失败",
                    //     type: 'error',
                    //     duration: 1000
                    // })
                },

                );
        },
        getOptionsOfModelName() {
            return new Promise((resolve, reject) => {
                this.$axios.get('http://localhost:5000/user/getModelAndModelClassOptions')
                    .then(response => {
                        // console.log(response)
                        this.optionsOfModelName = response.data.data;
                        resolve(); // 表示异步请求成功
                    })
                    .catch(error => {
                        console.error(error);
                        reject(error); // 表示异步请求失败
                    });
            });
        },
        openError() {
            this.$message.error('未查询到结果，请检查输入查询内容是否正确！');
        },
        handleClick(row) {
            this.this_row = row;
            console.log(row);
            this.sendData();
            // window.open("http://localhost:8080/#/Demonstration/Demonstration_graph", '_blank');
        },
        deleteRow(index, rows) {
            rows.splice(index, 1);
        },
        sendData() {
            this.$emit('send-data', this.this_row, '这是从子组件发送的数据');
        },
        sendData2() {
            this.$emit('send-data2', this.nodeidentifier, '这是从子组件发送的数据');
        },
        updateChart3(treeData) {
            // this.disposeAllEchartsInstances();
            var chartDom = document.getElementById("chart_graph1");
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
            myChart.on("click",
                function (params) {
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
                                this.sendData2();
                            });
                    }
                }.bind(this)
            );
            myChart.setOption(option);
        },
        getModelEvolutionInfoNull() {
            this.$axios
                .get("http://localhost:5000/user/getModelEvolutionInfo", {
                    params: {
                        model_name: this.selectedModelName[0],
                    },
                })
                .then((Response) => {
                    this.model_tree_data = Response.data.data.model_tree;
                    this.updateChart3(this.model_tree_data);
                });
        },
        getModelEvolutionInfo() {
            this.$axios
                .get("http://localhost:5000/user/getModelEvolutionInfo", {
                    params: {
                        model_name: this.selectedModelName[0],
                    },
                })
                .then((Response) => {
                    // console.log(Response);
                    if (Response.data.data.model_message == "暂无演化信息") {
                        this.getModelEvolutionInfoNull();
                    } else {
                        this.model_message = Response.data.data.model_message;
                        this.model_tree_data = Response.data.data.model_tree;
                        this.updateChart3(this.model_tree_data);
                    }
                });
        },
    }
}
</script>

<style>
.namebox {
    height: 40px;
    background-color: #0da4f6;
    border-radius: 15px;
    color: white;
    text-align: center;
    margin-left: 30%;
    width: 8%;
    /* padding: 8px; */
    margin-right: 2%;
}
</style>