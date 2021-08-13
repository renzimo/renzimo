# -*- coding: utf-8 -*-

import os
import json
from datetime import datetime

import yaml
from httprunner.task import HttpRunner
from rest_framework.response import Response

from testcases.models import Testcases
from debugtalks.models import DebugTalks
from configures.models import Configures
from reports.models import Reports


def generate_testcase_file(instance, env, testcase_dir_path):
    # 获取当前用例所属项目名称、所属接口名称
    instance: Testcases
    interface_name = instance.interface.name
    project_name = instance.interface.project.name

    # 构造以所属项目名称的路径
    testcase_dir_path = os.path.join(testcase_dir_path, project_name)
    if not os.path.exists(testcase_dir_path):
        os.makedirs(testcase_dir_path)
        # 1、创建debugtalk.py
        debugtalk_obj = DebugTalks.objects.filter(project__name=project_name).first()
        with open(os.path.join(testcase_dir_path, 'debugtalk.py'), 'w', encoding='utf-8') as one_file:
            one_file.write(debugtalk_obj.debugtalk)

    # 2、创建以接口命名的路径
    testcase_dir_path = os.path.join(testcase_dir_path, interface_name)
    if not os.path.exists(testcase_dir_path):
        os.makedirs(testcase_dir_path)

    # 3、创建yaml配置文件
    # testcase_list = []
    # config = {
    #     'name': instance.name,
    #     'request': {
    #         'base_url': env.base_url if env.base_url else '',
    #     }
    # }
    # testcase_list.append(config)
    testcase_list = []

    # 获取config
    include = json.loads(instance.include, encoding='utf-8')
    config_id = include.get('config')
    base_url = env.base_url if env.base_url else ''
    if config_id is not None:
        config_obj = Configures.objects.filter(id=config_id).first()
        # if config_obj:
        config_data = json.loads(config_obj.request, encoding='utf-8')
        config_data['config']['request']['base_url'] = base_url
    else:
        config_data = {
            'config': {
                'name': instance.name,
                'request': {
                    'base_url': base_url,
                }
            }
        }

    testcase_list.append(config_data)

    # 获取前置用例id
    testcase_id_list = include.get('testcases')
    if testcase_id_list:
        for testcase_id in testcase_id_list:
            prefix_testcase_obj = Testcases.objects.filter(id=testcase_id).first()
            try:
                testcase_request = json.loads(prefix_testcase_obj.request, encoding='utf-8')
            except Exception:
                continue
            testcase_list.append(testcase_request)

    # 获取当前用例的请求数据
    try:
        current_testcase_request = json.loads(instance.request, encoding='utf-8')
        testcase_list.append(current_testcase_request)
    except Exception:
        pass

    # 将嵌套字典的列表数据转化为yaml配置文件
    testcase_dir_path = os.path.join(testcase_dir_path, instance.name + '.yaml')
    with open(testcase_dir_path, 'w', encoding='utf-8') as file:
        yaml.dump(testcase_list, file, allow_unicode=True)


def create_report(runner: HttpRunner, instance: Testcases):
    """
    创建测试报告
    :param runner:
    :param report_name:
    :return:
    """
    report_name = instance.name

    time_stamp = int(runner.summary["time"]["start_at"])
    start_datetime = datetime.fromtimestamp(time_stamp).strftime('%Y-%m-%d %H:%M:%S')
    runner.summary['time']['start_datetime'] = start_datetime
    # duration保留3位小数
    runner.summary['time']['duration'] = round(runner.summary['time']['duration'], 3)
    report_name = report_name if report_name else start_datetime
    runner.summary['html_report_name'] = report_name

    for item in runner.summary['details']:
        try:
            for record in item['records']:
                record['meta_data']['response']['content'] = record['meta_data']['response']['content']. \
                    decode('utf-8')
                record['meta_data']['response']['cookies'] = dict(record['meta_data']['response']['cookies'])

                request_body = record['meta_data']['request']['body']
                if isinstance(request_body, bytes):
                    record['meta_data']['request']['body'] = request_body.decode('utf-8')
        except Exception as e:
            continue

    summary = json.dumps(runner.summary, ensure_ascii=False)

    report_name = report_name + '_' + datetime.strftime(datetime.now(), '%Y%m%d%H%M%S')
    report_path = runner.gen_html_report(html_report_name=report_name)

    with open(report_path, encoding='utf-8') as stream:
        reports = stream.read()

    test_report = {
        'name': report_name,
        'result': runner.summary.get('success'),
        'success': runner.summary.get('stat').get('successes'),
        'count': runner.summary.get('stat').get('testsRun'),
        'html': reports,
        'summary': summary
    }
    report_obj = Reports.objects.create(**test_report)
    return report_obj.id


def run_testcase(instance, testcase_dir_path):
    runner = HttpRunner()
    try:
        runner.run(testcase_dir_path)
    except Exception:
        return Response({'msg': '用例执行失败'}, status=400)

    # 创建报告
    report_id = create_report(runner, instance)
    # return Response({'id': 1}, status=201)
    return Response({'id': report_id}, status=201)


