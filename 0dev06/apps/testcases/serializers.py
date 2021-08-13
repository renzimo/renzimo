
from rest_framework import serializers

from .models import Testcases
from interfaces.models import Interfaces
from projects.models import Projects
from utils import validators


class ProjectInterfaceModelSerializer(serializers.ModelSerializer):
    project = serializers.SlugRelatedField(label='所属项目名称', help_text='所属项目名称',
                                           read_only=True, slug_field='name')
    # project_id = serializers.PrimaryKeyRelatedField(label='所属项目名称', help_text='所属项目名称', write_only=True,
    #                                                 queryset=Projects.objects.all())
    pid = serializers.IntegerField(label='所属项目id', help_text='所属项目id', write_only=True, validators=[
        validators.is_exist_project_id])
    iid = serializers.IntegerField(label='所属接口id', help_text='所属接口id', write_only=True, validators=[
        validators.is_exist_interface_id])

    class Meta:
        model = Interfaces
        # fields = ('name', 'project', 'id', 'project_id')
        # fields = ('name', 'project', 'pid', 'iid')
        fields = ('name', 'project', 'pid', 'iid')
        extra_kwargs = {
            'name': {
                'read_only': True,
            }
        }

    def validate(self, attrs: dict):
        pid = attrs.get('pid')
        iid = attrs.get('iid')
        if not Interfaces.objects.filter(id=iid, project_id=pid).exists():
            raise serializers.ValidationError('所属项目id与接口id不匹配')
        return attrs


class TestcasesModelSerializer(serializers.ModelSerializer):
    interface = ProjectInterfaceModelSerializer(label='所属项目和接口信息', help_text='所属项目和接口信息')

    class Meta:
        model = Testcases
        exclude = ('update_time', 'create_time')
        extra_kwargs = {
            'request': {
                'write_only': True,
            },
            'include': {
                'write_only': True,
            }
        }

    def to_internal_value(self, data):
        result = super().to_internal_value(data)
        result['interface_id'] = result.pop('interface').get('iid')
        return result


class TestcaseRunSerializer(serializers.ModelSerializer):
    env_id = serializers.IntegerField(validators=[validators.is_exist_env_id])

    class Meta:
        model = Testcases
        fields = ('id', 'env_id')
