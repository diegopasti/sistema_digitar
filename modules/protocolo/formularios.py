# -*- encoding: utf-8 -*-
'''
Created on 2 de set de 2015

@author: Diego
'''

import datetime

from django import forms

from modules.protocolo.models import documento

MENSAGENS_ERROS={'required': 'Precisa ser Informado!',
                 'invalid' : 'Formato Inválido!'
}


class formulario_adicionar_documento(forms.Form):
    documento      = forms.CharField(label="Documento: ", max_length=100, required=True, error_messages=MENSAGENS_ERROS,
                           widget=forms.TextInput(attrs={'class': 'form-control uppercase','id': 'documento'}))

    descricao = forms.CharField(label="Descrição (Opcional): ",max_length=500,required=False,error_messages=MENSAGENS_ERROS,
                                widget=forms.Textarea(attrs={'class':"form-control", 'id':'descricao' }))


class formulario_gerar_relatorio(forms.Form):
    
    filtrar_por_cliente = forms.CharField(label="Cliente",max_length=100,required=False,error_messages=MENSAGENS_ERROS,widget=forms.TextInput(attrs={'class':'form-control uppercase' ,'id':'filtrar_por_cliente','readonly':True,'type':"hidden" })) #
    
    opcoes_filtro = (                            
        ('TODOS PROTOCOLOS','TODOS PROTOCOLOS'),
        ('ABERTOS','PROTOCOLOS EM ABERTO'),
        ('CONFIRMADOS','PROTOCOLOS CONFIRMADOS'),
    )

    lista_documentos = documento.objects.all()
    filtrar_documentos = forms.ModelMultipleChoiceField(label='Documentos',required=False,queryset=lista_documentos,
        widget=forms.SelectMultiple(attrs={'class': "form-control", 'id': 'filtrar_documentos'})
    )

    filtrar_por_status = forms.ChoiceField(label="Protocolo",choices=opcoes_filtro,required=False,error_messages=MENSAGENS_ERROS, #choices=opcoes_tipos_registros, default='C',
                    widget=forms.Select(attrs={'class':"form-control" ,'id':'filtrar_por_status'})
                    )


    opcoes_operacao = (                            
        ('EMITIDOS','PROTOCOLO EMITIDOS'),
        ('RECEBIDOS','PROTOCOLOS RECEBIDOS'),
    )
    
    filtrar_por_operacao = forms.ChoiceField(label="Operação",choices=opcoes_operacao,required=False,error_messages=MENSAGENS_ERROS, #choices=opcoes_tipos_registros, default='C',
                    widget=forms.Select(attrs={'class':"form-control" ,'id':'filtrar_por_operacao', 'onchange':'selecionar_situacao_protocolo()'})
                    )

    filtrar_desde          = forms.DateField(
                                label="Emitidos desde",required=False,
                                widget= forms.DateInput(attrs={'class':"form-control" ,'id':'filtrar_desde'},format = '%d/%m/%Y'), 
                                input_formats=('%d/%m/%Y',)
                                ) 
    
    filtrar_ate          = forms.DateField(
                                label="Até",initial=datetime.date.today,required=False,
                                widget= forms.DateInput(attrs={'class':"form-control" ,'id':'filtrar_ate'},format = '%d/%m/%Y'), 
                                input_formats=('%d/%m/%Y',)
                                )


