# -*- encoding: utf-8 -*-
'''
Created on 1 de abr de 2016

@author: Win7
'''
import datetime

from django.contrib.auth.models import User
from rest_framework import serializers

"""
class parametros_impressao_protocolo():
    
        
    'emissor_nome':emissor.nome_razao,
    'emissor_cpf_cnpj':formatar_cpf_cnpj(emissor.cpf_cnpj),
    'emissor_endereco':"Reta da Penha, Vitoria - ES",
    
    'destinatario_nome':destinatario_nome,
    'destinatario_cpf_cnpj':destinatario_cpf_cnpj,
    'destinatario_endereco':destinatario_endereco,
    'destinatario_complemento':destinatario_complemento,
    #destinatario.endereco_id.complemento
    
    'destinatario_contatos':destinatario_contatos,
    
    
    'codigo_protocolo':codigo_protocolo,
    'emitido_por':'Marcelo',
    
    'recebido_por':recebido_por,
    'identificacao':identidade,
    'data_entrega':data_entrega,
    'hora_entrega':hora_entrega,
    
    
    
    #'emissor':emissor,
    
    #'destinatario':destinatario,
    #'endereco_destinatario':endereco,
    #'contatos_destinatario':contatos,
    
    #'documentos':formulario.temporarios,
    #'documentos':[
    #                  ["33","IMPOSTO DE RENDA","2015","","R$ 285,50"],
    #                  ["8","EMISSAO DE CERTIFICADO DIGITAL","","31/12/2018","R$ 175,10"],
    #                  ["14","CONTRATO - PLANO COMPLETO","","31/12/2018","R$ 475,00"],
    #              ],
    'formulario_protocolo':"Nada por enquanto",
    'erro':"sem erros tambem",
    'path':path,
    
    'path_imagens':path
"""   

from django.db import models

from modules.entidade.formularios import MENSAGENS_ERROS
from modules.entidade.models import entidade

class documento(models.Model):
    nome      = models.CharField("Nome:", max_length=100, unique=True, null=True, error_messages=MENSAGENS_ERROS)
    descricao = models.TextField("Descrição:",max_length=500,null=True,error_messages=MENSAGENS_ERROS)

    def precarregar_dados_digitar(self):
        from modules.nucleo.initial_data import protocolo
        for item in protocolo.referencias_documentos:
            novo_documento = documento()
            novo_documento.nome = item

    def __str__(self):
        return self.nome



class protocolo(models.Model):
    emissor      = models.ForeignKey(User,related_name='entidade_emissora')
    emitido_por  = models.CharField("Emitido por:",max_length=100,null=True,error_messages=MENSAGENS_ERROS)
    destinatario = models.ForeignKey(entidade,null=True,related_name='entidade_destinatario')
    data_emissao = models.DateField(auto_now_add=True)
    hora_emissao = models.TimeField(auto_now_add=True)
    numeracao_destinatario = models.CharField(max_length=6,null=True)
    
    nome_avulso      = models.CharField(max_length=100,null=True,blank=True)
    endereco_avulso  = models.CharField(max_length=500,null=True,blank=True)
    documento_avulso = models.CharField(max_length=30,null=True,blank=True)
    contatos_avulso  = models.CharField(max_length=50,null=True,blank=True)
    
    data_recebimento = models.DateField(null=True,blank=True)
    hora_recebimento = models.TimeField(null=True,blank=True)
    recebido_por     = models.CharField("Recebido por:",max_length=100,null=True,blank=True,error_messages=MENSAGENS_ERROS)
    doc_receptor     = models.CharField("Identidade:",max_length=20,null=True,blank=True,error_messages=MENSAGENS_ERROS)
    situacao         = models.BooleanField(default=False)


    index = 0

    def calculate_index(self):
        protocolo.index = protocolo.index + 1
        return protocolo.index

    def calcular_dias_atraso(self):
        data_atual = datetime.date.today()
        resultado = data_atual - self.data_emissao
        #print("VEJA O RESULTADO: ", resultado.days)
        return resultado.days

     
    
class item_protocolo(models.Model):    
    protocolo      = models.ForeignKey(protocolo)
    documento      = models.CharField("Item:",max_length=100,null=False,error_messages=MENSAGENS_ERROS)
    referencia     = models.CharField("Mês de Referência:",max_length=100,null=True,error_messages=MENSAGENS_ERROS)
    vencimento     = models.CharField("Vencimento:",max_length=100,null=True,error_messages=MENSAGENS_ERROS)
    valor          = models.CharField("Valor:",max_length=10,null=True,default=0,error_messages=MENSAGENS_ERROS)
    complemento    = models.TextField("Complemento:",max_length=500,null=True,error_messages=MENSAGENS_ERROS)


    
class item_protocolo_serializer(serializers.Serializer):
    #protocolo      = models.ForeignKey(protocolo)
    documento      = serializers.CharField(max_length=100) #models.CharField("Item:",max_length=100,null=False,error_messages=MENSAGENS_ERROS)
    #referencia     = models.CharField("Mês de Referência:",max_length=100,null=False,error_messages=MENSAGENS_ERROS)
    #vencimento     = models.CharField("Vencimento:",max_length=100,null=False,error_messages=MENSAGENS_ERROS)
    #valor          = models.CharField("Valor:",max_length=100,null=False,error_messages=MENSAGENS_ERROS)
    #complemento
    
    """
    logradouro   = serializers.CharField(max_length=100)
    bairro       = serializers.CharField(max_length=100)
    municipio    = serializers.CharField(max_length=100)
    estado       = serializers.CharField(max_length=100)
    pais         = serializers.CharField(max_length=100)
    codigo_municipio = serializers.CharField(max_length=7)
    codigo_bairro = serializers.CharField(max_length=10)
    """
