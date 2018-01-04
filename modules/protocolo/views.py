# -*- encoding: utf-8 -*-
'''
Created on 1 de abr de 2016

@author: Win7
'''

import datetime
import json, os
from datetime import date
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.http.response import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.template.context import RequestContext
from modules.entidade.models import entidade, contato, localizacao_simples  # , localizacao

from modules.entidade.views import verificar_erros_formulario
from modules.protocolo.formularios import formulario_emitir_protocolo, formulario_confirmar_entrega, formulario_gerar_relatorio, formulario_adicionar_documento
from modules.protocolo.models import protocolo, item_protocolo, documento
from modules.protocolo.report import report_protocols_per_documents
from sistema_contabil.settings import BASE_DIR


#from sistema_contabil.settings import BASE_DIR, STATIC_URL
#from endereco.models import localizacao

def cadastro_documentos(request):
    erro = False
    documentos = documento.objects.all()
    formulario = formulario_adicionar_documento()

    if (request.method == "POST"):
        formulario = formulario_adicionar_documento(request.POST)

        if 'adicionar_documento' in request.POST:

            if formulario.is_valid():
                doc = documento()
                doc.nome = formulario['documento'].value().upper()
                doc.descricao = formulario['descricao'].value()
                doc.save()
                formulario = formulario_adicionar_documento()
                messages.add_message(request, messages.SUCCESS, "Inclusão Realizada com sucesso!")

            else:
                messages.add_message(request, messages.SUCCESS, "Erro! Inclusão não pode ser realizada!")
                erro = True

        elif 'alterar_documento' in request.POST:
            id_documento = int(request.POST['alterar_documento'])
            doc = documento.objects.get(pk=id_documento)
            doc.nome = formulario['documento'].value().upper()
            doc.descricao = formulario['descricao'].value()
            doc.save()
            formulario = formulario_adicionar_documento()
            messages.add_message(request, messages.SUCCESS, "Alteração realizada com sucesso!")

        else:
            pass

    return render(request,"protocolo/cadastro_documentos.html",{'dados': documentos,'formulario':formulario,'erro':erro})


def get_documento(request, id):
    doc = documento.objects.get(pk=id)
    if doc != None:
        resultado = [doc.nome,doc.descricao]
    else:
        resultado = ["", ""]
        raise Http404

    data = json.dumps(resultado)
    return HttpResponse(data, content_type='application/json')

def excluir_documento(request, id):
    doc = documento.objects.get(pk=id)
    try:
        doc.delete()
        resultado = ["SUCESS"]
    except:
        resultado = ["ERROR"]
        raise Http404

    data = json.dumps(resultado)
    return HttpResponse(data, content_type='application/json')










    

@login_required
def get_detalhes_protocolo(request,protocolo_id):
    #if request.is_ajax():
    resultado = {}
    documentos = item_protocolo.objects.filter(protocolo_id=protocolo_id)
    p = protocolo.objects.get(pk=protocolo_id)
    
    if documentos.count() != 0:
        lista =[]
        for item in documentos:

            if item.valor != "0,00":
                valor = "R$ "+item.valor.replace(".",",")

            else:
                valor = ""


            lista.append([item.documento,item.complemento,item.referencia,item.vencimento,valor])
            
        resultado['data'] = lista
        resultado['emitido_por'] = p.emitido_por
        data = json.dumps(resultado)
        
    else:
        print("Nenhum detalhe encontrado")
                
    data = json.dumps(resultado)
    return HttpResponse(data, content_type='application/json')

    #else:
    #    print("tentaram acessar os detalhes sem ser do jeito certo..")
    #    raise Http404
    

def validar_temporalidade(data_primeira_operacao,hora_primeira_operacao,data_segunda_operacao,hora_segunda_operacao):
    dp = data_primeira_operacao
    tp = hora_primeira_operacao
    
    ds = data_segunda_operacao
    ts = hora_segunda_operacao
        
    primeiro_datetime = datetime.datetime(dp.year,dp.month,dp.day,tp.hour,tp.minute,tp.second)
    segundo_datetime = datetime.datetime(ds.year,ds.month,ds.day,ts.hour,ts.minute,ts.second)
    
    return primeiro_datetime < segundo_datetime

