# 乡旅汇完整目录结构

```
village-connect/
│
├── frontend/                           # 前端项目目录
│   ├── public/                        # 静态资源
│   │   ├── index.html                # 主页面
│   │   ├── favicon.ico               # 网站图标
│   │   └── static/                   # 静态资源目录
│   │       ├── images/              # 图片资源
│   │       └── fonts/               # 字体资源
│   │
│   ├── src/                          # 源代码目录
│   │   ├── assets/                  # 资源文件
│   │   │   ├── images/             # 图片资源
│   │   │   ├── styles/             # 样式文件
│   │   │   └── icons/              # 图标文件
│   │   │
│   │   ├── components/             # 组件目录
│   │   │   ├── common/            # 通用组件
│   │   │   │   ├── Header.vue
│   │   │   │   ├── Footer.vue
│   │   │   │   ├── Sidebar.vue
│   │   │   │   └── Loading.vue
│   │   │   │
│   │   │   ├── activity/          # 活动相关组件
│   │   │   │   ├── ActivityCard.vue
│   │   │   │   ├── ActivityList.vue
│   │   │   │   └── ActivityForm.vue
│   │   │   │
│   │   │   ├── product/           # 农产品相关组件
│   │   │   │   ├── ProductCard.vue
│   │   │   │   └── ProductList.vue
│   │   │   │
│   │   │   └── user/              # 用户相关组件
│   │   │       ├── Login.vue
│   │   │       └── Register.vue
│   │   │
│   │   ├── views/                 # 页面视图
│   │   │   ├── home/             # 首页
│   │   │   │   └── Home.vue
│   │   │   │
│   │   │   ├── activity/         # 活动页面
│   │   │   │   ├── ActivityDetail.vue
│   │   │   │   └── ActivityCreate.vue
│   │   │   │
│   │   │   ├── product/          # 农产品页面
│   │   │   │   └── ProductDetail.vue
│   │   │   │
│   │   │   ├── farmer/           # 农户中心
│   │   │   │   ├── Dashboard.vue
│   │   │   │   └── Management.vue
│   │   │   │
│   │   │   ├── tourist/          # 游客中心
│   │   │   │   └── Profile.vue
│   │   │   │
│   │   │   └── admin/            # 管理后台
│   │   │       ├── UserManagement.vue
│   │   │       └── ContentManagement.vue
│   │   │
│   │   ├── router/               # 路由配置
│   │   │   ├── index.ts
│   │   │   └── routes.ts
│   │   │
│   │   ├── store/                # Vuex状态管理
│   │   │   ├── index.ts
│   │   │   ├── modules/
│   │   │   │   ├── user.ts
│   │   │   │   ├── activity.ts
│   │   │   │   └── product.ts
│   │   │   └── types.ts
│   │   │
│   │   ├── api/                  # API接口
│   │   │   ├── index.ts
│   │   │   ├── activity.ts
│   │   │   ├── product.ts
│   │   │   └── user.ts
│   │   │
│   │   ├── utils/               # 工具函数
│   │   │   ├── request.ts
│   │   │   ├── auth.ts
│   │   │   └── helpers.ts
│   │   │
│   │   ├── types/              # TypeScript类型定义
│   │   │   └── index.d.ts
│   │   │
│   │   ├── App.vue            # 根组件
│   │   └── main.ts            # 入口文件
│   │
│   ├── tests/                 # 测试目录
│   │   ├── unit/
│   │   └── e2e/
│   │
│   ├── .eslintrc.js          # ESLint配置
│   ├── .prettierrc           # Prettier配置
│   ├── tsconfig.json         # TypeScript配置
│   ├── package.json          # 包管理配置
│   └── vite.config.ts        # Vite配置
│
├── backend/                   # 后端项目目录
│   ├── village_connect/      # Django项目主目录
│   │   ├── settings/        # 配置文件
│   │   │   ├── __init__.py
│   │   │   ├── base.py     # 基础配置
│   │   │   ├── dev.py      # 开发环境配置
│   │   │   └── prod.py     # 生产环境配置
│   │   │
│   │   ├── urls.py         # URL配置
│   │   ├── wsgi.py         # WSGI配置
│   │   └── asgi.py         # ASGI配置
│   │
│   ├── apps/               # 应用模块
│   │   ├── users/         # 用户管理
│   │   │   ├── migrations/
│   │   │   ├── __init__.py
│   │   │   ├── models.py
│   │   │   ├── views.py
│   │   │   ├── serializers.py
│   │   │   ├── urls.py
│   │   │   └── tests.py
│   │   │
│   │   ├── activities/    # 活动管理
│   │   │   ├── migrations/
│   │   │   ├── __init__.py
│   │   │   ├── models.py
│   │   │   ├── views.py
│   │   │   ├── serializers.py
│   │   │   ├── urls.py
│   │   │   └── tests.py
│   │   │
│   │   ├── products/     # 农产品管理
│   │   │   ├── migrations/
│   │   │   ├── __init__.py
│   │   │   ├── models.py
│   │   │   ├── views.py
│   │   │   ├── serializers.py
│   │   │   ├── urls.py
│   │   │   └── tests.py
│   │   │
│   │   └── core/        # 核心功能
│   │       ├── __init__.py
│   │       ├── models.py
│   │       ├── views.py
│   │       └── utils.py
│   │
│   ├── utils/           # 工具函数
│   │   ├── __init__.py
│   │   ├── constants.py
│   │   ├── decorators.py
│   │   └── helpers.py
│   │
│   ├── services/       # 外部服务集成
│   │   ├── deepseek/  # DeepSeek AI服务
│   │   │   ├── __init__.py
│   │   │   └── client.py
│   │   │
│   │   ├── storage/   # 文件存储服务
│   │   │   ├── __init__.py
│   │   │   └── s3.py
│   │   │
│   │   └── payment/   # 支付服务
│   │       ├── __init__.py
│   │       └── alipay.py
│   │
│   ├── tests/         # 测试用例
│   │   ├── __init__.py
│   │   ├── test_activities.py
│   │   ├── test_products.py
│   │   └── test_users.py
│   │
│   ├── requirements/  # 依赖管理
│   │   ├── base.txt
│   │   ├── dev.txt
│   │   └── prod.txt
│   │
│   ├── manage.py     # Django管理脚本
│   └── .env.example  # 环境变量示例
│
├── docs/            # 项目文档
│   ├── api/        # API文档
│   │   ├── activities.md
│   │   ├── products.md
│   │   └── users.md
│   │
│   ├── deployment/ # 部署文档
│   │   ├── docker.md
│   │   └── kubernetes.md
│   │
│   ├── development/ # 开发指南
│   │   ├── getting-started.md
│   │   └── coding-standards.md
│   │
│   └── database/   # 数据库设计文档
│       └── schema.md
│
├── scripts/        # 部署和工具脚本
│   ├── deploy/    # 部署脚本
│   │   ├── docker/
│   │   │   ├── Dockerfile.frontend
│   │   │   └── Dockerfile.backend
│   │   │
│   │   └── kubernetes/
│   │       ├── frontend.yaml
│   │       └── backend.yaml
│   │
│   ├── backup/    # 数据备份脚本
│   │   └── backup_db.sh
│   │
│   └── maintenance/ # 维护脚本
│       └── cleanup.sh
│
├── .gitignore     # Git忽略文件
├── README.md      # 项目说明
├── LICENSE        # 许可证文件
└── docker-compose.yml  # Docker编排配置
```

## 📝 说明

1. **前端结构特点**
   - 采用 TypeScript 进行开发
   - 使用 Vue 3 + Composition API
   - Vite 作为构建工具
   - 组件化开发，逻辑清晰

2. **后端结构特点**
   - Django 项目结构清晰
   - 模块化应用设计
   - 完整的测试覆盖
   - 服务层抽象

3. **文档结构**
   - API文档完整
   - 部署文档详细
   - 开发指南清晰

4. **部署配置**
   - Docker容器化
   - Kubernetes支持
   - 完整的CI/CD支持

5. **开发规范**
   - 遵循PEP 8
   - 遵循Vue.js风格指南
   - 统一的代码风格配置

这个目录结构设计考虑了：
- 代码组织的清晰性
- 模块的独立性
- 开发的便利性
- 部署的灵活性
- 维护的可持续性 