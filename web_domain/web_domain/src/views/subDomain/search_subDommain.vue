<template>
    <div class="box">
        <el-main>
            <el-card class="box-card">
                <!-- 选择查询模型 -->
                <div slot="header" class="clearfix input-container" style="text-align: center;">
                    <el-button type="primary" @click="searchall" round style="margin-right:20px">查询所有子域</el-button>
                    <el-cascader v-model="selectedModelNames" :options="optionsOfModelName" filterable clearable
                        @change="searchDetails" placeholder="请选择查询模型与其相关的表格" style="width:250px">
                    </el-cascader>

                </div>

                <el-row :gutter="7">
                    <!-- 图谱展示页面 -->
                    <el-col :span="12">
                        <div class="chat-container" :id="chartId"></div>
                    </el-col>

                    <!-- 右侧表格展示 -->
                    <el-col :span="12">
                        <div class="chart">
                            <template>
                                <!-- 对象类展示 -->
                                <el-table :data="dialogobject_class" style="width: 100%">
                                    <el-table-column type="expand">
                                        <template slot-scope="props">
                                            <el-form label-position="left" inline class="demo-table-expand">
                                                <el-form-item label="对象类名">
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
                                            </el-form>
                                        </template>
                                    </el-table-column>
                                    <el-table-column label="标识符" prop="identifier">
                                    </el-table-column>
                                    <el-table-column label="标签" prop="label">
                                    </el-table-column>
                                    <el-table-column label="描述" prop="describe">
                                    </el-table-column>
                                    <el-table-column align="right">
                                        <!-- eslint-disable -->
                                    </el-table-column>
                                </el-table>
                            </template>
                            <!-- 属性展示 -->
                            <template>
                                <el-table :data="dialogproperty" style="width: 100%">
                                    <el-table-column type="expand">
                                        <template slot-scope="props">
                                            <el-form label-position="left" inline class="demo-table-expand">
                                                <el-form-item label="属性名">
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
                                            </el-form>
                                        </template>
                                    </el-table-column>
                                    <el-table-column label="标识符" prop="identifier">
                                    </el-table-column>
                                    <el-table-column label="标签" prop="label">
                                    </el-table-column>
                                    <el-table-column label="描述" prop="describe">
                                    </el-table-column>
                                    <el-table-column align="right">
                                    </el-table-column>
                                </el-table>
                            </template>
                            <!-- 概念域表格列表 -->
                            <template>
                                <el-table :data="dialogconceptual_domain[0]" style="width: 100%">
                                    <el-table-column type="expand">
                                        <template slot-scope="props">
                                            <el-form label-position="left" inline class="demo-table-expand">
                                                <el-form-item label="概念域名">
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
                                                <el-divider content-position="center">可枚举值含义</el-divider>
                                                <el-form-item v-for="(item, index) in props.row.valueMeanings" :key="index">
                                                    <el-descriptions border>
                                                        <el-descriptions-item label="值含义">{{ item.name
                                                        }}</el-descriptions-item>
                                                        <el-descriptions-item label="标识符">{{ item.identifier
                                                        }}</el-descriptions-item>
                                                        <el-descriptions-item label="注册状态">{{ item.status
                                                        }}</el-descriptions-item>
                                                        <el-descriptions-item label="创建时间">{{ item.time
                                                        }}</el-descriptions-item>
                                                        <el-descriptions-item label="版本">{{ item.version
                                                        }}</el-descriptions-item>
                                                    </el-descriptions>
                                                </el-form-item>
                                            </el-form>
                                        </template>
                                    </el-table-column>
                                    <el-table-column label="标识符" prop="identifier">
                                    </el-table-column>
                                    <el-table-column label="标签" prop="label">
                                    </el-table-column>
                                    <el-table-column label="描述" prop="describe">
                                    </el-table-column>
                                    <el-table-column align="right">
                                    </el-table-column>
                                </el-table>
                            </template>
                            <!-- 数据元概念表格列表 -->
                            <template>
                                <el-table :data="dialogdata_element_concept" style="width: 100%">
                                    <el-table-column type="expand">
                                        <template slot-scope="props">
                                            <el-form label-position="left" inline class="demo-table-expand">
                                                <el-form-item label="数据元概念名">
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
                                                <el-form-item label="对象类">
                                                    <span>{{ props.row.OCLName }}</span>
                                                    <i class="el-icon-right"></i>
                                                    <span>{{ props.row.OCLIdentifier }}</span>
                                                </el-form-item>
                                                <el-form-item label="属性">
                                                    <span>{{ props.row.PRPName }}</span>
                                                    <i class="el-icon-right"></i>
                                                    <span>{{ props.row.PRPIdentifier }}</span>
                                                </el-form-item>
                                                <el-form-item label="概念域">
                                                    <span>{{ props.row.CDMName }}</span>
                                                    <i class="el-icon-right"></i>
                                                    <span>{{ props.row.CDMIdentifier }}</span>
                                                </el-form-item>
                                            </el-form>
                                        </template>
                                    </el-table-column>
                                    <el-table-column label="标识符" prop="identifier">
                                    </el-table-column>
                                    <el-table-column label="标签" prop="label">
                                    </el-table-column>
                                    <el-table-column label="描述" prop="describe">
                                    </el-table-column>
                                    <el-table-column align="right">
                                    </el-table-column>
                                </el-table>
                            </template>
                            <!-- 值域表格列表 -->
                            <template>
                                <el-table :data="dialogvalue_domain[0]" style="width: 100%">
                                    <el-table-column type="expand">
                                        <template slot-scope="props">
                                            <el-form label-position="left" inline class="demo-table-expand">
                                                <el-form-item label="值域名">
                                                    <span>{{ props.row.name }}</span>
                                                </el-form-item>
                                                <!-- <el-divider content-position="center">公共属性</el-divider> -->
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
                                                <!-- <el-divider content-position="center">管理信息</el-divider> -->
                                                <el-form-item label="版本">
                                                    <span>{{ props.row.version }}</span>
                                                </el-form-item>
                                                <el-form-item label="创建人员ID">
                                                    <span>{{ props.row.personId }}</span>
                                                </el-form-item>
                                                <el-form-item label="创建单位">
                                                    <span>{{ props.row.department }}</span>
                                                </el-form-item>
                                                <el-form-item label="概念域">
                                                    <span>{{ props.row.CDMName }}</span>
                                                    <i class="el-icon-right"></i>
                                                    <span>{{ props.row.CDMIdentifier }}</span>
                                                </el-form-item>
                                                <el-divider content-position="center">可允许值</el-divider>
                                                <el-form-item v-for="(item, index) in props.row.permissibleValues"
                                                    :key="index">
                                                    <el-descriptions :column="2" border>
                                                        <el-descriptions-item label="值">{{ item.PEVName
                                                        }}</el-descriptions-item>
                                                        <el-descriptions-item label="标识符">{{ item.PEVIdentifier
                                                        }}</el-descriptions-item>
                                                        <el-descriptions-item label="值含义">{{ item.VLMName
                                                        }}</el-descriptions-item>
                                                        <el-descriptions-item label="标识符">{{ item.VLMIdentifier
                                                        }}</el-descriptions-item>
                                                    </el-descriptions>
                                                    <el-divider><i class="el-icon-crop"></i></el-divider>
                                                </el-form-item>
                                            </el-form>
                                        </template>
                                    </el-table-column>
                                    <el-table-column label="标识符" prop="identifier">
                                    </el-table-column>
                                    <el-table-column label="标签" prop="label">
                                    </el-table-column>
                                    <el-table-column label="描述" prop="describe">
                                    </el-table-column>
                                    <el-table-column align="right">
                                    </el-table-column>
                                </el-table>
                            </template>
                            <!-- 数据元表格列表 -->
                            <template>
                                <el-table :data="dialogdata_element" style="width: 100%">
                                    <el-table-column type="expand">
                                        <template slot-scope="props">
                                            <el-form label-position="left" inline class="demo-table-expand">
                                                <el-form-item label="标签">
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
                                                <el-form-item label="数据元概念">
                                                    <span>{{ props.row.DECName }}</span>
                                                    <i class="el-icon-right"></i>
                                                    <span>{{ props.row.DECIdentifier }}</span>
                                                </el-form-item>
                                                <el-form-item label="值域">
                                                    <span>{{ props.row.VDMName }}</span>
                                                    <i class="el-icon-right"></i>
                                                    <span>{{ props.row.VDMIdentifier }}</span>
                                                </el-form-item>
                                            </el-form>
                                        </template>
                                    </el-table-column>
                                    <el-table-column label="标识符" prop="identifier">
                                    </el-table-column>
                                    <el-table-column label="标签" prop="label">
                                    </el-table-column>
                                    <el-table-column label="描述" prop="describe">
                                    </el-table-column>
                                    <el-table-column align="right">
                                    </el-table-column>
                                </el-table>
                            </template>
                            <el-drawer title="修改子域信息" :visible.sync="drawer" :with-header="true">
                                <el-form :label-position="labelPosition" label-width="80px" :model="formLabelAlign">
                                    <el-form-item label="名称">
                                        <el-input v-model="formLabelAlign.name"
                                            style="width: 400px;margin-left: 10px"></el-input>
                                    </el-form-item>
                                    <el-form-item label="活动区域">
                                        <el-input v-model="formLabelAlign.region"
                                            style="width: 400px;margin-left: 10px"></el-input>
                                    </el-form-item>
                                    <el-form-item label="活动形式">
                                        <el-input v-model="formLabelAlign.type"
                                            style="width: 400px;margin-left: 10px"></el-input>
                                    </el-form-item>
                                    <el-button type="primary" @click="handleEdit()"
                                        style="margin-left: 100px;">提交修改</el-button>
                                    <el-button style="width: 100px;" @click="drawer = false">取消</el-button>
                                </el-form>
                            </el-drawer>
                        </div>

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
            labelPosition: 'right',
            username: 'jym',
            formLabelAlign: {
                name: '',
                region: '',
                type: ''
            },
            drawer: false,//抽屉默认值
            activeMenu: '',
            selectedModelName: '',
            selectedModelNames: [],
            optionsOfModelName: [],
            graphData: {
                nodes: [],
                links: []
            },
            chartId: 'guanxi',
            tableData: [],
            showTable: false,
            dialogVisible: false,
            nodeDetails: {},
            categories: ["子域", "表", "表属性", "表属性值", "数据元", "值域", "值域组", "可允许值"],
            // descriptionsData: [],
            showDescriptions: false,
            dialogconceptual_domain: [],
            dialogdata_element: [],
            dialogdata_element_concept: [],
            dialogobject_class: [],
            dialogproperty: [],
            dialogvalue_domain: [],
            tableData1: [],
        }
    },

    mounted() {
        this.searchall();
    },
    methods: {
        // 查询所有子域
        searchall() {
            this.graphData.nodes = []
            this.graphData.links = []
            this.getOptionsOfModelName();
            this.search();
        },
        // 查询单个子域详细信息
        searchDetails() {
            var vm = this;
            // console.log(this.selectedModelNames)
            // return;
            this.$axios.get('http://localhost:5000/search/subDomain/getGraphOfTable', {
                params: {
                    // 子域名字
                    sub_domain_name: this.selectedModelNames[0],
                    // 表格ID
                    identifier_table: this.selectedModelNames[1]
                }
            })
                .then(function (response) {
                    if (response.data.data.length == 0) {
                        vm.openError();
                        vm.dialogconceptual_domain = [],
                            vm.dialogdata_element = [],
                            vm.dialogdata_element_concept = [],
                            vm.dialogobject_class = [],
                            vm.dialogproperty = [],
                            vm.dialogvalue_domain = [],
                            vm.tableData1 = [];
                    }
                    else {
                        console.log(response)
                        // let indexs = 0;
                        vm.graphData.nodes = response.data.data.map(function (node, idx) {
                            node.id = idx;
                            return node;
                        });
                        vm.graphData.links = response.data.links;
                        vm.updateChart(vm.chartId, vm.graphData);
                        // vm.descriptionsData = response.data.list;
                        vm.showDescriptions = true;
                    }

                })
                .catch(function (error) {
                    console.log(error);
                },
                );
        },
        // 查询子域函数
        search() {
            var vm = this;
            // console.log(this.selectedModelName)
            this.$axios.get('http://localhost:5000/search/subDomain/getSubDomainOptions', {
                params: {
                    name: this.selectedModelName,
                    label: "模型"
                }
            })
                .then(function (response) {
                    if (response.data.data.length == 0) {
                        vm.openError();
                    } else {
                        let indexs = 0;
                        const targetNodes = response.data.data.map(({ describe, id, label, value }) => {
                            return {
                                name: `子域模型${indexs += 1}`,
                                describe: describe,
                                id: id,
                                value: value,
                                label: label,
                                category: '子域'
                            };
                        });
                        vm.graphData.nodes.push(...targetNodes);
                        vm.updateChart(vm.chartId, vm.graphData);
                        vm.showDescriptions = true;
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
        // 获取所有上传过的子域名称
        getOptionsOfModelName() {
            this.$axios.get('http://localhost:5000/search/subDomain/getSubDomainAndTableOptions')
                .then(response => {
                    // console.log(response.data);
                    // console.log("++++_+_+_++++++++++++++++++++++++++++++++++++++++++++++++")
                    this.optionsOfModelName = response.data.data;
                    this.selectedModelName = response.data.data.value;
                })
                .catch(error => {
                    console.error(error);
                },
                );
        },
        updateChart(chartId, graphData) {
            let vm = this;
            var myChart = echarts.init(document.getElementById(chartId));

            var option = {
                tooltip: {
                    formatter: function (params) {
                        const nodeData = params.data;
                        let tooltipContent = `名称：${nodeData.name}<br/>`;

                        // 检查描述是否存在
                        if (nodeData.describe) {
                            tooltipContent += `描述：${nodeData.describe}<br/>`;
                        }
                        // 检查id是否存在
                        if (nodeData.id) {
                            tooltipContent += `ID：${nodeData.id}<br/>`;
                        }
                        // 检查label是否存在
                        if (nodeData.label) {
                            tooltipContent += `子域模型名称：${nodeData.label}<br/>`;
                        }
                        // 检查value是否存在
                        if (nodeData.value) {
                            tooltipContent += `属性值：${nodeData.value}<br/>`;
                        }
                        return tooltipContent;
                    }
                },
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
                    data: ["子域", "表", "表属性", "表属性值", "数据元", "值域", "值域组", "可允许值"]
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
                    categories: [
                        {
                            name: '子域'
                        },
                        {
                            name: '表'
                        },
                        {
                            name: '表属性'
                        },
                        {
                            name: '表属性值'
                        },
                        {
                            name: '数据元'
                        },
                        {
                            name: '值域'
                        },
                        {
                            name: '值域组'
                        },
                        {
                            name: '可允许值'
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
                    nodes: graphData.nodes,
                    links: graphData.links,
                }]
            };
            myChart.setOption(option, true);
            myChart.off('click');
            myChart.on("click", function (paramsvalue) {
                // console.log(paramsvalue.data)
                if (paramsvalue.data.category != 2) {
                    vm.$message.error('请选择表属性节点查询MDR信息');
                    return;
                }
                vm.$axios.get('http://localhost:5000/search/subDomain/getMDRTableThroughSubDomain', {
                    params: {
                        identifier_attribute: paramsvalue.data.identifier
                    }
                })
                    .then(response => { // 使用正确的参数名 response
                        // 处理 response
                        this.tableData1 = response.data;
                        console.log(this.tableData1)
                        vm.dialogconceptual_domain = this.tableData1.conceptual_domain;
                        // console.log(this.dialogconceptual_domain[0][0].identifier)
                        vm.dialogconceptual_domain[0][0].label = "概念域"
                        vm.dialogconceptual_domain[0][0].valueMeanings = vm.dialogconceptual_domain[1]
                        console.log(vm.dialogconceptual_domain)

                        vm.dialogdata_element = this.tableData1.data_element;
                        vm.dialogdata_element[0].label = "数据元"

                        vm.dialogdata_element_concept = this.tableData1.data_element_concept;
                        vm.dialogdata_element_concept[0].label = "数据元概念"

                        vm.dialogobject_class = this.tableData1.object_class;
                        vm.dialogobject_class[0].label = "对象类",
                            console.log(vm.dialogobject_class)

                        vm.dialogproperty = this.tableData1.property;
                        vm.dialogproperty[0].label = "属性"

                        vm.dialogvalue_domain = this.tableData1.value_domain;
                        vm.dialogvalue_domain[0][0].label = "值域"
                        vm.dialogvalue_domain[0][0].permissibleValues = vm.dialogvalue_domain[1]

                    })
                    .catch(error => {
                        console.log(error)
                        vm.$message.error("该表属性还未与数据元建立映射")
                    })
            });
        },
        handleEdit(index, row) {
            console.log(index, row);
        },

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
    /* width: 100px; */
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

.el-form-item__label {
    color: #B3C0D1;
}
</style>