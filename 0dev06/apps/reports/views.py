import os
import json

from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import permissions
from django.http import StreamingHttpResponse
from django.conf import settings

from .models import Reports
from . import serializers
from .utils import get_file_content


class ReportsViewSet(mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.DestroyModelMixin,
                     viewsets.GenericViewSet):

    queryset = Reports.objects.all()
    serializer_class = serializers.ReportModelSerializer
    permission_classes = [permissions.IsAuthenticated]

    # def list(self, request, *args, **kwargs):
    #     response = super().list(request, *args, **kwargs)
    #
    #     for item in response.data.get('results'):
    #         item: dict
    #         # if item.get('result'):
    #         #     item['result'] = "Pass"
    #         # else:
    #         #     item['result'] = "Fail"
    #         item['result'] = "成功" if item.get('result') else "失败"
    #
    #     return response

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        try:
            response.data['summary'] = json.loads(response.data.get('summary'), encoding='utf-8')
        except Exception as e:
            pass
        return response

    @action(detail=True)
    def download(self, request, *args, **kwargs):
        # 1、从数据库中获取报告html源码
        instance = self.get_object()    # type: Reports

        # 2、将源码写入到html文件
        full_report_path = os.path.join(settings.REPORT_PATH, instance.name + '.html')
        if not os.path.exists(full_report_path):
            with open(full_report_path, 'w') as file:
                file.write(instance.html)

        # 3、读取html文件流，将其返回给前端
        # instance.html
        # byte_data = instance.html.encode('utf-8')
        # response = StreamingHttpResponse(iter(byte_data))
        # response = StreamingHttpResponse(iter(instance.html))
        response = StreamingHttpResponse(get_file_content(full_report_path))

        # 需要添加相关响应头参数，浏览器才会当做文件来下载
        # Content-Type: application/octet-stream
        # 可以类似字典的方式，添加响应头参数
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = f"attachment; filename*=UTF-8''{instance.name + '.html'}"
        return response
