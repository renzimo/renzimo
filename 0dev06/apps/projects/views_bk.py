import json

from django.http import HttpResponse, JsonResponse, HttpRequest, Http404
from django.views import View
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Projects
from interfaces.models import Interfaces
from . import serializers
from utils.pagination import PageNumberPagination

class OneProject:
    def __init__(self, name, leader):
        self.name = name
        self.leader = leader


class ListMixin:
    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(instance=page, many=True)
            # d.必须调用get_paginated_response方法返回
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(instance=queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# class ProjectViews(View):
# class ProjectViews(APIView):
# 继承GenericAPIView类，是APIView子类
# a.支持APIView的所有功能
# b.支持过滤、排序、分页功能
class ProjectViews(GenericAPIView):
    """
    a.继承GenericAPIView之后，往往需要指定queryset和serializer_class类型
    b.queryset指定当前类视图需要使用的查询集对象
    c.serializer_class指定当前类视图需要使用的序列化器类
    d.self.get_queryset()获取查询集对象
    e.self.get_serializer()获取序列化器类
    f.lookup_field类属性用于指定传递主键参数时，接收的url路径参数名，默认为pk
    g.self.get_object()获取模型对象
    """
    queryset = Projects.objects.all()
    serializer_class = serializers.ProjectModelSerializer
    # filterset_fields = ['id', 'name', 'leader']

    # a.在类视图中指定过滤引擎，优先级高于全局
    # b.search_fields指定对模型类中哪些字段进行过滤
    filter_backends = [SearchFilter, OrderingFilter]
    # c.可以在字段前面添加前缀
    # '^': 'istartswith',
    # '=': 'iexact',
    # '$': 'iregex',
    # 哪些情况下，不会进行过滤？
    # 1.如果全局未指定过滤引擎
    # 2.如果search_fields类属性为空
    # 3.如果前端在搜索时，未指定search查询字符串参数
    search_fields = ['^name', '=leader']

    # a.指定模型类中支持排序的字段名称
    # b.在前端需要使用ordering作为排序的查询字符串参数名称
    # c.前端可以在字段前添加“-”，进行逆序排序，默认为升序
    # d.在前端可以指定多个排序字段，每个排序字段之间使用逗号分隔，如：?ordering=-id,name
    ordering_fields = ['id', 'name', 'leader']
    # ordering_fields = '__all__'
    # d.ordering指定使用默认排序字段
    # ordering = ['name']
    pagination_class = PageNumberPagination

    def get(self, request: Request):
        # qs = Projects.objects.all()
        # name = request.query_params.get('name')
        # if name:
        #     # queryset = self.queryset.filter(name__exact=request.query_params.get('name'))
        #     queryset = self.get_queryset().filter(name__exact=request.query_params.get('name'))

        # a.必须调用self.filter_queryset方法，进行过滤
        # b.需要传递查询集对象作为参数
        queryset = self.filter_queryset(self.get_queryset())

        # a.使用paginate_queryset方法，进行分页操作
        # b.需要接收查询集参数
        # c.如果返回的数据为空，说明不进行分页操作，否则需要进行分页操作
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(instance=page, many=True)
            # d.必须调用get_paginated_response方法返回
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(instance=queryset, many=True)

        # return JsonResponse(serializer.data, safe=False, json_dumps_params={"ensure_ascii": False})

        # a.第一个参数为Python中的常用数据类（字典或者嵌套字典的列表），serializer.data
        # b.status参数用于传递响应状态码
        # c.Response对象.data属性，可以获取返回给前端的数据
        # res = Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request: Request):
        """
        a.继承APIView之后，request为Request对象
        b.可以根据前端请求头中传递的Content-Type，自动解析参数
        c.统一了不同数据之间数据解析方式
        d.前端传递的www-form-urlencoded、application/json、form-data等，可以同时使用request.data属性获取
        e.前端传递的查询字符串参数，GET、query_params
        f.Request对Django中HttpRequest类进行了拓展，兼容HttpRequest类的操作方式
        g.必须返回Response对象，Response拓展了HttpResponse
        :param request:
        :return:
        """
        # err_msg = {
        #     "status": False,
        #     "msg": "参数有误",
        #     "num": 0
        # }
        #
        # try:
        #     json_str = request.body.decode('utf-8')
        #     python_data = json.loads(json_str)
        # except Exception:
        #     # raise Http404
        #     return JsonResponse(err_msg, json_dumps_params={"ensure_ascii": False}, status=400)

        # serializer = serializers.ProjectSerilizer(data=python_data)
        # serializer = serializers.ProjectModelSerializer(data=python_data)
        serializer = self.get_serializer(data=request.data)
        # if not serializer.is_valid():
        #     err = serializer.errors
        #     # return JsonResponse(err, json_dumps_params={"ensure_ascii": False}, status=400)
        #     return Response(err, status=status.HTTP_400_BAD_REQUEST)
        serializer.is_valid(raise_exception=True)
        # 1、创建序列化器对象时，如果仅仅只传data参数
        # 2、序列化器对象调用save方法时，会调用序列化器类中的create方法，进行数据创建操作
        # 3、
        serializer.save(user={'name': '开始', 'age': 18}, score=100)
        # obj = Projects(**serializer.validated_data)
        # obj.save()

        # serializer = serializers.ProjectSerilizer(instance=obj)
        # return JsonResponse(serializer.data, json_dumps_params={"ensure_ascii": False})
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# class ProjectDetailView(View):
class ProjectDetailView(GenericAPIView):
    queryset = Projects.objects.all()
    serializer_class = serializers.ProjectModelSerializer

    # def get_object(self, pk):
    #     try:
    #         # return Projects.objects.get(id=pk)
    #         return self.get_queryset().get(id=pk)
    #     except Exception:
    #         raise Http404

    def get(self, request, pk):
        serializer = self.get_serializer(instance=self.get_object())
        # return JsonResponse(serializer.data, json_dumps_params={"ensure_ascii": False}, status=201)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        serializer = self.get_serializer(instance=self.get_object(), data=request.data)
        # if not serializer.is_valid():
        #     err = serializer.errors
        #     return JsonResponse(err, json_dumps_params={"ensure_ascii": False}, status=400)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # return JsonResponse(serializer.data, json_dumps_params={"ensure_ascii": False}, status=201)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        obj = self.get_object()
        obj.delete()

        # 4、将删除成功的信息返回
        success_msg = {
            "status": True,
            "msg": "删除数据成功",
            "num": 1
        }
        # return JsonResponse(success_msg, json_dumps_params={"ensure_ascii": False}, status=204)
        return Response(success_msg, status=status.HTTP_204_NO_CONTENT)
