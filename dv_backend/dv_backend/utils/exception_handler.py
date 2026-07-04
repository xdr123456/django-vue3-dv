from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

def custom_exception_handler(exc, context):
    # 先调用DRF默认异常处理
    response = exception_handler(exc, context)

    # 1. JWT令牌相关异常 401
    if isinstance(exc, (InvalidToken, TokenError)):
        return Response({
            "code": 401,
            "msg": "登录令牌无效或已过期，请重新登录",
            "data": None
        }, status=status.HTTP_200_OK)

    # 2. 未登录无权限 401
    if response and response.status_code == 401:
        return Response({
            "code": 401,
            "msg": "请先登录",
            "data": None
        }, status=status.HTTP_200_OK)

    # 3. 权限不足 403
    if response and response.status_code == 403:
        return Response({
            "code": 403,
            "msg": "权限不足，禁止访问",
            "data": None
        }, status=status.HTTP_200_OK)

    # 4. 接口不存在 404
    if response and response.status_code == 404:
        return Response({
            "code": 404,
            "msg": "请求接口不存在",
            "data": None
        }, status=status.HTTP_200_OK)

    # 5. 参数错误 400
    if response and response.status_code == 400:
        return Response({
            "code": 400,
            "msg": "请求参数错误",
            "data": response.data
        }, status=status.HTTP_200_OK)

    # 6. 服务器未知异常 500
    if response is None:
        return Response({
            "code": 500,
            "msg": "服务器内部错误",
            "data": str(exc)
        }, status=status.HTTP_200_OK)

    return response