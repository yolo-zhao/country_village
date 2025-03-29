# 乡旅汇数据库设计文档

## 📝 数据库总体设计

数据库采用 MySQL 5.7+，字符集使用 UTF8MB4，排序规则使用 utf8mb4_unicode_ci。

## 📊 数据表设计

### 1. 用户相关表

#### 1.1 用户表 (users)
| 字段名 | 类型 | 长度 | 允许空 | 默认值 | 说明 |
|--------|------|------|--------|--------|------|
| id | BIGINT | 20 | NO | | 主键，自增 |
| username | VARCHAR | 50 | NO | | 用户名 |
| password | VARCHAR | 255 | NO | | 密码（加密存储）|
| email | VARCHAR | 100 | NO | | 邮箱 |
| phone | VARCHAR | 20 | YES | NULL | 手机号 |
| role | ENUM | - | NO | 'tourist' | 角色(tourist/farmer/admin) |
| status | TINYINT | 1 | NO | 1 | 状态(0:禁用,1:正常) |
| avatar | VARCHAR | 255 | YES | NULL | 头像URL |
| created_at | TIMESTAMP | - | NO | CURRENT_TIMESTAMP | 创建时间 |
| updated_at | TIMESTAMP | - | NO | CURRENT_TIMESTAMP | 更新时间 |

索引：
- PRIMARY KEY (id)
- UNIQUE KEY (username)
- UNIQUE KEY (email)
- UNIQUE KEY (phone)
- INDEX (role)

#### 1.2 农户信息表 (farmer_profiles)
| 字段名 | 类型 | 长度 | 允许空 | 默认值 | 说明 |
|--------|------|------|--------|--------|------|
| id | BIGINT | 20 | NO | | 主键，自增 |
| user_id | BIGINT | 20 | NO | | 关联用户ID |
| farm_name | VARCHAR | 100 | NO | | 农场名称 |
| address | VARCHAR | 255 | NO | | 地址 |
| description | TEXT | - | YES | NULL | 农场描述 |
| business_license | VARCHAR | 255 | YES | NULL | 营业执照号 |
| contact_person | VARCHAR | 50 | NO | | 联系人 |
| created_at | TIMESTAMP | - | NO | CURRENT_TIMESTAMP | 创建时间 |
| updated_at | TIMESTAMP | - | NO | CURRENT_TIMESTAMP | 更新时间 |

索引：
- PRIMARY KEY (id)
- FOREIGN KEY (user_id) REFERENCES users(id)
- INDEX (farm_name)

### 2. 活动相关表

#### 2.1 活动表 (activities)
| 字段名 | 类型 | 长度 | 允许空 | 默认值 | 说明 |
|--------|------|------|--------|--------|------|
| id | BIGINT | 20 | NO | | 主键，自增 |
| farmer_id | BIGINT | 20 | NO | | 关联农户ID |
| title | VARCHAR | 100 | NO | | 活动标题 |
| description | TEXT | - | NO | | 活动描述 |
| start_time | DATETIME | - | NO | | 开始时间 |
| end_time | DATETIME | - | NO | | 结束时间 |
| location | VARCHAR | 255 | NO | | 活动地点 |
| max_participants | INT | 11 | NO | | 人数上限 |
| current_participants | INT | 11 | NO | 0 | 当前参与人数 |
| price | DECIMAL | (10,2) | NO | 0.00 | 活动价格 |
| status | TINYINT | 1 | NO | 1 | 状态(0:下架,1:正常) |
| category | VARCHAR | 50 | NO | | 活动类型 |
| created_at | TIMESTAMP | - | NO | CURRENT_TIMESTAMP | 创建时间 |
| updated_at | TIMESTAMP | - | NO | CURRENT_TIMESTAMP | 更新时间 |

索引：
- PRIMARY KEY (id)
- FOREIGN KEY (farmer_id) REFERENCES users(id)
- INDEX (status)
- INDEX (category)
- INDEX (start_time)

