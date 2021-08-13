
from django.db import models


class BaseModel(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='id主键', help_text='id主键')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', help_text='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间', help_text='更新时间')

    class Meta:
        # a.abstract指定当前模型类为抽象模型类
        # b.因为某些模型类，仅仅是将多个模型类中公共的字段抽取出来，而不需要生成数据表
        abstract = True

