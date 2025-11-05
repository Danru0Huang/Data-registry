new Vue({
	el: '#app',
	data: {
		activeMenu: '',
		startIndex: 1,
		showObjectClass: false,
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
			valueDomain: ''
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
	},
	methods: {
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
		openSuccessful(message) {
			this.$message({
				message: message,
				type: 'success'
			});
		},
		// resetForm() {
		// 	this.registerObjectClassData.name = '';
		// 	this.registerObjectClassData.describe = '';
		// 	this.registerObjectClassData.department = '';
		// 	this.registerObjectClassData.personId = '';
		// 	this.registerPropertyData.name = '';
		// 	this.registerPropertyData.describe = '';
		// 	this.registerPropertyData.department = '';
		// 	this.registerPropertyData.personId = '';
		// },
		registerObjectClass() {
			vm = this;
			axios.post('/register/mdr/objectClass', this.registerObjectClassData)
				.then(response => {
					message = response.data.message
					vm.openSuccessful(message);
					vm.resetForm("registerObjectClassForm");
				})
				.catch(error => {
					console.error(error);
				});
		},
		registerProperty() {
			vm = this;
			axios.post('/register/mdr/property', this.registerPropertyData)
				.then(response => {
					message = response.data.message
					vm.openSuccessful(message);
					vm.resetForm("registerPropertyForm");
				})
				.catch(error => {
					console.error(error);
				});
		},
		registerConceptualDomain() {
			vm = this;
			axios.post('/register/mdr/conceptualDomain', this.registerConceptualDomainData)
				.then(response => {
					message = response.data.message
					vm.openSuccessful(message);
					vm.resetForm("registerConceptualDomainForm");
				})
				.catch(error => {
					console.error(error);
				});
		},
		registerDataElementConcept() {
			vm = this;
			axios.post('/register/mdr/dataElementConcept', this.registerDataElementConceptData)
				.then(response => {
					message = response.data.message
					vm.openSuccessful(message);
					vm.resetForm("registerDataElementConceptForm");
				})
				.catch(error => {
					console.error(error);
				});
		},
		registerValueDomain() {
			vm = this;
			axios.post('/register/mdr/valueDomain', this.registerValueDomainData)
				.then(response => {
					message = response.data.message
					vm.openSuccessful(message);
					vm.resetForm("registerValueDomainForm");
				})
				.catch(error => {
					console.error(error);
				});
		},
		registerDataElement() {
			vm = this;
			axios.post('/register/mdr/dataElement', this.registerDataElementData)
				.then(response => {
					message = response.data.message
					vm.openSuccessful(message);
					vm.resetForm("registerDataElementForm");
				})
				.catch(error => {
					console.error(error);
				});
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
		searchObjectClass(query) {
			this.objectClassLoading = true;
			axios.get('/search/mdr/getObjectClassOptions', {
					params: {
						query: query
					}
				})
				.then(response => {
					this.objectClassOptions = response.data.data;
					this.objectClassLoading = false;
				})
				.catch(error => {
					console.error(error);
					this.objectClassLoading = false;
				});
		},
		searchProperty(query) {
			this.propertyLoading = true;
			axios.get('/search/mdr/getPropertyOption', {
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
			axios.get('/search/mdr/getConceptualDomainOption', {
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
				});
		},
		searchValueMeanings(query) {
			this.valueMeaningsLoading = true;
			axios.get('/search/mdr/getValueMeaningsOption', {
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
				});
		},
		searchDataElementConcept(query) {
			this.dataElementConceptLoading = true;
			axios.get('/search/mdr/getDataElementConceptOption', {
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
				});
		},
		searchValueDomain(query) {
			this.valueDomainLoading = true;
			axios.get('/search/mdr/getValueDomainOption', {
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
				});
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
		},
	}
});