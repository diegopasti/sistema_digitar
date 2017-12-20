# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from modules.nucleo.config import ERRORS_MESSAGES, BaseConfiguration
from django.db import models


from modules.user.models import User


class Backup(models.Model):
    created_date = models.DateTimeField(auto_now_add=True, null=False)
    backup_file_name = models.CharField("Nome do Arquivo", null=False, blank=False, max_length=100, validators=[],error_messages=ERRORS_MESSAGES)
    backup_size = models.PositiveIntegerField("Tamanho do Arquivo", null=False, error_messages=ERRORS_MESSAGES)
    backup_link = models.CharField("Endereço", null=False, blank=False, max_length=100, validators=[], error_messages=ERRORS_MESSAGES)


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