#### 2.2 活动图片表 (activity_images)
| 字段名 | 类型 | 长度 | 允许空 | 默认值 | 说明 |
|--------|------|------|--------|--------|------|
| id | BIGINT | 20 | NO | | 主键，自增 |
| activity_id | BIGINT | 20 | NO | | 关联活动ID |
| image_url | VARCHAR | 255 | NO | | 图片URL |
| sort_order | INT | 11 | NO | 0 | 排序顺序 |
| created_at | TIMESTAMP | - | NO | CURRENT_TIMESTAMP | 创建时间 |

索引：
- PRIMARY KEY (id)
- FOREIGN KEY (activity_id) REFERENCES activities(id)
- INDEX (sort_order)

#### 2.3 活动预约表 (bookings)
| 字段名 | 类型 | 长度 | 允许空 | 默认值 | 说明 |
|--------|------|------|--------|--------|------|
| id | BIGINT | 20 | NO | | 主键，自增 |
| activity_id | BIGINT | 20 | NO | | 关联活动ID |
| user_id | BIGINT | 20 | NO | | 关联用户ID |
| booking_date | DATE | - | NO | | 预约日期 |
| status | TINYINT | 1 | NO | 0 | 状态(0:待确认,1:已确认,2:已取消) |
| participant_count | INT | 11 | NO | 1 | 参与人数 |
| contact_name | VARCHAR | 50 | NO | | 联系人姓名 |
| contact_phone | VARCHAR | 20 | NO | | 联系电话 |
| remarks | TEXT | - | YES | NULL | 备注信息 |
| created_at | TIMESTAMP | - | NO | CURRENT_TIMESTAMP | 创建时间 |
| updated_at | TIMESTAMP | - | NO | CURRENT_TIMESTAMP | 更新时间 |

索引：
- PRIMARY KEY (id)
- FOREIGN KEY (activity_id) REFERENCES activities(id)
- FOREIGN KEY (user_id) REFERENCES users(id)
- INDEX (booking_date)
- INDEX (status)

### 3. 农产品相关表

#### 3.1 农产品表 (products)
| 字段名 | 类型 | 长度 | 允许空 | 默认值 | 说明 |
|--------|------|------|--------|--------|------|
| id | BIGINT | 20 | NO | | 主键，自增 |
| farmer_id | BIGINT | 20 | NO | | 关联农户ID |
| name | VARCHAR | 100 | NO | | 产品名称 |
| description | TEXT | - | NO | | 产品描述 |
| price | DECIMAL | (10,2) | NO | 0.00 | 产品价格 |
| unit | VARCHAR | 20 | NO | | 计量单位 |
| stock | INT | 11 | NO | 0 | 库存数量 |
| category | VARCHAR | 50 | NO | | 产品类别 |
| status | TINYINT | 1 | NO | 1 | 状态(0:下架,1:正常) |
| created_at | TIMESTAMP | - | NO | CURRENT_TIMESTAMP | 创建时间 |
| updated_at | TIMESTAMP | - | NO | CURRENT_TIMESTAMP | 更新时间 |

索引：
- PRIMARY KEY (id)
- FOREIGN KEY (farmer_id) REFERENCES users(id)
- INDEX (category)
- INDEX (status)

#### 3.2 产品图片表 (product_images)
| 字段名 | 类型 | 长度 | 允许空 | 默认值 | 说明 |
|--------|------|------|--------|--------|------|
| id | BIGINT | 20 | NO | | 主键，自增 |
| product_id | BIGINT | 20 | NO | | 关联产品ID |
| image_url | VARCHAR | 255 | NO | | 图片URL |
| sort_order | INT | 11 | NO | 0 | 排序顺序 |
| created_at | TIMESTAMP | - | NO | CURRENT_TIMESTAMP | 创建时间 |

索引：
- PRIMARY KEY (id)
- FOREIGN KEY (product_id) REFERENCES products(id)
- INDEX (sort_order)

### 4. 评价相关表

