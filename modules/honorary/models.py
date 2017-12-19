# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

import datetime
from decimal import Decimal

from django.contrib.auth.models import User
from django.db import models
from modules.entidade.models import entidade

from modules.entidade.formularios import MENSAGENS_ERROS
from modules.servico.models import Plano


class Contrato(models.Model):
    plano = models.ForeignKey(Plano, default=1)

    cliente = models.ForeignKey(entidade, default=1)
    opcoes_tipos_clientes = (('PF', 'PESSOA FISICA'), ('PJ', 'PESSOA JURIDICA'),)
    tipo_cliente  = models.CharField("Tipo do Cliente:",max_length=2,null=False,default='PJ',choices = opcoes_tipos_clientes,error_messages=MENSAGENS_ERROS)

    vigencia_inicio = models.DateField(null=True)
    vigencia_fim    = models.DateField(null=True)

    taxa_honorario  = models.DecimalField("Honorário:", max_digits=5, decimal_places=2, null=True,blank=False)
    valor_honorario = models.DecimalField("Valor:", max_digits=6, decimal_places=2, null=True,blank=False)
    valor_total = models.DecimalField("Total:", max_digits=8, decimal_places=2, null=True, blank=False)
    dia_vencimento  = models.CharField("Dia do Vencimento",null=True,default=5,max_length=2)
    data_vencimento = models.DateField("Data de Vencimento",null=True)

    desconto_temporario = models.DecimalField("Desconto Temporário:", max_digits=5,default=0, decimal_places=2, null=True,blank=True)
    desconto_temporario_ativo  = models.DecimalField("Desconto Temporário Ativo:", max_digits=5,default=0, decimal_places=2, null=True,blank=True)
    desconto_inicio = models.DateField(null=True)
    desconto_fim    = models.DateField(null=True)

    desconto_indicacoes = models.DecimalField("Desconto por Indicações:", max_digits=5, decimal_places=2, default=0, null=True,blank=True)
    servicos_contratados = models.CharField("Serviços:",null=True,max_length=100)
    cadastrado_por = models.ForeignKey(entidade,  related_name = "cadastrado_por",default=1)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    ultima_alteracao = models.DateTimeField(null=True, auto_now=True)
    alterado_por = models.ForeignKey(entidade, related_name = "alterado_por",default=1)
    ativo = models.BooleanField(default=True)

    def serialize(self):
        serialized_values = {}

    def totalizar_honorario(self):
        desconto_temporario = self.calcular_desconto_temporario()
        desconto_fidelidade = self.calcular_desconto_fidelidade()
        self.desconto_temporario_ativo = desconto_temporario
        self.desconto_indicacoes = desconto_fidelidade
        desconto_total = Decimal(desconto_temporario)/100 + Decimal(desconto_fidelidade)/100
        self.valor_total = Decimal(self.valor_honorario)*(1-desconto_total)
        self.save()
        #print('HONORARIO: ',self.valor_honorario,' - DESC.TEMP.:',desconto_temporario,' - DESC.FID.:',desconto_fidelidade,' - DESC.TOTAL: ',desconto_total,' - TOTAL: ',self.valor_total)


    def calcular_desconto_temporario(self):
        if self.desconto_temporario is not None:
            if self.verificar_validade_desconto_temporario(self.desconto_inicio,self.desconto_fim):
                desconto = self.desconto_temporario
                return Decimal(desconto)
        return Decimal(0)

    def verificar_validade_desconto_temporario(self,inicio=None,termino=None):
        current_date = datetime.datetime.now().date()
        if inicio is not None:
            if current_date < inicio:
                return False

        if termino is not None:
            if current_date > termino:
                return False
        return True

    def calcular_desconto_fidelidade(self):
        indicacoes = Indicacao.objects.filter(cliente=self.cliente).filter(indicacao_ativa=True)
        print("VEJA QUANTAS INDICACOES ATIVAS TEMOS: ",indicacoes)
        if len(indicacoes) == 0:
            return Decimal(0)
        else:
            desconto = Decimal(0)
            for item in indicacoes:
                print(item.indicacao.nome_razao,item.indicacao.ativo,item.taxa_desconto)
                if item.indicacao.ativo:
                    desconto = desconto + item.taxa_desconto
            return desconto


class Indicacao (models.Model):
    cliente = models.ForeignKey(entidade, related_name = "cliente")
    indicacao = models.ForeignKey(entidade,related_name = "indicacao")
    taxa_desconto = models.DecimalField("Taxa Desconto",max_digits=5, decimal_places=2, default=0)
    indicacao_ativa = models.BooleanField(default=True)
    cadastrado_por = models.ForeignKey(entidade, related_name="indicacao_cadastrado_por", default=1)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    ultima_alteracao = models.DateTimeField(null=True, auto_now=True)
    alterado_por = models.ForeignKey(entidade, related_name="indicacao_alterado_por", default=1)


