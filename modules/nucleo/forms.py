from django import forms
from modules.nucleo.config import ERRORS_MESSAGES
from modules.user.validators import email_dangerous_symbols_validator, password_format_validator, email_format_validator


class FormAbstractEmail(forms.Form):

    email = forms.EmailField(
        label="Email",
        max_length=256,
        required=True,
        validators=[email_format_validator, email_dangerous_symbols_validator],
        error_messages=ERRORS_MESSAGES,
        widget=forms.TextInput(
            attrs={
                'type': "text", 'class': "form-control text-lowercase", 'id': 'email','name':'email',
                'ng-model': 'email', 'autocomplete': "off", 'placeholder': "",'required': "true"
            }
        )
    )

class FormAbstractUsername (forms.Form):
    username = forms.CharField(
        label='Usuário',
        max_length=150,
        required=True,
        validators=[],
        error_messages=ERRORS_MESSAGES,
        widget=forms.TextInput(
            attrs={
                'id':'username','name':'username','class':'form-control', 'autocomplete':'off',
                'required':'required'
            }
        )
    )


class FormAbstractPassword(forms.Form):
    password = forms.CharField(
        label="Senha",
        max_length=50,
        required=True,
        validators=[password_format_validator],
        error_messages=ERRORS_MESSAGES,
        widget=forms.TextInput(
            attrs={
                'id': 'password','name': 'password', 'class': "form-control ", 'type': "password",
                'autocomplete': "off", 'ng-model': 'password','required': "required",
                'data-validate-length-range': '8',
            }
        )
    )


class FormAbstractConfirmPassword(forms.Form):
    confirm_password = forms.CharField(
        label="Confirme a Senha",
        max_length=50,
        required=True, validators=[password_format_validator],
        error_messages=ERRORS_MESSAGES,
        widget=forms.TextInput(
            attrs={
                'id': 'confirm_password','name':'confirm_password', 'class': "form-control", 'type': "password",
                'autocomplete': "off",'ng-model': 'confirm_password','required': "required",
                'data-validate-length-range': '8', 'pattern': '(\d+[a-zA-Z]+)|([a-zA-Z]+\d+)','data-validate-linked':'password'
            }
        )
    )