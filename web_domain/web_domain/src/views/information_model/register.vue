<template>
    <div class="box">
        <el-container>
            <el-main>
                <el-card class="box-card">

                    <!-- 添加信息模型模块 -->
                    <div slot="header" class="clearfix input-container"
                        style="text-align: center; display: flex; align-items: center;margin-left: 25%;">
                        <!-- 添加信息模型按钮 -->
                        <el-button type="primary" icon="el-icon-plus" @click="showDialogOfAddModel = true"
                            style="width: 150px; margin-right:10px" round>添加信息模型</el-button>

                        <!-- 查询模型选择框 -->
                        <el-select v-model="selectedModelName" filterable @change="handleSelectChangeOfModelName"
                            placeholder="请选择查询模型" style="margin-right: 10px;">
                            <el-option v-for="(item, index) in optionsOfModelName" :key="index" :label="item.label"
                                :value="item.value">
                            </el-option>
                        </el-select>

                        <!-- 文件上传 -->
                        <div style="margin-right: 10px;">
                            <el-upload class="upload-demo" :action="uploadUrl" :on-success="handleSuccess"
                                :before-upload="beforeUpload" :file-list="fileList" :limit="1" :accept="'.json'">
                                <el-button slot="trigger" size="small" type="primary" icon="el-icon-plus"
                                    style="width: 150px;" round>选择文件</el-button>
                            </el-upload>
                        </div>
                    </div>
                    <!-- <div class="chat-container" :id="chartId"></div> -->

                    <!-- 注册类注册属性注册关系模块 -->
                    <el-row :gutter="5">
                        <el-col :span="17">
                            <div class="chat-container" :id="chartId"></div>
                        </el-col>
                        <el-col :span="7">
                            <div style="display: flex; justify-content: space-between; width: 100%;">
                                <el-button type="success" size="mini" @click="changeShowAddModelClassTable"
                                    style="flex: 1;">注册类</el-button>
                                <el-button type="success" size="mini" @click="changeShowAddModelPropertyTable"
                                    style="flex: 1;">注册属性</el-button>
                                <el-button type="success" size="mini" @click="changeShowAddModelRelationTable"
                                    style="flex: 1;">注册关系</el-button>
                                <!-- <el-button type="danger" size="mini" @click="changeShowDeleteModelPropertyTable" style="flex: 1;">属性删除</el-button> -->
                            </div>

                            <!-- 注册类 -->
                            <el-form ref="addModelClassTableForm" :model="addClassName" label-width="auto"
                                style="margin-top: 20px;" v-show="showAddModelClassTable">
                                <div style="text-align: center;">
                                    <h5>添加类</h5>
                                </div>
                                <br>
                                <el-form-item label="模型名称:">
                                    <el-input v-model="selectedModelName" :disabled="true"></el-input>
                                </el-form-item>
                                <el-form-item label="类名:">
                                    <el-input v-model="addClassName.class_name" clearable placeholder="请输入内容"></el-input>
                                </el-form-item>
                                <el-form-item>
                                    <el-button type="success" @click="addClass">注册类</el-button>
                                    <el-button type="danger" @click="resetForm">重置</el-button>
                                </el-form-item>
                            </el-form>

                            <!-- 注册属性 -->
                            <el-form ref="addModelPropertyTableForm" :model="addPropertyName" label-width="auto"
                                style="margin-top: 20px;" v-show="showAddModelPropertyTable">
                                <div style="text-align: center;">
                                    <h5>添加属性</h5>
                                </div>
                                <br>
                                <el-form-item label="模型名称:">
                                    <el-input v-model="selectedModelName" :disabled="true" clearable
                                        placeholder="请输入内容"></el-input>
                                </el-form-item>
                                <el-form-item label="类:">
                                    <template>
                                        <el-select v-model="addPropertyName.class_name" filterable default-first-option
                                            placeholder="请选择类:">
                                            <el-option v-for="item in optionsOfModelClassName" :key="item.value"
                                                :label="item.label" :value="item.value">
                                            </el-option>
                                        </el-select>
                                    </template>
                                </el-form-item>
                                <div v-for="(property, index) in addPropertyName.property_names" :key="index">
                                    <el-form-item :label="`属性名 ${index + 1}`">
                                        <div style="display: flex; align-items: center;">
                                            <el-input v-model="addPropertyName.property_names[index]" clearable
                                                placeholder="请输入内容"></el-input>
                                            <el-button icon="el-icon-delete" @click="removePropertyItem(index)"
                                                circle></el-button>
                                        </div>
                                    </el-form-item>
                                </div>
                                <el-form-item>
                                    <el-button icon="el-icon-plus" @click="addPropertyItem" circle></el-button>
                                    <el-button type="success" @click="addProperty">注册属性</el-button>
                                    <el-button type="danger" @click="resetForm">重置</el-button>
                                </el-form-item>
                            </el-form>

                            <!-- 注册关系 -->
                            <el-form ref="addModelRelaionTableForm" :model="addRelationData" label-width="auto"
                                style="margin-top: 20px;" v-show="showAddModelRelationTable">
                                <div style="text-align: center;">
                                    <h5>添加关系</h5>
                                </div>
                                <br>
                                <el-form-item label="模型名称:">
                                    <el-input v-model="selectedModelName" :disabled="true"></el-input>
                                </el-form-item>
                                <el-form-item label="类1:">
                                    <template>
                                        <el-select v-model="addRelationData.class_name1" filterable default-first-option
                                            placeholder="请选择类:">
                                            <el-option v-for="item in optionsOfModelClassName" :key="item.value"
                                                :label="item.label" :value="item.value">
                                            </el-option>
                                        </el-select>
                                    </template>
                                </el-form-item>
                                <el-form-item label="类 2:">
                                    <template>
                                        <el-select v-model="addRelationData.class_name2" filterable default-first-option
                                            placeholder="请选择类:">
                                            <el-option v-for="item in optionsOfModelClassName" :key="item.value"
                                                :label="item.label" :value="item.value">
                                            </el-option>
                                        </el-select>
                                    </template>
                                </el-form-item>
                                <el-form-item label="关系:">
                                    <el-input v-model="addRelationData.relation" clearable></el-input>
                                </el-form-item>
                                <el-form-item>
                                    <el-button type="success" @click="addRelation">注册关系</el-button>
                                    <el-button type="danger" @click="resetForm">重置</el-button>
                                </el-form-item>
                            </el-form>


                            <!-- 添加信息模型组件 -->
                            <el-dialog title="注册模型" :visible.sync="showDialogOfAddModel" width="25%"
                                :before-close="dialogClose" center>
                                <span>
                                    <el-form ref="addModelForm" :model="addModelData" label-width="auto"
                                        style="margin-top: 20px;">
                                        <el-form-item label="模型名称:">
                                            <el-input v-model="addModelData.model_name" clearable
                                                placeholder="请输入内容"></el-input>
                                        </el-form-item>
                                        <el-form-item label="类名称:">
                                            <el-input v-model="addModelData.class_name" clearable
                                                placeholder="请输入内容"></el-input>
                                        </el-form-item>
                                    </el-form>
                                </span>
                                <span slot="footer" class="dialog-footer">
                                    <el-button type="danger" @click="resetForm">重置</el-button>
                                    <el-button type="danger" @click="showDialogOfAddModel = false">取
                                        消</el-button>
                                    <!-- <el-button type="primary" @click="showDialogOfAddProperty = false">确 定</el-button> -->
                                    <el-button type="primary" @click="addModel">注册</el-button>
                                </span>
                            </el-dialog>

                            <!-- 暂时未知 -->
                            <el-dialog title="注册属性" :visible.sync="showDialogOfAddProperty" width="25%"
                                :before-close="dialogClose" center>
                                <span>
                                    <el-form ref="addPropertyForm" :model="addPropertyName" label-width="auto"
                                        style="margin-top: 20px;">
                                        <div v-for="(property, index) in addPropertyName.property_names" :key="index">
                                            <el-form-item :label="`属性名 ${index + 1}`">
                                                <div style="display: flex; align-items: center;">
                                                    <el-input v-model="addPropertyName.property_names[index]"
                                                        clearable></el-input>
                                                    <el-button icon="el-icon-delete" @click="removePropertyItem(index)"
                                                        circle></el-button>
                                                </div>
                                            </el-form-item>
                                        </div>
                                    </el-form>
                                </span>
                                <span slot="footer" class="dialog-footer">
                                    <el-button icon="el-icon-plus" @click="addPropertyItem" circle></el-button>
                                    <el-button type="danger" @click="showDialogOfAddProperty = false">取
                                        消</el-button>
                                    <!-- <el-button type="primary" @click="showDialogOfAddProperty = false">确 定</el-button> -->
                                    <el-button type="primary" @click="addProperty">注册</el-button>
                                    <el-button type="danger" @click="resetFormOfAddProperty">重置</el-button>
                                </span>
                            </el-dialog>

                            <!-- 暂时未知 -->
                            <el-dialog title="注册属性/关系" :visible.sync="showDialogOfSelect" width="25%"
                                :before-close="dialogClose" center>
                                <span>
                                    <el-button type="primary" @click="selectOfAddRelation"
                                        style="margin-left: 30px;">注册关系</el-button>
                                </span>
                                <span>
                                    <el-button type="primary" @click="selectOfAddProperty"
                                        style="margin-left: 30px;">注册属性</el-button>
                                </span>
                                <span slot="footer" class="dialog-footer">
                                    <el-button type="danger" @click="showDialogOfSelect = false">取消</el-button>
                                    <!-- <el-button type="primary" @click="showDialogOfAddProperty = false">确 定</el-button> -->
                                </span>
                            </el-dialog>

                            <!-- 暂时未知 -->
                            <el-dialog title="注册类" :visible.sync="showDialogOfAddClass" width="25%"
                                :before-close="dialogClose" center>
                                <span>
                                    <el-form ref="addClassForm" :model="addClassName" label-width="auto"
                                        style="margin-top: 20px;">
                                        <el-form-item label="名称">
                                            <el-input v-model="addClassName.class_name" clearable></el-input>
                                        </el-form-item>
                                    </el-form>
                                </span>
                                <span slot="footer" class="dialog-footer">
                                    <el-button type="danger" @click="showDialogOfAddClass = false">取消</el-button>
                                    <!-- <el-button type="primary" @click="showDialogOfAddProperty = false">确 定</el-button> -->
                                    <el-button type="primary" @click="addClass">注册</el-button>
                                    <el-button type="danger" @click="resetForm">重置</el-button>
                                </span>
                            </el-dialog>

                            <!-- 暂时未知 -->
                            <el-dialog title="注册关系" :visible.sync="showDialogOfAddRelation" width="25%"
                                :before-close="dialogClose" center>
                                <span>
                                    <el-form ref="addRelationForm" :model="addRelationData" label-width="auto"
                                        style="margin-top: 20px;">
                                        <el-form-item label="类1">
                                            <el-input v-model="addRelationData.class_name1" :disabled="true"></el-input>
                                        </el-form-item>
                                        <el-form-item label="类 2">
                                            <template>
                                                <el-select v-model="addRelationData.class_name2" filterable
                                                    default-first-option placeholder="请选择类">
                                                    <el-option v-for="item in optionsOfModelClassName" :key="item.value"
                                                        :label="item.label" :value="item.value">
                                                    </el-option>
                                                </el-select>
                                            </template>
                                        </el-form-item>
                                        <el-form-item label="关系">
                                            <el-input v-model="addRelationData.relation" clearable></el-input>
                                        </el-form-item>
                                    </el-form>
                                </span>
                                <span slot="footer" class="dialog-footer">
                                    <el-button type="danger" @click="showDialogOfAddRelation = false">取消</el-button>
                                    <el-button type="primary" @click="addRelation">注册</el-button>
                                    <el-button type="danger" @click="resetFormOfAddRelation">重置</el-button>
                                </span>
                            </el-dialog>
                        </el-col>
                    </el-row>
                </el-card>
            </el-main>
        </el-container>
    </div>
