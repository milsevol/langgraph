# LangGraph 项目

## 项目概述
本项目是一个基于 LangGraph 的学习和实践仓库，包含了 LangGraph 的各种用法示例，从基础 API 到高级功能如多代理架构、子图等。

## 目录结构
```
LangGraph/
├── 1-langgraph-api/        # LangGraph API 基础用法
├── 2-functional-api/       # 函数式 API 用法
├── 3-stream/               # 流模式相关示例
├── 4-persistence/          # 持久化功能
├── 5-tool/                 # 工具调用相关示例
├── 6-human-in-loop/        # 人机协作相关功能
├── 7-time-travel/          # 时间旅行功能
├── 8-subgraph/             # 子图功能
├── 9-multi-agent/          # 多代理架构
├── 10-mcp/                 # 消息传递中心相关示例
├── data/                   # 数据目录
└── requirement.txt         # 项目依赖
```

## 功能模块介绍

### 1. LangGraph API 基础
- `1-langgraph-api/` 目录包含了 LangGraph 核心 API 的基础用法示例
- 涵盖状态定义、更新、输入输出、运行时配置、重试策略等基础功能

### 2. 函数式 API
- `2-functional-api/` 目录展示了函数式风格的 LangGraph 使用方法
- 包括简单工作流、并行执行、图调用、流处理等示例

### 3. 流模式
- `3-stream/` 目录包含了流模式相关的示例
- 展示了如何处理流式输出和 LLM 消息流

### 4. 持久化
- `4-persistence/` 目录讲解了检查点、内存存储、Redis 检查点等持久化功能
- 包括消息修剪和移除等高级功能

### 5. 工具调用
- `5-tool/` 目录展示了如何在 LangGraph 中集成和调用外部工具
- 包括工具选择、调用、直接返回结果等示例

### 6. 人机协作
- `6-human-in-loop/` 目录展示了如何在工作流中加入人工干预
- 包括中断、审批、审查等机制

### 7. 时间旅行
- `7-time-travel/` 目录介绍了 LangGraph 的时间旅行功能
- 允许回溯和修改图的执行历史

### 8. 子图
- `8-subgraph/` 目录展示了如何创建和使用子图
- 用于构建更复杂的嵌套工作流

### 9. 多代理架构
- `9-multi-agent/` 目录展示了如何构建多代理系统
- 包括主管代理和网络代理架构

### 10. MCP
- `10-mcp/` 目录包含了消息传递中心相关的示例
- 展示了如何构建和使用数学服务器、天气服务器等

## 环境要求
- Python 3.10+
- 安装依赖：`pip install -r requirement.txt`

## 启动虚拟环境
- 在 macOS/Linux 下，进入项目根目录后执行：`source .venv/bin/activate`
- 在 Windows PowerShell 下执行：`\.venv\Scripts\Activate.ps1`
- 在 Windows CMD 下执行：`.venv\Scripts\activate.bat`
- 退出虚拟环境：`deactivate`
- 激活后再安装依赖：`pip install -r requirement.txt`

## 使用方法
1. 克隆本仓库
2. 安装依赖
3. 运行各个目录下的 Python 文件查看示例

## 关于
本项目旨在帮助开发者学习和掌握 LangGraph 的各种功能，提供了从基础到高级的全面示例。

