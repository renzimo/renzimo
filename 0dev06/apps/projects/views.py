import os
from datetime import datetime

from django.db.models import Count
from django.conf import settings
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework import permissions
from rest_framework.response import Response

from .models import Projects
from interfaces.models import Interfaces
from testsuits.models import Testsuits
from testcases.models import Testcases
from envs.models import Envs
from . import serializers
from utils.mixins import NamesMixin
from utils import common


class ProjectViewSet(NamesMixin, viewsets.ModelViewSet):
    """
    list:
    获取项目列表数据

    retrieve:
    获取项目详情数据

    update:
    更新项目数据

    create:
    创建项目

    partial_update:
    更新一条项目的部分数据

    destroy:
    删除一条项目数据

    names:
    获取所有项目的名称

    interfaces:
    获取某一条项目下的所有接口名称
    """
    queryset = Projects.objects.all()
    serializer_class = serializers.ProjectModelSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        # print(1/0)
        response = super().list(request, *args, **kwargs)
        results = response.data['results']
        for item in results:
            item: dict
            interface_testcase_qs = Interfaces.objects.filter(project_id=item.get('id')).values('id').\
                annotate(testcases=Count('testcases'))

            # item['interfaces'] = Interfaces.objects.filter(project_id=item.get('id')).count()
            item['interfaces'] = interface_testcase_qs.count()
            testcase_total = 0
            for i in interface_testcase_qs:
                i: dict
                # testcase_total = testcase_total + i.get('testcases')
                testcase_total += i.get('testcases')
            item['testcases'] = testcase_total

            configure_testcase_qs = Interfaces.objects.filter(project_id=item.get('id')).values('id').annotate(
                configures=Count('configures'))
            configure_total = 0
            for j in configure_testcase_qs:
                j: dict
                configure_total += j.get('configures')
            item['configures'] = configure_total
            # item['testsuites'] = Testsuits.objects.filter(project_id=item.get('id')).count()
            item['testsuits'] = Testsuits.objects.filter(project_id=item.get('id')).count()
            # testsuits
        # response.data['results'] = results
        return response

    @action(detail=True)
    def interfaces(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        response.data = response.data.get('interfaces')
        return response

    @action(methods=['post'], detail=True)
    def run(self, request, *args, **kwargs):
        # 1、取出项目模型对象并获取env_id
        instance = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        env_id = serializer.validated_data.get('env_id')
        env = Envs.objects.get(id=env_id)

        # 2、创建一个以时间戳命名的目录
        testcase_dir_path = os.path.join(settings.SUITES_PATH, datetime.strftime(datetime.now(), "%Y%m%d%H%M%S"))
        os.mkdir(testcase_dir_path)

        # 获取当前项目的接口数据
        interface_qs = Interfaces.objects.filter(project=instance)
        if not interface_qs.exists():
            data = {
                'ret': False,
                'msg': '此项目下没有接口，无法运行！'
            }
            return Response(data, status=400)

        # 获取每一个接口下的用例数据
        need_run_testcases = []
        for interface_obj in interface_qs:
            interface_obj: Interfaces
            testcase_qs = Testcases.objects.filter(interface=interface_obj)
            if not testcase_qs.exists():
                continue
            else:
                need_run_testcases.extend(list(testcase_qs))

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
        if self.action == 'names':
            return serializers.ProjectNamesModelSerializer
        elif self.action == 'interfaces':
            return serializers.InterfacesSerializer
        elif self.action == 'run':
            return serializers.ProjectsRunSerializer
        else:
            return self.serializer_class
