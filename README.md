# Django-Vue3-DV

基于 Django 4.2 + Vue 3 的前后端分离管理系统模板。

## 技术栈

### 后端
- **框架**: Django 4.2
- **API**: Django REST Framework
- **认证**: JWT (django-rest-framework-simplejwt)
- **数据库**: SQLite
- **日志**: loguru
- **Excel处理**: pandas + openpyxl

### 前端
- **框架**: Vue 3 (Composition API)
- **构建工具**: Vite 8
- **UI组件**: Element Plus
- **路由**: Vue Router 4
- **HTTP请求**: Axios

## 项目结构

```
django-vue3-dv/
├── dv_backend/                    # 后端 Django 项目
│   ├── dv_backend/               # 项目配置
│   │   ├── settings.py           # 配置文件
│   │   ├── urls.py               # 路由配置
│   │   ├── utils/                # 工具函数
│   │   │   ├── exception_handler.py  # 全局异常处理
│   │   │   └── middleware.py     # 中间件
│   ├── system/                   # 系统模块
│   │   ├── models.py             # 数据模型
│   │   ├── views.py              # 视图逻辑
│   │   ├── serializers.py        # 序列化器
│   │   └── migrations/           # 数据库迁移
│   └── manage.py                 # Django 管理脚本
├── frontend/                     # 前端 Vue 项目
│   ├── src/
│   │   ├── views/                # 页面组件
│   │   │   ├── Login.vue         # 登录页面
│   │   │   └── UserList.vue      # 用户列表页面
│   │   ├── router/               # 路由配置
│   │   ├── utils/                # 工具函数
│   │   ├── components/           # 公共组件
│   │   └── main.js               # 入口文件
│   └── package.json              # 依赖配置
└── README.md
```

## 快速开始

### 环境要求

- Python 3.8+
- Node.js 18+

### 后端启动

```bash
# 进入后端目录
cd dv_backend

# 安装依赖
pip install -r requirements.txt

# 数据库迁移
python manage.py migrate

# 创建管理员账号（可选）
python manage.py createsuperuser

# 启动开发服务器
python manage.py runserver 0.0.0.0:8000
```

### 前端启动

```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

## API 接口

### 认证接口

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/login` | 用户登录 |
| POST | `/api/token/refresh` | 刷新Token |

### 用户管理接口

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/user` | 查询用户列表 |
| POST | `/api/user` | 新增用户 |
| PUT | `/api/user/<id>` | 更新用户信息 |
| DELETE | `/api/user/<id>` | 删除用户 |
| GET | `/api/user/export` | 导出用户Excel |
| GET | `/api/user/template` | 下载导入模板 |
| POST | `/api/user/import` | 导入用户数据 |

### 登录示例

```bash
curl -X POST http://localhost:8000/api/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "123456"}'
```

### 响应格式

**成功响应:**
```json
{
  "code": 200,
  "msg": "操作成功",
  "data": {}
}
```

**失败响应:**
```json
{
  "code": 400,
  "msg": "操作失败"
}
```

## 数据库模型

### SysUser（系统用户）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer | 主键 |
| username | CharField | 登录账号（唯一） |
| password | CharField | 密码（加密存储） |
| nickname | CharField | 用户昵称 |
| age | Integer | 年龄 |
| status | BooleanField | 状态（默认启用） |
| create_time | DateTimeField | 创建时间 |

## 功能特性

- ✅ 用户登录认证（JWT）
- ✅ 用户 CRUD 操作
- ✅ 用户列表分页
- ✅ 用户 Excel 导入导出
- ✅ 全局异常处理
- ✅ 跨域请求支持
- ✅ 统一响应格式

## 默认账号

- **用户名**: admin
- **密码**: 123456

## 开发说明

### 后端配置

主要配置文件位于 `dv_backend/dv_backend/settings.py`：

- **JWT配置**: 访问令牌有效期30分钟，刷新令牌有效期7天
- **跨域配置**: 允许所有来源访问
- **分页配置**: 每页默认10条

### 前端配置

主要配置文件位于 `frontend/vite.config.js`。

## License

MIT