# -*- encoding: utf-8 -*-
'''
Created on 17 de ago de 2017

@author: Diego
'''
import datetime
import os

from django.db import connection
from django.shortcuts import render_to_response
from django.template import Context

from modules.entidade.models import entidade
from modules.protocolo.models import protocolo, item_protocolo as ItemProtocolo, documento as Documento
from sistema_contabil.settings import BASE_DIR


def report_protocols_per_documents(request, form):
    images_path = os.path.join(BASE_DIR, "static/imagens")
    filtro_cliente = form['filtrar_por_cliente'].value().upper()
    filtro_status  = form['filtrar_por_status'].value().upper()
    filtro_desde = form['filtrar_desde'].value()
    filtro_operacao = form['filtrar_por_operacao'].value()
    filtro_ate = form['filtrar_ate'].value()
    filtro_documento = form['filtrar_documentos'].value()

    #print ("INICIANDO AS QUERYs:",len(connection.queries))

    if filtro_cliente == 'TODOS' or filtro_cliente=='':
        filtro_cliente = "TODOS CLIENTES"
        protocols_list = protocolo.objects.all()
        #print ("PEGUEI TODOS PROTOCOLOS - CONEXOES:", len(connection.queries))

    else:
        #print("VEJA O CLIENTE: ", filtro_cliente)
        cliente = entidade.objects.get(pk=int(filtro_cliente))
        #print ("PEGUEI O CLIENTE ESPECIFICO - CONEXOES:", len(connection.queries))
        filtro_cliente = cliente.nome_razao
        protocols_list = protocolo.objects.filter(destinatario=cliente)
        #print ("PEGUEI TODOS OS PROTOCOLOS DO CLIENTE - CONEXOES:", len(connection.queries))

    if filtro_status == 'CONFIRMADOS':
        #print("VAMOS PEGAR TODOS PROTOCOLOS CONFIRMADOS")
        protocols_list = protocols_list.filter(situacao=1)
        #print ("FILTREI TODOS PROTOCOLOS CONFIRMADOS - CONEXOES:", len(connection.queries))
    elif filtro_status == "ABERTOS":
        protocols_list = protocols_list.filter(situacao=0)
        #print ("FILTREI TODOS PROTOCOLOS EM ABERTO - CONEXOES:", len(connection.queries))
    else:
        pass
        #print("VAMOS PEGAR TODOS PROTOCOLOS")

    if filtro_desde != '':
        campos = filtro_desde.split('/')
        data_desde = campos[2]+"-"+campos[1]+'-'+campos[0]

        if filtro_operacao == 'EMITIDOS':
            #print("PEGAR PELA DATA DE EMISSAO DESDE")
            protocols_list = protocols_list.filter(data_emissao__gte = data_desde)
            #print ("FILTREI TODOS PROTOCOLOS EMITIDOS DESDE - CONEXOES:", len(connection.queries))
        else:
            #print("PEGAR PELA DATA DE RECEBIMENTO DESDE")
            protocols_list = protocols_list.filter(data_recebimento__gte=data_desde)
            #print ("FILTREI TODOS PROTOCOLOS RECEBIDOS DESDE - CONEXOES:", len(connection.queries))
    else:
        #print("NAO TEM UMA DATA DE INICIO ENTAO PEGA TODOS")
        pass

    if filtro_ate != '':
        campos_fim = filtro_ate.split('/')
        data_ate = campos_fim[2]+"-"+campos_fim[1]+'-'+campos_fim[0]
        #print("TEM UMA DATA DE FIM", data_ate)
        if filtro_operacao == 'EMITIDOS':
            #print("PEGAR PELA DATA DE EMISSAO ATE")
            protocols_list = protocols_list.filter(data_emissao__lte = data_ate)
            #print ("FILTREI TODOS PROTOCOLOS EMITIDOS ATE - CONEXOES:", len(connection.queries))
        else:
            #print("PEGAR PELA DATA DE RECEBIMENTO ATE")
            protocols_list = protocols_list.filter(data_recebimento__lte=data_ate)
            #print ("FILTREI TODOS PROTOCOLOS RECEBIDOS ATE - CONEXOES:", len(connection.queries))
    else:
        #print("NAO TEM UMA DATA DE FIM ENTAO PEGA TODOS")
        pass

    resultado = []

    #print ("HORA DE FILTRAR PELOS DOCUMENTOS - CONEXOES ATE AQUI:", len(connection.queries))
    total_protocolos = 0
    if filtro_documento!="":
        for id_documento in filtro_documento:
            documento = Documento.objects.get(pk=int(id_documento))
            #print ("PEGUEI O DOCUMENTO ESPECIFICO - CONEXOES:", len(connection.queries))
            protocolos_selecionados = []
            protocolos_abertos = 0
            for item in protocols_list:
                item_protocolo = ItemProtocolo.objects.filter(documento=documento, protocolo=item)
                #print ("FILTREI TODOS PROTOCOLOS QUE TEM ESSE DOCUMENTO - CONEXOES:", len(connection.queries))
                #print("TOTAL: ",item_protocolo.count())
                #print ("VERIFIQUEI O TOTAL DE RESPOSTAS - CONEXOES:", len(connection.queries))
                #print("ESTAMOS PROCURANDO", documento.nome, " NO PROTOCOLO:", item.id,"RESULTADO: ",item_protocolo)
                if item_protocolo.count() != 0:
                    if item.situacao == 0:
                        protocolos_abertos = protocolos_abertos + 1
                    protocolos_selecionados.append(item)
                    total_protocolos = total_protocolos + 1
            resultado.append({'documento':documento.nome,'protocolos_abertos':protocolos_abertos,'protocolos':protocolos_selecionados})

        print ("HORA DE FILTRAR PELOS DOCUMENTOS - CONEXOES ATE AQUI:", len(connection.queries))


        #print("\n\n")
        #for item in protocols_list:
        #    protocolos_procurados = []
        #    for id_documento in filtro_documento:
        #        documento = Documento.objects.get(pk=int(id_documento))
        #        item_protocolo = ItemProtocolo.objects.filter(documento=documento,protocolo=item)
        #        print("ESTOU PROCURANDO ESSE DOCUMENTO: ",documento.nome," NO PROTOCOLO: ",item.id)
        #        print("VEJA SE ENCONTREI ITENS DE PROTOCOLO: ",item_protocolo)
        #        if len(item_protocolo) != 0:
        #            print("ENCONTREI")
        #            protocolos_procurados.append(item)
        #    if protocolos_procurados != []:
        #        resultado.append({'documento':documento.nome,'lista_protocolos':protocolos_procurados})

    else:
        print("NAO TEM COMO NAO TER DOCUMENTO INFORMADO KKK")

    #print("VEJA O QUE SOBROU NA LISTA: ",protocols_list)
    #print("VEJA O RESULTADO: ",resultado)




    #from django_xhtml2pdf.utils import generate_pdf
    #from django.template import Context
    #path = os.path.join(BASE_DIR, "static/imagens/")


    #protocols_list = list(protocolo.objects.all())
    #print("É ISSO ESTOU GERANDO O RELATORIO", protocols_list)


    """
    resultado = list(resultado)

    descricao_destinatario = ""
    descricao_periodo = ""

    if request.POST['filtrar_por_cliente'] != '':
        cliente = entidade.objects.get(pk=request.POST['filtrar_por_cliente']).nome_razao

        if request.POST['filtrar_por_status'] == 'ABERTOS':
            descricao_destinatario = descricao_destinatario + u"Relatório de Protocolos em aberto do cliente " + cliente
        else:
            descricao_destinatario = descricao_destinatario + u"Relatório de Protocolos do cliente " + cliente
    else:
        cliente = "TODOS"
        if request.POST['filtrar_por_status'] == 'ABERTOS':
            descricao_destinatario = descricao_destinatario + u"Relatório de protocolos em aberto dos clientes"
        else:
            descricao_destinatario = descricao_destinatario + u"Relatório de protocolos dos clientes"

    if request.POST['filtrar_desde'] != '':

        if request.POST['filtrar_por_operacao'] == 'EMITIDOS':
            # descricao_periodo = descricao_periodo +"Emitidos desde "+request.POST['filtrar_desde']
            descricao_periodo = descricao_periodo + request.POST['filtrar_desde']

        elif request.POST['filtrar_por_operacao'] == 'RECEBIDOS':
            descricao_periodo = descricao_periodo + request.POST['filtrar_desde']

    else:
        pass
        # if request.POST['filtrar_por_operacao'] == 'EMITIDOS':
        #    descricao_periodo = descricao_periodo +" Emitidos"

        # elif request.POST['filtrar_por_operacao'] == 'RECEBIDOS':
        #    descricao_periodo = descricao_periodo +"Recebidos"

    if request.POST['filtrar_ate'] != '':
        descricao_periodo = descricao_periodo + u" até " + request.POST['filtrar_ate']

    data = date.today()
    hora = datetime.datetime.now().strftime("%H:%M")
    
    
    parametros = {
        'protocolos': resultado,
        'path_imagens': path,
        'emitido_por': 'MARCELO',
        'descricao_destinatario': descricao_destinatario,
        
        'filtro_operacao': request.POST['filtrar_por_operacao'].capitalize(),
        'filtro_status': request.POST['filtrar_por_status'].upper(),
        'filtro_periodo': descricao_periodo,
        'filtro_cliente': cliente,
        
        'data_emissao': data,
        'hora_emissao': hora
    }
    """

    parametros = {
        'protocols_list':resultado,
        'total_protocolos': total_protocolos,
        'data_atual':datetime.datetime.now(),
        'images_path':images_path,
        'filtro_cliente':filtro_cliente,
        'filtro_status':filtro_status,
        'filtro_desde':filtro_desde,
        'filtro_operacao':filtro_operacao,
        'filtro_ate':filtro_ate,
        'filtro_documento':filtro_documento,
    }
    context = Context(parametros)
    return render_to_response('protocolo/report/report_per_documents.html', context)


    #resp = HttpResponse(content_type='application/pdf')
    #result = generate_pdf('protocolo/imprimir_relatorio_simples.html', file_object=resp, context=context)
    #return result