@login_required
def cadastro_protocolo(request, protocolo_id=None):
    erro = False
    if (request.method == "POST"):
        
        form_entrega = formulario_confirmar_entrega()
        form_relatorio = formulario_gerar_relatorio()
        
        if 'gerar_relatorio' in request.POST:

            form_relatorio = formulario_gerar_relatorio(request.POST)

            if form_relatorio.is_valid():
                filtro_por_cliente = form_relatorio['filtrar_por_cliente'].value().upper()
                filtro_por_status = form_relatorio['filtrar_por_status'].value().upper()
                filtro_por_data_desde = form_relatorio['filtrar_desde'].value()
                filtro_por_operacao = form_relatorio['filtrar_por_operacao'].value()
                filtro_por_data_ate = form_relatorio['filtrar_ate'].value()
                filtro_por_documento = form_relatorio['filtrar_documentos'].value()

                if len(filtro_por_documento) != 0:
                    return report_protocols_per_documents(request,form_relatorio)


                 
                if filtro_por_cliente == '':
                    resultado = protocolo.objects.all()
                
                else:
                    resultado = protocolo.objects.filter(destinatario_id=filtro_por_cliente)
                    
                if filtro_por_status == 'CONFIRMADOS':
                    resultado = resultado.filter(situacao=1)
                
                elif filtro_por_status == 'ABERTOS':
                    resultado = resultado.filter(situacao=0)
                
                if filtro_por_data_desde != "":
                    filtro_por_data_desde = converte_formato_data(filtro_por_data_desde)
                    print('emitidos desde: ',filtro_por_data_desde)
                    
                    if filtro_por_operacao == "EMITIDOS":
                        resultado = resultado.filter(data_emissao__gte=filtro_por_data_desde)
                    else:
                        resultado = resultado.filter(data_recebimento__gte=filtro_por_data_desde)

                if filtro_por_data_ate != "":
                    filtro_por_data_ate = converte_formato_data(filtro_por_data_ate)
                    
                    if filtro_por_operacao == "EMITIDOS":
                        resultado = resultado.filter(data_emissao__lte=filtro_por_data_ate)
                    else:
                        resultado = resultado.filter(data_recebimento__lte=filtro_por_data_ate)
                    print('emitidos ate: ',filtro_por_data_ate)
                    
                
                #print('resultados: ')
                #for item in resultado:
                #    print("Veja: ",item)
                
                form_entrega = formulario_confirmar_entrega()
                form_relatorio = formulario_gerar_relatorio()
                
                return gerar_relatorio_simples(request,resultado)
            else:
                print("DEU ERRO? ",form_relatorio.errors)
                
        elif 'confirmar_protocolo' in request.POST:
            form_entrega = formulario_confirmar_entrega(request.POST)
            p = protocolo.objects.get(pk=int(form_entrega['protocolo_id'].value()))

            if not p.situacao:
                #messages.add_message(request, messages.SUCCESS, "Protocolo já foi confirmado!")
                if form_entrega.is_valid():
                    p = protocolo.objects.get(pk=int(form_entrega['protocolo_id'].value()))
                    p.situacao = True
                    p.recebido_por = form_entrega['recebido_por'].value().upper()
                    p.doc_receptor = form_entrega['doc_receptor'].value()

                    data = form_entrega['data_entrega'].value()
                    data = data.replace(" ", "")
                    tempo = form_entrega['hora_entrega'].value()

                    if data != "":
                        dia = int(data[:2])
                        mes = int(data[3:5])
                        ano = int(data[6:])
                        data_entrega = datetime.date(ano, mes, dia)

                        if tempo != "":
                            tempo = tempo.split(':')
                            hora = int(tempo[0])
                            minuto = int(tempo[1])
                            hora_entrega = datetime.time(hora, minuto)

                            if validar_temporalidade(p.data_emissao, p.hora_emissao, data_entrega, hora_entrega):
                                p.data_recebimento = data_entrega
                                p.hora_recebimento = hora_entrega
                                p.save()
                                return redirect('/protocolo')

                            else:
                                messages.add_message(request, messages.SUCCESS,"Erro! Horário da entrega não pode ser anterior a emissão.")
                                erro = True

                        else:
                            print("foi informado somente o dia, que nao pode ser anterior ao da emissao")

                else:
                    msg = verificar_erros_formulario(form_entrega)
                    messages.add_message(request, messages.SUCCESS, msg)
                    erro = True
            else:
                return redirect('/protocolo')
            
        else:
            #print("e uma requisicao mas sem name do form")
            return redirect('protocolo/cadastro_protocolo.html')

    else:
        form_entrega = formulario_confirmar_entrega()
        form_relatorio = formulario_gerar_relatorio()
        #print("VEJA O NOVO CAMPO: ",form_relatorio.filtrar_documentos)
        
    dados = protocolo.objects.all().order_by('-id')#*30
    #print("VEJA O CARAI DESSE PRIMEIRO ITEM: ",dados[0].id)
    clientes = entidade.objects.all()[1:]

    selecionar_protocolo = None
    if protocolo_id is not None:
        try:
            selecionar_protocolo = protocolo.objects.get(pk=int(protocolo_id))
        except:
            pass



    return render(request,"protocolo/cadastro_protocolo.html",{"form_entrega":form_entrega,"form_relatorio":form_relatorio,'selecionar_protocolo':selecionar_protocolo,'clientes':clientes,'dados':dados,'erro':erro})

