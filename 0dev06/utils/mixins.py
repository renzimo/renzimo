# -*- coding: utf-8 -*-

from rest_framework.decorators import action


class NamesMixin:

    @action(methods=['get'], detail=False)
    def names(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def filter_queryset(self, queryset):
        if self.action == 'names':
            return self.queryset
        else:
            return super().filter_queryset(queryset)

    def paginate_queryset(self, queryset):
        if self.action == 'names':
            return None
        else:
            return super().paginate_queryset(queryset)
