# -*- encoding: utf-8 -*-
'''
Created on 2 de set de 2015

@author: Diego
'''

import datetime
from django import forms
from modules.entidade.models import entidade, localizacao_simples, contato, Documento, AtividadeEconomica
from modules.entidade.utilitarios import remover_simbolos

#from preferencias.models import Contrato
from modules.nucleo.models import estados_brasileiros

MENSAGENS_ERROS={'required': 'Precisa ser Informado!',
                 'invalid' : 'Formato Inválido!'
                }



    

class formulario_cadastro_entidade_observacao(forms.Form):
    
    #autor     = models.ForeignKey()
    titulo    = forms.CharField(label="Título: ",max_length=100,required=True,error_messages=MENSAGENS_ERROS,widget=forms.TextInput(attrs={'class':"form-control", 'id':'titulo' }),)
    descricao = forms.CharField(label="Descrição: ",max_length=500,required=True,error_messages=MENSAGENS_ERROS,widget=forms.Textarea(attrs={'class':"form-control", 'id':'descricao' }),)



def get_object_localizacao(argumentos,formulario):
    """if endereco == None:
        print("criando entidade")

    else:
        print("carregando..")
        registro = endereco"""

    registro = localizacao_simples()
    registro.cep=remover_simbolos(formulario['cep'].value())
    registro.numero=str(formulario.cleaned_data['numero_endereco'])
    registro.complemento=formulario.cleaned_data['complemento'].upper()
    registro.logradouro=formulario.cleaned_data['endereco'].upper()
    registro.bairro=formulario.cleaned_data['bairro'].upper()
    registro.codigo_ibge=formulario.cleaned_data['codigo_municipio'].upper()
    registro.municipio=formulario.cleaned_data['municipio'].upper()
    registro.estado=formulario.cleaned_data['estado'].upper()
    registro.pais=formulario.cleaned_data['pais'].upper()

    return registro

def get_object_contatos(argumentos,formulario, registro_entidade):
    contatos = formulario.cleaned_data['contatos']
    contatos = contatos.split("#")
    registros = []
    for item in contatos:
        item = item.replace("undefined","")
        if "|" in item:
            dados = item.split("|")
            registro = contato(
                nome_contato = registro_entidade.nome_razao,
                tipo_contato = dados[1],
                numero = dados[2],#remover_simbolos(),
                cargo_setor = dados[4],
                email = dados[5]
            )
            registros.append(registro)

    return registros

def get_object_cnae(argumentos,formulario):

    atividades = formulario.cleaned_data['atividade_economica']
    registros = []
    #print("olha o que veio do formulario: ",atividades)
    if atividades != "":
        atividades = atividades.split("#")
        for item in atividades:
            item = item.replace("undefined", "")
            dados = item.split("|")
            if "|" in item:
                registro = AtividadeEconomica()
                registro.atividade = dados[1]

                try:
                    registro.desde = datetime.datetime.strptime(dados[2], "%d/%m/%Y").date()
                except:
                    registro.desde = None
                registros.append(registro)
        return registros
    else:
        return []

def get_object_documentos(argumentos,formulario):

    documentos = formulario.cleaned_data['tabela_documentos']
    registros = []

    if documentos != "":
        documentos = documentos.split("#")
        for item in documentos:
            item = item.replace("undefined", "")
            dados = item.split("|")
            if "|" in item:
                registro = Documento()
                print("DOCUMENTOS: ")
                print("     TIPO:",dados[1])
                print("     NOME:", dados[2])
                print("     VENC:", dados[3])
                print("     PASS:", dados[4])

                registro.tipo = dados[1]
                registro.nome = dados[2]

                try:
                    registro.vencimento = datetime.datetime.strptime(dados[3], "%d/%m/%Y").date()
                except:
                    registro.desde = None

                registro.senha = dados[4]

                registros.append(registro)
        return registros
    else:
        return []

