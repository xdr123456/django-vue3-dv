from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from system.views import UserViewSet, login_view, export_excel, down_template, import_excel
from rest_framework_simplejwt.views import TokenRefreshView

# router = DefaultRouter()
# router.register(r'user', UserViewSet)

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('api/', include(router.urls)),
#     path('api/login', login_view),
# ]

urlpatterns = [
    # 无尾部斜杠 纯 /user
    path('api/user', UserViewSet.as_view({
        'get': 'list',          # GET 查询列表
        'post': 'create',       # POST 新增
        'put': 'update',        # PUT 全量编辑
        'delete': 'destroy',     # DELETE 删除
    })),
    # 单条用户详情（编辑/删除需要传id）
    path('api/user/<int:pk>', UserViewSet.as_view({
        'put': 'update',
        'delete': 'destroy'
    })),
    # 导入导出Excel接口
    path('api/user/export', export_excel),
    path('api/user/template', down_template),
    path('api/user/import', import_excel),

    path('api/login', login_view),
    path('api/token/refresh', TokenRefreshView.as_view(), name='token_refresh')
]