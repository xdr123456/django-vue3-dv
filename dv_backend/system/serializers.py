from rest_framework import serializers
from .models import SysUser
from datetime import datetime

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = SysUser
        fields = "__all__"

# 登录序列化
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