"""
def imprimir_protocolo(request,emissor,destinatario,documentos,):
    from django.template import Context
    path = os.path.join(BASE_DIR, "arquivos_estaticos/imagens")
"""


def split_subparts(objects, subpart_lenght):
    new_list = []
    index_subpart = 0
    init = 0
    finish = subpart_lenght
    while index_subpart < (len(objects)/subpart_lenght):
        subpart = objects[init:finish]
        new_list.append(subpart)
        init = init+subpart_lenght
        finish = finish+subpart_lenght
        index_subpart = index_subpart+1
    return new_list

def gerar_relatorio_simples(request,resultado):
    from django_xhtml2pdf.utils import generate_pdf
    from django.template import Context
    path = os.path.join(BASE_DIR, "static/imagens/")
    
    print(request.POST)
    
    resultado = list(resultado)
    
    descricao_destinatario = ""
    descricao_periodo = ""

    status = request.POST['filtrar_por_status']
    if status == 'TODOS PROTOCOLOS':
        status = "GERAL"

    
    if request.POST['filtrar_por_cliente'] != '':
        cliente = entidade.objects.get(pk=request.POST['filtrar_por_cliente']).nome_razao
        
        if request.POST['filtrar_por_status'] == 'ABERTOS':
            descricao_destinatario = descricao_destinatario +u"Relatório de Protocolos em aberto do cliente "+cliente
        else:
            descricao_destinatario = descricao_destinatario +u"Relatório de Protocolos do cliente "+cliente
    else:
        cliente = "TODOS"
        if request.POST['filtrar_por_status'] == 'ABERTOS':
            descricao_destinatario = descricao_destinatario +u"Relatório de protocolos em aberto dos clientes"
        else:
            descricao_destinatario = descricao_destinatario +u"Relatório de protocolos dos clientes"
        
    if request.POST['filtrar_desde'] != '':
        
        if request.POST['filtrar_por_operacao'] == 'EMITIDOS':
            #descricao_periodo = descricao_periodo +"Emitidos desde "+request.POST['filtrar_desde']
            descricao_periodo = descricao_periodo + request.POST['filtrar_desde']
            
        elif request.POST['filtrar_por_operacao'] == 'RECEBIDOS':
            descricao_periodo = descricao_periodo + request.POST['filtrar_desde']
    
    else:
        pass
        #if request.POST['filtrar_por_operacao'] == 'EMITIDOS':
        #    descricao_periodo = descricao_periodo +" Emitidos"
        #
        #elif request.POST['filtrar_por_operacao'] == 'RECEBIDOS':
        #    descricao_periodo = descricao_periodo +"Recebidos"
        #else:
        #    pass
            
    if request.POST['filtrar_ate'] != '':
        descricao_periodo = descricao_periodo +u" até "+request.POST['filtrar_ate']
    
    data = date.today() 
    hora = datetime.datetime.now().strftime("%H:%M")
    
    resultado = resultado*60
    novo_result = []

    nova_lista = split_subparts(resultado, 50)
    #print("VEJA QUANTAS PAGINAS DEVEM TER:",len(resultado),"REGISTROS EM ",len(nova_lista)," PAGINA(S)")

    protocolo.index = 0;
    parametros = {
        'protocolos':nova_lista,
        'counter': 0,
        'path_imagens':path,
        'emitido_por':'MARCELO',
        'descricao_destinatario':descricao_destinatario,
        'filtro_operacao':request.POST['filtrar_por_operacao'].capitalize(),
        'filtro_status':status,
        'filtro_periodo':descricao_periodo,
        'filtro_cliente':cliente,

        'data_emissao':data,
        'hora_emissao':hora
    }
    #context = Context(parametros)
    resp = HttpResponse(content_type='application/pdf')
    result = generate_pdf('protocolo/imprimir_relatorio_simples.html', file_object=resp,context=parametros)
    return result


