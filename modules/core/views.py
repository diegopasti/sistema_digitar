from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render
#from modules.core.models import NaturezaJuridica, EconomicActivity
from modules.core.working_api import WorkingApi, WorkingManager
from django.http.response import Http404

#from modules.entity.permissions import EntityPermissions
#from modules.user.models import User, Permissions


@login_required
def index(request):
    return render(request,"base_page.html")


def system_configurations(request):
    return render(request, "core/configurations/backup/configbackup.html")


def access_denied(request):
    return render(request, "error/access_denied.html")


def working(request):
    if request.is_ajax():
        if "unit/frontend/run_test.html" in request.GET['request_page']:
            result = WorkingManager().register_test_front()
            return result
        else:
            return WorkingManager().register_programming_frontend(request.GET['request_page'])
    else:
        raise Http404