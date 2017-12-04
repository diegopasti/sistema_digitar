# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from modules.nucleo.config import ERRORS_MESSAGES, BaseConfiguration
from django.db import models

# Create your models here.
class Backup(models.Model):
    created_date = models.DateTimeField(auto_now_add=True, null=False)
    backup_file_name = models.CharField("Nome do Arquivo", null=False, blank=False, max_length=100, validators=[],error_messages=ERRORS_MESSAGES)
    backup_size = models.PositiveIntegerField("Tamanho do Arquivo", null=False, error_messages=ERRORS_MESSAGES)
    backup_link = models.CharField("Endereço", null=False, blank=False, max_length=100, validators=[], error_messages=ERRORS_MESSAGES)


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