class formulario_emitir_protocolo(forms.Form):
    documento = forms.CharField(label="Documento: ", max_length=100, required=True, error_messages=MENSAGENS_ERROS,
                                widget=forms.TextInput(attrs={'class': "form-control uppercase", 'id': 'item', "ng-model":"documento",'':'definir_documento(this)'}), )

    referencia = forms.DateField(label="Referência:", required=False,
                                 widget=forms.DateInput(attrs={'class': "form-control", 'id': 'referencia',"ng-model":"referencia"},
                                                        format='%m/%Y'), input_formats=('%m/%Y',))
    vencimento = forms.DateField(label="Vencimento:", required=False,
                                 widget=forms.DateInput(attrs={'class': "form-control", 'id': 'vencimento', "ng-model":"vencimento"},
                                                        format='%d/%m/%Y'), input_formats=('%d/%m/%Y',))

    valor = forms.CharField(label="Valor (R$): ", required=False,
                            widget=forms.TextInput(attrs={'class': "form-control", 'id': 'valor',"ng-model":"valor"}))

    complemento = forms.CharField(label="Complemento: ", max_length=500, required=False, error_messages=MENSAGENS_ERROS,
                                  widget=forms.TextInput(attrs={'class': "form-control uppercase", 'id': 'complemento',"ng-model":"complemento"}))

    
    
"""class formulario_adicionar_item_protocolo(forms.Form):
    documento       = forms.CharField(label="Documento: ",max_length=100,required=True,error_messages=MENSAGENS_ERROS,widget=forms.TextInput(attrs={'class':"form-control", 'id':'item' }),)
    referencia = forms.DateField(label="Referência:",required=False,
                                            widget= forms.DateInput(attrs={'class':"form-control" ,'id':'referencia'},format = '%m/%Y'), 
                                            input_formats=('%m/%Y',)
                                            )
    vencimento = forms.DateField(label="Vencimento:",required=False,
                                            widget= forms.DateInput(attrs={'class':"form-control" ,'id':'vencimento'},format = '%d/%m/%Y'), 
                                            input_formats=('%d/%m/%Y',)
                                            )
    
    valor = forms.DecimalField(label="Valor (R$): ",max_digits=10, decimal_places=2,required=False,
                               widget = forms.TextInput(attrs={'class':"form-control" ,'id':'valor'}))
    
    complemento = forms.CharField(label="Complemento: ",max_length=500,required=False,error_messages=MENSAGENS_ERROS,widget=forms.TextInput(attrs={'class':"form-control uppercase", 'id':'complemento' }))
    temporarios = []
"""


class formulario_confirmar_entrega(forms.Form):
    protocolo_id = forms.CharField(label="Protocolo: ", max_length=5, required=True, error_messages=MENSAGENS_ERROS,
                                   widget=forms.TextInput(
                                       attrs={'class': 'form-control uppercase', 'id': 'protocolo_id', 'readonly': True,
                                              'type': "hidden"}))  # ,

    data_entrega = forms.DateField(label="Data da Entrega:", initial=datetime.date.today, required=False,
        widget=forms.DateInput(attrs={'class': "form-control", 'id': 'data_entrega'}, format='%d/%m/%Y'),
        input_formats=('%d/%m/%Y',))

    hora_entrega = forms.TimeField(label="Hora da Entrega:", initial=datetime.date.today, required=False,
                                   widget=forms.TimeInput(attrs={'class': "form-control", 'id': 'hora_entrega'}),
                                   # ,format='%H:%M'),
        input_formats=(['%H:%M']))
    # forms.DateField(initial=datetime.date.today,)
    #                                        widget=forms.DateInput(attrs={"class":"form-control"}))
    recebido_por = forms.CharField(label="Recebido por: ", required=True, error_messages=MENSAGENS_ERROS,
                                   widget=forms.TextInput(
                                       attrs={'class': 'form-control uppercase', 'id': 'recebido_por'}))
    doc_receptor = forms.CharField(label="Documento:", required=False, error_messages=MENSAGENS_ERROS,
                                   widget=forms.TextInput(attrs={'class': 'form-control uppercase', 'id': 'documento'}))

    observacao_entrega = forms.CharField(label="Observação:", required=False, error_messages=MENSAGENS_ERROS,
                                         widget=forms.Textarea(
                                             attrs={'class': 'form-control uppercase', 'id': 'observacao_entrega'}))

