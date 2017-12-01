from django import forms

from libs.default.core import BaseForm
from modules.nucleo.config import ERRORS_MESSAGES
from modules.nucleo.forms import FormAbstractPassword, FormAbstractConfirmPassword, FormAbstractEmail, \
    FormAbstractUsername
from modules.user.models import User
from modules.user.validators import password_format_validator


class FormLogin(FormAbstractUsername, FormAbstractPassword,BaseForm):

    def __init__(self, *args, **kwargs):
        super(FormAbstractPassword, self).__init__(*args, **kwargs)
        super(FormAbstractUsername, self).__init__(*args,**kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Usuário..'
        self.fields['password'].widget.attrs['placeholder'] = 'Senha..'


class FormRegister(FormAbstractUsername,FormAbstractPassword,FormAbstractConfirmPassword,FormAbstractEmail,BaseForm):
    model = User

    choices = ((1, 'Gerente'), (2, 'Administrador'), (3, 'Operador'), (4, 'Sem acesso'))
    level_permission = forms.ChoiceField(
        label="Nivel Permissão",
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
    )

    def __init__(self, *args, **kwargs):
        super(FormAbstractUsername, self).__init__(*args,**kwargs)
        super(FormAbstractPassword, self).__init__(*args, **kwargs)
        super(FormAbstractConfirmPassword, self).__init__(*args, **kwargs)
        super(FormAbstractEmail, self).__init__(*args,**kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Nome do usuario'
        self.fields['email'].widget.attrs['placeholder'] = 'Email..'
        self.fields['password'].widget.attrs['placeholder'] = 'Senha..'
        self.fields['confirm_password'].widget.attrs['placeholder'] = 'Repita a Senha..'



    def clean(self):
        form_data = self.cleaned_data
        if len(self.cleaned_data) == len(self.fields):
            if form_data['password'] != form_data['confirm_password']:
                self._errors["password"] = ["Confirme a Senha: Precisa ser igual ao campo Senha"]  # Will raise a error message
                del form_data['password']
        return form_data


class FormConfirmRegister(FormAbstractEmail):

    def __init__(self, *args, **kwargs):
        super(FormAbstractEmail, self).__init__(*args,**kwargs)
        self.fields['email'].widget.input_type = 'hidden'


class FormResetPassword(FormAbstractEmail, BaseForm):

    model = None

    def __init__(self, *args, **kwargs):
        super(FormAbstractEmail, self).__init__(*args,**kwargs)
        self.fields['email'].widget.attrs['placeholder'] = 'Informe seu Email..'


class FormChangePassword(FormAbstractPassword, FormAbstractConfirmPassword):

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

    def __init__(self, *args, **kwargs):
        super(FormAbstractPassword, self).__init__(*args, **kwargs)
        super(FormAbstractConfirmPassword, self).__init__(*args, **kwargs)
        self.fields['password'].label = "Nova Senha"

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