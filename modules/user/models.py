from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from modules.nucleo.config import ERRORS_MESSAGES
from django.utils.translation import ugettext_lazy as _


class User(AbstractBaseUser):

    class Meta:
        db_table = 'user'
        verbose_name = _('Usuário')
        verbose_name_plural = _('Usuários')

    user_name         = models.CharField("Nome de Usuário:", max_length=20,unique=True, null=False, error_messages=ERRORS_MESSAGES)
    email             = models.EmailField(_('Email'), max_length=255, error_messages=ERRORS_MESSAGES)#, validators=[email_format_validator, email_dangerous_symbols_validator], error_messages=ERRORS_MESSAGES)
    type_user         = models.CharField("Tipo de Usuário:", max_length=1, null=False, default='1', error_messages=ERRORS_MESSAGES)
    joined_date       = models.DateTimeField(null=True, auto_now_add=True)
    last_update       = models.DateTimeField(null=True, auto_now=True)
    active_user       = models.BooleanField(default=True)
    #group             = models.ForeignKey('GroupPermissions')

    USERNAME_FIELD    = 'user_name'
    REQUIRED_FIELDS   = []



class Session(models.Model):
    class Meta:
        db_table = 'user_session'
        verbose_name = _('Sessão')
        verbose_name_plural = _('Sessões')

    session_key = models.CharField("Chave de Sessão", max_length=32, null=False, error_messages=ERRORS_MESSAGES)

    user = models.ForeignKey('User')
    internal_ip = models.GenericIPAddressField("IP Interno:", null=False, error_messages=ERRORS_MESSAGES)
    external_ip = models.GenericIPAddressField("IP Externo:", null=False, error_messages=ERRORS_MESSAGES)
    country_name = models.CharField("País", max_length=50, null=False, error_messages=ERRORS_MESSAGES)
    country_code = models.CharField("Sigla do País", max_length=2, null=False, error_messages=ERRORS_MESSAGES)
    region_code  = models.CharField("Sigla do Estado", max_length=2, null=False, error_messages=ERRORS_MESSAGES)
    region_name  = models.CharField("Estado", max_length=60, null=False, error_messages=ERRORS_MESSAGES)
    city         = models.CharField("Cidade", max_length=100, null=False, error_messages=ERRORS_MESSAGES)
    zip_code     = models.CharField("Código Postal", max_length=10, null=False, error_messages=ERRORS_MESSAGES)
    time_zone    = models.CharField("Fuzo Horário", max_length=30, null=False, error_messages=ERRORS_MESSAGES)
    latitude     = models.CharField("Latitude", max_length=20, null=False, error_messages=ERRORS_MESSAGES)
    longitude    = models.CharField("Longitude", max_length=20, null=False, error_messages=ERRORS_MESSAGES)

    is_expired   = models.BooleanField("Sessão Expirada", null=False,blank=False, default=False,error_messages=ERRORS_MESSAGES)
    created_date = models.DateTimeField(auto_now_add=True, null=False)
    last_update  = models.DateTimeField(auto_now=True, null=False)


class SessionAction(models.Model):
    class Meta:
        db_table = 'user_session_action'
        verbose_name = _('Atividade de Sessão')
        verbose_name_plural = _('Atividades de Sessões')

    options_types_tasks = (
        (1, "REQUEST PAGE"),
        (2, "REQUEPES SERVICE"),
    )

    request_type    = models.CharField("Tipo da Requisição", max_length=1, null=False, default=2, choices=options_types_tasks, error_messages=ERRORS_MESSAGES)
    request_path    = models.CharField("Requisição", max_length=200, null=False, error_messages=ERRORS_MESSAGES)

    server_process_duration = models.PositiveIntegerField("Tempo de Processamento no Servidor (milisegundos)",null=True, blank=True)
    client_loading_duration = models.PositiveIntegerField("Tempo de Recebimento da Página (milisegundos)",null=True, blank=True)
    client_service_duration = models.PositiveIntegerField("Tempo de Carregamento dos Serviços (milisegundos)",null=True, blank=True)
    client_request_duration = models.PositiveIntegerField("Duração da Requisição (milisegundos)", null=True, blank=True)

    action_date = models.DateTimeField(auto_now_add=True, null=False)

    #SESSION_PARAMTERS['init_load_page'] = ''
    #SESSION_PARAMTERS['load_page_duration'] = ''
    #SESSION_PARAMTERS['setup_page_duration'] = ''