class formulario_cadastro_entidade_observacao(forms.Form):
    
    #autor     = models.ForeignKey()
    titulo    = forms.CharField(label="Título: ",max_length=100,required=True,error_messages=MENSAGENS_ERROS,widget=forms.TextInput(attrs={'class':"form-control", 'id':'titulo' }),)
    descricao = forms.CharField(label="Descrição: ",max_length=500,required=True,error_messages=MENSAGENS_ERROS,widget=forms.Textarea(attrs={'class':"form-control", 'id':'descricao' }),)

class formulario_cadastro_entidade_completo(forms.Form):
    opcoes_tipos_registros = (
                            
        ('C', 'CLIENTE'),
        ('F', 'FORNECEDOR'),
        ('U', 'FUNCIONÁRIO'),
        ('O', 'OUTRO')
    )
    
    #print "Type: ",type(opco)
    
    cpf_cnpj              = forms.CharField(label="Cpf / Cnpj:",max_length=18,required=True,error_messages=MENSAGENS_ERROS,
                                            widget=forms.TextInput(attrs={'class':"form-control", 'id':'cpf_cnpj' }),
                                            )
    nome_razao            = forms.CharField(label="Nome / Razão Social:",max_length=100,required=True,error_messages=MENSAGENS_ERROS,
                                            widget=forms.TextInput(attrs={'class':"form-control uppercase", 'id':'nome_razao'})
                                            ) 
    
    apelido_fantasia      = forms.CharField(label="Apelido / Nome Fantasia:",max_length=50,required=False,error_messages=MENSAGENS_ERROS,
                                            widget=forms.TextInput(attrs={'class':"form-control uppercase" ,'id':'apelido_fantasia'})
                                            )
    tipo_registro         = forms.ChoiceField(label="Tipo Registro:",choices=opcoes_tipos_registros,required=False,error_messages=MENSAGENS_ERROS, #choices=opcoes_tipos_registros, default='C',
                                            widget=forms.Select(attrs={'class':"form-control" ,'id':'tipo_registro'})
                                            )
    
    registro_geral        = forms.CharField(label="Inscrição Estadual / Identidade:",max_length=12,required=False,error_messages=MENSAGENS_ERROS,
                                            widget=forms.TextInput(attrs={'class':"form-control" ,'id':'registro_geral'})
                                            )
    
    nascimento_fundacao   = forms.DateField(label="Nascimento / Fundação:",required=False,
                                            widget= forms.DateInput(attrs={'class':"form-control" ,'id':'nascimento_fundacao'},format = '%d/%m/%Y'), 
                                            input_formats=('%d/%m/%Y',)
                                            )
    
    cep          = forms.CharField(label="Código Postal:",max_length=15,required=True,error_messages=MENSAGENS_ERROS,
                                            widget=forms.TextInput(attrs={'class':"form-control" ,'id':'codigo_postal'})
                                            )
                                   
    numero_endereco       = forms.CharField(label="Número:",max_length=5,required=False,error_messages=MENSAGENS_ERROS,
                                            widget=forms.TextInput(attrs={'class':"form-control" ,'id':'numero_endereco'})
                                            )
    complemento  = forms.CharField(label="Complemento:",max_length=100,required=False,error_messages=MENSAGENS_ERROS,
                                            widget=forms.TextInput(attrs={'class':"form-control uppercase" ,'id':'complemento'})
                                            )
    
    endereco    = forms.CharField(label="Endereço:",max_length=100,required=True,error_messages=MENSAGENS_ERROS,
                                  widget=forms.TextInput(attrs={'class':"form-control uppercase" ,'id':'endereco'})
                          )
    bairro      = forms.CharField(label="Bairro:",max_length=100,required=True,error_messages=MENSAGENS_ERROS,
                                  widget=forms.TextInput(attrs={'class':"form-control uppercase" ,'id':'bairro'})
                                  )
    
    codigo_municipio = forms.CharField(label="Código Município:",max_length=10,required=True,error_messages=MENSAGENS_ERROS,
                                       widget=forms.TextInput(attrs={'class':"form-control uppercase" ,'id':'codigo_municipio'})
                                  )
    municipio = forms.CharField(label="Município:",max_length=100,required=True,error_messages=MENSAGENS_ERROS,
                                       widget=forms.TextInput(attrs={'class':"form-control uppercase" ,'id':'municipio'})
                                  )
    
    opcoes_estados = (
                            
        ('AC', 'ACRE'),
        ('AL', 'ALAGOAS'),
        ('AM', 'AMAZONAS'),
        ('AP', 'AMAPÁ'),
        ('BA', 'BAHIA'),
        ('CE', 'CEARÁ'),
        ('DF', 'DESTRITO FEDERAL'),
        ('ES', 'ESPIRÍTO SANTO'),
        ('GO', 'GOIÁS'),
        ('MA', 'MARANHÃO'),
        ('MG', 'MINAS GERAIS'),
        ('MS', 'MATO GROSSO DO SUL'),
        ('MT', 'MATO GROSSO'),
        ('PA', 'PARÁ'),
        ('PB', 'PARAÍBA'),
        ('PE', 'PERNAMBUCO'),
        ('PI', 'PIAUÍ'),
        ('PR', 'PARANÁ'),
        ('RJ', 'RIO DE JANEIRO'),
        
        ('RN', 'RIO GRANDE DO NORTE'),
        ('RO', 'RONDÔNIA'),
        ('RR', 'RORAIMA'),
        ('RS', 'RIO GRANDE DO SUL'),
        ('SC', 'SANTA CATARINA'),
        ('SE', 'SERGIPE'),
        ('SP', 'SÃO PAULO'),
        ('TO', 'TOCANTIS'),
        
    )
    
    estado       = forms.ChoiceField(label="Estado:",choices=opcoes_estados,required=True,error_messages=MENSAGENS_ERROS,
                                         widget=forms.Select(attrs={'class':"form-control uppercase" ,'id':'estado'})
                  )

    pais       = forms.CharField(label="País:",required=True,error_messages=MENSAGENS_ERROS,
                                       widget=forms.TextInput(attrs={'class':"form-control uppercase" ,'id':'pais'})
                              )
    
    opcoes_tipos_contatos = (
                            
        ('C', 'CELULAR'),
        ('F', 'COMERCIAL'),
        ('R', 'RESIDENCIAL'),
        ('O', 'OUTROS'),
    )
    
    tipo_contato  = forms.ChoiceField(label="Tipo:",choices=opcoes_tipos_contatos,required=True,error_messages=MENSAGENS_ERROS, # choices=opcoes_tipos_contatos,default='C',)
                                    widget=forms.Select(attrs={'class':"form-control" ,'id':'tipo_contato'})
                                    )
    
    numero_contato        = forms.CharField(label="Telefone:",max_length=15,required=True,error_messages=MENSAGENS_ERROS,
                                    widget=forms.TextInput(attrs={'class':"form-control" ,'id':'numero_contato'})
                                    )
    cargo_setor   = forms.CharField(label="Cargo ou Setor:",max_length=50,required=False,error_messages=MENSAGENS_ERROS,
                                    widget=forms.TextInput(attrs={'class':"form-control uppercase" ,'id':'cargo_setor'})
                                    )
    email         = forms.EmailField(max_length=100,required=False,error_messages=MENSAGENS_ERROS,
                                     widget=forms.TextInput(attrs={'class':"form-control lowercase" ,'id':'email:'})
                                    )
    
    
    """
    1. Administração Pública
    101-5 - Órgão Público do Poder Executivo Federal
    102-3 - Órgão Público do Poder Executivo Estadual ou do Distrito Federal
    103-1 - Órgão Público do Poder Executivo Municipal
    104-0 - Órgão Público do Poder Legislativo Federal
    105-8 - Órgão Público do Poder Legislativo Estadual ou do Distrito Federal
    106-6 - Órgão Público do Poder Legislativo Municipal
    107-4 - Órgão Público do Poder Judiciário Federal
    108-2 - Órgão Público do Poder Judiciário Estadual
    110-4 - Autarquia Federal
    111-2 - Autarquia Estadual ou do Distrito Federal
    112-0 - Autarquia Municipal
    113-9 - Fundação Pública de Direito Público Federal
    114-7 - Fundação Pública de Direito Público Estadual ou do Distrito Federal
    115-5 - Fundação Pública de Direito Público Municipal
    116-3 - Órgão Público Autônomo Federal
    117-1 - Órgão Público Autônomo Estadual ou do Distrito Federal
    118-0 - Órgão Público Autônomo Municipal
    119-8 - Comissão Polinacional
    120-1 - Fundo Público
    121-0 - Consórcio Público de Direito Público (Associação Pública)
    122-8 - Consórcio Público de Direito Privado
    123-6 - Estado ou Distrito Federal
    124-4 - Município
    125-2 - Fundação Pública de Direito Privado Federal
    126-0 - Fundação Pública de Direito Privado Estadual ou do Distrito Federal
    127-9 - Fundação Pública de Direito Privado Municipal
    
    2. Entidades Empresariais
    201-1 - Empresa Pública
    203-8 - Sociedade de Economia Mista
    204-6 - Sociedade Anônima Aberta
    205-4 - Sociedade Anônima Fechada
    206-2 - Sociedade Empresária Limitada
    207-0 - Sociedade Empresária em Nome Coletivo
    208-9 - Sociedade Empresária em Comandita Simples
    209-7 - Sociedade Empresária em Comandita por Ações
    212-7 - Sociedade em Conta de Participação
    213-5 - Empresário (Individual)
    214-3 - Cooperativa
    215-1 - Consórcio de Sociedades
    216-0 - Grupo de Sociedades
    217-8 - Estabelecimento, no Brasil, de Sociedade Estrangeira
    219-4 - Estabelecimento, no Brasil, de Empresa Binacional Argentino-Brasileira
    221-6 - Empresa Domiciliada no Exterior
    222-4 - Clube/Fundo de Investimento
    223-2 - Sociedade Simples Pura
    224-0 - Sociedade Simples Limitada
    225-9 - Sociedade Simples em Nome Coletivo
    226-7 - Sociedade Simples em Comandita Simples
    227-5 - Empresa Binacional
    228-3 - Consórcio de Empregadores
    229-1 - Consórcio Simples
    230-5 - Empresa Individual de Responsabilidade Limitada (de Natureza Empresária)
    231-3 - Empresa Individual de Responsabilidade Limitada (de Natureza Simples)
    
     
    
    3. Entidades sem Fins Lucrativos
    303-4 - Serviço Notarial e Registral (Cartório)
    306-9 - Fundação Privada
    307-7 - Serviço Social Autônomo
    308-5 - Condomínio Edilício
    310-7 - Comissão de Conciliação Prévia
    311-5 - Entidade de Mediação e Arbitragem
    313-1 - Entidade Sindical
    320-4 - Estabelecimento, no Brasil, de Fundação ou Associação Estrangeiras
    321-2 - Fundação ou Associação Domiciliada no Exterior
    322-0 - Organização Religiosa
    323-9 - Comunidade Indígena
    324-7 - Fundo Privado
    325-5 - Órgão de Direção Nacional de Partido Político
    326-3 - Órgão de Direção Regional de Partido Político
    327-1 - Órgão de Direção Local de Partido Político
    328-0 - Comitê Financeiro de Partido Político
    329-8 - Frente Plebiscitária ou Referendária
    330-1 - Organização Social (OS)
    399-9 - Associação Privada
    
    4. Pessoas Físicas
    401-4 - Empresa Individual Imobiliária
    402-2 - Segurado Especial
    408-1 - Contribuinte individual
    409-0 - Candidato a Cargo Político Eletivo
    411-1 - Leiloeiro
    412-0 - Produtor Rural (Pessoa Física)
    
    5.Organizações Internacionais e Outras Instituições Extraterritoriais
    501-0 - Organização Internacional
    502-9 - Representação Diplomática Estrangeira
    503-7 - Outras Instituições Extraterritoriais

    """
    
    
    
    codigo_natureza_juridica = forms.CharField(label="Código:",max_length=50,required=False,error_messages=MENSAGENS_ERROS,
                                    widget=forms.TextInput(attrs={'class':"form-control" ,'id':'codigo_natureza_juridica'})
                                    )
    
    natureza_juridica = forms.CharField(label="Natureza Jurídica:",max_length=50,required=False,error_messages=MENSAGENS_ERROS,
                                    widget=forms.TextInput(attrs={'class':"form-control" ,'id':'natureza_juridica'})
                                    )
    
    codigo_atividade_economica = forms.CharField(label="Código de Atividade:",max_length=50,required=False,error_messages=MENSAGENS_ERROS,
                                    widget=forms.TextInput(attrs={'class':"form-control" ,'id':'codigo_atividade_economica'})
                                    )
    
    atividade_economica = forms.CharField(label="Atividade Econômica:",max_length=50,required=False,error_messages=MENSAGENS_ERROS,
                                    widget=forms.TextInput(attrs={'class':"form-control" ,'id':'atividade_economica'})
                                    )
    
    """ Tentar utilizar o campo do estado pra definir automaticamente a mascara da inscricao estadual para o estado definido """
    inscricao_estadual = forms.CharField(label="Inscrição Estadual:",max_length=50,required=False,initial="ISENTO",error_messages=MENSAGENS_ERROS,
                              widget=forms.TextInput(attrs={'class':"form-control" ,'id':'inscricao_estadual'})
                                    )
    codigo_estado_inscricao = forms.CharField(label="Código do Estado:",max_length=50,required=False,error_messages=MENSAGENS_ERROS,
                                    widget=forms.TextInput(attrs={'class':"form-control" ,'id':'codigo_estado_inscricao'})
                                    )
    
    
    inscricao_municipal = forms.CharField(label="Inscrição Municipal:",max_length=50,required=False,error_messages=MENSAGENS_ERROS,
                                    widget=forms.TextInput(attrs={'class':"form-control" ,'id':'inscricao_municipal'})
                                    )
    
    codigo_municipio_inscricao = forms.CharField(label="Código do Município:",max_length=50,required=False,error_messages=MENSAGENS_ERROS,
                                    widget=forms.TextInput(attrs={'class':"form-control" ,'id':'codigo_municipio_inscricao'})
                                    )

    inscricao_produtor_rural = forms.CharField(label="Inscrição Rural:",max_length=50,required=False,error_messages=MENSAGENS_ERROS,
                                    widget=forms.TextInput(attrs={'class':"form-control" ,'id':'inscricao_produtor_rural'})
                                    )
    
    inscricao_imovel_rural = forms.CharField(label="Inscrição Imóvel Rural:",max_length=50,required=False,error_messages=MENSAGENS_ERROS,
                                    widget=forms.TextInput(attrs={'class':"form-control" ,'id':'inscricao_imovel_rural'})
                                    )
    
    
    
    #inscricao_estadual    = forms.BooleanField("Inscrição Estadual:",null=False,default=False,error_messages=MENSAGENS_ERROS)
    #inscricao_municipal   = forms.BooleanField("Inscrição Municipal:",null=False,default=False,error_messages=MENSAGENS_ERROS)
    #inscricao_rural       = forms.BooleanField("Inscrição Rural:",null=False,default=False,error_messages=MENSAGENS_ERROS)
    #data_cadastro         = forms.DateField(auto_now=True)
    #desabilitado          = forms.BooleanField(default=False)    

    #entidade = forms.ForeignKey(entidade)
