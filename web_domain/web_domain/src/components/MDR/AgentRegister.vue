<template>
	<div class="agent-register-container">
		<el-card class="box-card">
			<div slot="header" class="clearfix">
				<span style="font-size: 18px; font-weight: bold;">智能化注册</span>
				<el-button style="float: right; padding: 3px 10px" type="text" @click="checkAgentStatus">
					检查状态
				</el-button>
			</div>

			<!-- 使用说明 -->
			<el-alert title="使用说明" type="info" :closable="false" style="margin-bottom: 20px;">
				<div>
					<p>1. 上传Excel文件（支持.xlsx或.xls格式）</p>
					<p>2. Excel文件需包含列：本体类、属性、值、值含义</p>
					<p>3. 点击"开始注册"按钮，智能体将自动完成批量注册</p>
					<p>4. 注册数据与人工注册格式完全一致</p>
				</div>
			</el-alert>

			<!-- 文件上传 -->
			<div class="upload-section">
				<el-upload
					class="upload-demo"
					drag
					:action="uploadUrl"
					:on-change="handleChange"
					:on-success="handleSuccess"
					:on-error="handleError"
					:before-upload="beforeUpload"
					:file-list="fileList"
					:auto-upload="false"
					ref="upload"
					accept=".xlsx,.xls">
					<i class="el-icon-upload"></i>
					<div class="el-upload__text">
						将Excel文件拖到此处，或<em>点击上传</em>
					</div>
					<div class="el-upload__tip" slot="tip">
						只能上传xlsx/xls文件
					</div>
				</el-upload>
			</div>

			<!-- 操作按钮 -->
			<div class="button-section">
				<el-button
					type="primary"
					@click="submitUpload"
					:loading="uploading"
					:disabled="fileList.length === 0">
					{{ uploading ? '注册中...' : '开始注册' }}
				</el-button>
				<el-button @click="clearFiles">清空</el-button>
			</div>

			<!-- 进度显示 -->
			<div v-if="uploading" class="progress-section">
				<el-progress :percentage="progress" :status="progressStatus"></el-progress>
				<p style="text-align: center; margin-top: 10px;">{{ progressText }}</p>
			</div>

			<!-- 注册日志显示 -->
			<div v-if="logs.length > 0" class="logs-section">
				<el-divider>注册日志</el-divider>
				<el-card class="logs-card">
					<div class="log-container" ref="logContainer">
						<div
							v-for="(log, index) in logs"
							:key="index"
							:class="['log-item', log.type]">
							<span class="log-time">{{ log.time }}</span>
							<span class="log-message">{{ log.message }}</span>
						</div>
					</div>
				</el-card>
			</div>

			<!-- 结果显示 -->
			<div v-if="result" class="result-section">
				<el-divider></el-divider>
				<h3>注册结果</h3>
				<el-row :gutter="20">
					<el-col :span="6">
						<el-statistic title="总计" :value="result.total"></el-statistic>
					</el-col>
					<el-col :span="6">
						<el-statistic title="成功" :value="result.success_count">
							<template slot="suffix">
								<i class="el-icon-success" style="color: #67C23A"></i>
							</template>
						</el-statistic>
					</el-col>
					<el-col :span="6">
						<el-statistic title="失败" :value="result.error_count">
							<template slot="suffix">
								<i class="el-icon-error" style="color: #F56C6C"></i>
							</template>
						</el-statistic>
					</el-col>
					<el-col :span="6">
						<el-statistic title="跳过" :value="result.skip_count"></el-statistic>
					</el-col>
				</el-row>

				<!-- 错误详情 -->
				<div v-if="result.errors && result.errors.length > 0" style="margin-top: 20px;">
					<el-collapse>
						<el-collapse-item title="错误详情" name="1">
							<el-table :data="result.errors" style="width: 100%">
								<el-table-column prop="ontology_class" label="本体类" width="180"></el-table-column>
								<el-table-column prop="attribute" label="属性" width="180"></el-table-column>
								<el-table-column prop="error" label="错误信息"></el-table-column>
							</el-table>
						</el-collapse-item>
					</el-collapse>
				</div>
			</div>
		</el-card>
	</div>
</template>

