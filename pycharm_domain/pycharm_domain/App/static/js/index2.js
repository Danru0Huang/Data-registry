var app = new Vue({
	el: '#app',
	data: {
		graphData: [],
		graphLinks: [],
		categories: ["模型", "模型类", "模型属性"],
	},
	created() {
		this.search();
		this.updateChartOfModelData();
	},
	methods: {
		search: function() {
			var vm = this;
			axios.get('/search/model/graphOfName', {
					params: {
						// name: this.searchInput,
						name: "测试模型2",
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
						vm.updateChartOfModelGraph(vm.graphData, vm.graphLinks);
						// vm.tableData = response.data.tableData;
						// vm.showTable = true;
						// vm.descriptionsData = response.data.list;
						// vm.showDescriptions = true;
					}

				})
				.catch(function(error) {
					console.log(error);
				});
		},
		openError() {
			this.$message.error('未查询到结果，请检查输入查询内容是否正确！');
		},
		updateChartOfModelGraph(graphData, graphLinks) {

			var divModelGraph = document.getElementById('chartIdModelGraph');

			// 使用 echarts 初始化图表
			var chartOfModelGraph = echarts.init(divModelGraph, 'purple-passion');
			// var chartOfModelGraph = echarts.init(divModelGraph);

			var optionOfModelGraph = {
				title: {
					text: '测试模型2',
					left: 'center',
					top: 'bottom',
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
			chartOfModelGraph.setOption(optionOfModelGraph, true);

			var divModelData = document.getElementById('chartIdModelData');
			console.log(divModelData);
			var chartOfModelData = echarts.init(divModelData, 'purple-passion');
			var option = {
				tooltip: {
					trigger: 'item'
				},
				legend: {
					top: '5%',
					left: 'center'
				},
				series: [{
					type: 'pie',
					radius: ['40%', '70%'],
					avoidLabelOverlap: false,
					itemStyle: {
						borderRadius: 10,
						borderColor: '#fff',
						borderWidth: 2
					},
					label: {
						show: false,
						position: 'center'
					},
					emphasis: {
						label: {
							show: true,
							fontSize: 40,
							fontWeight: 'bold'
						}
					},
					labelLine: {
						show: false
					},
					data: [{
							value: 1048,
							name: '类'
						},
						{
							value: 735,
							name: '属性'
						},
						{
							value: 735,
							name: '模型数量'
						},
					]
				}]
			};
			chartOfModelData.setOption(option);
		},
	}
});




(function(root, factory) {
	if (typeof define === 'function' && define.amd) {
		// AMD. Register as an anonymous module.
		define(['exports', 'echarts'], factory);
	} else if (typeof exports === 'object' && typeof exports.nodeName !== 'string') {
		// CommonJS
		factory(exports, require('echarts'));
	} else {
		// Browser globals
		factory({}, root.echarts);
	}
}(this, function(exports, echarts) {
	var log = function(msg) {
		if (typeof console !== 'undefined') {
			console && console.error && console.error(msg);
		}
	};
	if (!echarts) {
		log('ECharts is not Loaded');
		return;
	}
	echarts.registerTheme('purple-passion', {
		"color": [
			"#9b8bba",
			"#e098c7",
			"#8fd3e8",
			"#71669e",
			"#cc70af",
			"#7cb4cc"
		],
		"backgroundColor": "rgba(91,92,110,1)",
		"textStyle": {},
		"title": {
			"textStyle": {
				"color": "#ffffff"
			},
			"subtextStyle": {
				"color": "#cccccc"
			}
		},
		"line": {
			"itemStyle": {
				"borderWidth": "2"
			},
			"lineStyle": {
				"width": "3"
			},
			"symbolSize": "7",
			"symbol": "circle",
			"smooth": true
		},
		"radar": {
			"itemStyle": {
				"borderWidth": "2"
			},
			"lineStyle": {
				"width": "3"
			},
			"symbolSize": "7",
			"symbol": "circle",
			"smooth": true
		},
		"bar": {
			"itemStyle": {
				"barBorderWidth": 0,
				"barBorderColor": "#ccc"
			}
		},
		"pie": {
			"itemStyle": {
				"borderWidth": 0,
				"borderColor": "#ccc"
			}
		},
		"scatter": {
			"itemStyle": {
				"borderWidth": 0,
				"borderColor": "#ccc"
			}
		},
		"boxplot": {
			"itemStyle": {
				"borderWidth": 0,
				"borderColor": "#ccc"
			}
		},
		"parallel": {
			"itemStyle": {
				"borderWidth": 0,
				"borderColor": "#ccc"
			}
		},
		"sankey": {
			"itemStyle": {
				"borderWidth": 0,
				"borderColor": "#ccc"
			}
		},
		"funnel": {
			"itemStyle": {
				"borderWidth": 0,
				"borderColor": "#ccc"
			}
		},
		"gauge": {
			"itemStyle": {
				"borderWidth": 0,
				"borderColor": "#ccc"
			}
		},
		"candlestick": {
			"itemStyle": {
				"color": "#e098c7",
				"color0": "transparent",
				"borderColor": "#e098c7",
				"borderColor0": "#8fd3e8",
				"borderWidth": "2"
			}
		},
		"graph": {
			"itemStyle": {
				"borderWidth": 0,
				"borderColor": "#ccc"
			},
			"lineStyle": {
				"width": 1,
				"color": "#aaaaaa"
			},
			"symbolSize": "7",
			"symbol": "circle",
			"smooth": true,
			"color": [
				"#9b8bba",
				"#e098c7",
				"#8fd3e8",
				"#71669e",
				"#cc70af",
				"#7cb4cc"
			],
			"label": {
				"color": "#eeeeee"
			}
		},
		"map": {
			"itemStyle": {
				"areaColor": "#eee",
				"borderColor": "#444",
				"borderWidth": 0.5
			},
			"label": {
				"color": "#000"
			},
			"emphasis": {
				"itemStyle": {
					"areaColor": "#e098c7",
					"borderColor": "#444",
					"borderWidth": 1
				},
				"label": {
					"color": "#ffffff"
				}
			}
		},
		"geo": {
			"itemStyle": {
				"areaColor": "#eee",
				"borderColor": "#444",
				"borderWidth": 0.5
			},
			"label": {
				"color": "#000"
			},
			"emphasis": {
				"itemStyle": {
					"areaColor": "#e098c7",
					"borderColor": "#444",
					"borderWidth": 1
				},
				"label": {
					"color": "#ffffff"
				}
			}
		},
		"categoryAxis": {
			"axisLine": {
				"show": true,
				"lineStyle": {
					"color": "#cccccc"
				}
			},
			"axisTick": {
				"show": false,
				"lineStyle": {
					"color": "#333"
				}
			},
			"axisLabel": {
				"show": true,
				"color": "#cccccc"
			},
			"splitLine": {
				"show": false,
				"lineStyle": {
					"color": [
						"#eeeeee",
						"#333333"
					]
				}
			},
			"splitArea": {
				"show": true,
				"areaStyle": {
					"color": [
						"rgba(250,250,250,0.05)",
						"rgba(200,200,200,0.02)"
					]
				}
			}
		},
		"valueAxis": {
			"axisLine": {
				"show": true,
				"lineStyle": {
					"color": "#cccccc"
				}
			},
			"axisTick": {
				"show": false,
				"lineStyle": {
					"color": "#333"
				}
			},
			"axisLabel": {
				"show": true,
				"color": "#cccccc"
			},
			"splitLine": {
				"show": false,
				"lineStyle": {
					"color": [
						"#eeeeee",
						"#333333"
					]
				}
			},
			"splitArea": {
				"show": true,
				"areaStyle": {
					"color": [
						"rgba(250,250,250,0.05)",
						"rgba(200,200,200,0.02)"
					]
				}
			}
		},
		"logAxis": {
			"axisLine": {
				"show": true,
				"lineStyle": {
					"color": "#cccccc"
				}
			},
			"axisTick": {
				"show": false,
				"lineStyle": {
					"color": "#333"
				}
			},
			"axisLabel": {
				"show": true,
				"color": "#cccccc"
			},
			"splitLine": {
				"show": false,
				"lineStyle": {
					"color": [
						"#eeeeee",
						"#333333"
					]
				}
			},
			"splitArea": {
				"show": true,
				"areaStyle": {
					"color": [
						"rgba(250,250,250,0.05)",
						"rgba(200,200,200,0.02)"
					]
				}
			}
		},
		"timeAxis": {
			"axisLine": {
				"show": true,
				"lineStyle": {
					"color": "#cccccc"
				}
			},
			"axisTick": {
				"show": false,
				"lineStyle": {
					"color": "#333"
				}
			},
			"axisLabel": {
				"show": true,
				"color": "#cccccc"
			},
			"splitLine": {
				"show": false,
				"lineStyle": {
					"color": [
						"#eeeeee",
						"#333333"
					]
				}
			},
			"splitArea": {
				"show": true,
				"areaStyle": {
					"color": [
						"rgba(250,250,250,0.05)",
						"rgba(200,200,200,0.02)"
					]
				}
			}
		},
		"toolbox": {
			"iconStyle": {
				"borderColor": "#999999"
			},
			"emphasis": {
				"iconStyle": {
					"borderColor": "#666666"
				}
			}
		},
		"legend": {
			"textStyle": {
				"color": "#cccccc"
			}
		},
		"tooltip": {
			"axisPointer": {
				"lineStyle": {
					"color": "#cccccc",
					"width": 1
				},
				"crossStyle": {
					"color": "#cccccc",
					"width": 1
				}
			}
		},
		"timeline": {
			"lineStyle": {
				"color": "#8fd3e8",
				"width": 1
			},
			"itemStyle": {
				"color": "#8fd3e8",
				"borderWidth": 1
			},
			"controlStyle": {
				"color": "#8fd3e8",
				"borderColor": "#8fd3e8",
				"borderWidth": 0.5
			},
			"checkpointStyle": {
				"color": "#8fd3e8",
				"borderColor": "#8a7ca8"
			},
			"label": {
				"color": "#8fd3e8"
			},
			"emphasis": {
				"itemStyle": {
					"color": "#8fd3e8"
				},
				"controlStyle": {
					"color": "#8fd3e8",
					"borderColor": "#8fd3e8",
					"borderWidth": 0.5
				},
				"label": {
					"color": "#8fd3e8"
				}
			}
		},
		"visualMap": {
			"color": [
				"#8a7ca8",
				"#e098c7",
				"#cceffa"
			]
		},
		"dataZoom": {
			"backgroundColor": "rgba(0,0,0,0)",
			"dataBackgroundColor": "rgba(255,255,255,0.3)",
			"fillerColor": "rgba(167,183,204,0.4)",
			"handleColor": "#a7b7cc",
			"handleSize": "100%",
			"textStyle": {
				"color": "#333"
			}
		},
		"markPoint": {
			"label": {
				"color": "#eeeeee"
			},
			"emphasis": {
				"label": {
					"color": "#eeeeee"
				}
			}
		}
	});
}));