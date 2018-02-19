# -*- encoding: utf-8 -*-
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from libs.default.decorators import request_ajax_required, permission_level_required
from django.utils.decorators import method_decorator
from libs.default.core import BaseController

from modules.nucleo.models import RestrictedOperation
from modules.nucleo.utils import response_format_error, generate_activation_code, generate_random_password, response_format_success
from modules.nucleo.comunications import send_generate_activation_code, resend_generate_activation_code ,send_reset_password
from modules.user.forms import FormRegister, FormLogin, FormResetPassword, FormUpdateProfile, FormAlterarPassword, FormChangePassword, FromChangePersonalInfo
from django.contrib.auth.models import Permission, User, Group
from django.http import HttpResponse, HttpResponseForbidden
import json


def criar_grupos_permissao():
    '''
    Função que cria os grupos iniciais
    '''
    lista = Group.objects.filter()
    try:
        if len(lista) == 0 :
            print('Vou criar')
            Group.objects.get_or_create(name='ADMINISTRADOR')
            Group.objects.get_or_create(name='SUPERVISOR')
            Group.objects.get_or_create(name='OPERADOR')
    except:
        print("Deu erro no filter")
        pass
    return


class UserController(BaseController):

    @request_ajax_required
    def save_first_register(self,request):
        criar_grupos_permissao()
        username = request.POST['username']
        email = request.POST['email'].lower()
        senha = request.POST['password']
        nome = request.POST['first_name'].lower()
        sobrenome = request.POST['last_name'].lower()
        try:
            user = User.objects.create_superuser(username, email, senha, first_name=nome, last_name=sobrenome)
            grupo = Group.objects.get(name='Administrador')
            grupo.user_set.add(user)
        except Exception as ex:
            user = None
            print("Olha a exeption;",ex)
        if user is not None:
            # activation_code = generate_activation_code(email)
            # send_generate_activation_code(email, activation_code)
            response_dict = self.notify.success(user, list_fields=['username'])
        else:
            response_dict = self.notify.error({'username':'Não foi possivel criar o usuario'})
        return self.response(response_dict)

    @request_ajax_required
    @method_decorator(permission_level_required(2, raise_exception=HttpResponseForbidden()))
    def salvar_registro(self, request):
        return self.signup(request,FormRegister)

    @request_ajax_required
    def login_autentication(self, request):
        return self.login(request, FormLogin)

    @request_ajax_required
    @method_decorator(permission_level_required(2, raise_exception=HttpResponseForbidden()))
    def change_active(self, request):
        if request.POST['action_type'] == 'DESATIVAR':
            return self.disable(request, User)
        else:
            return self.enable(request, User)

    @method_decorator(login_required)
    @request_ajax_required
    @method_decorator(permission_level_required(2, raise_exception=HttpResponseForbidden()))
    def upate_user(self,request):
        self.start_process(request)
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
                        send_reset_password(new_password, email, user.username)
                        response_dict = BaseController.notify.success(user, ['username','email','first_name','last_name'])

                    except Exception as erro:
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
        print("Olha o POST:",request.POST)
        form = FormChangePassword(request.POST)
        if form.is_valid():
            print("Passou o form é valido:")#,form)
            user = request.user
            if user.check_password(form.cleaned_data['old_password']):
                try:
                    print("entrando pra torcar pois:\n",form.cleaned_data['old_password'])
                    user.set_password(form.cleaned_data['password'])
                    #auth = User.objects.authenticate(request, email=user.email, password=user.password)
                    user.save()
                    response_dict = self.notify.success(user, message='Usuário alterado com sucesso.', list_fields=['email'])
                except:
                    pass
            else:
                response_dict = response_format_error({'password':'Senha antiga está incorreta'})#response_format_error('Senha antiga está incorreta.')#self.notify.error({'email': 'Senha antiga está incorreta.'})
                print("é Nao é a mesma senha")
        else:
            print("Formulario com erros")
            response_dict = response_format_error(form.format_validate_response())
            print("VEJA OS ERROS: ",response_dict)
        return self.response(response_dict)

    @request_ajax_required
    def change_personal_info(self, request):
        email = request.POST['email']
        nome = request.POST['first_name']
        sobrenome = request.POST['last_name']
        try:
            user = User.objects.get(username=request.user)
            user.email = email
            user.last_name = sobrenome
            user.first_name = nome
            user.save()
            response_dict = response_format_success(user,['username'])
        except:
            response_dict = response_format_error('Não foi possivel aterar')
        return HttpResponse(json.dumps(response_dict))


    #@user_passes_test(lambda u: u.permissions.can_view_entity(), login_url='/error/access_denied',redirect_field_name=None)
    @method_decorator(login_required)
    @method_decorator(permission_level_required(3, raise_exception=HttpResponseForbidden()))
    def filter_users(self, request):
        return BaseController().filter(request, User,list_fields=['email','username','is_active','date_joined','first_name','last_name','id','groups','last_login'],extra_fields=['get_full_name'],order_by='id')