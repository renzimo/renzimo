import os
import json
from datetime import datetime

from django.conf import settings
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import Testsuits
from envs.models import Envs
from interfaces.models import Interfaces
from testcases.models import Testcases
from . import serializers
from utils import common


class TestsuitsViewSet(viewsets.ModelViewSet):

    queryset = Testsuits.objects.all()
    serializer_class = serializers.TestsuitModelSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(methods=['post'], detail=True)
    def run(self, request, *args, **kwargs):
        # 1、取出套件模型对象并获取env_id
        instance = self.get_object()  # type: Testsuits

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        env_id = serializer.validated_data.get('env_id')
        env = Envs.objects.get(id=env_id)

        # 2、创建一个以时间戳命名的目录
        testcase_dir_path = os.path.join(settings.SUITES_PATH, datetime.strftime(datetime.now(), "%Y%m%d%H%M%S"))
        os.mkdir(testcase_dir_path)

        # 获取当前套件中的用例
        try:
            interface_id_list = json.loads(instance.include, encoding='utf-8')
        except Exception as e:
            data = {
                'ret': False,
                'msg': '此套件下的include参数有误！'
            }
            return Response(data, status=400)

        if len(interface_id_list) == 0:
            data = {
                'ret': False,
                'msg': '此套件下没有接口！'
            }
            return Response(data, status=400)

        need_run_testcases = []
        for interface_id in interface_id_list:
            testcase_qs = Testcases.objects.filter(interface_id=interface_id)
            need_run_testcases.extend(list(testcase_qs))
        # 获取当前接口下的用例数据
        # need_run_testcases = list(instance.testcases.all())

        if len(need_run_testcases) == 0:
            data = {
                'ret': False,
                'msg': '此套件下没有用例，无法运行！'
            }
            return Response(data, status=400)

        for testcase_obj in need_run_testcases:
            # 3、创建以项目命名的目录/创建以接口命名的目录/创建yaml用例文件
            common.generate_testcase_file(testcase_obj, env, testcase_dir_path)

        # 4、运行用例并生成测试报告
        return common.run_testcase(instance, testcase_dir_path)

    def get_serializer_class(self):
        return serializers.TestsuitsRunSerializer if self.action == 'run' else self.serializer_class