</template> 

<script>
import * as echarts from 'echarts';
export default {
    data() {
        return {
            deleteProperty: {
                deletePropertyName: [],
            },
            uploadUrl: 'http://localhost:5000/upload_json_file',
            fileList: [], // 上传的文件列表
            result: null, // 上传成功后的结果
            searchInput: '',
            graphData: [],
            graphLinks: [],
            chartId: 'guanxi',
            tableData: [],
            showTable: false,
            dialogVisible: false,
            nodeDetails: {},
            selectedLabel: '',
            labelOptions: ["模型"],
            categories: ["模型", "模型类", "模型属性"],
            descriptionsData: [],
            showDescriptions: false,
            showDialogOfAddProperty: false,
            addPropertyName: {
                property_names: [],
                class_name: '',
                model_name: '',
                evolution: 'no',
            },
            showDialogOfAddClass: false,
            addClassName: {
                class_name: '',
            },
            showDialogOfSelect: false,
            showDialogOfAddRelation: false,
            addRelationData: {
                class_name1: '',
                class_name2: '',
                relation: ''
            },
            optionsOfModelClassName: [],
            showDialogOfAddModel: false,
            addModelData: {
                model_name: '',
                class_name: ''
            },
            optionsOfModelName: [],
            selectedModelName: '',
            showAddModelClassTable: false,
            showAddModelPropertyTable: false,
            showAddModelRelationTable: false,
        }
    },
    mounted() {
        this.getOptionsOfModelName();
    },
    methods: {
        //文件上传成功提示
        handleSuccess(response) {
            // 上传成功的回调函数
            if (response) {
                // console.log(response)
                this.result = {
                    name: response.name,
                    content: response.content,
                };
                if (response.message === "该参考域数据目录已注册！！！") {
                    // console.log(response)
                    this.getOptionsOfModelName();
                    this.$message({
                        message: response.message,
                        type: 'error',
                        duration: 1000,
                        showClose: true,
                    })
                } else {
                    this.getOptionsOfModelName();
                    this.$message({
                        message: response.message,
                        type: 'success',
                        duration: 1000,
                        showClose: true,
                    })
                }


            }
        },
        beforeUpload(file) {
            // 上传之前的钩子函数
            const isJSON = file.type === 'application/json';
            if (!isJSON) {
                this.$message.error('只能上传json文件！');
                return false;
            }
            return true;
        },
        //查询已注册属性
        getModelPropertyNameOptions() {
            this.$axios.get('http://localhost:5000/search/model/getClassNameAndPropertyNameOptions', {
                params: {
                    model_name: this.selectedModelName,
                }
            })
                .then(response => {
                    // console.log(response.data);
                    this.optionsOfModelPropertyName = response.data;
                })
                .catch(
                    error => {
                        console.error(error);
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
        updateChart(chartId, graphData, graphLinks) {
            let vm = this
            var myChart = echarts.init(document.getElementById(chartId));
            console.log(graphLinks)
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
            // console.log(option)
            myChart.setOption(option, true);
            myChart.off('click');
            myChart.on("click", function (params) {

                var name = params.name
                var category_id = params.data.category;
                var category = vm.categories[category_id];

                if (category == "模型类") {
                    vm.addPropertyName.class_name = name;
                    vm.addRelationData.class_name1 = name;
                    vm.showDialogOfSelect = true;
                };
                if (category == "模型") {
                    vm.showDialogOfAddClass = true;
                }
            });
        },
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
                        vm.opennews("查询失败，请检查输入数据");
                    } else {
                        vm.getModelPropertyNameOptions();
                        vm.graphData = response.data.data.map(function (node, idx) {
                            node.id = idx;
                            return node;
                        });
                        vm.graphLinks = response.data.links;
                        vm.updateChart(vm.chartId, vm.graphData, vm.graphLinks);
                        vm.tableData = response.data.tableData;
                        // vm.showTable = true;
                        vm.descriptionsData = response.data.list;
                        vm.showDescriptions = true;
                    }

                })
                .catch(error => {
                    console.log(error)
                    // 获取失败消息提示
                    this.$message({
                        showClose: true,
                        message: '查询失败',
                        type: 'error',
                        duration: 1000
                    })
                }
                );
        },
        // 查询消息提示
        opennews(message) {
            this.$message({
                showClose: true,
                message: message,
                type: 'success',
                duration: 1000
            });
        },
        // 关闭窗口提示
        dialogClose(done) {
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
        // 注册属性函数
        addProperty() {
            var vm = this;
            if (this.selectedModelName === '') {
                this.$message.error("请先选择信息模型");
                return;
            }
            vm.addPropertyName.model_name = vm.selectedModelName;
            this.$axios.post('http://localhost:5000/register/model/addProperty', vm.addPropertyName)
                .then(function (response) {
                    vm.opennews(response.data.message);
                    vm.showDialogOfAddProperty = false;
                    vm.graphData = [];
                    vm.graphLinks = [];
                    vm.search();
                    vm.resetForm();
                })
                .catch(error => {
                    console.log(error)
                    // 获取失败消息提示
                    this.$message({
                        showClose: true,
                        message: "添加失败",
                        type: 'error',
                        duration: 1000
                    })
                }
                );
        },
        // 注册类函数
        addClass() {
            var vm = this;
            if (this.selectedModelName === '') {
                this.$message.error("请先选择信息模型");
                return;
            }
            this.$axios.post('http://localhost:5000/register/model/addClass',
                {
                    params: {
                        model_name: this.selectedModelName,
                        class_name: this.addClassName.class_name,
                        evolution: 'no',
                    }
                })
                .then(response => {
                    // 获取成功消息提示
                    vm.$message({
                        showClose: true,
                        message: response.data.message,
                        type: 'success',
                        duration: 1000
                    })
                    vm.showDialogOfAddClass = false;
                    vm.graphData = [];
                    vm.graphLinks = [];
                    vm.search();
                    vm.getMdodelClassNameOptions();
                    vm.resetForm();
                })
                .catch(error => {
                    console.log(error);
                    //获取失败消息提示
                    this.$message({
                        showClose: true,
                        message: '添加失败，请检查网络设置',
                        type: 'error',
                        duration: 1000
                    })
                }
                );
        },
        selectOfAddRelation() {
            this.getMdodelClassNameOptions();
            this.showDialogOfSelect = false;
            this.showDialogOfAddRelation = true;
        },
        selectOfAddProperty() {
            this.showDialogOfSelect = false;
            this.showDialogOfAddProperty = true;
        },
        // 查询已注册的函数
        getMdodelClassNameOptions() {
            this.$axios.get('http://localhost:5000/search/model/getModelClassNameOptions', {
                params: {
                    model_name: this.selectedModelName,
                }
            })
                .then(response => {
                    this.optionsOfModelClassName = response.data.data;
                })
                .catch(
                    error => {
                        console.error(error);
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
        // 注册关系
        addRelation() {
            var vm = this;
            if (this.selectedModelName === '') {
                this.$message.error("请先选择信息模型");
                return;
            }
            this.$axios.get('http://localhost:5000/register/model/addRelation', {
                params: {
                    model_name: this.selectedModelName,
                    class_name1: this.addRelationData.class_name1,
                    class_name2: this.addRelationData.class_name2,
                    relation: this.addRelationData.relation
                }
            })
                .then(function (response) {
                    vm.opennews(response.data.message);
                    vm.showDialogOfAddRelation = false;
                    vm.graphData = [];
                    vm.graphLinks = [];
                    vm.search();
                    vm.resetForm();
                })
                .catch(function (error) {
                    console.log(error);
                    // 获取失败消息提示
                    // this.$message({
                    //     showClose: true,
                    //     message: "添加失败",
                    //     type: 'error',
                    //     duration: 1000
                    // })
                },
                );

        },
        // 添加信息模型组件
        addModel() {
            var vm = this;
            this.$axios.get('http://localhost:5000/register/model/addModel', {
                params: {
                    model_name: this.addModelData.model_name,
                    class_name: this.addModelData.class_name
                }
            })
                .then(response => {
                    vm.opennews(response.data.message);
                    this.showDialogOfAddModel = false;
                    this.getOptionsOfModelName();
                    this.resetForm();
                })
                .catch(error => {
                    console.error(error);
                });
        },
        getOptionsOfModelName() {
            this.$axios.get('http://localhost:5000/search/model/getModelTypeOptions')
                .then(response => {
                    this.optionsOfModelName = response.data.data;
                })
                .catch(error => {
                    console.error(error);
                },
                );
        },
        handleSelectChangeOfModelName() {
            this.getMdodelClassNameOptions();
            this.search();
        },
        addPropertyItem() {
            this.addPropertyName.property_names.push('');
        },
        removePropertyItem(index) {
            this.addPropertyName.property_names.splice(index, 1);
        },
        changeShowAddModelClassTable() {
            this.showAddModelClassTable = true;
            this.showAddModelPropertyTable = false;
            this.showAddModelRelationTable = false;
        },
        changeShowAddModelPropertyTable() {
            this.showAddModelPropertyTable = true;
            this.showAddModelClassTable = false;
            this.showAddModelRelationTable = false;
        },
        changeShowAddModelRelationTable() {
            this.showAddModelRelationTable = true;
            this.showAddModelClassTable = false;
            this.showAddModelPropertyTable = false;
        },
        resetForm() {
            this.addPropertyName.property_names = [];
            this.addPropertyName.class_name = '';
            this.addClassName.class_name = '';
            this.addModelData.model_name = '';
            this.addModelData.class_name = '';
            this.addRelationData.class_name1 = '';
            this.addRelationData.class_name2 = '';
            this.addRelationData.relation = '';
        },
        resetFormOfAddProperty() {
            this.addPropertyName.property_names = [];
        },
        resetFormOfAddRelation() {
            this.addRelationData.class_name2 = '';
            this.addRelationData.relation = '';
        }
    }
}
</script>

<style scoped>
.box {
    margin-left: 250px;
    /* margin-top: 15px;
        border-radius: 5px;
        box-shadow: 0 2px 5px 0 rgba(0,0,0,.2);
        height: 99vh; */
}

.el-menu-vertical-demo {
    height: 100vh;
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
    height: 750px;
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