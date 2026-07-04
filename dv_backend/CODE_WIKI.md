# dv_backend Code Wiki

## 项目概述

`dv_backend` 是一个基于 **Django 4.2** 构建的后端服务项目，采用 **Django REST Framework** 提供 RESTful API，使用 **JWT** 进行身份认证，**SQLite** 作为数据库存储。

**项目定位**：通用后端基础框架，提供用户管理、身份认证等核心功能，可作为快速开发企业级应用的基础模板。

---

## 目录结构

```
dv_backend/
├── dv_backend/                    # Django项目配置目录
│   ├── __init__.py
│   ├── asgi.py                    # ASGI服务器入口
│   ├── settings.py                # 项目核心配置
│   ├── urls.py                    # URL路由配置
│   ├── wsgi.py                    # WSGI服务器入口
│   └── utils/                     # 工具模块
│       ├── exception_handler.py   # 全局异常处理
│       └── middleware.py          # 自定义中间件
├── system/                        # 系统模块（业务逻辑）
│   ├── __init__.py
│   ├── admin.py                   # Django Admin配置
│   ├── apps.py                    # App配置
│   ├── models.py                  # 数据模型
│   ├── serializers.py             # 序列化器
│   ├── views.py                   # API视图
│   ├── tests.py                   # 测试文件
│   └── migrations/                # 数据库迁移文件
├── db.sqlite3                     # SQLite数据库文件
├── manage.py                      # Django命令行工具
└── shell.py                       # 初始化脚本
```

---

## 架构设计

### 技术栈

| 组件 | 技术 | 版本 |
|------|------|------|
| 框架 | Django | 4.2 |
| API框架 | Django REST Framework | - |
| 认证 | JWT (SimpleJWT) | - |
| 数据库 | SQLite | - |
| 日志 | loguru | - |
| 跨域 | django-cors-headers | - |

