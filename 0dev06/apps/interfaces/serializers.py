# -*- coding: utf-8 -*-
"""
-------------------------------------------------
  @Time : 2021/1/26 20:18 
  @Auth : 可优
  @File : serializers.py
  @IDE  : PyCharm
  @Motto: ABC(Always Be Coding)
  @Email: keyou100@qq.com
  @Company: 湖南省零檬信息技术有限公司
  @Copyright: 柠檬班
-------------------------------------------------
"""
from rest_framework import serializers

from .models import Interfaces
from projects.models import Projects
from configures.models import Configures
from testcases.models import Testcases
from utils import validators


class InterfaceModelSerializer(serializers.ModelSerializer):
    project = serializers.StringRelatedField()
    project_id = serializers.PrimaryKeyRelatedField(queryset=Projects.objects.all())

    class Meta:
        model = Interfaces
        exclude = ('update_time',)
        extra_kwargs = {
            'create_time': {
                'read_only': True,
                'format': '%Y年%m月%d日 %H:%M:%S'
            }
        }

    def to_internal_value(self, data):
        tmp = super().to_internal_value(data)
        tmp['project_id'] = tmp.get('project_id').id
        return tmp


class ConfiguresNamesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Configures
        fields = ('id', 'name')


class ConfiguresSerializer(serializers.ModelSerializer):
    configures = ConfiguresNamesSerializer(label='接口所属配置信息',
                                           help_text='接口所属配置信息',
                                           many=True, read_only=True)

    class Meta:
        model = Interfaces
        fields = ('configures',)


class TestcasesNamesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testcases
        fields = ('id', 'name')


class TestcasesSerializer(serializers.ModelSerializer):
    testcases = TestcasesNamesSerializer(label='接口所属用例信息',
                                         help_text='接口所属用例信息',
                                         many=True, read_only=True)

    class Meta:
        model = Interfaces
        fields = ('testcases',)


class InterfacesRunSerializer(serializers.ModelSerializer):
    env_id = serializers.IntegerField(validators=[validators.is_exist_env_id])

    class Meta:
        model = Interfaces
        fields = ('id', 'env_id')