"""
def formatar_valor_documentos(lista_documentos):
    for item in lista_documentos:
        item.valor = formatar_valor_tamanho_fixo(item.valor)
    return lista_documentos

def formatar_valor_tamanho_fixo(valor):
    novo_valor = "R$"
    if valor == None or valor == "":
        novo_valor = "R$" + 13 * " " + "-"

    elif len(valor) == 14:
        novo_valor = novo_valor + valor

    else:
        espaco_extra = 14 - len(valor)
        novo_valor = novo_valor + espaco_extra * " " + valor
    print(novo_valor)
    return novo_valor
"""
@login_required
def gerar_pdf(request,emissor, destinatario, protocolo):
    from django.template import Context# loader,Context, Template
    path = os.path.join(BASE_DIR, "static/imagens/")
    
    print(protocolo.data_emissao, protocolo.hora_emissao)

    
    parametros = {
                  'emissor_nome':emissor.nome,
                  'emissor_cpf_cnpj':formatar_cpf_cnpj(emissor.cpf_cnpj),
                  'emissor_endereco':emissor.endereco,
                  'emissor_contatos':emissor.contatos,
                  
                  'destinatario_nome':destinatario.nome,
                  'destinatario_cpf_cnpj':destinatario.cpf_cnpj,
                  'destinatario_endereco':destinatario.endereco,
                  'destinatario_complemento':destinatario.complemento,
                  'destinatario_contatos':destinatario.contatos,
                  
                  'codigo_protocolo':destinatario.codigo_protocolo,
                  'emitido_por':'Marcelo',
                  'data_emissao':protocolo.data_emissao,
                  'hora_emissao':protocolo.hora_emissao,
                  
                  
                  'recebido_por':"",#recebido_por,
                  'identificacao':"",#identidade,
                  'data_entrega':"",#data_entrega,
                  'hora_entrega':"",#hora_entrega,
                  
                  'documentos':"",#formulario.temporarios,

                  #'documentos':[
                  #                  ["33","IMPOSTO DE RENDA","2015","","R$ 285,50"],
                  #                  ["8","EMISSAO DE CERTIFICADO DIGITAL","","31/12/2018","R$ 175,10"],
                  #                  ["14","CONTRATO - PLANO COMPLETO","","31/12/2018","R$ 475,00"],
                  #              ],
                  #'formulario_protocolo':"Nada por enquanto",
                  #'erro':"sem erros tambem",
                  #'path':path,
                  
                  'path_imagens':path
                   
                }
    
    c = Context(parametros)
    
    # RENDERIZAR NORMAL
    #return render_to_response('protocolo/imprimir_protocolo.html', c)
    
    # RENDERIZAR PDF
    from django_xhtml2pdf.utils import generate_pdf
    resp = HttpResponse(content_type='application/pdf')
    result = generate_pdf('protocolo/imprimir_protocolo.html', file_object=resp,context=c)
    return result


class ParametroProtocolo:
    entidade         = None
    nome             = None
    contatos         = None
    endereco         = None
    cpf_cnpj         = None
    complemento      = None
    codigo_protocolo = None
    

