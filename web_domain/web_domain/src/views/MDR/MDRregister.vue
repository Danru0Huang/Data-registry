<template>
	<div class="box">
		<el-header style="color: #2fb9c2;font-size: 25px;height: 60px; background-color: #f0f0f0">MDR注册</el-header>

		<!-- Tab切换：手动注册 vs 智能体注册 -->
		<el-tabs v-model="activeTab" type="card" style="margin: 10px 20px 0 170px;">
			<el-tab-pane label="人工注册" name="manual">
			</el-tab-pane>
			<el-tab-pane label="智能化注册" name="agent">
			</el-tab-pane>
		</el-tabs>

		<el-container v-show="activeTab === 'manual'">
			<!-- 左侧按钮 -->
			<el-aside style="width:150px">
				<el-aside id="sidebar" style="width:150px">
					<el-row>
						<el-col>
							<el-button class="button" type="success" @click="changeShowObjectClass">
								对象类
							</el-button>
						</el-col>
					</el-row>
					<el-row>
						<el-col>
							<el-button class="button" type="success" @click="changeShowProperty">
								属性
							</el-button>
						</el-col>
					</el-row>
					<el-row>
						<el-col>
							<el-button class="button" type="success" @click="changeShowConceptualDomain">
								概念域
							</el-button>
						</el-col>
					</el-row>
					<el-row>
						<el-col>
							<el-button class="button" type="success" @click="changeShowDataElementConcept">
								数据元概念
							</el-button>
						</el-col>
					</el-row>
					<el-row>
						<el-col>
							<el-button class="button" type="success" @click="changeShowValueDomain">
								值域
							</el-button>
						</el-col>
					</el-row>
					<el-row>
						<el-col>
							<el-button class="button" type="success" @click="changeShowDataElement">
								数据元
							</el-button>
						</el-col>
					</el-row>
				</el-aside>
			</el-aside>
			<el-main class="main">
				<div class="container">
					<div class="left-panel">
						<!-- 对象类注册 -->
						<div v-show="showObjectClass" class="showbox">
							<div>
								<h3>对象类注册</h3>
							</div>
							<div>
								<el-form ref="registerObjectClassForm" :model="registerObjectClassData" label-width="auto"
									style="margin-top: 20px; width: 90%; " v-show="showObjectClass">
									<el-form-item label="名称:" prop="name">
										<el-input v-model="registerObjectClassData.name" width="20px" clearable
											placeholder="请输入内容"></el-input>
									</el-form-item>
									<el-form-item label="描述:" prop="describe">
										<el-input v-model="registerObjectClassData.describe" width="20px" clearable
											placeholder="请输入内容"></el-input>
									</el-form-item>
									<el-form-item label="创建人员ID:" prop="personId">
										<el-input v-model="registerObjectClassData.personId" width="20px" clearable
											placeholder="请输入内容"></el-input>
									</el-form-item>
									<el-form-item label="创建单位:" prop="department">
										<el-input v-model="registerObjectClassData.department" width="20px" clearable
											placeholder="请输入内容"></el-input>
									</el-form-item>
									<el-button type="primary" @click="registerObjectClass">注册</el-button>
									<el-button type="danger" @click="resetForm('registerObjectClassForm')">重置</el-button>
								</el-form>
							</div>
						</div>

						<!-- 属性注册 -->
						<div v-show="showProperty" class="showbox">
							<div>
								<h3>属性注册</h3>
							</div>
							<div>
								<el-form ref="registerPropertyForm" :model="registerPropertyData" label-width="auto"
									style="margin-top: 20px; width: 90%;" v-show="showProperty">
									<el-form-item label="名称:" prop="name">
										<el-input v-model="registerPropertyData.name" width="20px" clearable
											placeholder="请输入内容"></el-input>
									</el-form-item>
									<el-form-item label="描述:" prop="describe">
										<el-input v-model="registerPropertyData.describe" width="20px" clearable
											placeholder="请输入内容"></el-input>
									</el-form-item>
									<el-form-item label="创建人员ID:" prop="personId">
										<el-input v-model="registerPropertyData.personId" width="20px" clearable
											placeholder="请输入内容"></el-input>
									</el-form-item>
									<el-form-item label="创建单位:" prop="department">
										<el-input v-model="registerPropertyData.department" width="20px" clearable
											placeholder="请输入内容"></el-input>
									</el-form-item>
									<el-button type="primary" @click="registerProperty">注册</el-button>
									<el-button type="danger" @click="resetForm('registerPropertyForm')">重置</el-button>
								</el-form>
							</div>
						</div>

						<!-- 概念域注册 -->
						<div v-show="showConceptualDomain" class="showbox">
							<div>
								<h3 style="margin-bottom: 20px;">概念域注册</h3>
							</div>
							<div>
								<!-- {% raw %} -->
								<el-form :model="registerConceptualDomainData" ref="registerConceptualDomainForm"
									label-width="auto" class="demo-dynamic" style="width: 90%;"
									v-show="showConceptualDomain">
									<el-form-item label="名称:" prop="name">
										<el-input v-model="registerConceptualDomainData.name" width="20px" clearable
											placeholder="请输入内容"></el-input>
									</el-form-item>
									<el-form-item label="描述:" prop="describe">
										<el-input v-model="registerConceptualDomainData.describe" width="20px" clearable
											placeholder="请输入内容"></el-input>
									</el-form-item>
									<el-form-item label="创建人员ID:" prop="personId">
										<el-input v-model="registerConceptualDomainData.personId" width="20px" clearable
											placeholder="请输入内容"></el-input>
									</el-form-item>
									<el-form-item label="创建单位:" prop="department">
										<el-input v-model="registerConceptualDomainData.department" width="20px" clearable
											placeholder="请输入内容"></el-input>
									</el-form-item>
									<el-form-item
										v-for="(valueMeaning, index) in registerConceptualDomainData.valueMeanings"
										:label="'值含义:' + (startIndex + index)" :key="startIndex + index"
										prop="'valueMeaning'  + (startIndex + index)">
										<div style="display: flex; align-items: center;">
											<el-input v-model="registerConceptualDomainData.valueMeanings[index]"
												width="20px" clearable placeholder="请输入内容"></el-input>
											<el-button icon="el-icon-delete" style="margin-left: 10px;"
												@click.prevent="removeValueMeaning(valueMeaning)" circle></el-button>
										</div>
									</el-form-item>
									<el-form-item>
										<el-button type="primary" @click="registerConceptualDomain">注册</el-button>
										<el-button @click="addValueMeaning" icon="el-icon-plus">新增值含义</el-button>
										<el-button type="danger"
											@click="resetForm('registerConceptualDomainForm')">重置</el-button>
									</el-form-item>
								</el-form>
								<!-- {% endraw %} -->
							</div>
						</div>

						<!-- 数据元概念注册 -->
						<div v-show="showDataElementConcept" class="showbox">
							<div>
								<h3>数据元概念注册</h3>
							</div>
							<div>
								<el-form ref="registerDataElementConceptForm" :model="registerDataElementConceptData"
									label-width="auto" style="margin-top: 20px; width:90%;" v-show="showDataElementConcept">
									<el-form-item label="名称:" prop="name">
										<el-input v-model="registerDataElementConceptData.name" width="20px" clearable
											placeholder="请输入内容"></el-input>
									</el-form-item>
									<el-form-item label="描述:" prop="describe">
										<el-input v-model="registerDataElementConceptData.describe" width="20px" clearable
											placeholder="请输入内容"></el-input>
									</el-form-item>
									<el-form-item label="创建人员ID:" prop="personId">
										<el-input v-model="registerDataElementConceptData.personId" width="20px" clearable
											placeholder="请输入内容"></el-input>
									</el-form-item>
									<el-form-item label="创建单位:" prop="department">
										<el-input v-model="registerDataElementConceptData.department" width="20px" clearable
											placeholder="请输入内容"></el-input>
									</el-form-item>
									<el-form-item label="对象类:" prop="objectClass">
										<el-select v-model="registerDataElementConceptData.objectClass" filterable remote
											@focus="searchObjectClass" :loading="objectClassLoading" :value-key="'label'">
											<!-- {% raw %} -->
											<el-option v-for="(option, index) in objectClassOptions" :key="index"
												:label="option.label" :value="option.value">
												<span style="float: left">{{ option.label }}</span>
												<span style="float: right; color: #8492a6; font-size: 13px">{{ option.value
												}}</span>
											</el-option>
											<!-- {% endraw %} -->
										</el-select>
									</el-form-item>

									<el-form-item label="属性" prop="property">
										<el-select v-model="registerDataElementConceptData.property" filterable remote
											@focus="searchProperty" :loading="propertyLoading" :value-key="'label'">
											<!-- {% raw %} -->
											<el-option v-for="(option, index) in propertyOptions" :key="index"
												:label="option.label" :value="option.value">
												<span style="float: left">{{ option.label }}</span>
												<span style="float: right; color: #8492a6; font-size: 13px">{{ option.value
												}}</span>
											</el-option>
											<!-- {% endraw %} -->
										</el-select>
									</el-form-item>

									<el-form-item label="概念域" prop="conceptualDomain">
										<el-select v-model="registerDataElementConceptData.conceptualDomain" filterable
											remote @focus="searchConceptualDomain" :loading="conceptualDomainLoading"
											:value-key="'label'">
											<!-- {% raw %} -->
											<el-option v-for="(option, index) in conceptualDomainOptions" :key="index"
												:label="option.label" :value="option.value">
												<span style="float: left">{{ option.label }}</span>
												<span style="float: right; color: #8492a6; font-size: 13px">{{ option.value
												}}</span>
											</el-option>
											<!-- {% endraw %} -->
										</el-select>
									</el-form-item>

									<el-form-item>
										<el-button type="primary" @click="registerDataElementConcept">注册</el-button>
										<el-button type="danger"
											@click="resetForm('registerDataElementConceptForm')">重置</el-button>
									</el-form-item>
								</el-form>
							</div>
						</div>

						<!-- 值域注册 -->
						<div v-show="showValueDomain" class="showbox">
							<div>
								<h3>值域注册</h3>
							</div>
							<div>
								<el-form ref="registerValueDomainForm" :model="registerValueDomainData" label-width="auto"
									style="margin-top: 20px; width: 90%;" v-show="showValueDomain">
									<el-form-item label="名称:" prop="name">
										<el-input v-model="registerValueDomainData.name" width="20px" clearable
											placeholder="请输入内容"></el-input>
									</el-form-item>
									<el-form-item label="描述:" prop="describe">
										<el-input v-model="registerValueDomainData.describe" width="20px" clearable
											placeholder="请输入内容"></el-input>
									</el-form-item>
									<el-form-item label="创建人员ID:" prop="personId">
										<el-input v-model="registerValueDomainData.personId" width="20px" clearable
											placeholder="请输入内容"></el-input>
									</el-form-item>
									<el-form-item label="创建单位:" prop="department">
										<el-input v-model="registerValueDomainData.department" width="20px" clearable
											placeholder="请输入内容"></el-input>
									</el-form-item>
									<el-form-item label="不可枚举:" prop="indefinite">
										<el-input v-model="registerValueDomainData.indefinite" width="20px" clearable
											placeholder="请输入内容"></el-input>
									</el-form-item>

									<el-form-item label="可枚举:" prop="enumerable">
										<div v-for="(item, index) in registerValueDomainData.enumerable" :key="index">
											<el-form-item>
												<div style="align-items:left;">
													<div style="width: 100%; display: flex;">
														<el-input v-model="item.value" placeholder="请输入值"
															clearable></el-input>
														<el-input v-model="item.num" placeholder="请输入组号"
															clearable></el-input>
													</div>
													<div style="align-items: center; display: flex;">
														<el-select v-model="item.valueMeaning" filterable remote
															@focus="searchValueMeanings" :loading="valueMeaningsLoading"
															:value-key="'label'">
															<!-- {% raw %} -->
															<el-option v-for="(option, index) in valueMeaningsOptions"
																:key="index" :label="option.label" :value="option.value"
																placeholder="值含义">
																<span style="float: left">{{ option.label }}</span>
																<span
																	style="float: right; color: #8492a6; font-size: 13px">{{
																		option.value }}</span>
															</el-option>
															<!-- {% endraw %} -->
														</el-select>
														<el-button icon="el-icon-delete"
															@click.prevent="removePermissibleValues(item)"></el-button>
													</div>
												</div>
											</el-form-item>
										</div>
										<div>
											<el-button type="primary" icon="el-icon-plus"
												@click="addValueDomainItem">添加</el-button>
										</div>
									</el-form-item>
									<el-form-item label="概念域" prop="conceptualDomain">
										<el-select v-model="registerValueDomainData.conceptualDomain" filterable remote
											@focus="searchConceptualDomain" :loading="conceptualDomainLoading"
											:value-key="'label'">
											<!-- {% raw %} -->
											<el-option v-for="(option, index) in conceptualDomainOptions" :key="index"
												:label="option.label" :value="option.value">
												<span style="float: left">{{ option.label }}</span>
												<span style="float: right; color: #8492a6; font-size: 13px">{{ option.value
												}}</span>
											</el-option>
											<!-- {% endraw %} -->
										</el-select>
									</el-form-item>

									<el-form-item>
										<el-button type="primary" @click="registerValueDomain">注册</el-button>
										<el-button type="danger"
											@click="resetForm('registerValueDomainForm')">重置</el-button>
									</el-form-item>
								</el-form>
							</div>
						</div>

						<!-- 数据元注册 -->
						<div v-show="showDataElement" class="showbox">
							<div>
								<h3>数据元注册</h3>
							</div>
							<div>
								<el-form ref="registerDataElementForm" :model="registerDataElementData" label-width="auto"
									style="margin-top: 20px; width: 90%;" v-show="showDataElement">
									<el-form-item label="名称:" prop="name">
										<el-input v-model="registerDataElementData.name" width="20px" clearable
											placeholder="请输入内容"></el-input>
									</el-form-item>
									<el-form-item label="描述:" prop="describe">
										<el-input v-model="registerDataElementData.describe" width="20px" clearable
											placeholder="请输入内容"></el-input>
									</el-form-item>
									<el-form-item label="创建人员ID:" prop="personId">
										<el-input v-model="registerDataElementData.personId" width="20px" clearable
											placeholder="请输入内容"></el-input>
									</el-form-item>
									<el-form-item label="创建单位:" prop="department">
										<el-input v-model="registerDataElementData.department" width="20px" clearable
											placeholder="请输入内容"></el-input>
									</el-form-item>
									<el-form-item label="数据元概念:" prop="dataElementConcept">
										<el-select v-model="registerDataElementData.dataElementConcept" filterable remote
											@focus="searchDataElementConcept" :loading="dataElementConceptLoading"
											:value-key="'label'">
											<!-- {% raw %} -->
											<el-option v-for="(option, index) in dataElementConceptOptions" :key="index"
												:label="option.label" :value="option.value">
												<span style="float: left">{{ option.label }}</span>
												<span style="float: right; color: #8492a6; font-size: 13px">{{ option.value
												}}</span>
											</el-option>
											<!-- {% endraw %} -->
										</el-select>
									</el-form-item>
									<el-form-item label="值域:" prop="valueDomain">
										<el-select v-model="registerDataElementData.valueDomain" filterable remote
											@focus="searchValueDomain" :loading="valueDomainLoading" :value-key="'label'">
											<!-- {% raw %} -->
											<el-option v-for="(option, index) in valueDomainOptions" :key="index"
												:label="option.label" :value="option.value">
												<span style="float: left">{{ option.label }}</span>
												<span style="float: right; color: #8492a6; font-size: 13px">{{ option.value
												}}</span>
											</el-option>
											<!-- {% endraw %} -->
										</el-select>
									</el-form-item>
									<el-form-item>
										<el-button type="primary" @click="registerDataElement">注册</el-button>
										<el-button type="danger"
											@click="resetForm('registerDataElementForm')">重置</el-button>
									</el-form-item>
								</el-form>
							</div>
						</div>
					</div>
					<!--  信息模型查询 -->
					<div class="right-panel">
						<el-card style="margin-top:10px; min-height:85vh;">
							<!-- 选择查询模型 -->
							<div slot="header" style="text-align: center;">
								<el-select v-model="selectedModelName" filterable @change="search" placeholder="请选择查询模型">
									<el-option v-for="item in optionsOfModelName" :key="item.value" :label="item.label"
										:value="item.value"></el-option>
								</el-select>
							</div>
							<div id="chartIdModelGraph"
								style="width: 60%; height: 77vh; margin-top:110px;margin-right:28px">
								<!-- 在这里放置您的图表内容 -->
							</div>
						</el-card>
					</div>
				</div>
			</el-main>
		</el-container>

		<!-- 智能体自动注册Tab -->
		<div v-show="activeTab === 'agent'" style="margin-left: 170px;">
			<AgentRegister />
		</div>
	</div>
