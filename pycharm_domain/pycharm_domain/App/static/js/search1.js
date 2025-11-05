var app = new Vue({
	el: '#app',
	data: {
		activeMenu: '',
		showTableOfObjectClass: false,
		showTableOfMDRProperty: false,
		showTableOfConceptualDomain: false,
		showTableDataElementConcept: false,
		showTableOfValueDomain: false,
		showTableOfDataElement: false,
		tableTitle: "",
		searchInput: '',
		search: '',
		tableDataOfObjectClass: [],
		tableDataOfMDRProperty: [],
		tableDataOfConceptualDomain: [],
		tableDataOfDataElementConcept: [],
		tableDataOfValueDomain: [],
		tableDataOfDataElement: [],
		dialogDataObjectClass: {},
		dialogVisibleObjectClass: false,
		dialogVisibleProperty: false,
		dialogDataProperty: {},
		dialogVisibleConceptualDomain: false,
		dialogDataConceptualDomain: {},
		dialogDataValueMenings: [],
		dialogVisibleDataElementConcept: false,
		dialogDataDataElementConcept: {},
		dialogVisibleValueDomain: false,
		dialogDataValueDomain: {},
		dialogDataPermissibleValues: [],
		selectedLabel: '',
		dialogVisibleGraph: false,
		graphData: [],
		graphLinks: [],
		categories: ["对象类", "属性", "概念域", "数据元概念", "值域", "数据元", "可允许值", "值含义", "值域组"],
	},
	methods: {
		// search() {
		// 	var vm = this;
		// 	axios.get('/get_mdr_object_class_node', {
		// 			params: {
		// 				name: this.searchInput,
		// 				label: this.selectedLabel
		// 			}
		// 		})
		// 		.then(function(response) {
		// 			if (response.data.data.length == 0) {
		// 				vm.openError();
		// 			} else {
		// 				vm.tableData = response.data.data;
		// 			}

		// 		})
		// 		.catch(function(error) {
		// 			console.log(error);
		// 		});
		// },
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
		handleCommand(command) {
			var vm = this;
			axios.get('/search/mdr/getMDRTableList', {
					params: {
						label: command
					}
				})
				.then(function(response) {
					if (response.data.data.length == 0) {
						vm.openError();
					} else {
						vm.tableTitle = response.data.tableTitle;
						if (command === '对象类') {
							vm.showTableOfObjectClass = true;
							vm.showTableOfMDRProperty = false;
							vm.showTableOfConceptualDomain = false;
							vm.showTableDataElementConcept = false;
							vm.showTableOfValueDomain = false;
							vm.showTableOfDataElement = false;
							vm.tableDataOfObjectClass = response.data.data;
						};
						if (command == "属性") {
							vm.showTableOfMDRProperty = true;
							vm.showTableOfObjectClass = false;
							vm.showTableOfConceptualDomain = false;
							vm.showTableDataElementConcept = false;
							vm.showTableOfValueDomain = false;
							vm.showTableOfDataElement = false;
							vm.tableDataOfMDRProperty = response.data.data;
						};
						if (command == "概念域") {
							vm.showTableOfConceptualDomain = true;
							vm.showTableOfObjectClass = false;
							vm.showTableOfMDRProperty = false;
							vm.showTableDataElementConcept = false;
							vm.showTableOfValueDomain = false;
							vm.showTableOfDataElement = false;
							vm.tableDataOfConceptualDomain = response.data.data;
						};
						if (command == "数据元概念") {
							vm.showTableDataElementConcept = true;
							vm.showTableOfObjectClass = false;
							vm.showTableOfMDRProperty = false;
							vm.showTableOfConceptualDomain = false;
							vm.showTableOfValueDomain = false;
							vm.showTableOfDataElement = false;
							vm.tableDataOfDataElementConcept = response.data.data;
						};
						if (command == "值域") {
							vm.showTableOfValueDomain = true;
							vm.showTableOfMDRProperty = false;
							vm.showTableOfObjectClass = false;
							vm.showTableOfConceptualDomain = false;
							vm.showTableDataElementConcept = false;
							vm.showTableOfDataElement = false;
							vm.tableDataOfValueDomain = response.data.data;
						};
						if (command == "数据元") {
							vm.showTableOfDataElement = true;
							vm.showTableOfObjectClass = false;
							vm.showTableOfMDRProperty = false;
							vm.showTableOfConceptualDomain = false;
							vm.showTableDataElementConcept = false;
							vm.showTableOfValueDomain = false;
							vm.tableDataOfDataElement = response.data.data;
						}
					}

				})
				.catch(function(error) {
					console.log(error);
				});
		},
		handleDelete(index, row) {
			if (this.showTableOfObjectClass) {
				this.tableDataOfObjectClass.splice(index, 1); // 删除对象类的数据行
			} else if (this.showTableOfMDRProperty) {
				this.tableDataOfMDRProperty.splice(index, 1); // 删除MDR属性的数据行
			} else if (this.showTableOfConceptualDomain) {
				this.tableDataOfConceptualDomain.splice(index, 1); //删除概念域的数据行
			} else if (this.showTableDataElementConcept) {
				this.tableDataOfDataElementConcept.splice(index, 1); //删除数据元概念的数据行
			} else if (this.showTableOfValueDomain) {
				this.tableDataOfValueDomain.splice(index, 1);
			} else if (this.showTableOfDataElement) {
				this.tableDataOfDataElement.splice(index, 1);
			}
		},
		handleGetMDRTable(identifier, label) {
			var vm = this;
			axios.get('/search/mdr/getMDRTable', {
					params: {
						identifier: identifier,
						label: label
					}
				})
				.then(function(response) {
					if (response.data.data.length == 0) {
						vm.openError();
					} else {
						if (label == "对象类") {
							vm.dialogDataObjectClass = response.data.data[0];
							vm.dialogVisibleObjectClass = true;
						} else if (label == "属性") {
							vm.dialogDataProperty = response.data.data[0];
							vm.dialogVisibleProperty = true;
						} else if (label == "概念域") {
							vm.dialogDataConceptualDomain = response.data.data[0][0];
							vm.dialogDataValueMenings = response.data.data[1];
							vm.dialogVisibleConceptualDomain = true;
						} else if (label == "数据元概念") {
							vm.dialogDataDataElementConcept = response.data.data[0];
							vm.dialogVisibleDataElementConcept = true;
						} else if (label == "值域") {
							vm.dialogDataValueDomain = response.data.data[0][0];
							vm.dialogDataPermissibleValues = response.data.data[1];
							vm.dialogVisibleValueDomain = true;
						}
						// vm.dialogData = response.data.data[0];
						// vm.dialogVisible = true;
					}
				})
				.catch(function(error) {
					console.log(error);
				});
		},
		getMDRGraph(identifier) {
			var vm = this;
			vm.dialogVisibleGraph = true;
			axios.get('/search/mdr/getGraphOfMDR', {
					params: {
						identifier: identifier
					}
				})
				.then(function(response) {
					if (response.data.data.length == 0) {
						vm.openError();
					} else {
						console.log(response.data.data);
						vm.graphData = response.data.data.map(function(node, idx) {
							node.id = idx;
							return node;
						});
						vm.graphLinks = response.data.links;
						vm.updateChartOfMDRGraph(vm.graphData, vm.graphLinks);
					}
		
				})
				.catch(function(error) {
					console.log(error);
				});
		},
		updateChartOfMDRGraph(graphData, graphLinks) {
			var myChart = echarts.init(document.getElementById("MDRGraph"));
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
					data: ["对象类", "属性", "概念域", "数据元概念", "值域", "数据元", "可允许值", "值含义", "值域组"]
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
							name: '对象类'
						},
						{
							name: '属性'
						},
						{
							name: '概念域'
						},
						{
							name: '数据元概念'
						},
						{
							name: '值域'
						},
						{
							name: '数据元'
						},
						{
							name: '可允许值'
						},
						{
							name: '值含义'
						},
						{
							name: "值域组"
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
			// 	if (category == "表属性") {
			// 		app.attributeName = name;
			// 	};
			// 	if (category == "表属性值") {
			// 		app.attributeValueName = name;
			// 	}
			// });
		},
	}
});