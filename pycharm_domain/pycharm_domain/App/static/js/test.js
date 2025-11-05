var app = new Vue({
	el: '#app',
	data: {
		searchInput: '',
		graphData: [],
		graphLinks: [],
		chartId: 'guanxi'
	},
	methods: {
		search: function() {
			var vm = this;
			axios.get('/search_name', {
					params: {
						name: this.searchInput
					}
				})
				.then(function(response) {
					if (response.data.data.length == 0){
						vm.openError();
					} else {
						vm.graphData = response.data.data.map(function(node, idx) {
							node.id = idx;
							return node;
						});
						vm.graphLinks = response.data.links;
						updateChart(vm.chartId, vm.graphData, vm.graphLinks);
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
			data: ["Gene", "GeneInfo", "Location", "FPKM", "AlternativeSplicing"]
		},
		series: [{
			type: 'graph',
			layout: 'force',
			symbolSize: 50,
			edgeSymbol: ['circle', 'arrow'],
			edgeSymbolSize: [4, 4],
			edgeLabel: {
				normal: {
					show: true,
					textStyle: {
						fontSize: 10
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
					name: 'Gene'
				},
				{
					name: 'GeneInfo'
				},
				{
					name: 'Location'
				},
				{
					name: 'FPKM'
				},
				{
					name: 'AlternativeSplicing'
				}
			],
			label: {
				normal: {
					show: true,
					textStyle: {
						fontSize: 10
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
			links: graphLinks
		}]
	};

	myChart.setOption(option, true);
}
