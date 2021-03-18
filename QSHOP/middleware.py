#-*-coding:utf-8 -*-
"""
@project:QSHOP
@File: middleware.py
@user：liuhuan   
"""


# process_request 请求开始，视图之前
# process_views 请求开始，视图之中
# process_exception 错误
# process_template_response 视图结束，模板开始渲染
# process_response 响应结束


from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponse,JsonResponse


class MiddleWareIp(MiddlewareMixin):

    def process_request(self,request):
        request_ip = request.META["REMOTE_ADDR"]
        print(request_ip)
        # if request_ip == "127.0.0.1":
        #     return HttpResponse("非法IP")


    def process_view(self,request,view_func,view_args,view_kwargs):
        """
        :param request:             请求
        :param view_func:           视图函数
        :param view_args:           视图函数需要的参数，元组类型
        :param view_kwargs:         视图函数需要的参数，字典类型
        :return:
        """
        print(view_func,view_args,view_kwargs,1111111111)

    def process_exception(self,request,exception):
        print(exception)

    def process_template_response(self,request,response):
        """
        :param request:         请求
        :param response:        响应
        :return:
        """
        print("process_template_response")
        print(response)
        return response

    def process_response(self,request,response):
        return response
