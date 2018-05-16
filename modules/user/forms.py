from django import forms

from libs.default.core import BaseForm
from modules.nucleo.config import ERRORS_MESSAGES
from modules.nucleo.forms import FormAbstractPassword, FormAbstractConfirmPassword, FormAbstractEmail, \
    FormAbstractUsername
#from modules.user.models import User
from django.contrib.auth.models import Permission, User , Group

from modules.user.validators import password_format_validator


class FormLogin(FormAbstractUsername, FormAbstractPassword,BaseForm):
    model = User
    def __init__(self, *args, **kwargs):
        super(FormAbstractPassword, self).__init__(*args, **kwargs)
        super(FormAbstractUsername, self).__init__(*args,**kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Usuário..'
        self.fields['password'].widget.attrs['placeholder'] = 'Senha..'


class FormRegister(FormAbstractUsername,FormAbstractPassword,FormAbstractConfirmPassword,FormAbstractEmail,BaseForm):
    model = User
    grupos = [(1, '1 - ADMINISTRADOR'),
              (2, '1 - GERENTE GERAL'),
              (3, '2 - COORDENADOR(A)'),
              (4, '3 - ANALISTA'),
              (5, '3 - AUXILIAR'),
              (6, '3 - ASSISTENTE'),
              (7, '3 - MOTOBOY'),
              ]

    """choices = ((1, 'Gerente'), (2, 'Administrador'), (3, 'Operador'), (4, 'Sem acesso'))
    level_permission = forms.ChoiceField(
        label="Nivel Permissão..",
        choices=choices,
        required=True,
        validators=[],
        error_messages=ERRORS_MESSAGES,
        widget=forms.Select(
            attrs={
                'id': 'level_permission', 'class': "form-control", 'type': "level_permission", 'autocomplete': "off",
                'ng-model': 'level_permission', 'required': "required"
            }
        )
    )"""

    first_name = forms.CharField(
        label="Primeiro Nome..",
        required=True,
        validators=[],
        error_messages=ERRORS_MESSAGES,
        widget=forms.TextInput(
            attrs={
                'id': 'first_name', 'name': 'primeiro_nome', 'class': "form-control uppercase",
                'autocomplete': "off", 'ng-model': 'primeiro_nome', 'required': "required",
            }
        )
    )

    last_name = forms.CharField(
        label="Sobrenome..",
        required=True,
        validators=[],
        error_messages=ERRORS_MESSAGES,
        widget=forms.TextInput(
            attrs={
                'id': 'last_name', 'name': 'sobrenome', 'class': "form-control uppercase",
                'autocomplete': "off", 'ng-model': 'sobrenome', 'required': "required",
            }
        )
    )

    groups = forms.ChoiceField(
        label='Grupo',
        required=True,
        choices=grupos,#[[g.id, g.name] for g in Group.objects.filter()],
        widget=forms.Select(
            attrs={
                'id': 'groups', 'name': 'groups', 'class': "form-control ",
                'autocomplete': "off", 'required': "required",
            }
        )
    )

    def __init__(self, *args, **kwargs):
        super(FormAbstractUsername, self).__init__(*args,**kwargs)
        super(FormAbstractPassword, self).__init__(*args, **kwargs)
        super(FormAbstractConfirmPassword, self).__init__(*args, **kwargs)
        super(FormAbstractEmail, self).__init__(*args,**kwargs)
        #self.fields['username'].widget.attrs['placeholder'] = 'Login..'
        #self.fields['email'].widget.attrs['placeholder'] = 'Email..'
        #self.fields['first_name'].widget.attrs['placeholder'] = 'Primeiro nome..'
        #self.fields['last_name'].widget.attrs['placeholder'] = 'Sobrenome..'
        #self.fields['password'].widget.attrs['placeholder'] = 'Senha..'
        #self.fields['confirm_password'].widget.attrs['placeholder'] = 'Confirmar senha..'


    def clean(self):
        form_data = self.cleaned_data
        if len(self.cleaned_data) == len(self.fields):
            if form_data['password'] != form_data['confirm_password']:
                self._errors["password"] = ["Confirme a Senha: Precisa ser igual ao campo Senha"]  # Will raise a error message
                del form_data['password']
        return form_data

class FormUpdateProfile (BaseForm,FormAbstractUsername,FormAbstractEmail):
    model = User
    grupos = [(1, '1 - ADMINISTRADOR'),
              (2, '1 - GERENTE GERAL'),
              (3, '2 - COORDENADOR(A)'),
              (4, '3 - ANALISTA'),
              (5, '3 - AUXILIAR'),
              (6, '3 - ASSISTENTE'),
              (7, '3 - MOTOBOY'),
              ]


    first_name = forms.CharField(
        label="Primeiro Nome..",
        required=False,
        validators=[],
        error_messages=ERRORS_MESSAGES,
        widget=forms.TextInput(
            attrs={
                'id': 'first_name', 'name': 'update_first_name', 'class': "form-control uppercase",
                'autocomplete': "off", 'ng-model': 'first_name',
                'placeholder':'Nome..'
            }
        )
    )

    last_name = forms.CharField(
        label="Sobrenome..",
        required=False,
        validators=[],
        error_messages=ERRORS_MESSAGES,
        widget=forms.TextInput(
            attrs={
                'id': 'last_name', 'name': 'update_last_name', 'class': "form-control uppercase",
                'autocomplete': "off", 'ng-model': 'sobrenome', 'required': "required",
                'placeholer':'Sobrenome..'
            }
        )
    )

    groups = forms.ChoiceField(
        label='Grupo',
        required=True,
        choices=grupos,
        widget=forms.Select(
            attrs={
                'id': 'groups', 'name': 'groups_update', 'class': "form-control ",
                'autocomplete': "off", 'ng-model': 'groups', 'required': "required",
            }
        )
    )

    def __init__(self,*args,**kwargs):
        super(FormAbstractUsername, self).__init__(*args,**kwargs)
        super(FormAbstractEmail,self).__init__(*args,**kwargs)
        self.fields['username'].required = False
        self.fields['email'].required = False
        set_field_html_name(self.fields['username'], 'username_update')
        set_field_html_name(self.fields['email'],'email_update')
        set_field_html_name(self.fields['last_name'], 'last_name_update')
        set_field_html_name(self.fields['first_name'], 'first_name_update')
        #self.fields['username'].widget.attrs['placeholder'] = 'Username..'
        #self.fields['email'].widget.attrs['placeholder'] = 'Informe seu Email..'

def set_field_html_name(cls, new_name):
    """
    This creates wrapper around the normal widget rendering,
    allowing for a custom field name (new_name).
    """
    old_render = cls.widget.render
    def _widget_render_wrapper(name, value, attrs=None):
        return old_render(new_name, value, attrs)

    cls.widget.render = _widget_render_wrapper

class FormConfirmRegister(FormAbstractEmail):

    def __init__(self, *args, **kwargs):
        super(FormAbstractEmail, self).__init__(*args,**kwargs)
        self.fields['email'].widget.input_type = 'hidden'


class FormResetPassword(FormAbstractEmail, BaseForm):

    model = User

    def __init__(self, *args, **kwargs):
        super(FormAbstractEmail, self).__init__(*args,**kwargs)
        self.fields['email'].widget.attrs['placeholder'] = 'Informe seu Email..'


class FormAlterarPassword(FormAbstractPassword, FormAbstractConfirmPassword, BaseForm):
    '''
    old_password = forms.CharField(
        label="Senha Antiga",
        max_length=50,
        required=True,
        validators=[password_format_validator],
        error_messages=ERRORS_MESSAGES,
        widget=forms.TextInput(
            attrs={
                'id': 'old_password', 'class': "form-control",'type': "password",'autocomplete': "off", 'ng-model': 'old_password',
                'required': "required", 'data-validate-length-range': '8', 'ng-pattern': '(\d+[a-zA-Z]+)|([a-zA-Z]+\d+)'
            }
        )
    )
    '''

    def __init__(self, *args, **kwargs):
        super(FormAbstractPassword, self).__init__(*args, **kwargs)
        super(FormAbstractConfirmPassword, self).__init__(*args, **kwargs)
        self.fields['password'].widget.attrs['placeholder'] = 'Digite Nova Senha..'
        self.fields['confirm_password'].widget.attrs['placeholder'] = 'Confirmar Nova Senha..'

    '''
    def clean(self):
        form_data = self.cleaned_data
        if len(self.cleaned_data) == len(self.fields):
            if form_data['password'] != form_data['confirm_password']:
                self._errors["confirm_password"] = ["Senhas não conferem"]  # Will raise a error message
                del form_data['confirm_password']

            elif form_data['old_password'] == form_data['password']:
                self._errors["password"] = ["Nova senha precisa ser diferente da antiga."]  # Will raise a error message
                del form_data['password']
        return form_data
    
    
    def format_validate_response(self):
        response_errors = {}
        #print("VEJA OS ERROS: ",self.errors.as_data)
        if self.errors:
            errors = self.errors
            for campo in errors:
                response_errors[campo] = []
                for erro in errors[campo]:
                    erro_format = str(erro)
                    erro_format = erro_format.replace("['","")
                    erro_format = erro_format.replace("']", "")
                    response_errors[campo].append(erro_format)
            print(response_errors)
        else:
            print("TEM NADA DE ERRO EU AXO")
        return response_errors
    '''
class FormChangePassword(FormAbstractPassword, FormAbstractConfirmPassword, BaseForm):
    old_password = forms.CharField(
        label="Senha Antiga",
        max_length=50,
        required=True,
        validators=[password_format_validator],
        error_messages=ERRORS_MESSAGES,
        widget=forms.TextInput(
            attrs={
                'id': 'old_password', 'class': "form-control",'type': "password",'autocomplete': "off", 'ng-model': 'old_password',
                'required': "required", 'data-validate-length-range': '8', # 'ng-pattern': '(\d+[a-zA-Z]+)|([a-zA-Z]+\d+)',
            }
        )
    )

    def __init__(self, *args, **kwargs):
        super(FormAbstractPassword, self).__init__(*args, **kwargs)
        super(FormAbstractConfirmPassword, self).__init__(*args, **kwargs)

    def clean(self):
        form_data = self.cleaned_data
        if len(self.cleaned_data) == len(self.fields):
            if form_data['password'] != form_data['confirm_password']:
                self._errors["confirm_password"] = ["Senhas não conferem"]  # Will raise a error message
                del form_data['confirm_password']

            elif form_data['old_password'] == form_data['password']:
                self._errors["password"] = ["Nova senha precisa ser diferente da antiga."]  # Will raise a error message
                del form_data['password']
        return form_data


class FormActivationCode(forms.Form):

    activation_code = forms.CharField(
        label="Código de Ativação",
        max_length=46,
        required=False,
        error_messages=ERRORS_MESSAGES,
        widget=forms.TextInput(
            attrs={
                'id': 'activation_code',
                'class': "form-control",
                'readonly': True,
                'ng-model': 'activation_code',
                'required': "required",
                'data-validate-length-range': '46'
            }
        )
    )

class FromChangePersonalInfo (BaseForm,FormAbstractEmail):
    model = User

    first_name = forms.CharField(
        label="Primeiro Nome",
        required=True,
        validators=[],
        error_messages=ERRORS_MESSAGES,
        widget=forms.TextInput(
            attrs={
                'id': 'first_name', 'name': 'primeiro_nome', 'class': "form-control uppercase",
                'autocomplete': "off", 'ng-model': 'primeiro_nome', 'required': "required",
            }
        )
    )

    last_name = forms.CharField(
        label="Sobrenome",
        required=True,
        validators=[],
        error_messages=ERRORS_MESSAGES,
        widget=forms.TextInput(
            attrs={
                'id': 'last_name', 'name': 'sobrenome', 'class': "form-control uppercase",
                'autocomplete': "off", 'ng-model': 'sobrenome', 'required': "required",
            }
        )
    )

    def __init__(self,*args, **kwargs):
        super(FormAbstractEmail,self).__init__(*args,**kwargs)

