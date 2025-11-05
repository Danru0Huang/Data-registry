<template>
	<div class="box">
		<div class="sidebar">
			<el-row :gutter="20" style="width:60vw"> <!-- 使用 :gutter="20" 来设置行内元素之间的间距 -->
				<el-col :span="6">
					<el-button type="primary" @click="changeShowDialogOfAddSubDomain" style="width: 100%">新增子域</el-button>
				</el-col>
				<el-col :span="6">
					<el-button type="success" @click="startAutoMapping" :loading="loadingMapping" :disabled="!subDomainName" style="width: 100%">
						智能化映射
					</el-button>
				</el-col>
				<el-col :span="6">
					<el-upload class="upload-demo" :action="uploadUrl" :on-success="handleSuccess"
						:before-upload="beforeUpload" :file-list="fileList" :limit="1" :accept="'.xlsx'"
						style="width: 100%">
						<el-button slot="trigger" size="small" type="primary">选择文件</el-button>
						<div slot="tip" class="el-upload__tip">只能上传xlsx文件</div>
					</el-upload>
				</el-col>
				<el-col :span="6">
					<div v-if="result" style="margin-top: 10px;"> <!-- 设置顶部边距 -->
						<h3>上传成功！</h3>
						<p>文件名：{{ result.name }}</p>
						<p>表标识符：</p>
						<pre>{{ identifier_table }}</pre>
					</div>
				</el-col>
			</el-row>
		</div>
		<el-main style="border-radius: 5px;
        box-shadow: 0 2px 5px 0 rgba(0,0,0,.2);
		margin:10px">
			<el-row :gutter="10">
				<!-- 子域图谱展示区域 -->
				<el-col :span="18" style="height: 100vh">
					<div id="graphOfTable" style="height: 100vh">
					</div>
				</el-col>
				<el-col :span="6">
					<template>
						<h3 style="text-align: center; color: #2fb9c2; margin-bottom: 10px;">人工映射</h3>
						<el-tabs v-model="activeName" @tab-click="handleClick">
							<!-- 建立表属性与数据元之间联系 -->
							<el-tab-pane label="表属性" name="first">
								<el-divider content-position="center">表属性名</el-divider>
								<div style="margin: 20px;">
									<el-input v-model="attributeName" :disabled="true"></el-input>
								</div>
								<el-divider content-position="center">数据元</el-divider>
								<div style="margin: 20px; display: flex;">
									<el-select v-model="dataElement" filterable remote :value-key="'label'" clearable>
										<!-- {% raw %} -->
										<el-option v-for="option in dataElementOptions" :key="option.value"
											:label="option.label" :value="option.value">
											<span style="float: left">{{ option.label }}</span>
											<span style="float: right; color: #8492a6; font-size: 13px">{{ option.value
											}}</span>
										</el-option>
										<!-- {% endraw %} -->
									</el-select>
								</div>
								<div style="margin: 20px; display: flex;">
									<el-button type="primary"
										@click="addRelationBetweenAttributeAndDataElement">添加联系</el-button>
									<el-button type="primary" @click="goyanhua">执行演化</el-button>
								</div>

								<!-- <el-divider content-position="center">值域</el-divider>
								<div style="margin: 20px; display: flex;">
									<el-select v-model="valueDomain" filterable remote
										:value-key="'label'" clearable>
										
										<el-option v-for="option in valueDomainOptions" :key="option.value"
											:label="option.label" :value="option.value">
											<span style="float: left">{{ option.label }}</span>
											<span
												style="float: right; color: #8492a6; font-size: 13px">{{ option.value }}</span>
										</el-option>
										
									</el-select>
								</div> -->
								<!-- <div style="margin: 20px; display: flex;">
									<el-button type="primary"
										@click="addRelationBetweenAttributeAndValueDomain">添加联系</el-button>
								</div> -->
							</el-tab-pane>

							<!-- 建立表属性与可允许值联系 -->
							<el-tab-pane label="表属性值" name="second">
								<el-divider content-position="center">表属性值名</el-divider>
								<div style="margin: 20px;">
									<el-input v-model="attributeValueName" :disabled="true"></el-input>
								</div>
								<el-divider content-position="center">可允许值</el-divider>
								<div class="block">
									<!-- <span class="demonstration">请选择:   </span> -->
									<el-cascader v-model="permissibleValues" :options="permissibleValuesOptions" filterable
										clearable>
									</el-cascader>
								</div>
								<div style="margin: 20px; display: flex;">
									<el-button type="primary"
										@click="addRelationBetweenAttributeValueAndPermissibleValues">添加联系</el-button>
								</div>
							</el-tab-pane>
						</el-tabs>
					</template>
				</el-col>
			</el-row>
		</el-main>


		<!-- 新增子域弹框 -->
		<el-dialog title="新增子域" :visible.sync="showDialogOfAddSubDomain" width="25%" :before-close="dialogClose" center>
			<span>
				<el-form ref="addSubDomainForm" :model="addSubDomainData" label-width="auto" style="margin-top: 20px;">
					<el-form-item label="子域名称">
						<el-input v-model="addSubDomainData.name" clearable></el-input>
					</el-form-item>
					<el-form-item label="描述">
						<el-input v-model="addSubDomainData.describe" type="textarea" :rows="2" clearable></el-input>
					</el-form-item>
				</el-form>
			</span>
			<span slot="footer" class="dialog-footer">
				<el-button type="danger" @click="resetForm">重置</el-button>
				<el-button type="primary" @click="addSubDomain">添加</el-button>
				<el-button type="danger" @click="showDialogOfAddSubDomain = false">取
					消</el-button>
			</span>
		</el-dialog>

		<!-- 当文件上传成功时弹出该弹框,要求用户为该新上传的文件选择挂载的子域,并建立联系 -->
		<!-- {% raw %} -->
		<el-dialog title="请为数据选择子域" :visible.sync="showDialogOfSelectSubDomain" width="25%" center>
			<span>
				<el-descriptions title="表信息" :bordered="true" border v-if="result">
					<el-descriptions-item label="表名">{{ result.name }}</el-descriptions-item>
					<el-descriptions-item label="标识符">{{ identifier_table }}</el-descriptions-item>
				</el-descriptions>
				<el-select v-model="subDomainName" filterable default-first-option placeholder="请选子域"
					@change="handleSelectChangeOfSubdomain">
					<el-option v-for="item in optionsOfSubDomain" :key="item.value" :label="item.label" :value="item.value">
					</el-option>
				</el-select>
				<el-descriptions :title="subDomainName" :bordered="true" v-if="selectedOption" border>
					<el-descriptions-item label="描述">{{ selectedOption.describe }}</el-descriptions-item>
				</el-descriptions>
			</span>
			<span slot="footer" class="dialog-footer">
				<el-button type="primary" @click="addRelationBetweenTableAndSubdomain">确定</el-button>
			</span>
		</el-dialog>
		<!-- {% endraw %} -->

		<!-- ==================== 【新增】映射审核对话框 ==================== -->
		<el-dialog
			title="映射审核 - 请检查并修改自动生成的映射"
			:visible.sync="showMappingDialog"
			width="85%"
			:close-on-click-modal="false"
			top="5vh">

			<!-- 统计信息 -->
			<el-alert
				title="映射统计"
				type="info"
				:closable="false"
				style="margin-bottom: 15px;">
				<div>
					<span style="margin-right: 30px;">
						<i class="el-icon-document"></i> 属性映射: <strong>{{ editingMappings.cta.length }}</strong> 个
					</span>
					<span>
						<i class="el-icon-tickets"></i> 值映射: <strong>{{ editingMappings.cea.length }}</strong> 个
					</span>
				</div>
			</el-alert>

			<el-tabs type="border-card">
				<!-- ========== CTA 映射（表属性 → 数据元） ========== -->
				<el-tab-pane label="属性映射 (CTA)">
					<template slot="label">
						<span><i class="el-icon-document"></i> 属性映射</span>
					</template>

					<el-table
						:data="editingMappings.cta"
						border
						stripe
						style="width: 100%"
						max-height="450">

						<el-table-column type="index" label="序号" width="60" align="center"></el-table-column>

						<el-table-column prop="subdomain_data" label="表属性" width="200" align="center">
							<template slot-scope="scope">
								<el-tag type="primary">{{ scope.row.subdomain_data }}</el-tag>
							</template>
						</el-table-column>

						<el-table-column label="映射到数据元" min-width="300">
							<template slot-scope="scope">
								<el-select
									v-model="scope.row.data_element"
									filterable
									placeholder="请选择数据元"
									style="width: 100%;"
									@change="onCTAChange(scope.row, scope.row.data_element)">
									<el-option
										v-for="item in dataElementOptionsForMapping"
										:key="item.value"
										:label="item.label"
										:value="item.value">
										<span style="float: left">{{ item.label }}</span>
									</el-option>
								</el-select>
							</template>
						</el-table-column>

						<el-table-column label="操作" width="100" align="center">
							<template slot-scope="scope">
								<el-button
									type="danger"
									size="mini"
									icon="el-icon-delete"
									@click="deleteCTAMapping(scope.$index)">
									删除
								</el-button>
							</template>
						</el-table-column>
					</el-table>

					<p style="margin-top: 15px; color: #909399; text-align: center;">
						<i class="el-icon-info"></i> 共 <strong>{{ editingMappings.cta.length }}</strong> 个属性映射，您可以修改下拉框选择其他数据元，或删除不需要的映射
					</p>
				</el-tab-pane>

				<!-- ========== CEA 映射（表属性值 → 可允许值） ========== -->
				<el-tab-pane label="值映射 (CEA)">
					<template slot="label">
						<span><i class="el-icon-tickets"></i> 值映射</span>
					</template>

					<el-table
						:data="editingMappings.cea"
						border
						stripe
						style="width: 100%"
						max-height="450">

						<el-table-column type="index" label="序号" width="60" align="center"></el-table-column>

						<el-table-column prop="subdomain_value" label="表属性值" width="150" align="center">
							<template slot-scope="scope">
								<el-tag type="success" size="small">{{ scope.row.subdomain_value }}</el-tag>
							</template>
						</el-table-column>

						<el-table-column prop="subdomain_data" label="所属表属性" width="150" align="center">
							<template slot-scope="scope">
								<el-tag type="info" size="small">{{ scope.row.subdomain_data }}</el-tag>
							</template>
						</el-table-column>

						<el-table-column label="映射到可允许值" min-width="300">
							<template slot-scope="scope">
								<el-select
									v-model="scope.row.mdr_value"
									filterable
									placeholder="请选择可允许值"
									style="width: 100%;"
									@change="onCEAChange(scope.row, scope.row.mdr_value)">
									<el-option
										v-for="item in permissibleValuesOptionsForMapping"
										:key="item.value"
										:label="item.label"
										:value="item.value">
										<span style="float: left">{{ item.label }}</span>
									</el-option>
								</el-select>
							</template>
						</el-table-column>

						<el-table-column label="操作" width="100" align="center">
							<template slot-scope="scope">
								<el-button
									type="danger"
									size="mini"
									icon="el-icon-delete"
									@click="deleteCEAMapping(scope.$index)">
									删除
								</el-button>
							</template>
						</el-table-column>
					</el-table>

					<p style="margin-top: 15px; color: #909399; text-align: center;">
						<i class="el-icon-info"></i> 共 <strong>{{ editingMappings.cea.length }}</strong> 个值映射，您可以修改下拉框选择其他可允许值，或删除不需要的映射
					</p>
				</el-tab-pane>
			</el-tabs>

			<div slot="footer" class="dialog-footer">
				<el-button @click="showMappingDialog = false">
					<i class="el-icon-close"></i> 取消
				</el-button>
				<el-button
					type="primary"
					@click="confirmMappings"
					:disabled="editingMappings.cta.length === 0 && editingMappings.cea.length === 0">
					<i class="el-icon-check"></i> 确定建立映射
				</el-button>
			</div>
		</el-dialog>
	</div>