def get_object_entidade(argumentos,formulario):
    #if cliente == None:
    #    print("criando entidade")
    registro = entidade()
    #else:
    #    print("carregando..")
    #    registro = cliente

    registro.cpf_cnpj = remover_simbolos(formulario.cleaned_data['cpf_cnpj'])
    registro.nome_razao = formulario.cleaned_data['nome_razao'].upper()
    registro.apelido_fantasia = formulario.cleaned_data['apelido_fantasia'].upper()
    registro.tipo_registro = "C"
    registro.nascimento_fundacao = formulario.cleaned_data['nascimento_fundacao']
    registro.registro_geral      = formulario.cleaned_data['registro_geral']

    registro.inscricao_estadual  = formulario.cleaned_data['inscricao_estadual']
    registro.inscricao_municipal = formulario.cleaned_data['inscricao_municipal']
    registro.inscricao_produtor_rural  = formulario.cleaned_data['inscricao_produtor_rural']
    registro.inscricao_imovel_rural     = formulario.cleaned_data['inscricao_imovel_rural']

    registro.nome_filial     = formulario.cleaned_data['nome_filial'].upper()
    registro.natureza_juridica  = formulario.cleaned_data['natureza_juridica']
    registro.regime_apuracao    = formulario.cleaned_data['regime_apuracao']
    registro.regime_desde       = formulario.cleaned_data['regime_desde']
    registro.tipo_vencimento_iss = formulario.cleaned_data['tipo_vencimento']
    registro.data_vencimento_iss = formulario.cleaned_data['data_vencimento_iss']
    registro.dia_vencimento_iss  = formulario.cleaned_data['dia_vencimento_iss']
    registro.taxa_iss            = formulario.cleaned_data['taxa_iss']

    registro.responsavel_cliente = entidade.objects.get(pk=int(formulario.cleaned_data['responsavel_cliente']))
    registro.supervisor_cliente  = entidade.objects.get(pk=int(formulario.cleaned_data['supervisor_cliente']))

    registro.notificacao_email = formulario.cleaned_data['notificacao_email']
    registro.notificacao_responsavel = formulario.cleaned_data['notificacao_responsavel']
    registro.notificacao_envio = formulario.cleaned_data['notificacao_envio']


    registro.observacoes = formulario.cleaned_data['observacoes']
    return registro

def get_object_contrato(argumentos,formulario):
    """registro = Contrato()

    registro.vigencia_inicio = formulario.cleaned_data['contrato_inicio']
    registro.vigencia_fim = formulario.cleaned_data['contrato_fim']

    registro.tipo_cliente = ""
    registro.tipo_contrato = 0

    registro.taxa_honorario = 0
    registro.valor_honorario = 0
    registro.dia_vencimento = 5

    registro.desconto_temporario = 0
    registro.desconto_inicio = None
    registro.desconto_fim = None

    registro.desconto_indicacoes = None
    registro.cadastrado_por = 1
    registro.alterado_por = 1

    return registro"""



