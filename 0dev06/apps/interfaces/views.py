import os
from datetime import datetime

from django.conf import settings
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework import permissions

from .models import Interfaces
from testcases.models import Testcases
from configures.models import Configures
from . import serializers
from utils import common
from envs.models import Envs


class InterfacesViewSet(viewsets.ModelViewSet):

    queryset = Interfaces.objects.all()
    serializer_class = serializers.InterfaceModelSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        results = response.data['results']
        for item in results:
            item: dict
            # 获取用例总数
            item['testcases'] = Testcases.objects.filter(interface_id=item.get('id')).count()
            # 获取配置总数
            item['configures'] = Configures.objects.filter(interface_id=item.get('id')).count()
        return response

    @action(detail=True)
    def testcases(self, request, *args, **kwargs):
        """"""
        response = super().retrieve(request, *args, **kwargs)
        response.data = response.data.get('testcases')
        return response

    @action(detail=True, url_path='configs')
    def configures(self, reuqest, *args, **kwargs):
        response = super().retrieve(reuqest, *args, **kwargs)
        response.data = response.data.get('configures')
        return response

    @action(methods=['post'], detail=True)
    def run(self, request, *args, **kwargs):
        # 1、取出接口模型对象并获取env_id
        instance = self.get_object()  # type: Interfaces

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        env_id = serializer.validated_data.get('env_id')
        env = Envs.objects.get(id=env_id)

        # 2、创建一个以时间戳命名的目录
        testcase_dir_path = os.path.join(settings.SUITES_PATH, datetime.strftime(datetime.now(), "%Y%m%d%H%M%S"))
        os.mkdir(testcase_dir_path)

        # 获取当前接口下的用例数据
        need_run_testcases = list(instance.testcases.all())

        if len(need_run_testcases) == 0:
            data = {
                'ret': False,
                'msg': '此项目下没有用例，无法运行！'
            }
            return Response(data, status=400)

        for testcase_obj in need_run_testcases:
            # 3、创建以项目命名的目录/创建以接口命名的目录/创建yaml用例文件
            common.generate_testcase_file(testcase_obj, env, testcase_dir_path)

        # 4、运行用例并生成测试报告
        return common.run_testcase(instance, testcase_dir_path)

    def get_serializer_class(self):
        if self.action == "testcases":
            return serializers.TestcasesSerializer
        elif self.action == "configures":
            return serializers.ConfiguresSerializer
        elif self.action == "run":
            return serializers.InterfacesRunSerializer
        else:
            return self.serializer_class