<script>
export default {
	name: 'AgentRegister',
	data() {
		return {
			uploadUrl: 'http://127.0.0.1:5000/register/mdr/agent/batch',
			fileList: [],
			uploading: false,
			progress: 0,
			progressStatus: '',
			progressText: '准备上传...',
			result: null,
			agentStatus: null,
			logs: []  // 注册日志
		}
	},
	methods: {
		// 添加日志
		addLog(message, type = 'info') {
			const now = new Date();
			const time = `${now.getHours().toString().padStart(2, '0')}:${now.getMinutes().toString().padStart(2, '0')}:${now.getSeconds().toString().padStart(2, '0')}`;
			this.logs.push({
				time,
				message,
				type  // info, success, error, warning
			});
			// 自动滚动到底部
			this.$nextTick(() => {
				if (this.$refs.logContainer) {
					this.$refs.logContainer.scrollTop = this.$refs.logContainer.scrollHeight;
				}
			});
		},

		// 文件变化处理
		handleChange(file, fileList) {
			this.fileList = fileList;
		},

		// 上传前检查
		beforeUpload(file) {
			const isExcel = file.type === 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' ||
			                file.type === 'application/vnd.ms-excel';
			const isLt10M = file.size / 1024 / 1024 < 10;

			if (!isExcel) {
				this.$message.error('只能上传Excel文件！');
				return false;
			}
			if (!isLt10M) {
				this.$message.error('文件大小不能超过10MB！');
				return false;
			}
			return true;
		},

		// 提交上传
		submitUpload() {
			if (this.fileList.length === 0) {
				this.$message.warning('请先选择文件');
				return;
			}

			this.uploading = true;
			this.progress = 0;
			this.progressText = '正在上传文件...';
			this.result = null;
			this.logs = [];  // 清空之前的日志

			// 添加开始日志
			this.addLog(`开始上传文件: ${this.fileList[0].name}`, 'info');

			// 创建FormData
			const formData = new FormData();
			formData.append('file', this.fileList[0].raw);

			// 发送请求
			this.$axios.post(this.uploadUrl, formData, {
				headers: {
					'Content-Type': 'multipart/form-data'
				},
				onUploadProgress: (progressEvent) => {
					this.progress = Math.round((progressEvent.loaded * 100) / progressEvent.total);
					if (this.progress < 100) {
						this.progressText = '正在上传文件...';
					} else {
						this.progressText = '文件上传完成，智能体注册中...';
						this.addLog('文件上传完成，开始解析数据...', 'success');
					}
				}
			})
			.then(response => {
				this.uploading = false;
				const data = response.data;

				if (data.success) {
					this.progress = 100;
					this.progressStatus = 'success';
					this.progressText = '注册完成！';
					this.result = data;

					// 添加成功日志
					this.addLog(`智能体注册完成！`, 'success');
					this.addLog(`总计: ${data.total} 条，成功: ${data.success_count} 条，失败: ${data.error_count} 条，跳过: ${data.skip_count} 条`, 'success');

					// 如果有错误，添加错误日志
					if (data.errors && data.errors.length > 0) {
						this.addLog(`发现 ${data.errors.length} 个错误，请查看错误详情`, 'warning');
						data.errors.forEach(err => {
							this.addLog(`错误: [${err.ontology_class}] ${err.attribute} - ${err.error}`, 'error');
						});
					}

					this.$message.success(data.message || '注册成功');
				} else {
					this.progress = 100;
					this.progressStatus = 'exception';
					this.progressText = '注册失败';

					// 添加失败日志
					this.addLog(`注册失败: ${data.message}`, 'error');
					if (data.error) {
						this.addLog(`错误详情: ${data.error}`, 'error');
					}

					this.$message.error(data.message || '注册失败');
				}
			})
			.catch(error => {
				this.uploading = false;
				this.progress = 100;
				this.progressStatus = 'exception';
				this.progressText = '注册失败';

				console.error(error);
				this.addLog(`请求失败: ${error.response?.data?.message || error.message}`, 'error');
				this.$message.error('注册过程出错: ' + (error.response?.data?.message || error.message));
			});
		},

		// 上传成功回调
		handleSuccess(response, file, fileList) {
			console.log('Upload success:', response);
		},

		// 上传失败回调
		handleError(err, file, fileList) {
			console.error('Upload error:', err);
			this.$message.error('上传失败');
		},

		// 清空文件
		clearFiles() {
			this.$refs.upload.clearFiles();
			this.fileList = [];
			this.result = null;
			this.progress = 0;
			this.progressStatus = '';
			this.progressText = '准备上传...';
			this.logs = [];  // 清空日志
		},

		// 下载模板
		downloadTemplate() {
			this.$message.info('模板下载功能开发中...');
			// TODO: 实现模板下载
		},

		// 检查智能体状态
		checkAgentStatus() {
			this.$axios.get('http://127.0.0.1:5000/register/mdr/agent/status')
			.then(response => {
				if (response.data.success) {
					this.agentStatus = response.data;
					this.$message.success(response.data.message || '智能体服务正常');
				} else {
					this.$message.warning('智能体服务异常');
				}
			})
			.catch(error => {
				console.error(error);
				this.$message.error('无法连接到智能体服务');
			});
		}
	},
	mounted() {
		// 组件挂载时检查智能体状态
		// this.checkAgentStatus();
	}
}
</script>

<style scoped>
.agent-register-container {
	padding: 20px;
}

.box-card {
	max-width: 900px;
	margin: 0 auto;
}

.upload-section {
	margin: 20px 0;
}

.button-section {
	text-align: center;
	margin: 20px 0;
}

.progress-section {
	margin: 30px 0;
}

.logs-section {
	margin: 20px 0;
}

.logs-card {
	background-color: #f5f7fa;
}

.log-container {
	max-height: 300px;
	overflow-y: auto;
	font-family: 'Courier New', monospace;
	font-size: 12px;
	padding: 10px;
	background-color: #fff;
	border-radius: 4px;
}

.log-item {
	padding: 5px 0;
	border-bottom: 1px solid #ebeef5;
	display: flex;
	align-items: flex-start;
}

.log-item:last-child {
	border-bottom: none;
}

.log-time {
	color: #909399;
	margin-right: 10px;
	flex-shrink: 0;
	font-weight: bold;
}

.log-message {
	flex: 1;
	word-break: break-all;
}

.log-item.info .log-message {
	color: #409EFF;
}

.log-item.success .log-message {
	color: #67C23A;
	font-weight: 500;
}

.log-item.warning .log-message {
	color: #E6A23C;
}

.log-item.error .log-message {
	color: #F56C6C;
	font-weight: 500;
}

.result-section {
	margin-top: 20px;
}

.el-statistic {
	text-align: center;
}
</style>
