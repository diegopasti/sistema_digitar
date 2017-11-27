# -*- encoding: utf-8 -*-s
from __future__ import unicode_literals

from django.db import models

MENSAGENS_ERROS={'required': 'Campo Obrigatório!',
                 'invalid' : 'Formato Inválido!'
                }

class SalarioMinimo(models.Model):
    valor            = models.DecimalField("Valor:",max_digits=10, decimal_places=2, null=False, default=0,error_messages=MENSAGENS_ERROS)
    inicio_vigencia  = models.DateField("Início da vigência:",default="2017-01-01" ,null=False, blank=False)
    data_cadastro    = models.DateTimeField(null=False, auto_now_add=True)
    ultima_alteracao = models.DateTimeField(null=False, auto_now=True)
