var app = new Vue({
	el: '#app',
	data: {
		searchInput: '',
		graphData: [],
		graphLinks: [],
		chartId: 'guanxi',
		tableData: [],
		showTable: false,
		dialogVisible: false,
		nodeDetails: {},
		selectedLabel: '',
		labelOptions: ["Conceptual_Domain", "Context", "Data_Element", "Data_Element_Concept",
			"Diagram", "Domain", "Entity_Type", "Information_Model",
			"Information_Modelling_Language", "MDR_Registry", "Model_Element_Set",
			"Model_Element_Set_Mapping", "Model_Element_Set_Mapping_Type", "Model_Mapping",
			"Non_Key_Attribute", "Object_Class", "Permissible_Values", "Property",
			"Relationship", "Relationship_End", "Relationship_End_Group", "Representation_Class",
			"Subdomain", "Value_Domain", "Value_Meanings"
		],
		categories: [
			"Conceptual_Domain",
			"Context",
			"Data_Element",
			"Data_Element_Concept",
			"Diagram",
			"Domain",
			"Entity_Type",
			"Information_Model",
			"Information_Modelling_Language",
			"MDR_Registry",
			"Model_Element_Set",
			"Model_Element_Set_Mapping",
			"Model_Element_Set_Mapping_Type",
			"Model_Mapping",
			"Non_Key_Attribute",
			"Object_Class",
			"Permissible_Values",
			"Property",
			"Relationship",
			"Relationship_End",
			"Relationship_End_Group",
			"Representation_Class",
			"Subdomain",
			"Value_Domain",
			"Value_Meanings"
		]


	},
	methods: {
		search: function() {
			var vm = this;
			axios.get('/search_name', {
					params: {
						name: this.searchInput,
						label: this.selectedLabel
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
						vm.showTable = true;
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
			data: ["Conceptual_Domain", "Context", "Data_Element", "Data_Element_Concept",
				"Diagram", "Domain", "Entity_Type", "Information_Model",
				"Information_Modelling_Language", "MDR_Registry", "Model_Element_Set",
				"Model_Element_Set_Mapping", "Model_Element_Set_Mapping_Type", "Model_Mapping",
				"Non_Key_Attribute", "Object_Class", "Permissible_Values", "Property",
				"Relationship", "Relationship_End", "Relationship_End_Group", "Representation_Class",
				"Subdomain", "Value_Domain", "Value_Meanings"
			]
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
					name: 'Conceptual_Domain'
				},
				{
					name: 'Context'
				},
				{
					name: 'Data_Element'
				},
				{
					name: 'Data_Element_Concept'
				},
				{
					name: 'Diagram'
				},
				{
					name: "Domain"
				},
				{
					name: "Entity_Type"
				},
				{
					name: "Information_Model"
				},
				{
					name: "Information_Modelling_Language"
				},
				{
					name: "MDR_Registry"
				},
				{
					name: "Model_Element_Set"
				},
				{
					name: "Model_Element_Set_Mapping"
				},
				{
					name: "Model_Element_Set_Mapping_Type"
				},
				{
					name: "Model_Mapping"
				},
				{
					name: "Non_Key_Attribute"
				},
				{
					name: "Object_Class"
				},
				{
					name: "Permissible_Values"
				},
				{
					name: "Property"
				},
				{
					name: "Relationship"
				},
				{
					name: "Relationship_End"
				},
				{
					name: "Relationship_End_Group"
				},
				{
					name: "Representation_Class"
				},
				{
					name: "Subdomain"
				},
				{
					name: "Value_Domain"
				},
				{
					name: "Value_Meanings"
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
		axios.get('/search_node', {
				params: {
					category: category,
					name: name
				}
			})
			.then(function(response) {
				var nodeDetails = response.data; // 实际的查询结果数据
				app.showNodeResult(nodeDetails);

			})
			.catch(function(error) {
				console.log(error);
			});
	});
}