def criar_parametro_entidade_para_protocolo(entidade_id):
    print("Eu chego com o ID:",id)
    pessoa = entidade.objects.get(pk=entidade_id)
    print("Eu pego a pessoa:",pessoa.nome_razao)
    print("A localização tem ID:",pessoa.endereco_id)
    localizacao = localizacao_simples.objects.get(pk=pessoa.endereco_id)
    endereco = "%s, %s, %s, %s," % (localizacao.logradouro, localizacao.numero, localizacao.bairro, localizacao.municipio)
    endereco = endereco.title()
    endereco = endereco+" "+localizacao.estado+" - "+formatar_cep(localizacao.cep)


    parametros = ParametroProtocolo()
    parametros.entidade = pessoa
    parametros.nome = pessoa.nome_razao
    parametros.cpf_cnpj = pessoa.cpf_cnpj
    parametros.endereco = endereco
    try:
        parametros.complemento = localizacao.complemento.title()
    except:
        pass
    #parametros.codigo_protocolo = "%05d"%(pessoa.numeracao_protocolo)


    contatos = contato.objects.filter(entidade=pessoa)

    telefones = []
    for item in contatos:

        if item.numero:

            telefones.append(item.numero)
            if len(telefones) == 2:
                break

    parametros.contatos = telefones
    return parametros


def criar_protocolo(request,formulario):
    emissor = entidade.objects.get(pk=1)
    endereco = localizacao_simples.objects.get(pk=emissor.endereco_id)

    parametro_emissor = ParametroProtocolo()
    parametro_emissor.nome = emissor.nome_razao
    parametro_emissor.cpf_cnpj = emissor.cpf_cnpj

    
    endereco = "%s, %s, %s, %s, %s - %s"%(endereco.logradouro,endereco.numero,endereco.bairro,endereco.municipio, endereco.estado, formatar_cep(endereco.cep))
    parametro_emissor.endereco = endereco
    parametro_emissor.contatos = ["(27) 98834-2005","(27) 3022-1224"]

    p = protocolo()
    p.emissor = emissor
    p.emitido_por = "MARCELO"
    
    destinatario = formulario['entidade_destinatario'].value()
    
    if '|' in destinatario:
        campos = destinatario.split("|")
        cliente_id = -1
        destinatario             = ParametroProtocolo()
        destinatario.nome        = campos[0].upper()
        destinatario.cpf_cnpj    = formatar_cpf_cnpj(campos[1])
        destinatario.endereco    = campos[2].title()
        destinatario.complemento = ""
        destinatario.codigo_protocolo = "AVULSO"
        
        if campos[3] == "":
            destinatario.contatos = []
        else:
            destinatario.contatos = [campos[3]]
        
        #print("olha o que veio: ",formulario['entidade_destinatario'].value() )
        p.destinatario = None
        p.nome_avulso = destinatario.nome
        p.endereco_avulso = destinatario.endereco
        p.contatos_avulso = campos[3]
        
        p.numeracao_destinatario = destinatario.codigo_protocolo
    
    else:
        id_destinatario = int(destinatario[:destinatario.find(" - ")])
        registro = entidade.objects.get(pk=id_destinatario)
        cliente_id = id_destinatario
        
        destinatario             = ParametroProtocolo()
        destinatario.nome        = registro.nome_razao.upper()
        destinatario.cpf_cnpj    = formatar_cpf_cnpj(registro.cpf_cnpj)
        
        registro_endereco = localizacao_simples.objects.get(pk=registro.endereco_id)
        endereco = "%s, %s, %s, %s, %s - %s"%(registro_endereco.logradouro,registro_endereco.numero,registro_endereco.bairro,registro_endereco.municipio, registro_endereco.estado, formatar_cep(registro_endereco.cep))
        destinatario.endereco    = endereco.title()
        destinatario.complemento = registro_endereco.complemento.title()
        destinatario.codigo_protocolo = "%05d"%(registro.numeracao_protocolo)
        destinatario.contatos = []
        
        for item in contato.objects.filter(entidade=registro):
            destinatario.contatos.append(item.numero)
        
        p.destinatario = registro  
        p.numeracao_destinatario = destinatario.codigo_protocolo
        
    p.save()
    
    if cliente_id != -1:
        registro = entidade.objects.get(pk=cliente_id)
        registro.numeracao_protocolo = registro.numeracao_protocolo + 1
        registro.save()
    
    
    """for item in formulario.temporarios:
        item.protocolo_id = p.id
        
        #print(item.documentoooo,item.referencia,item.vencimento,item.valor,item.complemento)
        item.save()
    """
    return parametro_emissor,destinatario,p