class formulario_cadastro_entidade_completo(forms.Form):
    opcoes_tipos_registros = (

        ('C', 'CLIENTE'),
        ('F', 'FORNECEDOR'),
        ('U', 'FUNCIONÁRIO'),
        ('O', 'OUTRO')
    )

    cpf_cnpj              = forms.CharField(label="Cnpj:",max_length=14,required=True,error_messages=MENSAGENS_ERROS,
                                            widget=forms.TextInput(attrs={'class':"form-control numbersOnly", 'id':'cpf_cnpj'}),
                                            )

    nome_razao            = forms.CharField(label="Razão Social:",max_length=100,required=True,error_messages=MENSAGENS_ERROS,
                                            widget=forms.TextInput(attrs={'class':"form-control uppercase", 'id':'nome_razao'}))
    
    apelido_fantasia      = forms.CharField(label="Nome Fantasia:",max_length=50,required=False,error_messages=MENSAGENS_ERROS,
                                            widget=forms.TextInput(attrs={'class':"form-control uppercase" ,'id':'apelido_fantasia'}))

    tipo_registro         = forms.ChoiceField(label="Tipo Registro:",choices=opcoes_tipos_registros,required=False,error_messages=MENSAGENS_ERROS, #choices=opcoes_tipos_registros, default='C',
                                            widget=forms.Select(attrs={'class':"form-control" ,'id':'tipo_registro'}))
    
    registro_geral        = forms.CharField(label="Inscrição Estadual:",max_length=12,required=False,error_messages=MENSAGENS_ERROS,
                                            widget=forms.TextInput(attrs={'class':"form-control" ,'id':'registro_geral'}))
    
    nascimento_fundacao   = forms.DateField(label="Fundação:",required=False,
                                            widget= forms.DateInput(attrs={'class':"form-control" ,'id':'nascimento_fundacao'},format = '%d/%m/%Y'),
                                            input_formats=('%d/%m/%Y',))
    
    cep          = forms.CharField(label="Código Postal:",max_length=15,required=False,error_messages=MENSAGENS_ERROS,
                                            widget=forms.TextInput(attrs={'class':"form-control" ,'id':'codigo_postal'}))
                                   
    numero_endereco       = forms.CharField(label="Número:",max_length=5,required=False,error_messages=MENSAGENS_ERROS,
                                            widget=forms.TextInput(attrs={'class':"form-control" ,'id':'numero_endereco'}))

    complemento  = forms.CharField(label="Complemento:",max_length=100,required=False,error_messages=MENSAGENS_ERROS,
                                            widget=forms.TextInput(attrs={'class':"form-control uppercase" ,'id':'complemento'}))
    
    endereco    = forms.CharField(label="Endereço:",max_length=100,required=True,error_messages=MENSAGENS_ERROS,
                                  widget=forms.TextInput(attrs={'class':"form-control uppercase" ,'id':'endereco'}))

    bairro      = forms.CharField(label="Bairro:",max_length=100,required=True,error_messages=MENSAGENS_ERROS,
                                  widget=forms.TextInput(attrs={'class':"form-control uppercase" ,'id':'bairro'}))
    
    codigo_municipio = forms.CharField(label="Código Município:",max_length=10,required=False,error_messages=MENSAGENS_ERROS,
                                       widget=forms.TextInput(attrs={'class':"form-control uppercase" ,'id':'codigo_municipio'}))

    municipio = forms.CharField(label="Município:",max_length=100,required=True,error_messages=MENSAGENS_ERROS,
                                       widget=forms.TextInput(attrs={'class':"form-control uppercase" ,'id':'municipio'}))
    
    estado       = forms.ChoiceField(label="Estado:",choices=estados_brasileiros.lista_estados,required=True,error_messages=MENSAGENS_ERROS,
                                         widget=forms.Select(attrs={'class':"form-control uppercase" ,'id':'estado'}))

    pais       = forms.CharField(label="País:",required=True,error_messages=MENSAGENS_ERROS,
                                 widget=forms.TextInput(attrs={'class':"form-control uppercase" ,'id':'pais'})                              )

    """
    numero_contato        = forms.CharField(label="Telefone:",max_length=15,required=False,error_messages=MENSAGENS_ERROS,
                                    widget=forms.TextInput(attrs={'class':"form-control" ,'id':'numero_contato'})
                                    )
    cargo_setor   = forms.CharField(label="Cargo ou Setor:",max_length=50,required=False,error_messages=MENSAGENS_ERROS,
                                    widget=forms.TextInput(attrs={'class':"form-control uppercase" ,'id':'cargo_setor'})
                                    )
    email         = forms.EmailField(label="Email:",max_length=100,required=False,error_messages=MENSAGENS_ERROS,
                                     widget=forms.TextInput(attrs={'class':"form-control lowercase" ,'id':'email'})
                                    )
    """
    contatos = forms.CharField(label="Contatos:",required=True,error_messages=MENSAGENS_ERROS,
                                     widget=forms.TextInput(attrs={'id':'contatos','readonly':True,'type':"hidden"})
                                    )

    """ Tentar utilizar o campo do estado pra definir automaticamente a mascara da inscricao estadual para o estado definido """
    inscricao_estadual = forms.CharField(label="Inscrição Estadual:", max_length=9, required=False, initial="ISENTO",error_messages=MENSAGENS_ERROS,
                                         widget=forms.TextInput(attrs={'class': "form-control", 'id': 'inscricao_estadual'}))

    inscricao_municipal = forms.CharField(label="Inscrição Municipal:", max_length=20, initial="ISENTO",required=False,
                                          error_messages=MENSAGENS_ERROS, widget=forms.TextInput(
                                          attrs={'class': "form-control", 'id': 'inscricao_municipal'})
                                          )

    inscricao_produtor_rural = forms.CharField(label="INCRA:", max_length=20, required=False,
                                       error_messages=MENSAGENS_ERROS, widget=forms.TextInput(
                                       attrs={'class': "form-control", 'id': 'inscricao_produtor_rural'})
                                       )

    inscricao_imovel_rural = forms.CharField(label="NIRF:", max_length=20, required=False,
                                       error_messages=MENSAGENS_ERROS, widget=forms.TextInput(
                                       attrs={'class': "form-control", 'id': 'inscricao_imovel_rural'})
                                       )

    inscricao_junta_comercial = forms.CharField(label="Inscrição em Orgão:", max_length=20, required=False,
                                               error_messages=MENSAGENS_ERROS, widget=forms.TextInput(
            attrs={'class': "form-control", 'id': 'inscricao_junta_comercial'}))

    nome_filial = forms.CharField(label="Identificação de Filial:",max_length=20, required=False,
                                        error_messages=MENSAGENS_ERROS,
                                        widget=forms.TextInput(attrs={'class': "form-control uppercase", 'id': 'nome_filial'}))

    natureza_juridica = forms.CharField(label="Natureza Jurídica:",max_length=100,required=False,error_messages=MENSAGENS_ERROS,
                                    widget=forms.TextInput(attrs={'class':"form-control" ,'id':'natureza_juridica','list':"naturezas_juridicas",'name':"natureza_juridica"})
                                    )

    opcoes_regime = (
        ('SIMPLES_NACIONAL','SIMPLES NACIONAL'),
        ('LUCRO_PRESUMIDO','LUCRO PRESUMIDO'),
        ('LUCRO_REAL','LUCRO REAL'),
		('IMUNE','IMUNE'),
		('ISENTO','ISENTO')
    )

    regime_apuracao = forms.ChoiceField(label="Regime Tributário:", choices=opcoes_regime, required=False,
                                 error_messages=MENSAGENS_ERROS,  # choices=opcoes_tipos_contatos,default='C',)
                                 widget=forms.Select(attrs={'class': "form-control", 'id': 'regime_apuracao'}))

    regime_desde = forms.DateField(label="Desde:", required=False, error_messages=MENSAGENS_ERROS,
                    widget=forms.DateInput(attrs={'class': "form-control", 'id': 'regime_desde'},format='%d/%m/%Y'), input_formats=('%d/%m/%Y',))

    #forms.CharField(label="Desde:", max_length=50, required=False,
    #                                  error_messages=MENSAGENS_ERROS, widget=forms.TextInput(attrs={'class': "form-control", 'id': 'regime_desde'}))



    atividade_economica = forms.CharField(label="Atividade Econômica:",required=False,error_messages=MENSAGENS_ERROS,
                                    widget=forms.TextInput(attrs={'class':"form-control" ,'id':'atividade_economica','readonly':True,'type':"hidden"})
                                    )

    atividade_desde = forms.DateField(label="Desde:", required=False, error_messages=MENSAGENS_ERROS,
                                   widget=forms.DateInput(attrs={'class': "form-control", 'id': 'atividade_desde', "ng-model":"atividade_desde"},
                                                          format='%d/%m/%Y'), input_formats=('%d/%m/%Y',))

    #contribuinte_iss = forms.BooleanField()

    opcoes_tipo_vencimento = (
        ('FIXO', 'FIXO'), ('VARIAVEL', 'VARIAVEL'))

    tipo_vencimento = forms.ChoiceField(label="Modalidade do ISS:", choices=opcoes_tipo_vencimento, required=False,
                                        error_messages=MENSAGENS_ERROS, #default='fixo',  # choices=opcoes_tipos_contatos,,)
                                        widget=forms.Select(attrs={'class': "form-control", 'id': 'tipo_vencimento'}))

    data_vencimento_iss = forms.DateField(label="Vencimento (Anual):",required=False,error_messages=MENSAGENS_ERROS,
                                          widget=forms.TextInput(attrs={'class': "form-control", 'id': 'data_vencimento_iss'}))

    dia_vencimento_iss = forms.IntegerField(label="Vencimento (Mensal):",required=False,error_messages=MENSAGENS_ERROS,
                                          widget=forms.TextInput(attrs={'class': "form-control", 'id': 'dia_vencimento_iss'}))
    taxa_iss = forms.DecimalField("Taxa:",max_digits=5, decimal_places=2,required=False,
                                  widget=forms.TextInput(attrs={'class': "form-control", 'id': 'taxa_iss'}))

    opcoes_responsaveis = (('1', 'MARCELO BORGUINGNON'), ('2', 'DIEGO PASTI'))

    responsavel_cliente = forms.ChoiceField(label="Responsável:", required=False, choices=opcoes_responsaveis,
                                   widget=forms.Select(attrs={
                                       'class': "form-control uppercase",
                                       'id': 'responsavel_cliente'
                                   }))

    supervisor_cliente = forms.ChoiceField(label="Supervisor:", required=False,choices=opcoes_responsaveis,
                                     widget=forms.Select(attrs={
                                         'class': "form-control uppercase",
                                         'id': 'supervisor_cliente'
                                     }))



    opcoes_notificacao_envio = (
        ('N', 'NÃO'), ('S', 'SIM'))

    notificacao_envio = forms.ChoiceField(label="Notificações Automáticas:", choices=opcoes_notificacao_envio, required=False,
                                        error_messages=MENSAGENS_ERROS, #default='fixo',  # choices=opcoes_tipos_contatos,,)
                                        widget=forms.Select(attrs={'class': "form-control", 'id': 'notificacao_envio'}))

    notificacao_email = forms.EmailField(label="Email:",max_length=100,required=False,error_messages=MENSAGENS_ERROS,
                                     widget=forms.TextInput(attrs={'class':"form-control lowercase" ,'id':'notificacao_email','list':"sugestao_email"})
                                    )
    notificacao_responsavel = forms.CharField(label="Nome do Destinatário:",max_length=100,required=False,error_messages=MENSAGENS_ERROS,
                                    widget=forms.TextInput(attrs={'class':"form-control uppercase" ,'id':'notificacao_responsavel','list':"sugestao_responsavel"})
                                    )


    #observacoes = forms("Observações Administrativas", required=False)
    observacoes = forms.CharField(label="Observações Administrativas:", required=False, error_messages=MENSAGENS_ERROS,
                                         widget=forms.Textarea(attrs={'class': 'form-control uppercase', 'id': 'observacoes'}))


    #inscricao_estadual    = forms.BooleanField("Inscrição Estadual:",null=False,default=False,error_messages=MENSAGENS_ERROS)
    #inscricao_municipal   = forms.BooleanField("Inscrição Municipal:",null=False,default=False,error_messages=MENSAGENS_ERROS)
    #inscricao_rural       = forms.BooleanField("Inscrição Rural:",null=False,default=False,error_messages=MENSAGENS_ERROS)
    #data_cadastro         = forms.DateField(auto_now=True)
    #desabilitado          = forms.BooleanField(default=False)    

    #entidade = forms.ForeignKey(entidade)

    tabela_documentos = forms.CharField(label="documentos:", required=False, error_messages=MENSAGENS_ERROS,
                    widget=forms.TextInput(attrs={
                        'id': 'tabela_documentos',
                        'name':'tabela_documentos',
                        'reay':True,
                        'type': "hidden"})) #

    get_localizacao = get_object_localizacao
    get_contatos    = get_object_contatos
    get_cnae        = get_object_cnae
    get_entidade    = get_object_entidade
    get_documentos  = get_object_documentos

    get_contrato    = get_object_contrato

