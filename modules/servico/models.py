# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from modules.entidade.models import entidade

from modules.entidade.formularios import MENSAGENS_ERROS


class Servico(models.Model):
    nome      = models.CharField("Nome:", max_length=100, null=True, error_messages=MENSAGENS_ERROS)
    descricao = models.TextField("Descrição:",max_length=500,null=True,error_messages=MENSAGENS_ERROS)

class Plano(models.Model):
    nome             = models.CharField("Nome:", max_length=100, null=True, error_messages=MENSAGENS_ERROS)
    descricao        = models.TextField("Descrição:", max_length=500, null=True, error_messages=MENSAGENS_ERROS)
    servicos         = models.CharField("Serviços:", max_length=500, null=True, error_messages=MENSAGENS_ERROS)
    cadastrado_por   = models.ForeignKey(User, related_name="plano_cadastrado_por", default=0)
    data_cadastro    = models.DateTimeField(auto_now_add=True)
    ultima_alteracao = models.DateTimeField(null=True, auto_now=True)
    alterado_por     = models.ForeignKey(User, related_name="plano_alterado_por", default=0)
    ativo            = models.BooleanField(default=True)

    def __str__(self):
        return self.nome

