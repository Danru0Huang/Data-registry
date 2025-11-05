<template>
    <div class="mainpage">
        <div class="search" style="margin-left: 250px;">
            <div class="searchline" style="height: 60px;background-color:#a6d9f4; border-radius: 15px;
                padding: 10px; display: flex; align-items: center;">
                <el-button type="primary" round style="margin-left: 38%;width: 150px;"
                    @click="getSubDomainEvolutionTables">子域</el-button>
                <el-button type="primary" round style="width: 150px;margin-left: 5%;"
                    @click="getModelEvolutionTables">信息模型</el-button>
            </div>
            <div class="showbox1" style="margin-left: 20px;" v-show="showmodel_evolution_tables">
                <el-table :data="model_evolution_tables" style="width: 100%">>
                    <el-table-column label="模型名称" prop="model_name">
                    </el-table-column>
                    <el-table-column label="演化信息" prop="evolution">
                    </el-table-column>
                    <el-table-column align="right">
                        <template slot-scope="scope">
                            <el-button type="primary" icon="el-icon-search" @click="handleClick(scope.row)">查看</el-button>
                            <el-button type="danger" icon="el-icon-delete"
                                @click="handleDelete(scope.$index, scope.row)"></el-button>
                        </template>
                    </el-table-column>
                </el-table>
            </div>
            <div class="showbox2" style="margin-left: 20px;" v-show="showsub_domain_evolution_tables">
                <el-table :data="sub_domain_evolution_tables" style="width: 100%">>
                    <el-table-column label="子域名称" prop="name">
                    </el-table-column>
                    <el-table-column label="描述" prop="describe">
                    </el-table-column>
                    <el-table-column label="演化信息" prop="evolution">
                    </el-table-column>
                    <el-table-column align="right">
                        <template slot-scope="scope">
                            <el-button type="primary" icon="el-icon-search" @click="handleClick(scope.row)">查看</el-button>
                            <el-button type="danger" icon="el-icon-delete"
                                @click="handleDelete(scope.$index, scope.row)"></el-button>
                        </template>
                    </el-table-column>
                </el-table>
            </div>
        </div>
    </div>
</template>
  
<script>
export default {
    data() {
        return {
            selectedModelName: '',
            tableDataOfmodel: [],
            optionsOfModelName: [],
            this_row: '',
            model_evolution_tables: [],
            showmodel_evolution_tables: false,
            sub_domain_evolution_tables: [],
            showsub_domain_evolution_tables: true,
        }
    },
    mounted() {
        this.getSubDomainEvolutionTables();
        // this.disposeAllEchartsInstances()
    },
    beforeDestroy() {
        // 获取当前组件中所有 echarts 实例并销毁它们
        this.disposeAllEchartsInstances();
    },
    methods: {
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
        search() {
            var vm = this;
            // console.log(this.selectedModelName[1])
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
            if (row.evolution !== "暂无演化信息") {
                this.sendData();
                // window.open("http://localhost:8080/#/Demonstration/Demonstration_graph", '_blank');
            } else {
                this.$message.error('演化信息暂无,无法查询');
            }
        },
        sendData() {
            this.$emit('send-data', this.this_row, '这是从子组件发送的数据');
        },
        getModelEvolutionTables() {
            this.showmodel_evolution_tables = true;
            this.showsub_domain_evolution_tables = false;
            this.$axios
                .get("http://localhost:5000/user/getModelEvolutionTables")
                .then((Response) => {
                    this.model_evolution_tables = Response.data.data;
                    //   console.log("模型的演化信息表格列表");
                    //   console.log(this.model_evolution_tables);
                });
        },
        getSubDomainEvolutionTables() {
            this.showmodel_evolution_tables = false;
            this.showsub_domain_evolution_tables = true;
            this.$axios
                .get("http://localhost:5000/user/getSubDomainEvolutionTables")
                .then((Response) => {
                    console.log(Response)
                    this.sub_domain_evolution_tables = Response.data.data;
                    //   console.log("子域的演化信息表格列表");
                    //   console.log(this.sub_domain_evolution_tables);
                });
        },
    }
}
</script>
  
<style></style>