#### 4.1 活动评价表 (activity_reviews)
| 字段名 | 类型 | 长度 | 允许空 | 默认值 | 说明 |
|--------|------|------|--------|--------|------|
| id | BIGINT | 20 | NO | | 主键，自增 |
| activity_id | BIGINT | 20 | NO | | 关联活动ID |
| user_id | BIGINT | 20 | NO | | 关联用户ID |
| booking_id | BIGINT | 20 | NO | | 关联预约ID |
| rating | TINYINT | 1 | NO | | 评分(1-5) |
| content | TEXT | - | NO | | 评价内容 |
| status | TINYINT | 1 | NO | 1 | 状态(0:隐藏,1:显示) |
| created_at | TIMESTAMP | - | NO | CURRENT_TIMESTAMP | 创建时间 |
| updated_at | TIMESTAMP | - | NO | CURRENT_TIMESTAMP | 更新时间 |

索引：
- PRIMARY KEY (id)
- FOREIGN KEY (activity_id) REFERENCES activities(id)
- FOREIGN KEY (user_id) REFERENCES users(id)
- FOREIGN KEY (booking_id) REFERENCES bookings(id)
- INDEX (rating)
- INDEX (status)

#### 4.2 评价图片表 (review_images)
| 字段名 | 类型 | 长度 | 允许空 | 默认值 | 说明 |
|--------|------|------|--------|--------|------|
| id | BIGINT | 20 | NO | | 主键，自增 |
| review_id | BIGINT | 20 | NO | | 关联评价ID |
| image_url | VARCHAR | 255 | NO | | 图片URL |
| created_at | TIMESTAMP | - | NO | CURRENT_TIMESTAMP | 创建时间 |

索引：
- PRIMARY KEY (id)
- FOREIGN KEY (review_id) REFERENCES activity_reviews(id)

### 5. 统计相关表

#### 5.1 活动统计表 (activity_statistics)
| 字段名 | 类型 | 长度 | 允许空 | 默认值 | 说明 |
|--------|------|------|--------|--------|------|
| id | BIGINT | 20 | NO | | 主键，自增 |
| activity_id | BIGINT | 20 | NO | | 关联活动ID |
| view_count | INT | 11 | NO | 0 | 浏览次数 |
| booking_count | INT | 11 | NO | 0 | 预约次数 |
| review_count | INT | 11 | NO | 0 | 评价次数 |
| avg_rating | DECIMAL | (2,1) | NO | 0.0 | 平均评分 |
| updated_at | TIMESTAMP | - | NO | CURRENT_TIMESTAMP | 更新时间 |

索引：
- PRIMARY KEY (id)
- FOREIGN KEY (activity_id) REFERENCES activities(id)
- INDEX (view_count)
- INDEX (booking_count)
- INDEX (avg_rating)

## 🔗 表关系说明

1. **用户关系**
   - users -> farmer_profiles (1:1)
   - users -> activities (1:n)
   - users -> bookings (1:n)
   - users -> activity_reviews (1:n)

2. **活动关系**
   - activities -> activity_images (1:n)
   - activities -> bookings (1:n)
   - activities -> activity_reviews (1:n)
   - activities -> activity_statistics (1:1)

3. **产品关系**
   - products -> product_images (1:n)

4. **评价关系**
   - activity_reviews -> review_images (1:n)
   - activity_reviews -> bookings (1:1)

## 💡 设计说明

1. **主键设计**
   - 所有表使用BIGINT类型的自增主键
   - 主键名统一为id

2. **外键设计**
   - 外键命名规则：关联表名_id
   - 所有外键都建立了相应的索引

3. **时间字段**
   - created_at: 记录创建时间
   - updated_at: 记录更新时间
   - 统一使用TIMESTAMP类型

4. **状态字段**
   - 使用TINYINT类型
   - 统一使用status字段名
   - 0表示非正常状态，1表示正常状态

5. **索引设计**
   - 对常用查询字段建立索引
   - 考虑了查询效率和写入性能的平衡

6. **安全性考虑**
   - 密码字段使用加密存储
   - 敏感信息使用适当的字段长度

7. **扩展性考虑**
   - 预留了足够的字段长度
   - 使用了较为宽松的字段类型
   - 考虑了未来可能的功能扩展 