@login_required
def novo_emitir_protocolo(request):
    formulario_protocolo = formulario_emitir_protocolo()
    clientes = entidade.objects.all().filter(ativo=True).exclude(id=1).order_by('-id')
    documentos = documento.objects.all()
    return render(request,"protocolo/novo_emitir_protocolo.html",{'operador':'Marcelo Bourguignon','formulario_protocolo':formulario_protocolo,'destinatarios':clientes ,'documentos':documentos})

@login_required
def emitir_protocolo_identificado(request,operador):
    formulario_protocolo = formulario_emitir_protocolo()
    operador = operador.replace("_"," ").title()
    clientes = entidade.objects.all().filter(ativo=True).exclude(id=1).order_by('-id')
    documentos = documento.objects.all()
    return render(request,"protocolo/novo_emitir_protocolo.html",{'operador':operador,'formulario_protocolo':formulario_protocolo,'destinatarios':clientes ,'documentos':documentos})

@login_required
def visualizar_protocolo(request, protocolo_id):
    from django.template import Context  # loader,Context, Template
    path = os.path.join(BASE_DIR, "static/imagens/")

    # if request.is_ajax():

    parametros_emissor = criar_parametro_entidade_para_protocolo(1)
    protocolo_selecionado = protocolo.objects.get(pk=protocolo_id)

    documentos = item_protocolo.objects.filter(protocolo_id=protocolo_id)
    #print("VOU ACERTAR TODOS OS PROTOCOLOS.. ")
    #for doc in item_protocolo.objects.all():
    #    if doc.valor is None or doc.valor == "":
    #        print("ID: ",doc.id," ESTA SEM VALOR.. VOU COLOCAR ZERO COMO PADRAO."
    #        doc.valor = '0,00'
    #        doc.save()

    # contatos = contato.objects.filter(entidade=p.destinatario)

    if protocolo_selecionado.destinatario == None:
        parametros_destinatario = ParametroProtocolo()
        parametros_destinatario.entidade = None
        parametros_destinatario.complemento = ''
        parametros_destinatario.nome = protocolo_selecionado.nome_avulso
        parametros_destinatario.cpf_cnpj = protocolo_selecionado.documento_avulso

        if protocolo_selecionado.endereco_avulso != None:
            parametros_destinatario.endereco = protocolo_selecionado.endereco_avulso.title()
        else:
            parametros_destinatario.endereco = ""

        if protocolo_selecionado.contatos_avulso != None:
            parametros_destinatario.contatos = [protocolo_selecionado.contatos_avulso]
        else:
            parametros_destinatario.contatos = []

    else:
        parametros_destinatario = criar_parametro_entidade_para_protocolo(protocolo_selecionado.destinatario_id)

        """destinatario_nome = p.destinatario.nome_razao
        destinatario_endereco = p.destinatario.endereco.get_endereco()
        destinatario_cpf_cnpj = formatar_cpf_cnpj(p.destinatario.cpf_cnpj)
        destinatario_contatos = contatos
        destinatario_complemento = p.destinatario.endereco.complemento.title()"""

    if protocolo_selecionado.doc_receptor != None:
        documento_receptor = protocolo_selecionado.doc_receptor

    else:
        documento_receptor = ""

    linhas_extras = [1] * (10 - len(documentos))

    parametros = {'emissor_nome': parametros_emissor.nome,
        'emissor_cpf_cnpj': formatar_cpf_cnpj(parametros_emissor.cpf_cnpj),
        'emissor_endereco': parametros_emissor.endereco,
        'emissor_complemento': parametros_emissor.complemento,
        'emissor_contatos': parametros_emissor.contatos,
        'destinatario_nome': parametros_destinatario.nome,
        'destinatario_cpf_cnpj': formatar_cpf_cnpj(parametros_destinatario.cpf_cnpj),
        'destinatario_endereco': parametros_destinatario.endereco,
        'destinatario_complemento': parametros_destinatario.complemento,
        'destinatario_contatos': parametros_destinatario.contatos,

        'codigo_protocolo': protocolo_selecionado.numeracao_destinatario,
        'emitido_por': protocolo_selecionado.emitido_por.title(),
        'data_emissao': protocolo_selecionado.data_emissao,
        'hora_emissao': protocolo_selecionado.hora_emissao,

        'recebido_por': protocolo_selecionado.recebido_por,  # recebido_por,
        'identificacao': protocolo_selecionado.doc_receptor if protocolo_selecionado.doc_receptor != None else "",
    # identidade,
        'data_entrega': protocolo_selecionado.data_recebimento,  # data_entrega,
        'hora_entrega': protocolo_selecionado.hora_recebimento,  # hora_entrega,

        'documentos': documentos,  # formulario.temporarios,
        'linhas_extras': linhas_extras, # 'documentos':[
        #                  ["33","IMPOSTO DE RENDA","2015","","R$ 285,50"],
        #                  ["8","EMISSAO DE CERTIFICADO DIGITAL","","31/12/2018","R$ 175,10"],
        #                  ["14","CONTRATO - PLANO COMPLETO","","31/12/2018","R$ 475,00"],
        #              ],
        # 'formulario_protocolo':"Nada por enquanto",
        # 'erro':"sem erros tambem",
        # 'path':path,

        'path_imagens': path

    }

    c = Context(parametros)

    # RENDERIZAR NORMAL
    # return render_to_response('protocolo/imprimir_protocolo.html', c)

    # RENDERIZAR PDF
    from django_xhtml2pdf.utils import generate_pdf
    resp = HttpResponse(content_type='application/pdf')
    result = generate_pdf('protocolo/imprimir_protocolo.html', file_object=resp, context=parametros)
    return result


