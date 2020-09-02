import json

from rest_framework.views import APIView

from tool.get_workflow_id import GetWorkflowId
from common.api_response import JsonResponse


class ChangeK2TravelWorkflowStatus(APIView):
    def post(self, request):
        print(request.data)
        tenantcode = request.data.get('tenantcode')
        environment = request.data.get('environment')
        title = request.data.get('title')
        businessType = request.data.get('businessType')
        approvalStatus = request.data.get('approvalStatus')
        get_date = GetWorkflowId(tenantcode, environment, title, businessType, approvalStatus)
        resp = {}
        status = get_date.change_k2_travel_status()
        if status[0] == 'success':
            resp['returnMsg'] = "成功"
        else:
            resp['returnMsg'] = '审核出错'
        return JsonResponse(data=status, code=200, msg=resp['returnMsg'], template_name="tool.html")


class ChangeK2SupplierWorkflowStatus(APIView):
    def post(self, request):
        print(request.data)
        tenantcode = request.data.get('tenantcode')
        environment = request.data.get('environment')
        supplier_name = request.data.get('supplier_name')
        businessType = request.data.get('operation')
        approvalStatus = request.data.get('approvalStatus')
        get_date = GetWorkflowId(tenantcode, environment, supplier_name, businessType, approvalStatus)
        resp = {}
        status = get_date.change_supplier_status()
        if status[0] == 'success':
            resp['returnMsg'] = "成功"
        else:
            resp['returnMsg'] = '审核出错'
        return JsonResponse(data=status, code=200, msg=resp['returnMsg'], template_name="tool.html")
