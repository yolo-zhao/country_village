# 乡村旅游平台前端 (ZYT)

## 项目简介

这是一个基于Vue 3、Vite和Element Plus开发的乡村旅游平台前端项目。该项目旨在连接城市与乡村，为用户提供多样化的乡村活动体验和优质农产品购买渠道。

## 主要功能

- 用户认证（登录、注册）
- 乡村活动浏览与参与
- 农产品展示与购买
- 用户个人中心
- 活动评价与点赞
- 农场主管理面板

## 技术栈

- Vue 3 - 渐进式JavaScript框架
- Vite - 下一代前端构建工具
- Vue Router - 官方路由管理器
- Pinia - 状态管理库
- Element Plus - UI组件库
- Axios - HTTP客户端

## 开发环境设置

### 前提条件

- Node.js (v16+)
- npm (v8+)

### 安装步骤

1. 克隆项目
```bash
git clone <项目仓库地址>
cd zyt
```

2. 安装依赖
```bash
npm install
```

3. 启动开发服务器
```bash
npm run dev
```

4. 构建生产版本
```bash
npm run build
```

## API对接

项目默认配置与本地运行的Django后端（http://localhost:8000）进行通信。确保后端服务器正在运行并已配置好CORS。

## 项目结构

```
zyt/
├── src/              # 源代码
│   ├── api/          # API接口
│   ├── assets/       # 静态资源
│   ├── components/   # 通用组件
│   ├── router/       # 路由配置
│   ├── stores/       # Pinia状态存储
│   ├── utils/        # 工具函数
│   ├── views/        # 视图组件
│   ├── App.vue       # 主组件
│   └── main.js       # 入口文件
├── public/           # 公共资源
├── index.html        # HTML模板
├── package.json      # 依赖和脚本
└── vite.config.js    # Vite配置
```

## 贡献指南

欢迎贡献！请确保遵循项目的代码风格和提交规范。

## 许可证

[MIT许可证](LICENSE)
