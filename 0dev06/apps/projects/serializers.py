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
from rest_framework.validators import UniqueValidator

from .models import Projects
from interfaces.models import Interfaces
from debugtalks.models import DebugTalks
from utils import validators


class ProjectModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Projects
        exclude = ('update_time', )
        extra_kwargs = {
            'create_time': {
                'read_only': True,
                'format': '%Y年%m月%d日 %H:%M:%S'
            }
        }

    def create(self, validated_data):
        """

        :param validated_data:
        :return:
        """
        instance = super().create(validated_data)
        DebugTalks.objects.create(project=instance)
        return instance


class ProjectNamesModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projects
        fields = ('id', 'name')


class InterfacesNamesModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interfaces
        fields = ('id', 'name')


class InterfacesSerializer(serializers.ModelSerializer):
    interfaces = InterfacesNamesModelSerializer(label='项目所属接口信息',
                                                help_text='项目所属接口信息',
                                                many=True, read_only=True)

    class Meta:
        model = Projects
        fields = ('interfaces', )


class ProjectsRunSerializer(serializers.ModelSerializer):
    env_id = serializers.IntegerField(validators=[validators.is_exist_env_id])

    class Meta:
        model = Projects
        fields = ('id', 'env_id')
