# -*- coding: utf-8 -*-
from rest_framework.views import APIView
from tool.login_token import TokenApp
from common.api_response import JsonResponse
from django.views.decorators.csrf import csrf_exempt



class AutoAppLogin(APIView):
    def post(self, request):
        print(request.data)
        tenantcode = request.data.get('tenantcode')
        environment = request.data.get('environment')
        user = request.data.get('user')
        password = request.data.get('password')
        resp = {}
        get_data = TokenApp(tenantcode, environment, user, password)
        login_status = get_data.login_app_url()
        if login_status[0] == 'success':
            resp['returnMsg'] = login_status[1]
        else:
            resp['returnMsg'] = '账号或密码错误'
        return JsonResponse(data=resp, code=200, msg="请求成功",template_name="tool.html")
