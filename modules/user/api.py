# -*- encoding: utf-8 -*-
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator

from libs.default.core import BaseController
from libs.default.decorators import request_ajax_required
from modules.nucleo.models import RestrictedOperation

from modules.nucleo.utils import response_format_error, generate_activation_code, generate_random_password
from modules.nucleo.comunications import send_generate_activation_code, resend_generate_activation_code ,send_reset_password
from modules.user.forms import FormRegister, FormLogin, FormResetPassword, FormUpdateProfile, FormAlterarPassword
from django.contrib.auth.models import Permission, User
from django.http import HttpResponse
import json


class UserController(BaseController):

    @request_ajax_required
    def save_first_register(self,request):
        username = request.POST['username']
        email = request.POST['email'].lower()
        senha = request.POST['password']
        nome = request.POST['first_name'].lower()
        sobrenome = request.POST['last_name'].lower()

        user = User.objects.create_superuser(username, email, senha, first_name=nome, last_name=sobrenome)
        if user is not None:
            # activation_code = generate_activation_code(email)
            # send_generate_activation_code(email, activation_code)
            response_dict = self.notify.success(user, list_fields=['username'])
        else:
            response_dict = self.notify.error({'username': 'Nao foi possivel criar objeto.'})
        return self.response(response_dict)

    @request_ajax_required
    def salvar_registro(self, request):
        return self.signup(request,FormRegister)

    @request_ajax_required
    def login_autentication(self, request):
        return self.login(request, FormLogin)

    @request_ajax_required
    def change_active(self, request):
        user = request.user
        if request.POST['action_type'] == 'DESATIVAR':
            self.disable(request, User)
        else:
            self.enable(request, User)
        try:
            operation = RestrictedOperation()
            operation.user = user
            operation.set_type(request.POST['action_type'])
            operation.object_id = request.POST['id']
            operation.object_name = request.POST['action_object']
            operation.justify = request.POST['action_justify']
            operation.table = User._meta.db_table
            operation.save()
            response_dict = BaseController.notify.success(user,'Consegui')
        except Exception as e:
            response_dict = BaseController.notify.error(e)
        return self.response(response_dict)


    @request_ajax_required
    def upate_user(self,request):
        return self.update(request,FormUpdateProfile)

    @request_ajax_required
    def reset_password(self, request):
        form = FormResetPassword(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email'].lower()
            try:
                user = User.objects.get(email=email)
            except:
                user = None
            if user is not None:
                if user.is_active:
                    new_password = generate_random_password(email)
                    user.set_password(new_password)
                    try:
                        user.save()
                        send_reset_password(new_password, email)
                        response_dict = BaseController.notify.success(user, ['username','email','first_name','last_name'])

                    except Exception as erro:
                        print("Erro! Verifique a excecao: ", erro)
                        response_dict = BaseController.notify.error({'email': 'Falha ao gerar nova senha.'})
                else:
                    response_dict = BaseController.notify.error(
                        {'email': 'Usuário não autorizado!'})
            else:
                response_dict = BaseController.notify.error({'email': 'Usuário não cadastrado.'})
        else:
            response_dict = BaseController.get_exceptions(None, form)
        return self.response(response_dict)

    @request_ajax_required
    def reset_password_old(self, request):
        password = request.POST['password']
        #print("OLHA O PASSWORD Q ESTOU INDO SALVAR:",password)
        try:
            user = User.objects.get(id=request.POST['id'])
            user.set_password(password)
            user.save()
            response_dict = BaseController.notify.success(user, ['username','email','first_name','last_name'])
        except Exception as e:
            print ("EXception e")
            response_dict = BaseController.notify.error(e)
        return self.response(response_dict)

    @request_ajax_required
    def resend_activation_code(self, request):
        form = FormResetPassword(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email'].lower()
            user = User.objects.get_user_email(email)
            if user is not None:
                if not user.account_activated:
                    activation_code = generate_activation_code(email)
                    user.activation_code = activation_code
                    user.save()
                    resend_generate_activation_code(email, activation_code)
                    response_dict = BaseController.notify.success(user,['email'])
                else:
                    response_dict = BaseController.notify.error({'email': 'Conta já atividade.'})
            else:
                response_dict = BaseController.notify.error({'email': 'Email não cadastrado.'})
        else:
            response_dict = BaseController.notify.error({'email': 'Email inválido.'})
        return self.response(response_dict)

    @request_ajax_required
    @method_decorator(login_required)
    def change_password(self, request):
        form = FormAlterarPassword(request.POST)
        if form.is_valid():
            user = request.user
            if user.check_password(form.cleaned_data['old_password']):
                user.change_password(form.cleaned_data['password'])
                auth = User.objects.authenticate(request, email=user.email, password=user.password)
                response_dict = self.notify.success(user, message='Usuário alterado com sucesso.', list_fields=['email'])
            else:
                response_dict = self.notify.error({'email': 'Senha antiga está incorreta.'})
        else:
            response_dict = response_format_error(form.format_validate_response())
            print("VEJA OS ERROS: ",response_dict)
        return self.response(response_dict)



    #@user_passes_test(lambda u: u.permissions.can_view_entity(), login_url='/error/access_denied',redirect_field_name=None)

    def filter_users(request):
        return BaseController().filter(request, User,list_fields=['email','username','is_active','date_joined','first_name','last_name','id','groups'],extra_fields=['get_full_name'])
