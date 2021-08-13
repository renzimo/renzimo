# -*- coding: utf-8 -*-
"""
-------------------------------------------------
  @Time : 2021/1/14 20:30 
  @Auth : 可优
  @File : urls.py
  @IDE  : PyCharm
  @Motto: ABC(Always Be Coding)
  @Email: keyou100@qq.com
  @Company: 湖南省零檬信息技术有限公司
  @Copyright: 柠檬班
-------------------------------------------------
"""
from rest_framework import routers

from . import views

router = routers.SimpleRouter()
router.register(r'testsuits', views.TestsuitsViewSet)
urlpatterns = [
]

urlpatterns += router.urls
