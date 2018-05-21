from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponse
from operation.operation_forms import UserAskForm
# Create your views here.


class UserAskView(View):
    """
    用户添加咨询
    """
    def post(self, request):
        """
        HttpResponse中前面一个是字符串类型的，后面是指定格式为json，必需这么写，且字符串中单双引号的关系不能变
        """
        u = UserAskForm(request.POST)
        if u.is_valid():
            u.save()
            return HttpResponse('{"status": "success"}', content_type='application/json')
        else:
            return HttpResponse('{"status": "fail", "msg": "提交失败"}', content_type='application/json')