### 架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                        请求层 (HTTP)                            │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     URL路由层 (urls.py)                         │
│  /api/user        →  UserViewSet                               │
│  /api/user/:id    →  UserViewSet (单个资源)                     │
│  /api/login       →  login_view                                │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    中间件层 (Middleware)                        │
│  CorsMiddleware          →  跨域处理                            │
│  HandleOptionsMiddleware →  OPTIONS请求放行                     │
│  SessionMiddleware       →  会话管理                            │
│  AuthenticationMiddleware → 认证管理                           │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     视图层 (views.py)                           │
│  UserViewSet  →  list/create/update/destroy                    │
│  login_view   →  用户登录认证                                   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                  序列化层 (serializers.py)                       │
│  UserSerializer   →  用户数据序列化/反序列化                     │
│  LoginSerializer  →  登录请求参数校验                           │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    数据模型层 (models.py)                        │
│  SysUser  →  系统用户模型                                       │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    数据库层 (SQLite)                            │
│  db.sqlite3  →  sys_user 表                                    │
└─────────────────────────────────────────────────────────────────┘
```

---

## 核心模块详解

### 1. 项目配置模块 (`dv_backend/`)

#### 1.1 settings.py

[settings.py](file:///d:/agents/dv_backend/dv_backend/settings.py) 是项目的核心配置文件，包含以下关键配置：

**日志配置**：
- 使用 `loguru` 替代默认日志
- 控制台输出，格式包含时间、级别、模块、函数、行号

**应用配置**：
- `INSTALLED_APPS` 包含 Django 内置应用和自定义应用
- `system.apps.SystemConfig` 是系统模块的注册入口

**中间件配置**：
- `CorsMiddleware`：跨域处理
- `HandleOptionsMiddleware`：OPTIONS 请求放行
- 注释掉 `CsrfViewMiddleware`，关闭 CSRF 校验

**跨域配置**：
- `CORS_ALLOW_ALL_ORIGINS = True`：允许所有来源
- `CORS_ALLOW_HEADERS = "*"`：允许所有请求头
- `CORS_ALLOW_METHODS = "*"`：允许所有请求方法

**REST Framework 配置**：
- 注册全局异常处理：`custom_exception_handler`
- 全局分页：每页 10 条

**JWT 配置**：
- `ACCESS_TOKEN_LIFETIME`：2小时
- `REFRESH_TOKEN_LIFETIME`：1天
- `AUTH_HEADER_TYPES`：Bearer

**数据库配置**：
- 使用 SQLite，数据库文件为 `db.sqlite3`

#### 1.2 urls.py

[urls.py](file:///d:/agents/dv_backend/dv_backend/urls.py) 定义了项目的路由映射：

| 路径 | 方法 | 视图 | 功能 |
|------|------|------|------|
| `/api/user` | GET | UserViewSet.list | 查询用户列表 |
| `/api/user` | POST | UserViewSet.create | 新增用户 |
| `/api/user` | PUT | UserViewSet.update | 全量更新用户 |
| `/api/user` | DELETE | UserViewSet.destroy | 删除用户 |
| `/api/user/:id` | PUT | UserViewSet.update | 更新指定用户 |
| `/api/user/:id` | DELETE | UserViewSet.destroy | 删除指定用户 |
| `/api/login` | POST | login_view | 用户登录 |

#### 1.3 工具模块 (`dv_backend/utils/`)

##### 1.3.1 exception_handler.py

[exception_handler.py](file:///d:/agents/dv_backend/dv_backend/utils/exception_handler.py) 提供全局异常处理，统一返回格式：

| 异常类型 | HTTP状态 | code | 消息 |
|----------|----------|------|------|
| JWT令牌无效/过期 | 200 | 401 | 登录令牌无效或已过期 |
| 未登录 | 200 | 401 | 请先登录 |
| 权限不足 | 200 | 403 | 权限不足，禁止访问 |
| 接口不存在 | 200 | 404 | 请求接口不存在 |
| 参数错误 | 200 | 400 | 请求参数错误 |
| 服务器未知异常 | 200 | 500 | 服务器内部错误 |

##### 1.3.2 middleware.py

[middleware.py](file:///d:/agents/dv_backend/dv_backend/utils/middleware.py) 定义了 `HandleOptionsMiddleware`，用于处理浏览器的预检请求（OPTIONS）：

- 所有 OPTIONS 请求直接返回 200
- 设置跨域响应头

---

### 2. 系统模块 (`system/`)

#### 2.1 models.py

[models.py](file:///d:/agents/dv_backend/system/models.py) 定义了 `SysUser` 模型：

**字段说明**：

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | BigAutoField | 主键 | 自增ID |
| username | CharField | max_length=30, unique | 账号，默认值"admin" |
| password | CharField | max_length=128 | 密码（加密存储），默认值"123456" |
| nickname | CharField | max_length=30, blank | 昵称 |
| age | IntegerField | default=0 | 年龄 |
| status | BooleanField | default=True | 状态（启用/禁用） |
| create_time | DateTimeField | auto_now_add | 创建时间 |

**自定义方法**：

- `save()`：重写保存方法，自动加密密码（使用 `make_password`）

**Meta配置**：
- `db_table = "sys_user"`：数据库表名
- `verbose_name = "系统用户"`：中文显示名

#### 2.2 serializers.py

[serializers.py](file:///d:/agents/dv_backend/system/serializers.py) 定义了序列化器：

##### UserSerializer

继承 `serializers.ModelSerializer`，用于用户数据的序列化和反序列化：

**序列化字段**：`id`, `username`, `nickname`, `age`, `status`, `create_time`

> **注意**：密码字段不在序列化输出中，确保安全性。

##### LoginSerializer

继承 `serializers.Serializer`，用于登录请求参数校验：

**字段**：`username`（CharField）、`password`（CharField）

#### 2.3 views.py

[views.py](file:///d:/agents/dv_backend/system/views.py) 包含视图逻辑：

##### 统一返回函数

- `result_success(data=None, msg="操作成功")`：成功响应，返回 `{"code":200, "msg":..., "data":...}`
- `result_fail(msg="操作失败")`：失败响应，返回 `{"code":400, "msg":...}`

##### UserViewSet

继承 `GenericViewSet` 并混入以下 Mixin：

| Mixin | 方法 | 功能 |
|-------|------|------|
| ListModelMixin | list() | 查询用户列表（带分页） |
| CreateModelMixin | create() | 新增用户（校验账号唯一性） |
| UpdateModelMixin | update() | 更新用户（禁止修改admin账号名） |
| DestroyModelMixin | destroy() | 删除用户（禁止删除admin） |

**权限类**：`AllowAny`（允许匿名访问）

**业务规则**：
1. 列表查询：支持分页，按ID降序排列
2. 新增用户：校验账号唯一性，密码自动加密
3. 更新用户：禁止修改管理员账号名
4. 删除用户：禁止删除系统管理员

##### login_view

登录视图函数，使用 `@api_view(["POST"])` 装饰：

**登录流程**：
1. 获取 `username` 和 `password`
2. 参数校验（不能为空）
3. 查询用户是否存在
4. 校验密码是否正确（使用 `check_password`）
5. 校验用户状态是否启用
6. 生成 JWT Token（access_token + refresh_token）
7. 返回登录成功信息

---

## 关键类与函数

### 类

| 类名 | 文件 | 功能说明 |
|------|------|----------|
| SysUser | [models.py](file:///d:/agents/dv_backend/system/models.py) | 系统用户数据模型 |
| UserSerializer | [serializers.py](file:///d:/agents/dv_backend/system/serializers.py) | 用户数据序列化器 |
| LoginSerializer | [serializers.py](file:///d:/agents/dv_backend/system/serializers.py) | 登录参数序列化器 |
| UserViewSet | [views.py](file:///d:/agents/dv_backend/system/views.py) | 用户CRUD视图集 |
| HandleOptionsMiddleware | [middleware.py](file:///d:/agents/dv_backend/dv_backend/utils/middleware.py) | OPTIONS请求处理中间件 |
| SystemConfig | [apps.py](file:///d:/agents/dv_backend/system/apps.py) | 系统模块配置类 |

### 函数

| 函数名 | 文件 | 功能说明 |
|--------|------|----------|
| custom_exception_handler | [exception_handler.py](file:///d:/agents/dv_backend/dv_backend/utils/exception_handler.py) | 全局异常处理 |
| result_success | [views.py](file:///d:/agents/dv_backend/system/views.py) | 成功响应包装 |
| result_fail | [views.py](file:///d:/agents/dv_backend/system/views.py) | 失败响应包装 |
| login_view | [views.py](file:///d:/agents/dv_backend/system/views.py) | 用户登录API |
| init_admin_user | [shell.py](file:///d:/agents/dv_backend/shell.py) | 初始化管理员账号 |

---

## API接口文档

### 用户管理接口

#### 1. 查询用户列表

- **路径**：`GET /api/user`
- **请求参数**：无
- **响应示例**：

```json
{
    "code": 200,
    "msg": "列表查询成功",
    "data": {
        "count": 1,
        "next": null,
        "previous": null,
        "results": [
            {
                "id": 1,
                "username": "admin",
                "nickname": "系统管理员",
                "age": 28,
                "status": true,
                "create_time": "2026-07-02T17:25:00"
            }
        ]
    }
}
```

#### 2. 新增用户

- **路径**：`POST /api/user`
- **请求参数**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| username | string | 是 | 账号 |
| password | string | 是 | 密码 |
| nickname | string | 否 | 昵称 |
| age | integer | 否 | 年龄 |

- **响应示例**：

```json
{
    "code": 200,
    "msg": "新增用户成功",
    "data": {
        "id": 2,
        "username": "test",
        "nickname": "测试用户",
        "age": 25,
        "status": true,
        "create_time": "2026-07-03T10:00:00"
    }
}
```

#### 3. 更新用户

- **路径**：`PUT /api/user/:id`
- **请求参数**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| username | string | 否 | 账号（admin不可修改） |
| nickname | string | 否 | 昵称 |
| age | integer | 否 | 年龄 |
| status | boolean | 否 | 状态 |

- **响应示例**：

```json
{
    "code": 200,
    "msg": "用户信息修改成功",
    "data": {
        "id": 2,
        "username": "test",
        "nickname": "测试用户2",
        "age": 26,
        "status": true,
        "create_time": "2026-07-03T10:00:00"
    }
}
```

#### 4. 删除用户

- **路径**：`DELETE /api/user/:id`
- **请求参数**：无
- **响应示例**：

```json
{
    "code": 200,
    "msg": "删除用户成功",
    "data": null
}
```

### 认证接口

#### 5. 用户登录

- **路径**：`POST /api/login`
- **请求参数**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| username | string | 是 | 账号 |
| password | string | 是 | 密码 |

- **响应示例**：

```json
{
    "code": 200,
    "msg": "登录成功",
    "data": {
        "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
        "userInfo": {
            "id": 1,
            "username": "admin",
            "nickname": "系统管理员"
        }
    }
}
```

---

## 依赖关系

### 项目依赖

| 依赖包 | 用途 |
|--------|------|
| Django | Web框架核心 |
| djangorestframework | REST API支持 |
| djangorestframework-simplejwt | JWT认证 |
| django-cors-headers | 跨域支持 |
| loguru | 日志记录 |

### 模块依赖关系

```
dv_backend/
├── settings.py → loguru, rest_framework, corsheaders
├── urls.py → system.views
└── utils/
    ├── exception_handler.py → rest_framework, rest_framework_simplejwt
    └── middleware.py → django.http

