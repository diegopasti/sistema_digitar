from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.utils.translation import ugettext_lazy as _
from modules.nucleo.validators import is_empty, contain_alpha, contain_numbers, contain_minimal_size


email_format_validator = EmailValidator(message="Erro! Email inválido.")


def check_email_format(email):
    from django.core.validators import validate_email
    from django.core.exceptions import ValidationError
    try:
        validate_email(email) and email_dangerous_symbols_validator(email)
        return True
    except ValidationError:
        return False


def email_dangerous_symbols_validator(value):
    if '+' in value:
        raise ValidationError(_("Email can not contain the '+' character"), code='security')


def password_format_validator(value):
    if is_empty(value) or not contain_minimal_size(value,8) or not contain_alpha(value) or not contain_numbers(value):
        raise ValidationError(_('Password must be 8 characters or more with numbers and letters'),code='invalid')