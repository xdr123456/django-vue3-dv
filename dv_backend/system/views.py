from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
import pandas as pd
from io import BytesIO
from django.http import HttpResponse
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from .models import SysUser
from .serializers import UserSerializer, LoginSerializer
from rest_framework.decorators import api_view
from django.contrib.auth.hashers import check_password, make_password
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import permission_classes
from loguru import logger
from rest_framework.mixins import ListModelMixin,CreateModelMixin,UpdateModelMixin,DestroyModelMixin


# 统一返回格式
def result_success(data=None, msg="操作成功"):
    return Response({"code":200, "msg":msg, "data":data})

def result_fail(msg="操作失败"):
    return Response({"code":400, "msg":msg}, status=status.HTTP_200_OK)

# 用户CRUD
class UserViewSet(
    ListModelMixin,        # 列表查询 list
    CreateModelMixin,      # 新增 create
    UpdateModelMixin,      # 修改 update
    DestroyModelMixin,     # 删除 destroy
    GenericViewSet
):
    queryset = SysUser.objects.all().order_by("-id")
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    # 1. 【单独：查询列表】独立逻辑
    def list(self, request, *args, **kwargs):
        logger.info('===== 执行 查询列表 逻辑 =====')
        logger.debug(f"查询列表参数：{request.data}")

        queryset = self.get_queryset()
        page_data = self.paginate_queryset(queryset)
        if page_data:
            ser = self.get_serializer(page_data, many=True)
            page_res = self.get_paginated_response(ser.data)
            return result_success(page_res.data, "列表查询成功")
        
        ser = self.get_serializer(queryset, many=True)
        return result_success(ser.data, "查询成功")

    # 2. 【单独：新增用户】独立逻辑
    def create(self, request, *args, **kwargs):
        logger.info('===== 执行 新增用户 逻辑 =====')
        logger.debug(f"新增用户参数：{request.data}")

        ser = self.get_serializer(data=request.data)
        if not ser.is_valid():
            return result_fail(f"参数校验失败：{ser.errors}")
        # 可在这里加新增前置校验
        username = request.data.get("username")
        if SysUser.objects.filter(username=username).exists():
            return result_fail("账号已存在，无法新增")
        
        self.perform_create(ser)
        return result_success(ser.data, "新增用户成功")

    # 3. 【单独：编辑修改】独立逻辑
    def update(self, request, *args, **kwargs):
        logger.info('===== 执行 编辑用户 逻辑 =====')
        logger.debug(f"编辑用户参数：{request.data}")
        instance = self.get_object()
        ser = self.get_serializer(instance, data=request.data)
        if not ser.is_valid():
            return result_fail(f"修改参数错误：{ser.errors}")
        
        # 自定义修改业务判断
        if instance.username == "admin" and request.data.get("username") != "admin":
            return result_fail("管理员账号不允许修改账号名")
        
        self.perform_update(ser)
        return result_success(ser.data, "用户信息修改成功")

    # 4. 【单独：删除用户】独立逻辑
    def destroy(self, request, *args, **kwargs):
        logger.info('===== 执行 删除用户 逻辑 =====')
        logger.debug(f"删除用户参数：{request.data}")
        instance = self.get_object()
        # 禁止删除超级管理员
        if instance.username == "admin":
            return result_fail("禁止删除系统管理员账号")
        
        self.perform_destroy(instance)
        return result_success(msg="删除用户成功")

        
# 登录视图
@api_view(["POST"])
def login_view(request):
    username = request.data.get("username")
    password = request.data.get("password")

    if not username or not password:
        return Response({"code":400,"msg":"账号密码不能为空"}, status=status.HTTP_200_OK)
    
    try:
        user = SysUser.objects.get(username=username)

        if not check_password(password, user.password):
            return Response({"code":400,"msg":"密码错误"}, status=status.HTTP_200_OK)
        if not user.status:
            return Response({"code":400,"msg":"账号已禁用"}, status=status.HTTP_200_OK)
        
        refresh = RefreshToken.for_user(user)
        res_data = {
            "code":200,
            "msg":"登录成功",
            "data":{
                "access":str(refresh.access_token),
                "refresh":str(refresh),
                "userInfo":{"id":user.id,"username":user.username,"nickname":user.nickname}
            }
        }
        return Response(res_data)
    except SysUser.DoesNotExist:
        return Response({"code":400,"msg":"账号不存在"}, status=status.HTTP_200_OK)
    


# 导出
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def export_excel(request):
    users = SysUser.objects.all().values("id", "username", "nickname", "status", "create_time")
    df = pd.DataFrame(list(users))
    if df.empty:
        df = pd.DataFrame(columns=["ID", "登录账号", "用户昵称", "账号状态", "创建时间"])
    else:
        df.columns = ["ID", "登录账号", "用户昵称", "账号状态", "创建时间"]
        df["账号状态"] = df["账号状态"].map({True: "正常启用", False: "禁用停用"})

    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="用户列表", index=False)
    output.seek(0)

    res = HttpResponse(
        output.read(),
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    res["Content-Disposition"] = "attachment; filename=用户列表数据.xlsx"
    return res

# 下载模板
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def down_template(request):
    template_data = [
        {"登录账号": "test001", "用户昵称": "测试用户1"},
        {"登录账号": "test002", "用户昵称": "测试用户2"},
    ]
    df = pd.DataFrame(template_data)
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="导入模板", index=False)
    output.seek(0)

    res = HttpResponse(
        output.read(),
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    res["Content-Disposition"] = "attachment; filename=用户导入模板.xlsx"
    return res

# 导入
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def import_excel(request):
    file = request.FILES.get("file")
    if not file:
        return Response({"code": 400, "msg": "请选择Excel文件上传"})
    if file.size > 5 * 1024 * 1024:
        return Response({"code": 400, "msg": "文件不能超过5MB"})

    try:
        df = pd.read_excel(file)
        if not all(col in df.columns for col in ["登录账号", "用户昵称"]):
            return Response({"code": 400, "msg": "表头格式错误，请下载标准模板"})

        success_num = 0
        error_list = []
        encrypt_pwd = make_password("123456")

        for idx, row in df.iterrows():
            line = idx + 2
            username = str(row.get("登录账号", "")).strip()
            nickname = str(row.get("用户昵称", "")).strip()

            if not username:
                error_list.append(f"第{line}行：账号不能为空")
                continue
            if SysUser.objects.filter(username=username).exists():
                error_list.append(f"第{line}行：账号{username}已存在")
                continue

            SysUser.objects.create(
                username=username,
                nickname=nickname,
                password=encrypt_pwd,
                status=True
            )
            success_num += 1

        return Response({
            "code": 200,
            "msg": f"导入完成！成功{success_num}条，失败{len(error_list)}条",
            "data": error_list
        })
    except Exception as e:
        return Response({"code": 500, "msg": f"导入失败：{str(e)}"})
    
