# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from modules.entidade.models import entidade
from modules.nucleo.config import ERRORS_MESSAGES, BaseConfiguration
from django.db import models


from modules.user.models import User


class Notification(models.Model):

    class Meta:
        db_table = 'core_notifications'
        unique_together = ("module", "group", "tag", "message", "related_model", "related_object", "related_users")

    module = models.CharField("Módulo:", max_length=50, null=True, error_messages=ERRORS_MESSAGES)
    group  = models.CharField("Grupo:", max_length=50, null=True, error_messages=ERRORS_MESSAGES)
    tag    = models.CharField("Tag:", max_length=50, null=True, error_messages=ERRORS_MESSAGES)
    type   = models.CharField("Tipo:", max_length=50, null=True, error_messages=ERRORS_MESSAGES)
    title  = models.CharField("Titulo:", max_length=100, null=True, error_messages=ERRORS_MESSAGES)
    message = models.CharField("Mensagem:", max_length=500, null=True, error_messages=ERRORS_MESSAGES)
    related_entity = models.ForeignKey(entidade, null=True)
    related_model  = models.CharField("Modelo relacionado:", max_length=50, null=True, error_messages=ERRORS_MESSAGES)
    related_object = models.CharField("Objeto relacionado:", max_length=50, null=True, error_messages=ERRORS_MESSAGES)
    related_users = models.CharField("Lista de Destinatários:", max_length=50, null=True, error_messages=ERRORS_MESSAGES)
    related_users_readed = models.CharField("Usuários que conferiram:", max_length=50, null=True, error_messages=ERRORS_MESSAGES)
    related_user_names = models.CharField("Nome dos Destinatários:", max_length=500, null=True, error_messages=ERRORS_MESSAGES)

    last_view_date = models.DateTimeField(null=True)
    last_view_by = models.ForeignKey(User, null=True, related_name="last_view_by")

    competence = models.CharField("Mês de Competencia:", null=False, max_length=8,default='JAN/2018')
    created_date = models.DateTimeField(auto_now_add=True, null=False)
    status = models.BooleanField("Status da Notificação", default=False)

    def get_related_user_names(self):
        self.related_user_names = ''
        for user_id in self.related_users.split(';'):
            user = User.objects.get(pk=int(user_id))
            self.related_user_names = self.related_user_names+user.get_full_name()+";"

        self.related_user_names = self.related_user_names[:-1]

    def show_details(self):
        print('module:', self.module)
        print('group:', self.group)
        print('tag:', self.tag)
        print('type:', self.type)
        print('title:', self.title)
        print('message:', self.message)
        print('related_model:', self.related_model)
        print('related_object:', self.related_object)
        print('related_users:', self.related_users)
        print('created_date:', self.created_date)


class Backup(models.Model):
    created_date = models.DateTimeField(auto_now=True, null=False)
    backup_file_name = models.CharField("Nome do Arquivo", null=False, blank=False,unique=True, max_length=20, validators=[],error_messages=ERRORS_MESSAGES)
    backup_size = models.PositiveIntegerField("Tamanho do Arquivo", null=False, error_messages=ERRORS_MESSAGES)
    backup_link = models.CharField("Endereço", null=False, blank=False, max_length=100, validators=[], error_messages=ERRORS_MESSAGES)


class BaseOperation(models.Model):

    class Meta:
        db_table = 'core_base_operations'

    opcoes_operacoes = (
        ('ADD', 'ADIÇÃO'), ('ALT', 'ALTERAÇÃO'), ('DEL', 'EXCLUSÃO'), ('DES', 'DESATIVAÇÃO'),('REA','REATIVAR'))

    user = models.ForeignKey(User, null=True)
    type = models.CharField("Tipo:", max_length=3, null=False, choices=opcoes_operacoes, error_messages=ERRORS_MESSAGES)
    table = models.CharField("Tabela:", max_length=50, null=False, error_messages=ERRORS_MESSAGES, default='')
    object_id = models.IntegerField("Id do Registro",null=False)
    object_name = models.CharField("Nome do Registro:", max_length=100, null=False, error_messages=ERRORS_MESSAGES, default='')
    description = models.TextField("Descrição da Operação: ", null=True, blank=True)
    date_operation = models.DateTimeField(auto_now_add=True)


class RestrictedOperation(models.Model):

    class Meta:
        db_table = 'core_restricted_operations'

    opcoes_operacoes = (
        ('ADD', 'ADIÇÃO'), ('ALT', 'ALTERAÇÃO'), ('DEL', 'EXCLUSÃO'), ('DES', 'DESATIVAÇÃO'),('REA','REATIVAR'))

    user = models.ForeignKey(User, null=True)
    type = models.CharField("Tipo:", max_length=3, null=False, choices=opcoes_operacoes, error_messages=ERRORS_MESSAGES)
    table = models.CharField("Tabela:", max_length=50, null=False, error_messages=ERRORS_MESSAGES, default='')
    object_id = models.IntegerField("Id do Registro",null=False)
    object_name = models.CharField("Nome do Registro:", max_length=100, null=False, error_messages=ERRORS_MESSAGES, default='')
    description = models.TextField("Descrição da Operação: ", null=True, blank=True)
    justify = models.TextField("Justificativa: ", null=False, blank=False)
    date_operation = models.DateTimeField(auto_now_add=True)

    def get_type(self, type):
        if type=='ADIÇÃO': return 'ADD'
        elif type=='ALTERAÇÃO': return 'ALT'
        elif type=='EXCLUSÃO': return 'DEL'
        elif type=='DESATIVAR': return 'DES'
        else: return 'OTHER'

    def set_type(self,type):
        if type=='ADIÇÃO': self.type = 'ADD'
        elif type=='ALTERAÇÃO': self.type =  'ALT'
        elif type=='EXCLUSÃO': self.type =  'DEL'
        elif type=='DESATIVAR': self.type =  'DES'
        elif type=='REATIVAR' : self.type = 'REA'
        else: self.type =  'OTHER'

class estados_brasileiros:

    lista_estados = (
        ('AC', 'ACRE'), ('AL', 'ALAGOAS'), ('AM', 'AMAZONAS'),
        ('AP', 'AMAPÁ'), ('BA', 'BAHIA'), ('CE', 'CEARÁ'),
        ('DF', 'DESTRITO FEDERAL'), ('ES', 'ESPIRÍTO SANTO'),
        ('GO', 'GOIÁS'), ('MA', 'MARANHÃO'), ('MG', 'MINAS GERAIS'),
        ('MS', 'MATO GROSSO DO SUL'), ('MT', 'MATO GROSSO'), ('PA', 'PARÁ'),
        ('PB', 'PARAÍBA'), ('PE', 'PERNAMBUCO'),('PI', 'PIAUÍ'),
        ('PR', 'PARANÁ'), ('RJ', 'RIO DE JANEIRO'),('RN', 'RIO GRANDE DO NORTE'),
        ('RO', 'RONDÔNIA'), ('RR', 'RORAIMA'), ('RS', 'RIO GRANDE DO SUL'),
        ('SC', 'SANTA CATARINA'), ('SE', 'SERGIPE'), ('SP', 'SÃO PAULO'), ('TO', 'TOCANTIS'),
    )