</template>


<script>
import * as echarts from 'echarts';
import AgentRegister from '../../components/MDR/AgentRegister.vue';

export default {
	components: {
		AgentRegister
	},
	data() {
		return {
			// Tab切换
			activeTab: 'manual',
			// 信息模型查询数据
			selectedModelName: '',
			optionsOfModelName: [],
			dialogVisible: false,
			nodeDetails: {},
			categories: ["模型", "模型类", "模型属性"],
			descriptionsData: [],
			showDescriptions: false,
			// MDR数据
			startIndex: 1,
			graphData: {
				nodes: [],
				links: []
			},
			showObjectClass: true,
			showProperty: false,
			showConceptualDomain: false,
			showDataElementConcept: false,
			showValueDomain: false,
			showDataElement: false,
			registerObjectClassData: {
				name: '',
				describe: '',
				personId: '',
				department: ''
			},
			registerPropertyData: {
				name: '',
				describe: '',
				personId: '',
				department: ''
			},
			registerConceptualDomainData: {
				name: '',
				describe: '',
				personId: '',
				department: '',
				valueMeanings: []
			},
			registerDataElementConceptData: {
				name: '',
				describe: '',
				personId: '',
				department: '',
				objectClass: '',
				property: '',
				conceptualDomain: ''
			},
			registerValueDomainData: {
				name: '',
				describe: '',
				personId: '',
				department: '',
				conceptualDomain: '',
				indefinite: '',
				enumerable: []
			},
			registerDataElementData: {
				name: '',
				describe: '',
				personId: '',
				department: '',
				dataElementConcept: '',
				valueDomain: '',
				evolution: "no"
			},
			objectClassOptions: [],
			objectClassLoading: false,
			propertyOptions: [],
			propertyLoading: false,
			conceptualDomainOptions: [],
			conceptualDomainLoading: false,
			valueMeaningsOptions: [],
			valueMeaningsLoading: false,
			dataElementConceptOptions: [],
			dataElementConceptLoading: false,
			valueDomainOptions: [],
			valueDomainLoading: false
		}
	},
	mounted() {
		this.getOptionsOfModelName();
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
						vm.updateChart(vm.graphData, vm.graphLinks);
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
		showNodeResult(nodeDetails) {
			this.nodeDetails = nodeDetails;
			this.dialogVisible = true;
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
		updateChart(graphData, graphLinks) {
			var myChart = echarts.init(document.getElementById('chartIdModelGraph'));

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
		},
		// updateChart(graphData) {
		// 	// var ROOT_PATH = 'https://echarts.apache.org/examples';
		// 	var chartDom = document.getElementById('chartIdModelGraph');
		// 	// 检查是否已经存在图表实例
		// 	var existingChart = echarts.getInstanceByDom(chartDom);
		// 	if (existingChart) {
		// 		// 如果已经存在，销毁它
		// 		existingChart.dispose();
		// 	}
		// 	var myChart = echarts.init(chartDom);

		// 	// myChart.showLoading();
		// 	// $.getJSON(ROOT_PATH + '/data/asset/data/les-miserables.json', function (graph) {
		// 	// myChart.hideLoading();
		// 		// console.log(graphData)
		// 	var option = {
		// 			tooltip: {
		// 				formatter: function(params) {
		// 				const nodeData = params.data;
		// 				let tooltipContent = `名称：${nodeData.name}<br/>`;

		// 				// 检查描述是否存在
		// 				if (nodeData.description) {
		// 					tooltipContent += `描述：${nodeData.description}<br/>`;
		// 				}

		// 				// 检查创建人员ID是否存在
		// 				if (nodeData.personId) {
		// 					tooltipContent += `创建人员ID：${nodeData.personId}<br/>`;
		// 				}

		// 				// 检查是否有效是否存在
		// 				if (nodeData.valuename) {
		// 					if(nodeData.valuename === 1)
		// 					{
		// 						tooltipContent += `是否有效：有效<br/>`;
		// 					}else{
		// 						tooltipContent += `是否有效：无效<br/>`;
		// 					}
		// 				}
		// 				// 检查选择类ID
		// 				if (nodeData.valueID) {
		// 					tooltipContent += `模型ID：${nodeData.valueID}<br/>`;
		// 				}

		// 				// 检查组号是否存在
		// 				if (nodeData.valuenum) {
		// 					tooltipContent += `组号：${nodeData.valuenum}`;
		// 				}

		// 				return tooltipContent;
		// 			}
		// 			},
		//         title: {
		//             textStyle: {
		//                 fontWeight: "lighter"
		//             }
		//         },
		//         // animationDurationUpdate 设置图表更新动画的持续时间
		//         animationDurationUpdate: 1500,
		//         // animationEasingUpdate 设置图表更新动画的缓动效果
		//         animationEasingUpdate: 'quinticInOut',
		//         legend: {
		//             x: "center",
		//             show: true,
		//             data: ["对象类", "属性", "概念域","值含义","数据元概念","值域","枚举","数据元"]
		//         },
		//         series: [{
		//             type: 'graph',
		//             layout: 'force',
		//             symbolSize: 60,
		//             edgeSymbol: ['circle', 'arrow'],
		//             edgeSymbolSize: [4, 4],
		//             edgeLabel: {
		//                 normal: {
		//                     show: true,
		//                     textStyle: {
		//                         fontSize: 12
		//                     },
		//                     formatter: "{c}"
		//                 }
		//             },
		//             force: {
		//                 repulsion: 2500,
		//                 edgeLength: [10, 100]
		//             },
		//             focusNodeAdjacency: true,
		//             draggable: true,
		//             roam: true,
		//             categories: [{
		//                     name: '对象类'
		//                 },
		//                 {
		//                     name: '属性'
		//                 },
		//                 {
		//                     name: '概念域'
		//                 },
		// 				{
		// 					name: '值含义'
		// 				},
		// 				{
		// 					name: '数据元概念'
		// 				},
		// 				{
		// 					name: '值域'
		// 				},
		// 				{
		// 					name: '枚举'
		// 				},
		// 				{
		// 					name: '数据元'
		// 				}
		//             ],
		//             label: {
		//                 normal: {
		//                     show: true,
		//                     textStyle: {
		//                         fontSize: 15
		//                     },
		//                 }
		//             },
		//             lineStyle: {
		//                 normal: {
		//                     opacity: 0.9,
		//                     width: 1,
		//                     curveness: 0.3
		//                 }
		//             },
		//             nodes: graphData.nodes,
		//             links: graphData.links,
		//         }]
		//     };
		// 	myChart.setOption(option);
		// 	// option && myChart.setOption(option);
		// },
		openSuccessful(message) {
			this.$message({
				message: message,
				type: 'success',
				duration: 1000,
				showClose: true,
			});
		},
		//注册对象类 
		registerObjectClass() {
			var vm = this;
			// const node = 
			// 	{
			// 		name: this.registerObjectClassData.name,
			// 		description: this.registerObjectClassData.describe,
			// 		personId: this.registerObjectClassData.personId,
			// 		department: this.registerObjectClassData.department,
			// 		category: '对象类'
			// 	}
			// this.graphData.nodes.push(node);
			// this.updateChart(this.graphData);
			this.$axios.post('http://localhost:5000/register/mdr/objectClass', this.registerObjectClassData)
				.then(response => {
					let message = response.data.message
					vm.openSuccessful(message);
					// console.log(this.registerObjectClassData)
					vm.resetForm("registerObjectClassForm");

				})
				.catch(error => {
					console.error(error);
					// 获取失败消息提示
					this.$message({
						showClose: true,
						message: "注册失败",
						type: 'error',
						duration: 1000
					})
				},
				);
		},
		// 注册属性
		registerProperty() {
			var vm = this;
			// const node = 
			// 	{
			// 		name: this.registerPropertyData.name,
			// 		description: this.registerPropertyData.describe,
			// 		personId: this.registerPropertyData.personId,
			// 		department: this.registerPropertyData.department,
			// 		category: '属性'
			// 	}
			// this.graphData.nodes.push(node);
			// this.updateChart(this.graphData);
			this.$axios.post('http://localhost:5000/register/mdr/property', this.registerPropertyData)
				.then(response => {
					let message = response.data.message
					vm.openSuccessful(message);
					vm.resetForm("registerPropertyForm");
				})
				.catch(error => {
					console.error(error);
					// 获取失败消息提示
					this.$message({
						showClose: true,
						message: "注册失败",
						type: 'error',
						duration: 1000
					})
				},

				);
		},
		// 注册概念域
		registerConceptualDomain() {
			var vm = this;
			// 创建起始节点
			// const sourceNode = 
			// 	{
			// 		name: this.registerConceptualDomainData.name,
			// 		description: this.registerConceptualDomainData.describe,
			// 		personId: this.registerConceptualDomainData.personId,
			// 		department: this.registerConceptualDomainData.department,
			// 		category: '概念域'
			// 	}
			// // console.log(this.registerConceptualDomainData.valueMeanings)
			// // 创建目标节点列表
			// const targetNodes = this.registerConceptualDomainData.valueMeanings.map(value => {
			// 	return {
			// 		name: value,
			// 		category: '值含义' 
			// 	};
			// });
			// // console.log(targetNodes)
			// // 创建起始节点到目标节点的边
			// const edges = targetNodes.map(target => {
			// 	return {
			// 		source: sourceNode.name, // 起始节点的名称
			// 		target: target.name, // 目标节点的名称
			// 		name: "值含义",
			// 		value: "值含义"
			// 	};
			// });
			// // 将起始节点和目标节点添加到图数据中
			// this.graphData.nodes.push(sourceNode);
			// this.graphData.nodes.push(...targetNodes);
			// this.graphData.links.push(...edges);
			// this.updateChart(this.graphData);
			this.$axios.post('http://localhost:5000/register/mdr/conceptualDomain', this.registerConceptualDomainData)
				.then(response => {
					let message = response.data.message
					vm.openSuccessful(message);
					vm.resetForm("registerConceptualDomainForm");
				})
				.catch(error => {
					console.error(error);
					// 获取失败消息提示
					this.$message({
						showClose: true,
						message: "注册失败",
						type: 'error',
						duration: 1000
					})
				},

				);
		},
		// 数据元概念注册
		registerDataElementConcept() {
			var vm = this;
			// let index = 1;
			// // 创建节点
			// const node = 
			// {
			// 	name: this.registerDataElementConceptData.name,
			// 	description: this.registerDataElementConceptData.describe,
			// 	personId: this.registerDataElementConceptData.personId,
			// 	department: this.registerDataElementConceptData.department,
			// 	category: '数据元概念'
			// }
			// const nodeclass = 
			// {
			// name: `对象类${index++}`,
			// 	valueID: this.registerDataElementConceptData.objectClass,
			// 	category: '对象类'
			// }
			// index = 1;
			// const nodeproperty = 
			// {
			// 	name: `属性${index++}`,
			// 	valueID: this.registerDataElementConceptData.property,
			// 	category: '属性'
			// }
			// index = 1;
			// const nodeconceptualDomain = 
			// {
			// 	name: `概念域${index++}`,
			// 	valueID: this.registerDataElementConceptData.conceptualDomain,
			// 	category: '概念域'
			// }

			// this.graphData.nodes.push(node);
			// this.graphData.nodes.push(nodeclass);
			// this.graphData.nodes.push(nodeproperty);
			// this.graphData.nodes.push(nodeconceptualDomain);

			// // 创建边对象并指定边的名称
			// const edge1 = {
			// 	source: node.name, // 起始节点是node
			// 	target: nodeclass.name, // 目标节点是nodeclass
			// 	name: "对象类与数据元概念", // 边的名称
			// 	value: "对象类与数据元概念"
			// };

			// const edge2 = {
			// 	source: node.name, // 起始节点是node
			// 	target: nodeproperty.name, // 目标节点是nodeproperty
			// 	name: "属性与数据元概念", // 边的名称
			// 	value: "属性与数据元概念"
			// };

			// const edge3 = {
			// 	source: node.name, // 起始节点是node
			// 	target: nodeconceptualDomain.name, // 目标节点是nodeconceptualDomain
			// 	name: "概念域与数据元概念", // 边的名称
			// 	value: "概念域与数据元概念"
			// };

			// // 将边对象添加到图的边数组中
			// this.graphData.links.push(edge1);
			// this.graphData.links.push(edge2);
			// this.graphData.links.push(edge3);
			// this.updateChart(this.graphData)
			this.$axios.post('http://localhost:5000/register/mdr/dataElementConcept', this.registerDataElementConceptData)
				.then(response => {
					let message = response.data.message
					vm.openSuccessful(message);
					vm.resetForm("registerDataElementConceptForm");
				})
				.catch(error => {
					console.error(error);
					// 获取失败消息提示
					this.$message({
						showClose: true,
						message: "注册失败",
						type: 'error',
						duration: 1000
					})
				},

				);
		},
		// 值域注册
		registerValueDomain() {
			var vm = this;
			// let index = 1;
			// // console.log(this.registerValueDomainData.enumerable)
			// const node = 
			// {
			// 	name: this.registerValueDomainData.name,
			// 	description: this.registerValueDomainData.describe,
			// 	personId: this.registerValueDomainData.personId,
			// 	department: this.registerValueDomainData.department,
			// 	category: '值域'
			// }
			// const nodeconceptualDomain = 
			// {
			// 	name: `概念域${index++}`,
			// 	valueID: this.registerValueDomainData.conceptualDomain,
			// 	category: '概念域'
			// }
			// const nodeindefinite = 
			// {
			// 	name: "不可枚举值",
			// 	value: this.registerValueDomainData.indefinite,
			// 	category: '枚举'
			// }

			// const edge1 = {
			// 	source: node.name, // 起始节点是node
			// 	target: nodeconceptualDomain.name, // 目标节点是nodeconceptualDomain
			// 	name: "概念域与值域", // 边的名称
			// 	value: "概念域与值域"
			// };
			// const edge2 = {
			// 	source: node.name, // 起始节点是node
			// 	target: nodeindefinite.name, // 目标节点是nodeconceptualDomain
			// 	name: "不可枚举", // 边的名称
			// 	value: "不可枚举"
			// };

			// 	// 创建目标节点列表
			// 	// 假设registerValueDomainData.enumerable是一个包含多个对象的数组
			// 	// const nodeValue = this.registerValueDomainData.enumerable.map(item => item.value);

			// 	// //现在nodeValue数组中包含了registerValueDomainData.enumerable中每个对象的value值
			// 	// console.log(this.registerValueDomainData.enumerable);
			// 	// this.registerValueDomainData.enumerable.forEach(element => {
			// 	// });
			// index = 1;
			// const targetNodes = this.registerValueDomainData.enumerable.map(({ num, value, valueID }) => {
			// 	return {
			// 		name: `可枚举值${index += 1}`,
			// 		valuenum: num,
			// 		valuename: value,
			// 		valueID: valueID,
			// 		category: '枚举' 
			// 	};
			// });
			// 	// console.log(targetNodes)
			// 	// 创建起始节点到目标节点的边
			// const edges = targetNodes.map(target => {
			// 	return {
			// 		source: node.name, // 起始节点的名称
			// 		target: target.name, // 目标节点的名称
			// 		name: "可枚举",
			// 		value: "可枚举"
			// 	};
			// });
			// this.graphData.nodes.push(node);
			// this.graphData.nodes.push(nodeconceptualDomain);
			// this.graphData.nodes.push(nodeindefinite)

			// this.graphData.links.push(edge1);
			// this.graphData.links.push(edge2);

			// this.graphData.links.push(...edges);
			// this.graphData.nodes.push(...targetNodes);

			// this.updateChart(this.graphData);
			this.$axios.post('http://localhost:5000/register/mdr/valueDomain', this.registerValueDomainData)
				.then(response => {
					let message = response.data.message
					vm.openSuccessful(message);
					vm.resetForm("registerValueDomainForm");
				})
				.catch(error => {
					console.error(error);
					// 获取失败消息提示
					this.$message({
						showClose: true,
						message: "注册失败",
						type: 'error',
						duration: 1000
					})
				},

				);
		},
		// 数据元注册
		registerDataElement() {
			var vm = this;
			// let index = 1;
			// const node = 
			// 	{
			// 		name: this.registerDataElementData.name,
			// 		description: this.registerDataElementData.describe,
			// 		personId: this.registerDataElementData.personId,
			// 		department: this.registerDataElementData.department,
			// 		category: '数据元'
			// 	}
			// const nodedataElementConcept = 
			// {
			// 	name: `数据元概念${index++}`,
			// 	valueID: this.registerDataElementData.dataElementConcept,
			// 	category: '数据元概念'
			// }
			// index = 1;
			// const nodevalueDomain = 
			// {
			// 	name: `值域${index++}`,
			// 	valueID: this.registerDataElementData.valueDomain,
			// 	category: '值域'
			// }
			// const edge1 = {
			// 	source: node.name, // 起始节点是node
			// 	target: nodevalueDomain.name, // 目标节点是nodeconceptualDomain
			// 	name: "值域与数据元", // 边的名称
			// 	value: "值域与数据元"
			// };
			// const edge2 = {
			// 	source: node.name, // 起始节点是node
			// 	target: nodedataElementConcept.name, // 目标节点是nodeconceptualDomain
			// 	name: "数据元概念与数据元", // 边的名称
			// 	value: "数据元概念与数据元"
			// };
			// this.graphData.nodes.push(node);
			// this.graphData.nodes.push(nodedataElementConcept);
			// this.graphData.nodes.push(nodevalueDomain);

			// this.graphData.links.push(edge1);
			// this.graphData.links.push(edge2);
			// this.updateChart(this.graphData);
			this.$axios.post('http://localhost:5000/register/mdr/dataElement', this.registerDataElementData)
				.then(response => {
					let message = response.data.message
					vm.openSuccessful(message);
					vm.resetForm("registerDataElementForm");
				})
				.catch(error => {
					console.error(error);
					// 获取失败消息提示
					this.$message({
						showClose: true,
						message: '注册失败',
						type: 'error',
						duration: 1000
					})
				},

				);
		},
		changeShowObjectClass() {
			this.showObjectClass = true;
			this.showProperty = false;
			this.showConceptualDomain = false;
			this.showDataElementConcept = false;
			this.showValueDomain = false;
			this.showDataElement = false;
		},
		changeShowProperty() {
			this.showObjectClass = false;
			this.showProperty = true;
			this.showConceptualDomain = false;
			this.showDataElementConcept = false;
			this.showValueDomain = false;
			this.showDataElement = false;
		},
		changeShowConceptualDomain() {
			this.showObjectClass = false;
			this.showProperty = false;
			this.showConceptualDomain = true;
			this.showDataElementConcept = false;
			this.showValueDomain = false;
			this.showDataElement = false;
		},
		changeShowDataElementConcept() {
			this.showObjectClass = false;
			this.showProperty = false;
			this.showConceptualDomain = false;
			this.showDataElementConcept = true;
			this.showValueDomain = false;
			this.showDataElement = false;
		},
		changeShowValueDomain() {
			this.showObjectClass = false;
			this.showProperty = false;
			this.showConceptualDomain = false;
			this.showDataElementConcept = false;
			this.showValueDomain = true;
			this.showDataElement = false;
		},
		changeShowDataElement() {
			this.showObjectClass = false;
			this.showProperty = false;
			this.showConceptualDomain = false;
			this.showDataElementConcept = false;
			this.showValueDomain = false;
			this.showDataElement = true;
		},
		// 查询对象类
		searchObjectClass(query) {
			this.objectClassLoading = true;
			this.$axios.get('http://localhost:5000/search/mdr/getObjectClassOptions', {
				params: {
					query: query
				}
			})
				.then(response => {

					this.objectClassOptions = response.data.data;
					this.objectClassLoading = false;
					// console.log(this.objectClassOptions)
				})
				.catch(error => {
					console.error(error);
					this.objectClassLoading = false;
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
		searchProperty(query) {
			this.propertyLoading = true;
			this.$axios.get('http://localhost:5000/search/mdr/getPropertyOption', {
				params: {
					query: query
				}
			})
				.then(response => {
					this.propertyOptions = response.data.data;
					this.propertyLoading = false;
				})
				.catch(error => {
					console.error(error);
					this.propertyLoading = false;
				});
		},
		searchConceptualDomain(query) {
			this.conceptualDomainLoading = true;
			this.$axios.get('http://localhost:5000/search/mdr/getConceptualDomainOption', {
				params: {
					query: query
				}
			})
				.then(response => {
					this.conceptualDomainOptions = response.data.data;
					this.conceptualDomainLoading = false;
				})
				.catch(error => {
					console.error(error);
					this.conceptualDomainLoading = false;
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
		searchValueMeanings(query) {
			this.valueMeaningsLoading = true;
			this.$axios.get('http://localhost:5000/search/mdr/getValueMeaningsOption', {
				params: {
					query: query
				}
			})
				.then(response => {
					this.valueMeaningsOptions = response.data.data;
					this.valueMeaningsLoading = false;
				})
				.catch(error => {
					console.error(error);
					this.valueMeaningsLoading = false;
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
		searchDataElementConcept(query) {
			this.dataElementConceptLoading = true;
			this.$axios.get('http://localhost:5000/search/mdr/getDataElementConceptOption', {
				params: {
					query: query
				}
			})
				.then(response => {
					this.dataElementConceptOptions = response.data.data;
					this.dataElementConceptLoading = false;
				})
				.catch(error => {
					console.error(error);
					this.dataElementConceptLoading = false;
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
		searchValueDomain(query) {
			this.valueDomainLoading = true;
			this.$axios.get('http://localhost:5000/search/mdr/getValueDomainOption', {
				params: {
					query: query
				}
			})
				.then(response => {
					this.valueDomainOptions = response.data.data;
					this.valueDomainLoading = false;
				})
				.catch(error => {
					console.error(error);
					this.valueDomainLoading = false;
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

		resetForm(formName) {
			this.$refs[formName].resetFields();
			if (formName == "registerConceptualDomainForm") {
				this.registerConceptualDomainData.valueMeanings = [];
			};
			if (formName == "registerValueDomainForm") {
				this.registerValueDomainData.enumerable = [];
			};
		},

		removeValueMeaning(item) {
			var index = this.registerConceptualDomainData.valueMeanings.indexOf(item);
			if (index !== -1) {
				this.registerConceptualDomainData.valueMeanings.splice(index, 1)
			}
		},
		removePermissibleValues(item) {
			var index = this.registerValueDomainData.enumerable.indexOf(item);
			if (index !== -1) {
				this.registerValueDomainData.enumerable.splice(index, 1);
			};
		},
		addValueMeaning() {
			this.registerConceptualDomainData.valueMeanings.push('')
		},
		addValueDomainItem() {
			this.registerValueDomainData.enumerable.push({
				value: '',
				valueMeaning: '',
				num: ''
			});
		}
	}

}
</script>

<style scoped>
.container {
	display: flex;
	justify-content: space-between;
}

.left-panel {
	width: 35%;
}

.right-panel {
	width: 63%;
	/* 右侧占据剩余宽度 */
}

.box {
	margin-left: 250px;
}

.el-menu-vertical-demo {
	height: 100vh;
}

.el-header {
	/* background-color: #B3C0D1; */
	color: #333;
	line-height: 60px;
	text-align: center;
}

.el-container {
	height: 100vh;
}

.el-aside {
	color: #333;
}

.text {
	font-size: 14px;
}

.item {
	margin-bottom: 18px;
}

#sidebar {
	/* background-color: #f2f2f2; */
	padding: 20px;
}

.button {
	margin-bottom: 10px;
	margin-top: 10px;
	width: 100px;
}

.el-row {
	margin: 20px;
}

.main {
	/* display: flex;
		justify-content: center; */
	position: relative;
}

.showbox {
	border: 2px solid #f3f3f3;
	padding: 20px;
	/* width: 35%; */
	margin-top: 10px;
	box-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
	text-align: center;
}

#chartIdModelGraph {
	/* display: inline-block; */
	/* background-color: skyblue; */
	position: absolute;
	top: 0;
	right: 0;
}
</style>