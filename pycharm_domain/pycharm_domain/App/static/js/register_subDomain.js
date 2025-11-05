var app = new Vue({
	el: '#app',
	data: {
		activeMenu: '',
		uploadUrl: '/upload', // 后台接收上传的URL
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
		valueDomain: '',
		valueDomainOptions: [],
		permissibleValues: [],
		permissibleValuesOptions: [],
		attributeValueName: ''
	},
	created() {
		this.getOptionsOfSubDomain();
		this.getDataElementOptions();
		this.getValueDomainOptions();
		this.getValueDomainAndPermissibleValuesOptions();
	},
	methods: {
		handleOpen(key, keyPath) {
			console.log(key, keyPath);
		},
		handleClose(key, keyPath) {
			console.log(key, keyPath);
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
				.catch(_ => {});
		},
		changeShowDialogOfAddSubDomain() {
			this.showDialogOfAddSubDomain = true;
		},
		openSuccessful(message) {
			this.$message({
				message: message,
				type: 'success'
			});
		},
		addSubDomain() {
			vm = this;
			axios.get('/register/subDomain/addSubDomian', {
					params: {
						name: this.addSubDomainData.name,
						describe: this.addSubDomainData.describe
					}
				})
				.then(function(response) {
					message = response.data.message
					vm.openSuccessful(message);
					vm.resetForm();
					vm.showDialogOfAddSubDomain = false;
					vm.getOptionsOfSubDomain();
				})
				.catch(function(error) {
					console.log(error);
				});
		},
		getOptionsOfSubDomain() {
			axios.get('/search/subDomain/getSubDomainOptions')
				.then(response => {
					this.optionsOfSubDomain = response.data.data;
				})
				.catch(error => {
					console.error(error);
				});
		},
		handleSelectChangeOfSubdomain() {
			this.selectedOption = this.optionsOfSubDomain.find(item => item.value === this.subDomainName);
		},
		addRelationBetweenTableAndSubdomain() {
			var vm = this;
			axios.get('/register/subDomain/addRelationBetweenTableAndSubDomain', {
					params: {
						sub_domain_name: this.subDomainName,
						identifier: this.identifier_table
					}
				})
				.then(function(response) {
					vm.showDialogOfSelectSubDomain = false;
					vm.openSuccessful(response.data.data);
					vm.search();
				})
				.catch(function(error) {
					console.log(error);
				});
		},
		openError() {
			this.$message.error('未查询到结果，请检查输入查询内容是否正确！');
		},
		search: function() {
			var vm = this;
			axios.get('/search/subDomain/getGraphOfTable', {
					params: {
						// name: this.searchInput,
						sub_domain_name: this.subDomainName,
						identifier_table: this.identifier_table
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
						vm.updateChartOfTableGraph(vm.graphData, vm.graphLinks);
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
			myChart.on("click", function(params) {
				var name = params.name
				var category_id = params.data.category;
				var category = app.categories[category_id];
				if (category == "表属性") {
					app.attributeName = name;
				};
				if (category == "表属性值") {
					app.attributeValueName = name;
				}
			});
		},
		handleClick(tab, event) {
			console.log(tab, event);
		},
		getDataElementOptions() {
			axios.get('/search/mdr/getDataElementOption')
				.then(response => {
					this.dataElementOptions = response.data.data;
				})
				.catch(error => {
					console.error(error);
				});
		},
		getValueDomainOptions() {
			axios.get('/search/mdr/getValueDomainOption')
				.then(response => {
					this.valueDomainOptions = response.data.data;
				})
				.catch(error => {
					console.error(error);
				});
		},
		getValueDomainAndPermissibleValuesOptions() {
			// this.valueDomainLoading = true;
			axios.get('/search/mdr/getValueDomainAndPermissibleValuesOption')
				.then(response => {
					this.permissibleValuesOptions = response.data.data;
				})
				.catch(error => {
					console.error(error);
				});
		},
		addRelationBetweenAttributeAndDataElement() {
			var vm = this;
			axios.get('/register/subDomain/addRelationBetweenAttributeAndDataElement', {
					params: {
						sub_domain_name: this.subDomainName,
						identifier_table: this.identifier_table,
						name_attribute: this.attributeName,
						identifier_data_element: this.dataElement
					}
				})
				.then(response => {
					vm.openSuccessful(response.data.data);
					vm.search();
				})
				.catch(error => {
					console.error(error);
				});
		},
		addRelationBetweenAttributeAndValueDomain() {
			var vm = this;
			axios.get('/register/subDomain/addRelationBetweenAttributeAndValueDomain', {
					params: {
						sub_domain_name: this.subDomainName,
						identifier_table: this.identifier_table,
						name_attribute: this.attributeName,
						identifier_value_domain: this.valueDomain
					}
				})
				.then(response => {
					vm.openSuccessful(response.data.data);
					vm.search();
				})
				.catch(error => {
					console.error(error);
				});
		},
		addRelationBetweenAttributeValueAndPermissibleValues() {
			var vm = this;
			console.log(this.permissibleValues);
			axios.get('/register/subDomain/addRelationBetweenAttributeValueAndPermissibleValues', {
					params: {
						sub_domain_name: this.subDomainName,
						identifier_table: this.identifier_table,
						name_attribute_value: this.attributeValueName,
						identifier_permissible_values: this.permissibleValues[1]
					}
				})
				.then(response => {
					vm.openSuccessful(response.data.data);
					vm.search();
				})
				.catch(error => {
					console.error(error);
				});
		}
	}
});