new Vue({
	el: '#app',
	delimiters: ['[[', ']]'],
	data: {
		active: 0,
		form: {
		          name: '',
		          region: '',
		          date1: '',
		          date2: '',
		          delivery: false,
		          type: [],
		          resource: '',
		          desc: ''
		        }
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
		}
	}
});