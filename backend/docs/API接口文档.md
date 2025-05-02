# 乡村旅游平台 API 接口文档

## 目录

- [1. 用户管理](#1-用户管理)
- [2. 核心功能](#2-核心功能)
- [3. 活动管理](#3-活动管理)
- [4. 农产品管理](#4-农产品管理)
- [5. 统计分析](#5-统计分析)
- [6. 消息通知](#6-消息通知)

## 1. 用户管理

### 1.1 用户注册

- **接口**: `/api/users/register/`
- **方法**: POST
- **描述**: 创建新用户账号
- **请求参数**:

```json
{
  "username": "tourist001",
  "password": "password123",
  "email": "tourist001@example.com",
  "role": "tourist",  // "tourist" 或 "farmer"
  "first_name": "张",
  "last_name": "三"
}
```

- **响应**:

```json
{
  "message": "注册成功",
  "user_id": 10,
  "username": "tourist001",
  "role": "tourist"
}
```

### 1.2 用户登录

- **接口**: `/api/users/login/`
- **方法**: POST
- **描述**: 用户登录获取认证令牌
- **请求参数**:

```json
{
  "username": "tourist001",
  "password": "password123"
}
```

- **响应**:

```json
{
  "success": true,
  "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
  "user_id": 10,
  "username": "tourist001",
  "role": "tourist",
  "email": "tourist001@example.com",
  "first_name": "张",
  "last_name": "三"
}
```

### 1.3 当前用户信息

- **接口**: `/api/users/me/`
- **方法**: GET
- **描述**: 获取当前登录用户的详细信息
- **请求头**: 
  - Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
- **响应**:

```json
{
  "id": 10,
  "username": "tourist001",
  "email": "tourist001@example.com",
  "first_name": "张",
  "last_name": "三",
  "role": "tourist",
  "profile": {
    "nickname": "小张",
    "contact_phone": "13800138000"
  }
}
```

### 1.4 更新用户信息

- **接口**: `/api/users/update-info/`
- **方法**: PUT
- **描述**: 更新当前用户的信息
- **请求头**: 
  - Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
- **请求参数**:

```json
{
  "first_name": "张",
  "last_name": "小三",
  "email": "tourist001@example.com",
  "profile": {
    "nickname": "小张张",
    "contact_phone": "13900139000"
  }
}
```

- **响应**:

```json
{
  "message": "用户信息更新成功",
  "user": {
    "id": 10,
    "username": "tourist001",
    "email": "tourist001@example.com",
    "first_name": "张",
    "last_name": "小三",
    "profile": {
      "nickname": "小张张",
      "contact_phone": "13900139000"
    }
  }
}
```

### 1.5 修改密码

- **接口**: `/api/users/change-password/`
- **方法**: POST
- **描述**: 修改当前用户的密码
- **请求头**: 
  - Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
- **请求参数**:

```json
{
  "old_password": "password123",
  "new_password": "newpassword123"
}
```

- **响应**:

```json
{
  "message": "密码修改成功"
}
```

### 1.6 密码重置请求

- **接口**: `/api/users/password-reset/`
- **方法**: POST
- **描述**: 请求密码重置（发送重置邮件）
- **请求参数**:

```json
{
  "email": "tourist001@example.com"
}
```

- **响应**:

```json
{
  "message": "密码重置链接已发送到您的邮箱"
}
```

### 1.7 密码重置确认

- **接口**: `/api/users/password-reset-confirm/`
- **方法**: POST
- **描述**: 确认密码重置
- **请求参数**:

```json
{
  "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
  "uid": "MTA",
  "new_password": "newpassword123"
}
```

- **响应**:

```json
{
  "message": "密码重置成功"
}
```

### 1.8 用户登出

- **接口**: `/api/users/logout/`
- **方法**: POST
- **描述**: 用户登出（使当前token失效）
- **请求头**: 
  - Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
- **响应**:

```json
{
  "message": "登出成功"
}
```

## 2. 核心功能

### 2.1 系统公告

#### 2.1.1 获取系统公告列表

- **接口**: `/api/core/announcements/`
- **方法**: GET
- **描述**: 获取系统公告列表
- **请求参数**: 无
- **响应**:

```json
{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "平台正式上线",
      "content": "乡村旅游平台正式上线，欢迎大家使用！",
      "created_at": "2023-11-01T10:00:00Z",
      "is_active": true
    },
    {
      "id": 2,
      "title": "端午节活动",
      "content": "端午节期间，平台将推出多项特色活动，敬请期待！",
      "created_at": "2023-11-05T14:30:00Z",
      "is_active": true
    }
  ]
}
```

### 2.2 文件上传

- **接口**: `/api/core/upload/`
- **方法**: POST
- **描述**: 上传文件（图片等）
- **请求头**: 
  - Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
  - Content-Type: multipart/form-data
- **请求参数**:
  - file: (文件)
  - type: "image" (文件类型，可选值: "image", "document", "video")
- **响应**:

```json
{
  "url": "https://example.com/media/uploads/image_123456.jpg",
  "file_name": "image_123456.jpg",
  "file_type": "image",
  "size": 1024000
}
```

### 2.3 用户反馈

- **接口**: `/api/core/feedback/`
- **方法**: POST
- **描述**: 提交用户反馈
- **请求头**: 
  - Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
- **请求参数**:

```json
{
  "subject": "功能建议",
  "content": "希望能增加更多种类的农产品",
  "contact_info": "13800138000"
}
```

- **响应**:

```json
{
  "id": 1,
  "subject": "功能建议",
  "content": "希望能增加更多种类的农产品",
  "contact_info": "13800138000",
  "created_at": "2023-11-10T09:15:00Z",
  "status": "pending"
}
```

## 3. 活动管理

### 3.1 获取活动列表

- **接口**: `/api/activities/activities/`
- **方法**: GET
- **描述**: 获取活动列表
- **请求参数**:
  - page: 1 (页码，可选)
  - page_size: 10 (每页条数，可选)
  - category: 1 (活动分类ID，可选)
  - tag: 2 (活动标签ID，可选)
  - search: "采摘" (搜索关键词，可选)
- **响应**:

```json
{
  "count": 50,
  "next": "http://example.com/api/activities/activities/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "乡村采摘节",
      "slug": "countryside-harvest-festival",
      "description": "来体验采摘的乐趣，品尝新鲜水果",
      "start_time": "2023-11-15T09:00:00Z",
      "end_time": "2023-11-15T17:00:00Z",
      "location": "江苏省南京市江宁区",
      "category": {
        "id": 1,
        "name": "采摘活动"
      },
      "tags": [
        {
          "id": 1,
          "name": "水果"
        },
        {
          "id": 2,
          "name": "户外"
        }
      ],
      "cover_image": "http://example.com/media/activities/covers/harvest.jpg",
      "max_participants": 30,
      "farmer": {
        "id": 5,
        "username": "farmer001",
        "farm_name": "绿野果园"
      },
      "created_at": "2023-10-15T08:30:00Z",
      "updated_at": "2023-10-15T08:30:00Z"
    }
    // 更多活动...
  ]
}
```

### 3.2 创建活动

- **接口**: `/api/activities/activities/`
- **方法**: POST
- **描述**: 创建新活动
- **请求头**: 
  - Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
- **请求参数**:

```json
{
  "title": "农家乐烧烤体验",
  "description": "来我们的农家乐体验烧烤的乐趣，提供新鲜食材和烧烤设备",
  "start_time": "2023-12-01T10:00:00Z",
  "end_time": "2023-12-01T16:00:00Z",
  "location": "浙江省杭州市西湖区",
  "category": 2,
  "tags": [1, 3, 4],
  "cover_image": "http://example.com/media/activities/covers/bbq.jpg",
  "max_participants": 20
}
```

- **响应**:

```json
{
  "id": 2,
  "title": "农家乐烧烤体验",
  "slug": "farmhouse-bbq-experience",
  "description": "来我们的农家乐体验烧烤的乐趣，提供新鲜食材和烧烤设备",
  "start_time": "2023-12-01T10:00:00Z",
  "end_time": "2023-12-01T16:00:00Z",
  "location": "浙江省杭州市西湖区",
  "category": {
    "id": 2,
    "name": "农家乐"
  },
  "tags": [
    {
      "id": 1,
      "name": "美食"
    },
    {
      "id": 3,
      "name": "体验"
    },
    {
      "id": 4,
      "name": "烧烤"
    }
  ],
  "cover_image": "http://example.com/media/activities/covers/bbq.jpg",
  "max_participants": 20,
  "farmer": {
    "id": 5,
    "username": "farmer001",
    "farm_name": "绿野农家乐"
  },
  "created_at": "2023-11-10T09:15:00Z",
  "updated_at": "2023-11-10T09:15:00Z"
}
```

### 3.3 活动打卡

- **接口**: `/api/activities/activity-check-ins/`
- **方法**: POST
- **描述**: 创建活动打卡记录
- **请求头**: 
  - Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
- **请求参数**:

```json
{
  "activity": 1,
  "location_text": "江苏省南京市江宁区",
  "note": "今天天气很好，采摘了很多水果，非常开心！",
  "photo": "http://example.com/media/checkins/photo123.jpg"
}
```

- **响应**:

```json
{
  "id": 1,
  "activity": {
    "id": 1,
    "title": "乡村采摘节"
  },
  "user": {
    "id": 10,
    "username": "tourist001"
  },
  "location_text": "江苏省南京市江宁区",
  "note": "今天天气很好，采摘了很多水果，非常开心！",
  "photo": "http://example.com/media/checkins/photo123.jpg",
  "check_in_time": "2023-11-15T10:30:00Z"
}
```

### 3.4 我的活动

- **接口**: `/api/activities/my-activities/`
- **方法**: GET
- **描述**: 获取当前用户参与的活动
- **请求头**: 
  - Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
- **响应**:

```json
{
  "count": 3,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "乡村采摘节",
      "slug": "countryside-harvest-festival",
      "start_time": "2023-11-15T09:00:00Z",
      "end_time": "2023-11-15T17:00:00Z",
      "location": "江苏省南京市江宁区",
      "cover_image": "http://example.com/media/activities/covers/harvest.jpg",
      "status": "completed",
      "participation_time": "2023-11-15T10:30:00Z"
    },
    // 更多活动...
  ]
}
```

## 4. 农产品管理

### 4.1 获取产品列表

- **接口**: `/api/products/products/`
- **方法**: GET
- **描述**: 获取产品列表
- **请求参数**:
  - page: 1 (页码，可选)
  - page_size: 10 (每页条数，可选)
  - search: "水果" (搜索关键词，可选)
- **响应**:

```json
{
  "count": 25,
  "next": "http://example.com/api/products/products/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "有机草莓",
      "slug": "organic-strawberry",
      "description": "新鲜有机草莓，无农药，甜美多汁",
      "price": "35.00",
      "stock": 100,
      "status": "published",
      "farmer": {
        "id": 5,
        "username": "farmer001",
        "farm_name": "绿野果园"
      },
      "images": [
        {
          "id": 1,
          "image": "http://example.com/media/products/images/strawberry1.jpg",
          "caption": "草莓特写"
        },
        {
          "id": 2,
          "image": "http://example.com/media/products/images/strawberry2.jpg",
          "caption": "草莓包装"
        }
      ],
      "created_at": "2023-10-10T09:00:00Z",
      "updated_at": "2023-10-10T09:00:00Z"
    }
    // 更多产品...
  ]
}
```

### 4.2 购物车操作

#### 4.2.1 获取购物车

- **接口**: `/api/products/carts/1/`
- **方法**: GET
- **描述**: 获取当前用户的购物车
- **请求头**: 
  - Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
- **响应**:

```json
{
  "id": 1,
  "user": {
    "id": 10,
    "username": "tourist001"
  },
  "items": [
    {
      "id": 1,
      "product": {
        "id": 1,
        "name": "有机草莓",
        "price": "35.00",
        "images": [
          {
            "id": 1,
            "image": "http://example.com/media/products/images/strawberry1.jpg"
          }
        ]
      },
      "quantity": 2,
      "total_price": "70.00"
    }
  ],
  "total_items": 2,
  "total_price": "70.00",
  "created_at": "2023-11-01T10:00:00Z",
  "updated_at": "2023-11-10T11:30:00Z"
}
```

#### 4.2.2 添加商品到购物车

- **接口**: `/api/products/carts/1/add_item/`
- **方法**: POST
- **描述**: 添加商品到购物车
- **请求头**: 
  - Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
- **请求参数**:

```json
{
  "product_id": 1,
  "quantity": 2
}
```

- **响应**:

```json
{
  "id": 1,
  "user": {
    "id": 10,
    "username": "tourist001"
  },
  "items": [
    {
      "id": 1,
      "product": {
        "id": 1,
        "name": "有机草莓",
        "price": "35.00"
      },
      "quantity": 4,
      "total_price": "140.00"
    }
  ],
  "total_items": 4,
  "total_price": "140.00"
}
```

### 4.3 订单管理

#### 4.3.1 创建订单

- **接口**: `/api/products/orders/`
- **方法**: POST
- **描述**: 创建订单
- **请求头**: 
  - Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
- **请求参数**:

```json
{
  "items": [
    {
      "product_id": 1,
      "quantity": 4
    }
  ],
  "shipping_address": {
    "name": "张三",
    "phone": "13800138000",
    "province": "江苏省",
    "city": "南京市",
    "district": "江宁区",
    "address": "学府路1号",
    "zip_code": "210000"
  },
  "payment_method": "alipay"
}
```

- **响应**:

```json
{
  "id": "ORD20231110001",
  "items": [
    {
      "product": {
        "id": 1,
        "name": "有机草莓",
        "price": "35.00"
      },
      "quantity": 4,
      "price": "35.00",
      "total_price": "140.00"
    }
  ],
  "shipping_address": {
    "name": "张三",
    "phone": "13800138000",
    "province": "江苏省",
    "city": "南京市",
    "district": "江宁区",
    "address": "学府路1号",
    "zip_code": "210000"
  },
  "payment_method": "alipay",
  "total_price": "140.00",
  "status": "pending",
  "payment_url": "https://example.com/payment/alipay/9a8b7c6d5e4f",
  "created_at": "2023-11-10T11:45:00Z"
}
```

#### 4.3.2 获取订单列表

- **接口**: `/api/products/my-orders/`
- **方法**: GET
- **描述**: 获取当前用户的订单列表
- **请求头**: 
  - Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
- **响应**:

```json
{
  "count": 3,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": "ORD20231110001",
      "items_count": 1,
      "total_price": "140.00",
      "status": "paid",
      "created_at": "2023-11-10T11:45:00Z"
    },
    {
      "id": "ORD20231105002",
      "items_count": 2,
      "total_price": "85.50",
      "status": "delivered",
      "created_at": "2023-11-05T10:15:00Z"
    },
    {
      "id": "ORD20231101003",
      "items_count": 1,
      "total_price": "59.90",
      "status": "completed",
      "created_at": "2023-11-01T14:30:00Z"
    }
  ]
}
```

## 5. 统计分析

### 5.1 用户行为分析

- **接口**: `/api/analytics/user-behavior/`
- **方法**: GET
- **描述**: 获取用户行为分析数据
- **请求头**: 
  - Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
- **请求参数**:
  - start_date: "2023-11-01" (开始日期，可选)
  - end_date: "2023-11-10" (结束日期，可选)
- **响应**:

```json
{
  "page_views": {
    "total": 1250,
    "average_per_day": 125,
    "trend": [
      {"date": "2023-11-01", "value": 110},
      {"date": "2023-11-02", "value": 115},
      // 更多数据...
    ]
  },
  "active_users": {
    "total": 450,
    "average_per_day": 45,
    "trend": [
      {"date": "2023-11-01", "value": 40},
      {"date": "2023-11-02", "value": 42},
      // 更多数据...
    ]
  },
  "most_viewed_pages": [
    {"path": "/activities/", "views": 350},
    {"path": "/products/", "views": 280},
    {"path": "/activities/1/", "views": 180}
  ]
}
```

## 6. 消息通知

### 6.1 获取未读通知数量

- **接口**: `/api/notifications/count/`
- **方法**: GET
- **描述**: 获取当前用户的未读通知数量
- **请求头**: 
  - Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
- **响应**:

```json
{
  "unread_count": 5,
  "categories": {
    "system": 1,
    "activity": 2,
    "order": 1,
    "comment": 1
  }
}
```

### 6.2 获取最新通知

- **接口**: `/api/notifications/latest/`
- **方法**: GET
- **描述**: 获取当前用户的最新通知
- **请求头**: 
  - Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
- **请求参数**:
  - limit: 10 (限制返回的通知数量，可选)
- **响应**:

```json
{
  "count": 5,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "type": "activity",
      "title": "活动即将开始",
      "content": "您参与的"乡村采摘节"将于明天上午9点开始，请准时参加。",
      "is_read": false,
      "created_at": "2023-11-14T10:00:00Z"
    },
    {
      "id": 2,
      "type": "order",
      "title": "订单已发货",
      "content": "您购买的"有机草莓"已发货，物流单号：SF1234567890。",
      "is_read": false,
      "created_at": "2023-11-13T14:30:00Z"
    },
    // 更多通知...
  ]
}
```

### 6.3 标记通知为已读

- **接口**: `/api/notifications/mark-read/`
- **方法**: POST
- **描述**: 标记指定通知为已读
- **请求头**: 
  - Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
- **请求参数**:

```json
{
  "notification_ids": [1, 2]
}
```

- **响应**:

```json
{
  "message": "通知已标记为已读",
  "marked_count": 2
}
``` 