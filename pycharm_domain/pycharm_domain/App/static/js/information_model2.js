var app = new Vue({
	el: '#app',
	data: {
		activeMenu: '',
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
			model_name: ''
		},
		showDialogOfAddClass: false,
		addClassName: {
			class_name: ''
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
		showAddModelRelationTable: false
	},
	created() {
		this.getOptionsOfModelName();
	},
	methods: {
		search: function() {
			var vm = this;
			axios.get('/search/model/graphOfName', {
					params: {
						// name: this.searchInput,
						name: this.selectedModelName,
						label: "模型"
					}
				})
				.then(function(response) {
					if (response.data.data.length == 0) {
						vm.openError();
					} else {
						vm.graphData = response.data.data.map(function(node, idx) {
							node.id = idx;
							return node;
						});
						vm.graphLinks = response.data.links;
						updateChart(vm.chartId, vm.graphData, vm.graphLinks);
						vm.tableData = response.data.tableData;
						// vm.showTable = true;
						vm.descriptionsData = response.data.list;
						vm.showDescriptions = true;
					}

				})
				.catch(function(error) {
					console.log(error);
				});
		},
		handleOpen(key, keyPath) {
			console.log(key, keyPath);
		},
		handleClose(key, keyPath) {
			console.log(key, keyPath);
		},
		openError() {
			this.$message.error('未查询到结果，请检查输入查询内容是否正确！');
		},
		dialogClose(done) {
			this.$confirm('确认关闭？')
				.then(_ => {
					done();
				})
				.catch(_ => {});
		},
		showNodeResult(nodeDetails) {
			this.nodeDetails = nodeDetails;
			this.dialogVisible = true;
		},
		addProperty() {
			var vm = this;
			vm.addPropertyName.model_name = vm.selectedModelName;
			axios.post('/register/model/addProperty', vm.addPropertyName)
				.then(function(response) {
					alert(response.data.message);
					vm.showDialogOfAddProperty = false;
					vm.graphData = [];
					vm.graphLinks = [];
					vm.search();
					vm.resetForm();
				})
				.catch(function(error) {
					console.log(error);
				});
		},
		addClass() {
			var vm = this;
			axios.get('/register/model/addClass', {
					params: {
						model_name: this.selectedModelName,
						class_name: this.addClassName.class_name
					}
				})
				.then(function(response) {
					alert(response.data.message);
					vm.showDialogOfAddClass = false;
					vm.graphData = [];
					vm.graphLinks = [];
					vm.search();
					vm.getMdodelClassNameOptions();
					vm.resetForm();
				})
				.catch(function(error) {
					console.log(error);
				});
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
		getMdodelClassNameOptions() {
			axios.get('/search/model/getModelClassNameOptions', {
					params: {
						model_name: this.selectedModelName,
					}
				})
				.then(response => {
					this.optionsOfModelClassName = response.data.data;
				})
				.catch(error => {
					console.error(error);
				});
		},
		addRelation() {
			var vm = this;
			axios.get('/register/model/addRelation', {
					params: {
						model_name: this.selectedModelName,
						class_name1: this.addRelationData.class_name1,
						class_name2: this.addRelationData.class_name2,
						relation: this.addRelationData.relation
					}
				})
				.then(function(response) {
					alert(response.data.message);
					vm.showDialogOfAddRelation = false;
					vm.graphData = [];
					vm.graphLinks = [];
					vm.search();
					vm.resetForm();
				})
				.catch(function(error) {
					console.log(error);
				});
		},
		addModel() {
			axios.get('/register/model/addModel', {
					params: {
						model_name: this.addModelData.model_name,
						class_name: this.addModelData.class_name
					}
				})
				.then(response => {
					alert(response.data.message);
					this.showDialogOfAddModel = false;
					this.getOptionsOfModelName();
					this.resetForm();
				})
				.catch(error => {
					console.error(error);
				});
		},
		getOptionsOfModelName() {
			axios.get('/search/model/getModelTypeOptions')
				.then(response => {
					this.optionsOfModelName = response.data.data;
				})
				.catch(error => {
					console.error(error);
				});
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
});

function updateChart(chartId, graphData, graphLinks) {
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
	myChart.off('click');
	myChart.on("click", function(params) {
		var name = params.name
		var category_id = params.data.category;
		var category = app.categories[category_id];
		// axios.get('/search_node', {
		// 		params: {
		// 			category: category,
		// 			name: name
		// 		}
		// 	})
		// 	.then(function(response) {
		// 		var nodeDetails = response.data; // 实际的查询结果数据
		// 		app.showNodeResult(nodeDetails);

		// 	})
		// 	.catch(function(error) {
		// 		console.log(error);
		// 	});
		var mode_name = app.searchInput;
		if (category == "模型类") {
			app.addPropertyName.class_name = name;
			app.addRelationData.class_name1 = name;
			app.showDialogOfSelect = true;
		};
		if (category == "模型") {
			app.showDialogOfAddClass = true;
		}
	});
}