def salvar_protocolo(request):
    #print("Tentando salvar o protocolo - DADOS:",request.POST)
    if request.is_ajax():
        dados = request.POST.dict()
        parametros_emissor = criar_parametro_entidade_para_protocolo(1)

        #if "-" in dados['destinatario']:
        # TEM QUE CRIAR MECANISMO DO PROTOCOLO AVULSO

        if "#" in dados['destinatario']:
            id_destinatario = dados['destinatario'].split("-")[0].replace(" ","")
            id_destinatario = id_destinatario.replace("#", "")
            parametros_destinatario = criar_parametro_entidade_para_protocolo(id_destinatario)
            #print("TEM NO BANCO")

        else:
            #print("AVULSO")
            parametros_destinatario = ParametroProtocolo()
            parametros_destinatario.entidade = None
            parametros_destinatario.nome = dados['destinatario'].upper()
            parametros_destinatario.cpf_cnpj = dados['complemento_identificacao']
            parametros_destinatario.contatos = [dados['complemento_contato'].upper()]
            parametros_destinatario.endereco = dados['complemento_endereco'].upper()

        novo_protocolo = protocolo()
        novo_protocolo.emissor = parametros_emissor.entidade
        novo_protocolo.emitido_por = dados['operador'].upper()
        novo_protocolo.destinatario = parametros_destinatario.entidade

        cliente = parametros_destinatario.entidade
        if cliente != None:
            novo_protocolo.numeracao_destinatario = "%05d"%(cliente.numeracao_protocolo)
            cliente.numeracao_protocolo = cliente.numeracao_protocolo + 1
            cliente.save()

        else:
            novo_protocolo.numeracao_destinatario = "AVULSO"
            novo_protocolo.nome_avulso = parametros_destinatario.nome.upper()
            novo_protocolo.contatos_avulso = parametros_destinatario.contatos[0]
            novo_protocolo.endereco_avulso = parametros_destinatario.endereco
            novo_protocolo.documento_avulso = parametros_destinatario.cpf_cnpj

        novo_protocolo.save()


        for index in range(int(dados['total_documentos'])):
            prefixo = "documentos[" + str(index) + "]"
            item = get_object_documento_from_dict(dados, prefixo)
            item.protocolo = novo_protocolo
            item.save()

        #print("salvei tudo?")
        #return gerar_pdf(request,parametros_emissor, parametros_destinatario, novo_protocolo)

        response_dict = {}
        response_dict['success'] = True
        response_dict['message'] = "/protocolo/visualizar/"+str(novo_protocolo.id)+"/"
        data = json.dumps(response_dict)
        return HttpResponse(data, content_type='application/json')

    else:
        raise Http404


def get_object_documento_from_dict(dados,prefixo):
    item = item_protocolo()
    item.documento = dados[prefixo + "[documento]"].upper()
    item.complemento = dados[prefixo + "[complemento]"].upper()
    item.referencia = dados[prefixo + "[referencia]"]
    item.vencimento = dados[prefixo + "[vencimento]"]

    item.valor = str(dados[prefixo + "[valor]"])
    return item


