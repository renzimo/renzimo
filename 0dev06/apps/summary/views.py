from django.contrib.auth.models import User
from django.db.models import Sum
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions

from projects.models import Projects
from interfaces.models import Interfaces
from testcases.models import Testcases
from configures.models import Configures
from debugtalks.models import DebugTalks
from envs.models import Envs
from testsuits.models import Testsuits
from reports.models import Reports


class SummaryView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user   # type: User
        if user.date_joined:
            date_joined = user.date_joined.strftime('%Y年%m月%d日 %H:%M:%S')
        else:
            date_joined = ''
        if user.last_login:
            last_login = user.last_login.strftime('%Y年%m月%d日 %H:%M:%S')
        else:
            last_login = ''

        executed_testcases_count = Reports.objects.aggregate(testcases_count=Sum('count'))['testcases_count']
        executed_testcases_success = Reports.objects.aggregate(success_count=Sum('success'))['success_count']
        if executed_testcases_count != 0:
            success_rate = int((executed_testcases_success / executed_testcases_count) * 100)
        else:
            success_rate = 100

        fail_rate = 100 - success_rate
        data = {
            "user": {
                "username": user.username,
                "role": "管理员" if user.is_superuser else '普通用户',
                "date_joined": date_joined,
                "last_login": last_login,
            },
            "statistics": {
                "projects_count": Projects.objects.count(),
                "interfaces_count": Interfaces.objects.count(),
                "testcases_count": Testcases.objects.count(),
                "testsuits_count": Testsuits.objects.count(),
                "configures_count": Configures.objects.count(),
                "envs_count": Envs.objects.count(),
                "debug_talks_count": DebugTalks.objects.count(),
                "reports_count": Reports.objects.count(),
                "success_rate": success_rate,
                "fail_rate": fail_rate
            }
        }
        return Response(data, status=200)
