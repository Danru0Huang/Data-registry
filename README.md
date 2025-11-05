# MDR/MFI华农数据治理平台 v2.0智能化

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Vue](https://img.shields.io/badge/vue-2.6.14-green.svg)](https://vuejs.org/)
[![Neo4j](https://img.shields.io/badge/neo4j-5.0+-red.svg)](https://neo4j.com/)

> 基于ISO/IEC 11179(MDR)以及19763(MFI)标准的元数据注册与映射的智能化数据治理平台

## 📖 项目简介

MDR/MFI华农数据治理平台是一个面向农业数据资源的智能化数据治理系统，实现了从参考数据目录、共享域数据目录到子域数据目录的三级数据管理架构。平台通过引入智能体技术，实现了数据元的智能化注册、自动映射和协同演化，显著提升了数据治理效率。

### 核心特性

- 🎯 **三级数据目录管理**：参考数据目录、共享域数据目录、子域数据目录
- 🤖 **智能化注册**：基于智能体的自动化数据元批量注册
- 🔄 **智能化映射**：子域数据到共享域数据的自动语义映射
- 📊 **可视化展示**：基于ECharts的知识图谱可视化
- 🔍 **多维度查询**：支持数据元、概念域、值域等多维度检索
- 📈 **演化追踪**：数据目录协同演化记录与追溯

## 🏗️ 系统架构

```
MDR-MFI-Platform/
├── web_domain/              # 前端应用
│   └── web_domain/
│       ├── src/
│       │   ├── views/       # 页面组件
│       │   │   ├── MDR/     # 共享域数据目录
│       │   │   ├── subDomain/  # 子域数据目录
│       │   │   └── information_model/  # 参考数据目录
│       │   ├── components/  # 可复用组件
│       │   └── router/      # 路由配置
│       └── package.json
│
├── pycharm_domain/          # 后端应用
│   └── pycharm_domain/
│       ├── App/
│       │   ├── register/    # 注册模块
│       │   ├── search/      # 查询模块
│       │   ├── evolution/   # 演化模块
│       │   └── views.py     # API路由
│       ├── app.py           # Flask入口
│       └── requirements.txt
│
├── pe_agents/               # 智能体模块
│   ├── pe_registry_optimized.py  # 智能化注册
│   ├── backend_api.py       # 后端API接口
│   └── tools.py             # 工具函数
│
├── mapping/                 # 映射模块
│   ├── mdr_based_mapper.py  # 基础映射
│   ├── llm_enhanced_mapping.py  # LLM增强映射
│   └── llm_mapping_adapter.py   # 映射适配器
│
└── scripts/                 # 工具脚本
    └── reset_database.py    # 数据库重置
```

## 💻 技术栈

### 前端技术
- **框架**：Vue.js 2.6.14
- **UI组件库**：Element UI 2.15.14
- **可视化**：ECharts 5.5.0、D3.js 7.9.0
- **HTTP客户端**：Axios 1.8.4
- **路由**：Vue Router 3.6.5

### 后端技术
- **Web框架**：Flask
- **图数据库**：Neo4j 5.0+
- **图数据库驱动**：py2neo
- **跨域支持**：Flask-CORS
- **环境管理**：python-dotenv

### 智能化技术
- **智能体框架**：自研智能体系统
- **自然语言处理**：基于大语言模型的语义理解
- **自动映射**：基于语义相似度的智能匹配

## 🚀 快速开始

### 环境要求

- Node.js 14+
- Python 3.8+
- Neo4j 5.0+

### 安装步骤

#### 1. 克隆项目

```bash
git clone https://github.com/Danru0Huang/Data-registry.git
cd Data-registry
```

#### 2. 配置Neo4j数据库

安装并启动Neo4j数据库，创建`.env`文件配置数据库连接：

```env
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_password
```

#### 3. 初始化数据库

```bash
cd pycharm_domain/pycharm_domain
python init_database.py
```

#### 4. 启动后端服务

```bash
# 安装Python依赖
pip install flask flask-cors py2neo python-dotenv

# 启动Flask服务
python app.py
```

后端服务默认运行在 `http://localhost:5000`

#### 5. 启动前端服务

```bash
cd web_domain/web_domain

# 安装依赖
npm install

# 启动开发服务器
npm run serve
```

前端服务默认运行在 `http://localhost:8099`

### 访问系统

打开浏览器访问：`http://localhost:8099`

## 📚 功能模块

### 1. 参考数据目录管理

- **注册功能**：注册信息模型、模型类、模型属性
- **查询功能**：按名称、类型查询参考数据模型
- **可视化**：以知识图谱形式展示模型结构

### 2. 共享域数据目录管理

#### 人工注册
- 对象类注册
- 属性注册
- 概念域注册
- 数据元概念注册
- 值域注册
- 数据元注册

#### 智能化注册
- Excel文件批量导入
- 智能体自动解析和注册
- 注册进度实时反馈
- 错误日志详细记录

### 3. 子域数据目录管理

#### 数据上传与注册
- Excel文件上传解析
- 自动建立表结构
- 属性与属性值识别

#### 智能化映射
- 一键智能映射
- CTA映射（表属性→数据元）
- CEA映射（表属性值→可允许值）
- 映射结果人工审核与修正

#### 人工映射
- 手动选择数据元
- 手动选择可允许值
- 精确控制映射关系

### 4. 数据目录协同演化

- 演化事件记录
- 演化链追溯
- 影响分析
- 版本管理（当前版本：2.0智能化）

## 🔧 配置说明

### 前端配置

编辑 `web_domain/web_domain/src/config.js`：

```javascript
export const apiBaseUrl = 'http://localhost:5000';
```

### 后端配置

编辑 `.env` 文件：

```env
# Neo4j配置
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_password

# Flask配置
FLASK_ENV=development
FLASK_DEBUG=1
```

## 📊 数据模型

### MDR核心概念

- **对象类（Object Class）**：描述对象的类别
- **属性（Property）**：描述对象的特征
- **概念域（Conceptual Domain）**：属性取值的语义范围
- **值域（Value Domain）**：属性取值的表示形式
- **数据元概念（Data Element Concept）**：对象类+属性
- **数据元（Data Element）**：数据元概念+值域

### 子域数据结构

- **子域（SubDomain）**：业务领域
- **表（Table）**：数据表
- **表属性（Table Attribute）**：数据列
- **表属性值（Table Attribute Value）**：枚举值


## 📝 更新日志

### v2.0智能化 (2025-01)

**重大更新**
- ✨ 新增智能化注册功能
- ✨ 新增智能化映射功能
- 🎨 优化界面文字表述
- 📦 整合完整项目结构
- 🔧 版本号统一升级为"2.0智能化"

**界面优化**
- 系统名称更新为"MDR/MFI华农数据治理平台"
- "手动注册" → "人工注册"
- "智能体自动注册" → "智能化注册"
- "建立映射" → "智能化映射"
- 新增"人工映射"标题

### v1.0 (2024)
- 🎉 初始版本发布
- ✅ 实现基础的MDR注册与查询
- ✅ 实现子域数据管理
- ✅ 实现知识图谱可视化

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

**⭐ 如果这个项目对您有帮助，请给我们一个 Star！**