class formulario_justificar_operacao(forms.Form):

    operacao = forms.CharField(
        label="Operação:",
        max_length=3,
        required=True,
        error_messages=MENSAGENS_ERROS,
        widget=forms.TextInput(attrs={'class': "form-control", 'id': 'operacao','readonly': True, 'type': "hidden"
                 }))

    justificativa = forms.CharField(
        label="Justificativa:",
        required=True,
        error_messages=MENSAGENS_ERROS,
        widget=forms.Textarea(attrs={'class': 'form-control uppercase', 'id': 'operacao_justificativa'})
    )

    descricao = forms.CharField(label="Descrição:", required=True, error_messages=MENSAGENS_ERROS,
        widget=forms.TextInput(attrs={'class': 'form-control uppercase', 'id': 'operacao_descricao','readonly': True, 'type': "hidden"}))

    tabela = forms.CharField(label="Tabela:", max_length=50, required=False, error_messages=MENSAGENS_ERROS,
                              widget=forms.TextInput(attrs={'class': "form-control", 'id': 'operacao_tabela','readonly': True, 'type': "hidden"}))

    cliente = forms.CharField(label="Cliente:", max_length=6, required=False, error_messages=MENSAGENS_ERROS,
        widget=forms.TextInput(attrs={'class': "form-control", 'id': 'operacao_cliente', 'readonly': True, 'type': "hidden"})) #, 'readonly': True, 'type': "hidden"

    user = forms.CharField(label="Usuário:", max_length=6, required=False, error_messages=MENSAGENS_ERROS,
                                 widget=forms.TextInput(
                                     attrs={'class': "form-control", 'id': 'operacao_user','readonly': True, 'type': "hidden"}))


