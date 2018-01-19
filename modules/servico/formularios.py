# -*- encoding: utf-8 -*-
'''
Created on 2 de set de 2015

@author: Diego
'''

from django import forms

MENSAGENS_ERROS={'required': 'Precisa ser Informado!',
                 'invalid' : 'Formato Inválido!'
                }


class formulario_adicionar_servico(forms.Form):
    servico      = forms.CharField(label="Serviço: ", max_length=100, required=True, error_messages=MENSAGENS_ERROS,
                           widget=forms.TextInput(attrs={'class': 'form-control uppercase','id': 'modal_servico'}))

    descricao = forms.CharField(label="Descrição (Opcional): ",max_length=500,required=False,error_messages=MENSAGENS_ERROS,
                                widget=forms.Textarea(attrs={'class':"form-control uppercase", 'id':'modal_descricao'}))

class formulario_adicionar_plano(forms.Form):
    plano      = forms.CharField(label="Nome", max_length=100, required=True, error_messages=MENSAGENS_ERROS,
                           widget=forms.TextInput(attrs={'class': 'form-control uppercase','id': 'modal_plano','ng-model':'modal_plano'}))

    descricao = forms.CharField(label="Descrição",max_length=500,required=False,error_messages=MENSAGENS_ERROS,
                                widget=forms.Textarea(attrs={'class':"form-control uppercase", 'id':'modal_descricao','ng-model':'modal_descricao' }))


