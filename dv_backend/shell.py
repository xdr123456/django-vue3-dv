import os
import django

# 加载Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dv_backend.settings')
django.setup()

from system.models import SysUser

def init_admin_user():
    # 存在则跳过，不存在再创建
    if not SysUser.objects.filter(username="admin").exists():
        SysUser.objects.create(
            username="admin",
            password="123456",
            nickname="系统管理员",
            age=28,
            status=True
        )
        print("✅ 初始化管理员账号成功：admin / 123456")
    else:
        print("⚠️ 管理员账号已存在，无需重复创建")

if __name__ == "__main__":
    init_admin_user()