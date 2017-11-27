# -*- encoding: utf-8 -*-
'''
Created on 2 de set de 2015

@author: Diego
'''

from django import forms

MENSAGENS_ERROS={'required': 'Precisa ser Informado!',
                 'invalid' : 'Formato Inválido!'
                }


class adicionar_salario_minimo(forms.Form):
    valor = forms.DecimalField(label="Valor (R$):", max_digits=10, decimal_places=2, required=True,
                       widget=forms.TextInput(attrs={'class': "form-control field_required",'maxlength':'13', 'id': 'salario_valor', 'ng-model':'salario_valor'}))

    inicio_vigencia = forms.DateField(label="Vigência inicia em:", required=True, error_messages=MENSAGENS_ERROS,
                                      widget=forms.DateInput(attrs={'class': "form-control field_required", 'id': 'inicio_vigencia','ng-model': 'inicio_vigencia'},format = '%d/%m/%Y'),
                                            input_formats=('%d/%m/%Y',))


