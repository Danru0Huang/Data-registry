var app = new Vue({
	el: '#app',
	data: {
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
	},
	created() {
		this.getOptionsOfModelName();
	},
	methods: {
		search: function() {
			var vm = this;
			axios.get('/search/model/graphOfName', {
					params: {
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
						// vm.tableData = response.data.tableData;
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
		andleClose(done) {
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
		getOptionsOfModelName() {
			axios.get('/search/model/getModelTypeOptions')
				.then(response => {
					this.optionsOfModelName = response.data.data;
				})
				.catch(error => {
					console.error(error);
				});
		},
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