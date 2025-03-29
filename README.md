# 乡旅汇 (Village Connect)

![乡旅汇](https://placeholder-for-logo.com/village-connect-logo.png)

## 📝 项目简介

乡旅汇是一个连接农户与游客的乡村旅游体验平台，旨在促进乡村旅游发展，为游客提供独特的乡村体验，同时帮助农户展示和推广他们的特色产品与活动。

## ✨ 核心特色

- 🏡 **乡村体验活动**：农户可以轻松发布各类体验活动
- 🌾 **农特产品展示**：展示和推广当地特色农产品
- 📱 **便捷预约系统**：简单直观的在线预约流程
- 💬 **智能客服系统**：DeepSeek驱动的智能客服，提供24/7服务
- 📊 **数据分析中心**：提供详细的运营数据分析

## 👥 用户角色

### 游客功能
- 浏览和预约乡村体验活动
- 查看农特产品信息
- 发布评价和照片
- 参与互动社区

### 农户功能
- 发布和管理体验活动
- 农特产品管理
- 智能客服配置
- 数据统计分析
- 订单管理

### 管理员功能
- 用户管理
- 内容审核
- 系统配置
- 数据概览

## 🛠 技术架构

### 前端
- Vue.js
- 响应式设计
- 现代UI/UX

### 后端
- Python + Django
- RESTful API
- 文件存储系统

### 数据库
- MySQL
- 核心数据表设计

## 📱 页面结构

```
[首页]
└── 活动列表
    └── 活动详情
        ├── 介绍
        ├── 预约
        └── 评价
        
[农户中心]
├── 活动管理
├── 商品管理
└── 预约管理

[游客中心]
├── 我的预约
└── 我的评价
```

## 🚀 快速开始

1. 克隆项目
```bash
git clone https://github.com/your-org/village-connect.git
```

2. 安装依赖
```bash
cd village-connect
pip install -r requirements.txt
```

3. 配置环境变量
```bash
cp .env.example .env
# 编辑 .env 文件配置必要的环境变量
```

4. 运行项目
```bash
python manage.py runserver
```

## 📄 许可证

MIT License

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request 来帮助改进项目。

## 📞 联系我们

- 邮箱：support@village-connect.com
- 官网：https://www.village-connect.com

## 📋 更新日志

### v1.0.0 (MVP版本)
- 基础功能上线
- 支持活动发布与预约
- 农特产品展示
- 用户评价系统 