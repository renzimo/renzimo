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
import re

from rest_framework import serializers

from .models import Testsuits
from projects.models import Projects
from interfaces.models import Interfaces
from utils import validators


class TestsuitModelSerializer(serializers.ModelSerializer):
    project = serializers.StringRelatedField()
    project_id = serializers.PrimaryKeyRelatedField(queryset=Projects.objects.all())

    class Meta:
        model = Testsuits
        # exclude = ('update_time',)
        fields = "__all__"
        extra_kwargs = {
            'create_time': {
                'read_only': True,
                'format': '%Y年%m月%d日 %H:%M:%S'
            },
            'update_time': {
                'read_only': True,
                'format': '%Y年%m月%d日 %H:%M:%S'
            }
        }

    def validate_include(self, attr):
        attr: dict
        result = re.match(r'^\[\d+(, *\d+)*\]$', attr)
        if result is None:
            raise serializers.ValidationError('include参数格式有误')

        result = result.group()
        try:
            data = eval(result)
        except Exception:
            raise serializers.ValidationError('include参数格式有误')

        for item in data:
            if not Interfaces.objects.filter(id=item).exists():
                raise serializers.ValidationError('接口id不存在')

        return attr

    def to_internal_value(self, data):
        tmp = super().to_internal_value(data)
        tmp['project_id'] = tmp.get('project_id').id
        return tmp


class TestsuitsRunSerializer(serializers.ModelSerializer):
    env_id = serializers.IntegerField(validators=[validators.is_exist_env_id])

    class Meta:
        model = Testsuits
        fields = ('id', 'env_id')
