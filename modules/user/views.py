from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from libs.default.decorators import request_get_required
from modules.nucleo.utils import check_valid_activation_code
from modules.user.forms import FormRegister, FormLogin, FormChangePassword, FormResetPassword, FormActivationCode, FormConfirmRegister
from django.contrib.auth import logout, login
from modules.user.models import Session
from django.contrib.auth.models import Permission, User
from modules.user.validators import check_email_format

def register_first_user(request):
    form_register = FormRegister()
    return render(request, "user/register/register.html", {'formulario_register': form_register})


def login_page(request):
    form = FormLogin()
    return render(request, "user/login.html", {'formulario_login': form})


def logout_page(request):
    user = request.user
    #if not user.close_session(request):
    #   print("Erro! Sessão de usuário não foi encerrada corretamente.")
    logout(request)
    return redirect("/login")


def reset_password_page(request):
    form = FormResetPassword()
    return render(request, "user/reset_password.html", {'formulario_send': form})


def register_confirm_page(request, email):
    form = FormConfirmRegister()
    if check_email_format(email):
        user = User.objects.get_user_email(email)
        if user is None:
            return render(request, "user/register/register_error_unexist_user.html", {'formulary_confirm_register': form, 'email': email})
        else:
            return render(request, "user/register/register_confirm.html", {'formulary_confirm_register': form, 'email': email})
    else:
        return render(request, "user/register/register_error_invalid_email.html", {'formulary_confirm_register': form, 'email': email})


def profile_page(request):
    form_change_password = FormChangePassword()
    return render(request, "user/profile.html", {'form_change_password':form_change_password})


def activate_user(request, email, activation_code):
    activation_form = FormActivationCode({'activation_code': activation_code})
    if activation_form.is_valid():
        user = User.objects.get_user_email(email)
        if user is not None:
            if not user.account_activated:
                if check_valid_activation_code(email, activation_code):
                    if user.activation_code == activation_code:
                        user.account_activated = True
                        user.save()
                        login(request, user)
                        return redirect("/system/environment")
                    else:
                        # Activation code has been replaced with a new code as requested
                        return render(request, "user/register/register_error_activation_code.html", {'email': email})
                else:
                    # Activation code was invalid.
                    return render(request, "user/register/register_error_activation_code.html", {'email': email})
            else:
                # Activation code was used.
                return render(request, "user/register/register_error_activated_user.html", {'email': email})
        else:
            # User not exists.
            return render(request, "user/register/register_error_unexist_user.html", {'email': email})
    else:
        # Activation code was invalid.
        return render(request, "user/register/register_error_activation_code.html", {'email': email})

def user_administration (request):
    form_register = FormRegister()
    return render(request, "user/administration/user_administration.html",{'formulario_register': form_register})

def user_page (request):
    form_register = FormRegister()
    return render(request, "user/cadastro_usuario.html",{'formulario_register': form_register})