new Vue({
	el: '#app',
	data: {
		activeMenu: '',
		model_name: '',
		optionsOfModelName: [],
		optionsOfModelClassName: [],
		registerData: {
			model_name: '',
			class_name: '',
			properties: []
		},
		showAddClassTable: false,
		showAddRelationshipTable: false,
		registerRelationShip: {
			class1: '',
			class2: '',
			relation: ''
		}
	},
	// created() {
	// 	axios.get('/get_model_type_options') // 根据实际情况修改URL
	// 		.then(response => {
	// 			console.log(response.data.data);
	// 			this.options = response.data.data; // 根据实际情况修改赋值逻辑
	// 		})
	// 		.catch(error => {
	// 			console.error(error);
	// 		});
	// },
	methods: {
		registerModel() {
			axios.post('/register_model_class', this.registerData)
				.then(response => {
					alert(response.data.message);
					this.getMdodelTypeOptions();
				})
				.catch(error => {
					console.error(error);
				});
		},
		registerProperty() {
			axios.post('/register_model_property', this.registerData)
				.then(response => {
					alert(response.data.message);
				})
				.catch(error => {
					console.error(error);
				});
		},
		handleOpen(key, keyPath) {
			console.log(key, keyPath);
		},
		handleClose(key, keyPath) {
			console.log(key, keyPath);
		},
		next() {
			if (this.active++ > 2) this.active = 0;
		},
		onSubmit() {
			console.log('submit!');
		},
		addPropertyInput() {
			this.registerData.properties.push('');
		},
		getMdodelTypeOptions() {
			axios.get('/get_model_type_options')
				.then(response => {
					this.optionsOfModelName = response.data.data;
				})
				.catch(error => {
					console.error(error);
				});
		},
		changeShowAddClassTable() {
			this.showAddClassTable = true;
			this.showAddRelationshipTable = false;
			this.getMdodelTypeOptions();
		},
		changeShowAddRelationshipTable() {
			this.showAddRelationshipTable = true;
			this.showAddClassTable = false;
			this.getMdodelTypeOptions();
		},
		registerRelation() {
			axios.post('/register_model_relation', this.registerRelationShip)
				.then(response => {
					alert(response.data.message);
				})
				.catch(error => {
					console.error(error);
				});
		},
		resetForm() {
			this.model_name = '';
			this.registerData.model_name = '';
			this.registerData.class_name = '';
			this.registerData.properties = [];
			this.registerRelationShip.class1 = '';
			this.registerRelationShip.class2 = '';
			this.registerRelationShip.relation = '';
		},
		handleSelectChangeOfModelTypeRegisterRelation() {
			axios.post('/get_model_class_options', {
					selectedValue: this.model_name
				})
				.then(response => {
					this.optionsOfModelClassName = response.data.data;
				})
				.catch(error => {
					console.error(error);
				});
		},
		handleSelectChangeOfModelTypeRegisterClass() {
			axios.post('/get_model_class_options', {
					selectedValue: this.registerData.model_name
				})
				.then(response => {
					this.optionsOfModelClassName = response.data.data;
				})
				.catch(error => {
					console.error(error);
				});
		}
	}
});