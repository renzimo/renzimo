# -*- coding: utf-8 -*-

from rest_framework.pagination import PageNumberPagination as _PageNumberPagination


class PageNumberPagination(_PageNumberPagination):
    # 指定默认每一页显示的数据条数
    page_size = 3
    # 前端用于指定页号的查询字符串参数名称
    page_query_param = 'page'
    # 指定前端用于指定页号的查询字符串参数的描述
    page_query_description = '获取的页码'
    # page_size_query_param = "page_size"
    # 前端用于指定每一页的数据条数，查询字符串参数名称
    # 只要设置了page_size_query_param，那么前端就支持指定获取每一页的数据条数
    page_size_query_param = "size"
    # 前端用于指定每一页的数据条数，查询字符串参数的描述
    page_size_query_description = '每一页数据条数'
    max_page_size = 100

    def get_paginated_response(self, data):
        response = super().get_paginated_response(data)
        response.data['current_page_num'] = self.page.number
        response.data['total_pages'] = self.page.paginator.num_pages
        return response


