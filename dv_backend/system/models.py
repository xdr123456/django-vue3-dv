from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password

class SysUser(AbstractUser):
    username = models.CharField(max_length=30, unique=True, verbose_name="账号" ,default="admin")
    password = models.CharField(max_length=128, verbose_name="密码",default="123456")
    nickname = models.CharField(max_length=30, blank=True, verbose_name="昵称")
    age = models.IntegerField(default=0, verbose_name="年龄")
    status = models.BooleanField(default=True, verbose_name="状态")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        db_table = "sys_user"
        verbose_name = "系统用户"

    def save(self, *args, **kwargs):
        # 新增/修改自动加密密码
        if not self.password.startswith('pbkdf2_sha256$'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)