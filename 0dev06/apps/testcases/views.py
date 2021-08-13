import json
import os
from datetime import datetime

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import permissions
from django.conf import settings

from .models import Testcases
from interfaces.models import Interfaces
from testsuits.models import Testsuits
from . import serializers
from utils.mixins import NamesMixin
from utils import handle_data
from utils import common
from envs.models import Envs


class TestcasesViewSet(viewsets.ModelViewSet):
    queryset = Testcases.objects.all()
    serializer_class = serializers.TestcasesModelSerializer
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        testcase_obj = self.get_object()    # type: Testcases

        # 获取用例前置信息（全局配置和前置用例id）
        try:
            testcase_include = json.loads(testcase_obj.include, encoding='utf-8')
        except Exception as e:
            testcase_include = dict()
        testcase_id_list = testcase_include.get('testcases')
        selected_testcase_id = testcase_id_list if testcase_id_list else []

        # 获取当前用例的请求参数
        try:
            testcase_request = json.loads(testcase_obj.request, encoding='utf-8')
        except Exception as e:
            err = {'msg': '用例格式有误', 'status': 0}
            return Response(err, status=400)

        testcase_request_data = testcase_request.get('test').get('request')
        # 解析请求头参数
        testcase_request_header = testcase_request_data.get('headers')
        testcase_request_header = handle_data.handle_data4(testcase_request_header)
        # 解析json参数并转化为json字符串
        testcase_request_json = json.dumps(testcase_request_data.get('json'), ensure_ascii=False)

        # 解析extract参数
        testcase_extract = testcase_request.get('test').get('extract')
        testcase_extract = handle_data.handle_data3(testcase_extract)

        # 解析parameters参数
        testcase_parameter = testcase_request.get('test').get('parameters')
        testcase_parameter = handle_data.handle_data3(testcase_parameter)

        # 解析setupHooks参数
        testcase_setup_hooks = testcase_request.get('test').get('setup_hooks')
        testcase_setup_hooks = handle_data.handle_data5(testcase_setup_hooks)

        # 解析teardown_hooks参数
        testcase_teardown_hooks = testcase_request.get('test').get('teardown_hooks')
        testcase_teardown_hooks = handle_data.handle_data5(testcase_teardown_hooks)

        # 解析validate参数
        testcase_validate = testcase_request.get('test').get('validate')
        testcase_validate = handle_data.handle_data1(testcase_validate)

        testcase_variable = testcase_request.get('test').get('variables')
        testcase_variable = handle_data.handle_data2(testcase_variable)

        data = {
            "author": testcase_obj.author,
            "testcase_name": testcase_obj.name,
            "selected_configure_id": testcase_include.get('config'),
            "selected_interface_id": testcase_obj.interface_id,
            "selected_project_id": testcase_obj.interface.project_id,
            "selected_testcase_id": selected_testcase_id,
            "method": testcase_request_data.get('method') or 'GET',
            "url": testcase_request_data.get('url'),
            "param": handle_data.handle_data4(testcase_request_data.get('params')),
            "header": testcase_request_header,
            # data x-www-form-urlencoded
            "variable": handle_data.handle_data2(testcase_request_data.get('data')),
            # "jsonVariable": "{"username": "haha", "age": 18, "sex": null}",
            "jsonVariable": testcase_request_json,
            "extract": testcase_extract,
            "validate": testcase_validate,
            # config中的variable
            "globalVar": testcase_variable,
            "parameterized": testcase_parameter,
            "setupHooks": testcase_setup_hooks,
            "teardownHooks": testcase_teardown_hooks,
        }

        return Response(data, status=200)

    @action(methods=['post'], detail=True)
    def run(self, request, *args, **kwargs):
        # 1、取出用例模型对象并获取env_id
        instance = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # res = super().create(request, *args, **kwargs)
        # env_id = res.data.get('env_id')
        env_id = serializer.validated_data.get('env_id')
        env = Envs.objects.get(id=env_id)

        # 2、创建一个以时间戳命名的目录
        testcase_dir_path = os.path.join(settings.SUITES_PATH, datetime.strftime(datetime.now(), "%Y%m%d%H%M%S"))
        os.mkdir(testcase_dir_path)

        # 3、创建以项目命名的目录/创建以接口命名的目录/创建yaml用例文件
        common.generate_testcase_file(instance, env, testcase_dir_path)

        # 4、运行用例并生成测试报告
        return common.run_testcase(instance, testcase_dir_path)

    def get_serializer_class(self):
        return serializers.TestcaseRunSerializer if self.action == "run" else self.serializer_class

    def perform_create(self, serializer):
        if self.action == "run":
            return
        else:
            return super().perform_create(serializer)
