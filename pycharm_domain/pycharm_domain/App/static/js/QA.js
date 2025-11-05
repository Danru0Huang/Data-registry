new Vue({
	el: '#app',
	delimiters: ['[[', ']]'],
	data: {
		inputText: '',
		messages: []
	},
	created() {
		this.messages.push({
			sender: 'bot',
			content: '欢迎使用KBQA！',
			type: 'text'
		});
		this.messages.push({
			sender: 'bot',
			content: '有关任何水稻信息都可以向我提问',
			type: 'text'
		});
	},
	methods: {
		sendMessage() {
			const message = {
				sender: 'user',
				content: this.inputText,
				type: 'text'
			};

			this.messages.push(message);
			this.inputText = '';

			axios.post('/api/ask', {
					question: message.content
				})
				.then(response => {
					const answer = response.data.answer;
					for(var item of answer){
						const botMessage = {
							sender: 'bot',
							content: item,
							type: 'text'
						};
						this.messages.push(botMessage);
					}
					// const botMessage = {
					// 	sender: 'bot',
					// 	// content: "/static/img/aa.png",
					// 	content: "<img src='/static/img/aa.png'/>",
					// 	type: 'img'
					// };
					// this.messages.push(botMessage);
					this.$nextTick(() => {
						this.scrollToBottom();
					});
				})
				.catch(error => {
					console.error(error);
				});
		},
		scrollToBottom() {
			const container = this.$refs.messageContainer;
			container.scrollTop = container.scrollHeight;
		},
		handleOpen(key, keyPath) {
			console.log(key, keyPath);
		},
		handleClose(key, keyPath) {
			console.log(key, keyPath);
		}
	}
});