system/
├── views.py → rest_framework, models, serializers, loguru, django.contrib.auth
├── serializers.py → rest_framework, models
├── models.py → django.db, django.contrib.auth.hashers
├── apps.py → django.apps
└── migrations/ → django.db.migrations
```

---

## 项目运行

### 环境要求

- Python 3.x
- Django 4.2+

### 安装依赖

```bash
pip install django djangorestframework djangorestframework-simplejwt django-cors-headers loguru
```

### 初始化数据库

```bash
# 执行数据库迁移
python manage.py migrate

# 初始化管理员账号（admin / 123456）
python shell.py
```

### 启动开发服务器

```bash
python manage.py runserver
```

默认监听地址：`http://127.0.0.1:8000/`

### 访问接口

```bash
# 查询用户列表
curl http://127.0.0.1:8000/api/user

# 用户登录
curl -X POST http://127.0.0.1:8000/api/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"123456"}'

# 新增用户
curl -X POST http://127.0.0.1:8000/api/user \
  -H "Content-Type: application/json" \
  -d '{"username":"test","password":"123456","nickname":"测试用户"}'
```

---

## 数据库结构

### sys_user 表

| 字段名 | 类型 | 约束 |
|--------|------|------|
| id | INTEGER | PRIMARY KEY AUTOINCREMENT |
| username | VARCHAR(30) | UNIQUE NOT NULL |
| password | VARCHAR(128) | NOT NULL |
| nickname | VARCHAR(30) | NULL |
| age | INTEGER | DEFAULT 0 |
| status | BOOLEAN | DEFAULT 1 |
| create_time | DATETIME | NOT NULL |

---

## 开发规范

### 代码风格

- 使用 `loguru` 进行日志记录
- API 统一返回格式：`{"code": 200, "msg": "...", "data": ...}`
- HTTP 状态码统一返回 200，业务状态码通过 `code` 字段区分
- 密码存储使用 Django 内置的 `make_password` 加密

### 安全注意事项

1. 密码加密存储，不返回密码字段
2. 禁止删除和修改管理员账号名
3. 登录校验密码使用 `check_password`
4. 用户状态校验（禁用用户无法登录）
5. 跨域配置已放行，生产环境建议限制来源

---

## 扩展建议

### 待完善功能

1. **权限系统**：添加角色和权限管理
2. **接口文档**：集成 Swagger/DRF Spectacular
3. **数据验证**：增强参数校验逻辑
4. **单元测试**：完善测试用例
5. **部署配置**：添加生产环境配置
6. **日志持久化**：日志写入文件
7. **缓存机制**：添加 Redis 缓存
8. **文件上传**：支持文件管理功能