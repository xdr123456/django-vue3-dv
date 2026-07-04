from django.http import HttpResponse

class HandleOptionsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 所有OPTIONS请求直接200放行
        if request.method == "OPTIONS":
            resp = HttpResponse(status=200)
            resp["Access-Control-Allow-Origin"] = "*"
            resp["Access-Control-Allow-Methods"] = "GET,POST,PUT,DELETE,OPTIONS"
            resp["Access-Control-Allow-Headers"] = "*"
            resp["Access-Control-Max-Age"] = "86400"
            return resp
        response = self.get_response(request)
        return response