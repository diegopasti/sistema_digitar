# -*- encoding: utf-8 -*-
import json
import locale
from datetime import date

from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
from django.http.response import Http404
from django.shortcuts import render, HttpResponse
from django.template import RequestContext

from libs.default.decorators import permission_level_required
from modules.preferencias.formularios import adicionar_salario_minimo

from modules.preferencias.models import SalarioMinimo

@login_required
@permission_level_required(1,'/error/access_denied')
def controle_preferencias(request):
    formulario_salario = adicionar_salario_minimo()
    return render(request, "preferencias/preferencias.html",{'formulario_salario':formulario_salario})

@login_required
def adicionar_salario(request):
    if request.is_ajax():
        formulario = adicionar_salario_minimo(request.POST)
        resultado = validar_formulario(formulario)
        if resultado == True:
            salario = SalarioMinimo()
            salario.valor = formulario.cleaned_data['valor']
            salario.inicio_vigencia = formulario.cleaned_data['inicio_vigencia']
            response_dict = executar_operacao(salario, "save")
            if response_dict["success"]:
                #print("Buscando o id:",response_dict['message'],type(response_dict['message']))
                novo_registro = SalarioMinimo.objects.get(pk=response_dict['message']).data_cadastro.strftime("%Y-%m-%d às %H:%M:%S")
                #print("Tentando buscar o novo registro:"+novo_registro)
                response_dict['message'] = str(response_dict['message']) + "#" +novo_registro

        else:
            response_dict = {}
            response_dict['success'] = False
            response_dict['message'] = resultado

        return HttpResponse(json.dumps(response_dict))
    else:
        raise Http404


def validar_formulario(formulario):
    if formulario.is_valid():
        return True
    else:
        for campo in formulario:
            erros = campo.errors.as_data()
            if erros != []:
                erro = erros[0]
                #print("olha o erro:",erro[0])
                msg = "Erro! "+campo.label.replace(":","")+str(erros[0])
                print(msg)
                return msg

@login_required
def alterar_salario(request,id):
    if request.is_ajax():
        formulario = adicionar_salario_minimo(request.POST)
        resultado = validar_formulario(formulario)
        if resultado == True:
            #dict_obj['valor'] = float(
            #dict_obj['valor'])  # str(locale.currency(float(dict_obj['valor']), grouping=True)).replace("R$","")
            #dict_obj['inicio_vigencia'] = dict_obj['inicio_vigencia'].strftime("%d/%m/%Y")
            salario = SalarioMinimo.objects.get(pk=int(id))
            salario.valor = formulario.cleaned_data['valor']
            salario.inicio_vigencia = formulario.cleaned_data['inicio_vigencia']

            response_dict = executar_operacao(salario, "save")


        else:
            response_dict = {}
            response_dict['success'] = False
            response_dict['message'] = resultado

        return HttpResponse(json.dumps(response_dict))
    else:
        raise Http404

@login_required
def excluir_salario(request,id):
    if request.is_ajax():
        salario = SalarioMinimo.objects.get(pk=int(id))
        response_dict = executar_operacao(salario,"delete")
        return HttpResponse(json.dumps(response_dict))

    else:
        raise Http404

@login_required
def listar_salarios(request):
    locale.setlocale(locale.LC_ALL, '')
    data_atual = date.today()
    # Outro recurso seria usar o modulo do proprio Django.
    #from django.contrib.humanize.templatetags.humanize import intcomma
    #return "$ %s" % intcomma(price)
    if request.is_ajax():
        salarios = SalarioMinimo.objects.all().order_by("-inicio_vigencia")
        salario_vigente = None
        registro_vigente = None
        dados = []
        cont = 0
        for item in salarios:
            dict_obj = model_to_dict(item)
            dict_obj['valor'] = float(dict_obj['valor'])  # str(locale.currency(float(dict_obj['valor']), grouping=True)).replace("R$","")
            dict_obj['inicio_vigencia'] = dict_obj['inicio_vigencia'].strftime("%Y-%m-%d")
            dict_obj['data_cadastro'] = item.data_cadastro.strftime("%Y-%m-%d às %H:%M:%S")
            dict_obj['vigente'] = False

            if salario_vigente == None:
                salario_vigente = item
            elif item.inicio_vigencia > salario_vigente.inicio_vigencia and item.inicio_vigencia <= data_atual:
                salario_vigente = item
                registro_vigente = cont
            else:
                pass
            cont = cont + 1
            dados.append(dict_obj)

        if registro_vigente != None:
            dados[registro_vigente]['vigente'] = True

        data = json.dumps(dados)
        return HttpResponse(data, content_type='application/json')
    else:
        raise Http404