</template>

<script>
import * as echarts from 'echarts'
export default {
	data() {
		return {
			activeMenu: '',
			uploadUrl: 'http://localhost:5000/upload', // 后台接收上传的URL
			fileList: [], // 上传的文件列表
			result: null, // 上传成功后的结果
			subDomainName: '',
			showDialogOfAddSubDomain: false,
			addSubDomainData: {
				name: '',
				describe: ''
			},
			optionsOfSubDomain: [],
			selectedOption: null,
			identifier_table: '',
			showDialogOfSelectSubDomain: false,
			graphData: [],
			graphLinks: [],
			categories: ["子域", "表", "表属性", "表属性值", "数据元", "值域", "值域组", "可允许值"],
			activeName: 'first',
			dataElement: '',
			dataElementOptions: [],
			attributeName: '',
			// valueDomain: '',
			valueDomainOptions: [],
			permissibleValues: [],
			permissibleValuesOptions: [],
			attributeValueName: '',

			// 新增：映射相关数据
			showMappingDialog: false,           // 是否显示映射审核对话框
			mappingCandidates: {
				cta: [],                        // CTA候选列表
				cea: []                         // CEA候选列表
			},
			editingMappings: {
				cta: [],                        // 用户审核后的CTA映射
				cea: []                         // 用户审核后的CEA映射
			},
			loadingMapping: false,              // 加载状态
			allDataElements: [],                // 所有数据元（用于下拉框）
			allPermissibleValues: []            // 所有可允许值（用于下拉框）
		}
	},
	mounted() {
		this.getOptionsOfSubDomain();
		this.getDataElementOptions();
		this.getValueDomainOptions();
		this.getValueDomainAndPermissibleValuesOptions();
	},
	methods: {
		goyanhua() {
			if (this.identifier_table === '') {
				this.$message.error("请先选择表格再执行演化");
				return;
			}
			// let id_table = this.identifier_table;
			// 传递 identifier_table 到目标路由
			// console.log()
			this.$router.push({ path: '/head/Data_evolution', query: { identifier_table: this.identifier_table } });
		},
		handleSuccess(response) {
			// 上传成功的回调函数
			if (response && response.success) {
				this.result = {
					name: response.name,
					content: response.content,
				};
				this.identifier_table = response.identifier;
				this.showDialogOfSelectSubDomain = true;
			}
		},
		beforeUpload(file) {
			// 上传之前的钩子函数
			const isXLSX = file.type === 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet';
			if (!isXLSX) {
				this.$message.error('只能上传xlsx文件！');
				return false;
			}
			return true;
		},
		resetForm() {
			this.addSubDomainData.name = '';
			this.addSubDomainData.describe = '';
		},
		dialogClose(done) {
			this.$confirm('确认关闭？')
				.then(_ => {
					done();
				})
				.catch(_ => { });
		},
		changeShowDialogOfAddSubDomain() {
			this.showDialogOfAddSubDomain = true;
		},
		openSuccessful(message) {
			this.$message({
				message: message,
				type: 'success',
				duration: 1000,
				showClose: true,
			});
		},
		addSubDomain() {
			let vm = this;
			this.$axios.get('http://localhost:5000/register/subDomain/addSubDomian', {
				params: {
					name: this.addSubDomainData.name,
					describe: this.addSubDomainData.describe
				}
			})
				.then(function (response) {
					let message = response.data.message
					vm.openSuccessful(message);
					vm.resetForm();
					vm.showDialogOfAddSubDomain = false;
					vm.getOptionsOfSubDomain();
				})
				.catch(function (error) {
					console.log(error);
					// 获取失败消息提示
					this.$message({
						showClose: true,
						message: "添加失败",
						type: 'error',
						duration: 1000
					})
				},

				);
		},
		getOptionsOfSubDomain() {
			this.$axios.get('http://localhost:5000/search/subDomain/getSubDomainOptions')
				.then(response => {
					this.optionsOfSubDomain = response.data.data;
				})
				.catch(error => {
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
		handleSelectChangeOfSubdomain() {
			this.selectedOption = this.optionsOfSubDomain.find(item => item.value === this.subDomainName);
		},
		addRelationBetweenTableAndSubdomain() {
			var vm = this;
			this.$axios.get('http://localhost:5000/register/subDomain/addRelationBetweenTableAndSubDomain', {
				params: {
					sub_domain_name: this.subDomainName,
					identifier: this.identifier_table
				}
			})
				.then(function (response) {
					// 处理新的返回格式
					if (response.data.success) {
						vm.showDialogOfSelectSubDomain = false;
						vm.openSuccessful(response.data.message);
						vm.search();
					} else {
						vm.$message.error(response.data.message || '操作失败');
					}
				})
				.catch(function (error) {
					console.log(error);
					vm.$message.error('请求失败：' + (error.response?.data?.message || error.message));
				},

				);
		},
		// 查询函数
		search() {
			var vm = this;
			this.$axios.get('http://localhost:5000/search/subDomain/getGraphOfTable', {
				params: {
					// name: this.searchInput,
					sub_domain_name: this.subDomainName,
					identifier_table: this.identifier_table
				}
			})
				.then(function (response) {
					if (response.data.data.length == 0) {
						vm.$message.error("查询失败");
					} else {
						vm.graphData = response.data.data.map(function (node, idx) {
							node.id = idx;
							return node;
						});
						vm.graphLinks = response.data.links;
						vm.updateChartOfTableGraph(vm.graphData, vm.graphLinks);
						// vm.tableData = response.data.tableData;
						// vm.showTable = true;
						// vm.descriptionsData = response.data.list;
						// vm.showDescriptions = true;
					}

				})
				.catch(function (error) {
					console.log(error);
					// 获取失败消息提示
					this.$message({
						showClose: true,
						message: '查询失败',
						type: 'error',
						duration: 1000
					})
				},

				);
		},
		updateChartOfTableGraph(graphData, graphLinks) {
			var myChart = echarts.init(document.getElementById("graphOfTable"));
			var vm = this;
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
					categories: [{
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
					nodes: graphData,
					links: graphLinks,
				}]
			};
			myChart.setOption(option, true);
			myChart.off('click');
			myChart.on("click", function (params) {
				var name = params.name
				var category_id = params.data.category;
				var category = vm.categories[category_id];
				if (category == "表属性") {
					vm.attributeName = name;
				};
				if (category == "表属性值") {
					vm.attributeValueName = name;
				}
			});
		},
		handleClick(tab, event) {
			console.log(tab, event);
		},
		getDataElementOptions() {
			this.$axios.get('http://localhost:5000/search/mdr/getDataElementOption')
				.then(response => {
					this.dataElementOptions = response.data.data;
				})
				.catch(error => {
					console.error(error);
					// 获取失败消息提示
					this.$message({
						showClose: true,
						message: "获取失败",
						type: 'error',
						duration: 1000
					})
				},

				);
		},
		getValueDomainOptions() {
			this.$axios.get('http://localhost:5000/search/mdr/getValueDomainOption')
				.then(response => {
					this.valueDomainOptions = response.data.data;
				})
				.catch(error => {
					console.error(error);
					// 获取失败消息提示
					this.$message({
						showClose: true,
						message: "获取失败",
						type: 'error',
						duration: 1000
					})
				},

				);
		},
		getValueDomainAndPermissibleValuesOptions() {
			// this.valueDomainLoading = true;
			this.$axios.get('http://localhost:5000/search/mdr/getValueDomainAndPermissibleValuesOption')
				.then(response => {
					// console.log(response.data.data)
					this.permissibleValuesOptions = response.data.data;
				})
				.catch(error => {
					console.error(error);
					// 获取失败消息提示
					this.$message({
						showClose: true,
						message: "获取失败",
						type: 'error',
						duration: 1000
					})
				},

				);
		},
		// 添加数据元联系
		addRelationBetweenAttributeAndDataElement() {
			var vm = this;
			if (this.attributeName === '') {
				this.$message.error('未选择节点，请选择节点后再进行添加');
				return;
			}
			this.$axios.get('http://localhost:5000/register/subDomain/addRelationBetweenAttributeAndDataElement', {
				params: {
					sub_domain_name: this.subDomainName,
					identifier_table: this.identifier_table,
					name_attribute: this.attributeName,
					identifier_data_element: this.dataElement
				}
			})
				.then(response => {
					vm.openSuccessful("添加成功");
					vm.search();
				})
				.catch(error => {
					console.error(error);
					// // 获取失败消息提示
					// this.$message({
					// 	showClose: true,
					// 	message: "添加失败",
					// 	type: 'error',
					// 	duration: 1000
					// })
				},

				);
		},
		// 添加值域联系
		// addRelationBetweenAttributeAndValueDomain() {
		// 	var vm = this;
		// 	if(this.attributeName === ''){
		// 		this.$message.error('未选择节点，请选择节点后再进行添加');
		// 		return;
		// 	}
		// 	this.$axios.get('http://localhost:5000/register/subDomain/addRelationBetweenAttributeAndValueDomain', {
		// 			params: {
		// 				sub_domain_name: this.subDomainName,
		// 				identifier_table: this.identifier_table,
		// 				name_attribute: this.attributeName,
		// 				identifier_value_domain: this.valueDomain
		// 			}
		// 		})
		// 		.then(response => {
		// 			vm.openSuccessful(response.data.data);
		// 			vm.search();
		// 		})
		// 		.catch(error => {
		// 			console.error(error);
		// 			// 获取失败消息提示
		// 			this.$message({
		// 				showClose: true,
		// 				message: response.data.message,
		// 				type: 'error',
		// 				duration: 1000
		// 			})
		// 		},

		// 		);
		// },
		// 添加表属性名
		addRelationBetweenAttributeValueAndPermissibleValues() {
			var vm = this;
			if (this.attributeValueName === '') {
				this.$message.error('未选择节点，请选择节点后再进行添加');
				return;
			}
			// console.log(this.permissibleValues);
			this.$axios.get('http://localhost:5000/register/subDomain/addRelationBetweenAttributeValueAndPermissibleValues', {
				params: {
					sub_domain_name: this.subDomainName,
					identifier_table: this.identifier_table,
					name_attribute_value: this.attributeValueName,
					identifier_permissible_values: this.permissibleValues[1]
				}
			})
				.then(response => {
					vm.openSuccessful("添加成功");
					vm.search();
				})
				.catch(error => {
					console.error(error);
					// 获取失败消息提示
					this.$message({
						showClose: true,
						message: response.data.message,
						type: 'error',
						duration: 1000
					})
				},
				);
		},

		// ==================== 新增：自动映射相关方法 ====================

		// 【新增】点击"建立映射"按钮
		startAutoMapping() {
			if (!this.subDomainName) {
				this.$message.warning('请先选择子域！');
				return;
			}

			this.loadingMapping = true;

			this.$axios.get('http://localhost:5000/register/subDomain/getMappingCandidates', {
				params: { subdomain_name: this.subDomainName }
			})
			.then(response => {
				if (response.data.success) {
					this.mappingCandidates.cta = response.data.data.cta_candidates || [];
					this.mappingCandidates.cea = response.data.data.cea_candidates || [];

					// 初始化编辑中的映射（用户可以修改）
					this.editingMappings.cta = JSON.parse(JSON.stringify(this.mappingCandidates.cta));
					this.editingMappings.cea = JSON.parse(JSON.stringify(this.mappingCandidates.cea));

					// 加载可选的数据元和可允许值
					this.loadAvailableOptions();

					// 显示审核对话框
					this.showMappingDialog = true;

					this.$message.success(`映射候选生成成功！CTA: ${this.mappingCandidates.cta.length} 个，CEA: ${this.mappingCandidates.cea.length} 个`);
				} else {
					this.$message.error('生成映射候选失败: ' + response.data.message);
				}
			})
			.catch(error => {
				console.error(error);
				this.$message.error('请求失败：' + (error.response?.data?.message || error.message));
			})
			.finally(() => {
				this.loadingMapping = false;
			});
		},

		// 【新增】加载可选的数据元和可允许值
		loadAvailableOptions() {
			// 加载所有数据元（根据子域筛选）
			this.$axios.get('http://localhost:5000/search/mdr/getAllDataElements', {
				params: { subdomain_name: this.subDomainName }
			})
				.then(response => {
					if (response.data.success) {
						this.allDataElements = response.data.data || [];
					}
				})
				.catch(error => {
					console.error('加载数据元失败:', error);
				});

			// 加载所有可允许值（根据子域筛选）
			this.$axios.get('http://localhost:5000/search/mdr/getAllPermissibleValues', {
				params: { subdomain_name: this.subDomainName }
			})
				.then(response => {
					if (response.data.success) {
						this.allPermissibleValues = response.data.data || [];
					}
				})
				.catch(error => {
					console.error('加载可允许值失败:', error);
				});
		},

		// 【新增】确认映射（用户审核后）
		confirmMappings() {
			this.$confirm('确认建立这些映射关系？', '提示', {
				confirmButtonText: '确定',
				cancelButtonText: '取消',
				type: 'warning'
			}).then(() => {
				const loading = this.$loading({
					lock: true,
					text: '正在创建映射关系...',
					spinner: 'el-icon-loading',
					background: 'rgba(0, 0, 0, 0.7)'
				});

				this.$axios.post('http://localhost:5000/register/subDomain/confirmMapping', {
					cta_results: this.editingMappings.cta,
					cea_results: this.editingMappings.cea
				})
				.then(response => {
					loading.close();
					if (response.data.success) {
						this.$message.success('映射创建成功！共创建 ' + response.data.data.total_mappings + ' 个映射');
						this.showMappingDialog = false;

						// 刷新图谱显示
						this.search();
					} else {
						this.$message.error('映射创建失败: ' + response.data.message);
					}
				})
				.catch(error => {
					loading.close();
					console.error(error);
					this.$message.error('请求失败：' + (error.response?.data?.message || error.message));
				});
			}).catch(() => {
				// 用户取消
			});
		},

		// 【新增】用户修改CTA映射（从下拉框选择其他数据元）
		onCTAChange(row, newDataElement) {
			row.data_element = newDataElement;
		},

		// 【新增】用户修改CEA映射（从下拉框选择其他可允许值）
		onCEAChange(row, newValue) {
			row.mdr_value = newValue;
		},

		// 【新增】删除某个CTA映射
		deleteCTAMapping(index) {
			this.$confirm('确认删除该映射？', '提示', {
				confirmButtonText: '确定',
				cancelButtonText: '取消',
				type: 'warning'
			}).then(() => {
				this.editingMappings.cta.splice(index, 1);
				this.$message.success('删除成功');
			}).catch(() => {});
		},

		// 【新增】删除某个CEA映射
		deleteCEAMapping(index) {
			this.$confirm('确认删除该映射？', '提示', {
				confirmButtonText: '确定',
				cancelButtonText: '取消',
				type: 'warning'
			}).then(() => {
				this.editingMappings.cea.splice(index, 1);
				this.$message.success('删除成功');
			}).catch(() => {});
		}
	},

	// 【新增】computed 属性
	computed: {
		// 格式化数据元选项供下拉框使用
		dataElementOptionsForMapping() {
			return this.allDataElements.map(de => ({
				value: de.name,
				label: de.name
			}));
		},

		// 格式化可允许值选项供下拉框使用
		permissibleValuesOptionsForMapping() {
			return this.allPermissibleValues.map(v => ({
				value: v.name,
				label: v.name
			}));
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

.sidebar {
	/* background-color: #f2f2f2; */
	margin: 10px;
	padding: 20px;
	display: flex;
	justify-content: center;
	align-items: center;
	border-radius: 5px;
	box-shadow: 0 2px 5px 0 rgba(0, 0, 0, .2);
}
</style>