from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from libs.default.decorators import request_get_required
from modules.user.forms import FormRegister

@login_required
def register_page(request):
    form_register = FormRegister()
    return render(request, "user/register/register.html", {'formulario_register': form_register})