@login_required()
def get_salario_vigente(request):
    from django.contrib.humanize.templatetags.humanize import intcomma
    #return
    data_atual = date.today()
    try:
        salario_vigente = SalarioMinimo.objects.filter(inicio_vigencia__lte=data_atual).latest('inicio_vigencia')
    except:
        salario_vigente = None

    try:
        proximo_salario_vigente = SalarioMinimo.objects.filter(inicio_vigencia__gt=data_atual).order_by('inicio_vigencia').first()
    except:
        proximo_salario_vigente = None

    response_dict = {}

    if salario_vigente is not None:
        response_dict['id_salario_vigencia_atual'] = salario_vigente.id
        response_dict['salario_vigencia_atual'] = "R$ %s" % intcomma(salario_vigente.valor)
        response_dict['inicio_vigencia_atual'] = salario_vigente.inicio_vigencia.strftime("%Y-%m-%d")
    else:
        print("Entro aqui salario_vigente = None")
        response_dict['id_salario_vigencia_atual'] = None
        response_dict['salario_vigencia_atual'] = None
        response_dict['inicio_vigencia_atual'] = None

    if proximo_salario_vigente:
        response_dict['salario_proxima_vigencia'] = "R$ %s" % intcomma(proximo_salario_vigente.valor)
        response_dict['inicio_proxima_vigencia'] = proximo_salario_vigente.inicio_vigencia.strftime("%Y-%m-%d")
        response_dict['duracao_vigencia_atual'] = (proximo_salario_vigente.inicio_vigencia-salario_vigente.inicio_vigencia).days
        response_dict['dias_restante_vigencia_atual'] = (proximo_salario_vigente.inicio_vigencia-data_atual).days
        response_dict['percentual_restante_vigencia_atual'] = "%.2f"%(100-(float(response_dict['dias_restante_vigencia_atual'])/response_dict['duracao_vigencia_atual'])*100)

    else:
        response_dict['salario_proxima_vigencia'] = None
        response_dict['inicio_proxima_vigencia'] = None
        response_dict['duracao_vigencia_atual'] = None
        response_dict['dias_restante_vigencia_atual'] = None
        response_dict['percentual_restante_vigencia_atual'] = None

    #print("olha a vigencia atual:",salario_vigente.inicio_vigencia)
    #print("olha a proxima vigencia: ",proximo_salario_vigente.inicio_vigencia)
    #print("OLHA A DURACAO DESSA VIGENCIA:",response_dict['duracao_vigencia_atual'])
    #print("OLHA OS DIAS RESTANTES: ",response_dict['dias_restante_vigencia_atual']," -> ",response_dict['percentual_restante_vigencia_atual'])
    data = json.dumps(response_dict)
    return HttpResponse(data, content_type='application/json')


def executar_operacao(registro,operacao):
    response_dict = {}
    if operacao == "save":
        metodo_selecionado = registro.save
        menssage_sucesso = "Registro adicionado com Sucesso!"
        menssage_falha = "Erro! Registro não pode ser Salvo.\n"

    elif operacao == "delete":
        metodo_selecionado = registro.delete
        menssage_sucesso = "Registro apagado com Sucesso!"
        menssage_falha = "Erro! Registro não pode ser Salvo.\n"

    try:
        metodo_selecionado()
        response_dict['success'] = True
        response_dict['message'] = registro.id

    except Exception as e:
        response_dict['success'] = False
        response_dict['message'] = menssage_falha+str(e)
    return response_dict
