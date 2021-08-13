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

from .models import Reports


class ReportModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reports
        exclude = ('update_time',)
        extra_kwargs = {
            'create_time': {
                'read_only': True,
                'format': '%Y年%m月%d日 %H:%M:%S'
            }
        }

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # item['result'] = "成功" if item.get('result') else "失败"
        data['result'] = "成功" if data.get('result') else "失败"
        return data
