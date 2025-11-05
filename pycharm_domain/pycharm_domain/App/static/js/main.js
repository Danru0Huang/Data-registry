
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
			content: '欢迎使用KBQA！'
		});
		this.messages.push({
			sender: 'bot',
			content: '有关任何水稻信息都可以向我提问'
		});
	},
	methods: {
		sendMessage() {
			const message = {
				sender: 'user',
				content: this.inputText
			};

			this.messages.push(message);
			this.inputText = '';

			axios.post('/api/ask', {
					question: message.content
				})
				.then(response => {
					const answer = response.data.answer;
					const botMessage = {
						sender: 'bot',
						content: answer
					};
					this.messages.push(botMessage);
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
		}
	}
});