def validar_registro(registro):
    msg = ""

    try:
        registro.full_clean()
        msg = "SUCESSO"
        #print("validacao ok")

    except ValidationError as excecao:
        msg = "Erro! " + excecao.message
        #print("Olha o erro:"+str(excecao))

    except IntegrityError as excecao:
        if "cpf_cnpj" in excecao.message:
            msg = "Erro! cpf ou cnpj já existe no cadastro!"

        else:
            msg = excecao.message

        #print("Olha o erro:" + msg)
        return msg, ""

    except Exception as excecao:
        print("Ve esse erro ai qualquer", excecao.message)

    finally:
        #print("Nao deu nada?")
        return False, ""

@login_required
def emitir_protocolo(request,numero_item):
    numero_item = int(numero_item)
    erro = False
    destinatarios = entidade.objects.all()[1:]
    documentos = documento.objects.all()
    
    if (request.method == "POST"):
        
        formulario_protocolo = formulario_emitir_protocolo(request.POST)
        
        if 'adicionar_item' in request.POST:
            
            if formulario_protocolo.is_valid(): 
                item            = item_protocolo()
                item.documento  = formulario_protocolo['documento'].value().upper()
                item.complemento= formulario_protocolo['complemento'].value().upper()
                item.referencia = formulario_protocolo['referencia'].value()
                item.vencimento = formulario_protocolo['vencimento'].value()
                
                valor = formulario_protocolo['valor'].value()
                
                if valor != "":
                    valor = valor.replace(".","")
                    valor = valor.replace(",",".")
                    item.valor      = Decimal(valor)
                
                formulario_protocolo.temporarios.append(item)
                
                cliente = formulario_protocolo['entidade_destinatario'].value().upper()
                temp = formulario_protocolo.temporarios
                
                formulario_protocolo  = formulario_emitir_protocolo({'entidade_destinatario':cliente})
                formulario_protocolo.temporarios = temp

                print("OLHA O CLIENTE: ",cliente,": DOCUMENTOS: ",temp)
            
            else:
                msg = verificar_erros_formulario(formulario_protocolo)
                messages.add_message(request, messages.SUCCESS, msg)
                erro = True
            
            
        elif 'gerar_protocolo' in request.POST:
            emissor, destinatario, protocolo = criar_protocolo(request, formulario_protocolo)
            print("GERANDO:",destinatario," PROTOCOLO:",protocolo)
            resposta_pdf = gerar_pdf(request,formulario_protocolo, emissor, destinatario, protocolo)
            return resposta_pdf
        
        elif 'excluir_item' in request.POST:
            formulario_protocolo = formulario_emitir_protocolo(request.POST)
            #print(formulario_protocolo["excluir_item"])
            
            try:
                formulario_protocolo.temporarios.remove(formulario_protocolo.temporarios[int(formulario_protocolo["excluir_item"].value())])
            except:
                pass
            
    else:
        formulario_protocolo = formulario_emitir_protocolo()
        formulario_protocolo.limpar_temporarios()
                    
    return render(request,"protocolo/emitir_protocolo.html",{'destinatarios':destinatarios ,'documentos':documentos,'dados':formulario_protocolo.temporarios,'formulario_protocolo':formulario_protocolo,'erro':erro})


def salvar_itens_protocolos(protocolo,itens_protocolo):
    for item in itens_protocolo:                
        item.protocolo = protocolo
        item.save()
        

"""
 
 COISAS QUE PODEM SER COLOCADAS EM OUTROS LUGARES

"""

def converte_formato_data(data):
    nova_data = data[6:]+"-"+data[3:5]+'-'+data[:2]
    return nova_data

def formatar_cep(cep):
    cep_formatado = ""+cep[:2]+"."+cep[2:5]+"-"+cep[5:]
    return cep_formatado

def formatar_cpf_cnpj(codigo):
    if codigo != None:
        if len(codigo) == 11:
            codigo_formatado = codigo[:3]+"."+codigo[3:6]+"."+codigo[6:9]+"-"+codigo[9:]
        else:
            codigo_formatado = codigo[:2]+"."+codigo[2:5]+"."+codigo[5:8]+"/"+codigo[8:12]+"-"+codigo[12:]
        return codigo_formatado

    else:
        return ""