class Proventos(models.Model):
    class Meta:
        db_table = 'honorary_provents'
        verbose_name = "Provento e Desconto"
        verbose_name_plural = "Proventos e Descontos"
    opcoes_tipos_provento = (('P', 'PROVENTO'), ('D', 'DESCONTO'), ('R', 'RESSARCIMENTO'))
    tipo = models.CharField("Tipo do Provento:", max_length=1, null=False, default='P', choices=opcoes_tipos_provento, error_messages=MENSAGENS_ERROS)
    nome = models.CharField("Nome:", max_length=100, null=False, error_messages=MENSAGENS_ERROS)
    descricao = models.CharField("Descrição:", max_length=500, null=True,blank=True, error_messages=MENSAGENS_ERROS)

    opcoes_tipos_valor = (('R', 'REAIS'), ('P', 'PERCENTUAL'))
    tipo_valor = models.CharField("Tipo do Valor:", max_length=1, null=False, default='R', choices=opcoes_tipos_valor, error_messages=MENSAGENS_ERROS)
    valor = models.DecimalField("Valor:", max_digits=7, decimal_places=2, null=True, blank=False)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    cadastrado_por = models.ForeignKey(entidade, related_name='provento_cadastrado_por',  default=1)
    ultima_alteracao = models.DateTimeField(null=True, auto_now=True)
    alterado_por = models.ForeignKey(entidade, related_name='provento_alterado_por', default=1)

    is_active = models.BooleanField(default=True)


class Honorary(models.Model):
    class Meta:
        db_table = 'honorary'
        verbose_name = "Honorário"
        verbose_name_plural = "Honorários"

    cliente = models.CharField("Cliente:", null=False, max_length=100)
    competence = models.CharField("Mês de Competencia:",null=False,max_length=8)
    contract = models.ForeignKey(Contrato, default=1, related_name='contrato')
    initial_value_contract = models.DecimalField("Valor base do contrato", max_digits=8, default=0, decimal_places=2, null=True, blank=False)
    temporary_discount = models.DecimalField("Desconto temporário", max_digits=5,default=0, decimal_places=2, null=False,blank=False)
    fidelity_discount = models.DecimalField("Desconto fidelidade", max_digits=5,default=0, decimal_places=2, null=False,blank=False)
    contract_discount = models.DecimalField("Desconto total em contrato", max_digits=5,default=0, decimal_places=2, null=False,blank=False)
    final_value_contract = models.DecimalField("Valor final do contrato", max_digits=8, decimal_places=2, null=True, blank=False)
    number_debit_credit = models.IntegerField("Total de débitos e créditos")
    total_debit =  models.DecimalField("Total à debitar", max_digits=5,default=0, decimal_places=2, null=False,blank=False)
    total_credit = models.DecimalField("Valor total à creditar", max_digits=5, default=0, decimal_places=2, null=False, blank=False)
    total_debit_credit = models.DecimalField("Valor total à creditar", max_digits=5, default=0, decimal_places=2, null=False, blank=False)
    total_honorary = models.DecimalField("Honorário", max_digits=8, default=0, decimal_places=2, null=False, blank=False)

    is_closed = models.BooleanField("Honorário Encerrado",default=False)
    closed_date = models.DateTimeField("Honorário encerrado em",auto_now_add=True)
    closed_by = models.ForeignKey(User, related_name = "finalizado_por",default=1)
    last_update = models.DateTimeField("Ultima atualização", null=True, auto_now=True)
    updated_by  = models.ForeignKey(User, related_name = "atualizado_por",default=1)
    updated_by_name = models.CharField("Atualizado por:", null=False, max_length=100)
    is_received = models.BooleanField("Honorário recebido",default=False)
    received_by = models.ForeignKey(User, related_name="recebido_por", default=1)


class HonoraryItem(models.Model):
    class Meta:
        db_table = 'honorary_item'
        verbose_name = "Item do Honorário"
        verbose_name_plural = "Items do Honorário"

    opcoes_tipos_item = (('P', 'PROVENTO'), ('D', 'DESCONTO'), ('R', 'RESSARCIMENTO'))
    type_item = models.CharField("Tipo do Provento:", max_length=1, null=False, default='P', choices=opcoes_tipos_item, error_messages=MENSAGENS_ERROS)
    honorary = models.ForeignKey(Honorary, default=1)
    item = models.ForeignKey(Proventos, default=1)
    quantity = models.IntegerField("Total de débitos e créditos")
    unit_value = models.DecimalField("Valor final do contrato", max_digits=6, decimal_places=2, null=True, blank=False)
    total_value = models.DecimalField("Valor final do contrato", max_digits=8, decimal_places=2, null=True, blank=False)
