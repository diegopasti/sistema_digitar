# -*- encoding: utf-8 -*-
from modules.honorario.models import Contrato, Indicacao, Proventos
from modules.honorario.forms import FormContrato, FormProventos
#from django.views.decorators.cache import never_cache
from modules.servico.models import Plano, Servico
from django.http import HttpResponse, Http404
from libs.default.core import BaseController
from modules.entidade.models import entidade
from sistema_contabil import settings
from django.core import serializers
from django.core.cache import cache
import json


def filter_request(request, formulary=None):
    if request.is_ajax() or settings.DEBUG:
        if formulary is not None:
            form = formulary(request.POST)
            if form.is_valid():
                return True, form
            else:
                return False, form
        else:
            return True, True
    else:
        raise Http404


def response_format_success_message(object,list_fields):
    return response_format(True, '', object, list_fields)


def response_format_error_message(message):
    return response_format(False, message, None, None)


def response_format(result,message,object,list_fields):
    response_dict = {}
    response_dict['success'] = result
    response_dict['message'] = message
    if result:
        if list_fields is not None:
            response_dict['data-object'] = serializers.serialize('json', [object], fields=tuple(list_fields))
        else:
            response_dict['data-object'] = serializers.serialize('json', [object])
        response_dict['data-object'] = response_dict['data-object'][1:-1]

    else:
        response_dict['data-object'] = None
    return response_dict


def get_lista_contratos(request):
    lista_clientes = entidade.objects.all().order_by('-pk')
    response_dict = []
    for item in lista_clientes:
        response_cliente = {}
        response_cliente['cliente_id'] = item.id
        response_cliente['cliente_nome'] = item.nome_razao
        response_cliente['selecionado'] = False
        contrato = Contrato.objects.filter(cliente=item.id)

        if len(contrato) != 0:
            contrato = contrato[0]
            response_cliente['contrato'] = {}
            if contrato.plano is not None:
                response_cliente['plano'] = contrato.plano.nome
                response_cliente['plano_id'] = contrato.plano.id
            else:
                response_cliente['plano'] = None
                response_cliente['plano_id'] = None
            response_cliente['indicacoes'] = []

            response_cliente['contrato']['servicos_contratados'] = contrato.servicos_contratados
            response_cliente['contrato']['tipo_cliente'] = contrato.tipo_cliente

            if(contrato.vigencia_inicio): response_cliente['contrato']['vigencia_inicio'] = str(contrato.vigencia_inicio.strftime('%d/%m/%Y'))

            if (contrato.vigencia_fim): response_cliente['contrato']['vigencia_fim'] = str(contrato.vigencia_fim.strftime('%d/%m/%Y'))
            response_cliente['contrato']['taxa_honorario'] = contrato.taxa_honorario

            if (contrato.taxa_honorario): response_cliente['contrato']['taxa_honorario'] = float(contrato.taxa_honorario)
            if (contrato.valor_honorario): response_cliente['contrato']['valor_honorario'] = float(contrato.valor_honorario)

            response_cliente['contrato']['dia_vencimento'] = contrato.dia_vencimento
            response_cliente['contrato']['data_vencimento'] = contrato.data_vencimento

            #contrato.totalizar_honorario()

            response_cliente['contrato']['desconto_temporario'] = float(contrato.desconto_temporario)
            response_cliente['contrato']['desconto_temporario_ativo'] = float(contrato.desconto_temporario_ativo)
            response_cliente['contrato']['desconto_indicacoes'] = float(contrato.desconto_indicacoes)
            response_cliente['contrato']['valor_total'] = float(contrato.valor_total)


            if (contrato.desconto_inicio): response_cliente['contrato']['desconto_inicio'] = str(contrato.desconto_inicio.strftime('%d/%m/%Y'))
            if (contrato.desconto_fim): response_cliente['contrato']['desconto_fim'] = str(contrato.desconto_fim.strftime('%d/%m/%Y'))

            response_cliente['contrato']['cadastrado_por'] = contrato.cadastrado_por.nome_razao
            response_cliente['contrato']['data_cadastro'] = str(contrato.data_cadastro.strftime('%d/%m/%Y'))
            response_cliente['contrato']['ultima_alteracao'] = str(contrato.ultima_alteracao.strftime('%d/%m/%Y'))
            response_cliente['contrato']['alterado_por'] = contrato.alterado_por.nome_razao

        else:
            response_cliente['contrato'] = {}
            response_cliente['plano'] = None
            response_cliente['indicacoes'] = []
            response_cliente['contrato']['servicos_contratados'] = None
            response_cliente['contrato']['tipo_cliente'] = None
            response_cliente['contrato']['vigencia_inicio'] = None
            response_cliente['contrato']['vigencia_fim'] = None
            response_cliente['contrato']['taxa_honorario'] = None
            response_cliente['contrato']['valor_honorario'] = None
            response_cliente['contrato']['valor_total'] = None
            response_cliente['contrato']['dia_vencimento'] = None
            response_cliente['contrato']['data_vencimento'] = None
            response_cliente['contrato']['desconto_temporario'] = None
            response_cliente['contrato']['desconto_inicio'] = None
            response_cliente['contrato']['desconto_fim'] = None
            response_cliente['contrato']['desconto_indicacoes'] = None
            response_cliente['contrato']['cadastrado_por'] = None
            response_cliente['contrato']['data_cadastro'] = None
            response_cliente['contrato']['ultima_alteracao'] = None
            response_cliente['contrato']['alterado_por'] = None

        response_dict.append(response_cliente)
    return HttpResponse(json.dumps(response_dict))


def atualizar_servicos(request):
    #print("VIM AQUI ATUALIZAR OS SERVICO DO CONTRATO DO CLIENTE: ",request.POST['cliente_id'])
    cliente_id = request.POST['cliente_id']
    novos_servicos = request.POST['servicos']
    contrato = Contrato.objects.get(cliente_id=int(cliente_id))
    #print("ENCONTREI O CONTRATO: ",contrato)
    contrato.servicos_contratados = novos_servicos
    contrato.save()
    response_dict = response_format_success_message(contrato, [])
    return HttpResponse(json.dumps(response_dict))

def carregar_servicos_contratados(request,cliente_id,plano_id):
    response_dict = []
    id_cliente = int(cliente_id)
    cliente = entidade.objects.get(pk=id_cliente)
    contrato = Contrato.objects.get(cliente=cliente)

    plano = Plano.objects.get(pk=int(plano_id))
    lista_servicos = plano.servicos.split(';')
    if plano is not None:
        for item in lista_servicos:
            servico = Servico.objects.get(pk=int(item))
            response_object = {}
            response_object['id'] = servico.id
            response_object['nome'] = servico.nome
            response_object['descricao'] = servico.descricao

            if str(servico.id) in contrato.servicos_contratados:
                response_object['ativo'] = True
            else:
                response_object['ativo'] = False
            response_dict.append(response_object)
    return HttpResponse(json.dumps(response_dict))


def get_lista_indicacoes(request,cliente_id):
    id_cliente = int(cliente_id)
    lista_indicacoes = Indicacao.objects.filter(cliente=id_cliente)
    response_dict = []
    for indicacao in lista_indicacoes :
        response_indicacao = {}
        response_indicacao['cliente_id'] = indicacao.cliente.id
        response_indicacao['indicacao'] = {}
        response_indicacao['indicacao']['selecionado'] = ''
        response_indicacao['indicacao']['nome_razao'] = indicacao.indicacao.nome_razao
        response_indicacao['indicacao']['indicacao_id'] = indicacao.indicacao.id
        response_indicacao['indicacao']['data_cadastro'] = str(indicacao.data_cadastro.strftime('%d/%m/%Y'))
        response_indicacao['indicacao']['taxa_desconto'] = float(indicacao.taxa_desconto)
        response_indicacao['indicacao']['indicacao_ativa'] = indicacao.indicacao_ativa
        response_indicacao['indicacao']['cadastrado_por'] = indicacao.cadastrado_por.nome_razao
        response_indicacao['indicacao']['ultima_alteracao'] = str(indicacao.ultima_alteracao.strftime('%d/%m/%Y'))
        response_indicacao['indicacao']['alterador_por'] = indicacao.alterado_por.nome_razao
        response_dict.append(response_indicacao)
    return HttpResponse(json.dumps(response_dict))


def salvar_indicacao (request):
    empresa = request.POST['empresa']
    taxa_desconto = float(request.POST['taxa_desconto'])
    cliente_id = request.POST['cliente_id']

    if company_was_indicated(empresa) == False:
        cliente = entidade.objects.get(pk=int(cliente_id))
        if cliente is not None:
            indicacao = Indicacao()
            indicacao.cliente_id = int(cliente_id)
            indicacao.indicacao_id = int(empresa)
            indicacao.taxa_desconto = taxa_desconto

            indicacao.save()
            #response_dict = response_format_success_message(indicacao,['indicacao','cliente','taxa_desconto','data_cadastro'])

            #contrato = Contrato.objects.get(cliente=cliente)
            #contrato.totalizar_honorario()
            #contrato.save()

            response_dict = response_format_success_message(indicacao, ['indicacao', 'cliente', 'taxa_desconto', 'data_cadastro'])
            #contrato.desconto_indicacoes = contrato.desconto_indicacoes + Decimal(taxa_desconto)

        else:
            response_dict = response_format_error_message("Cliente não existe.")
    else:
        response_dict = response_format_error_message("Essa empresa já foi indicada.")

    return HttpResponse(json.dumps(response_dict))


def alterar_indicacao (request):
    empresa_id = request.POST['empresa']
    empresa_nome = request.POST['empresa_nome']
    taxa_desconto = float(request.POST['taxa_desconto'])
    indicacao_bd = Indicacao.objects.get(indicacao=empresa_id)

    if (indicacao_bd.indicacao.nome_razao == empresa_nome and indicacao_bd.taxa_desconto != taxa_desconto):

        try:
            Indicacao.objects.filter(indicacao=empresa_id).update(taxa_desconto=taxa_desconto)
            response_dict = response_format_success_message(indicacao_bd,['indicacao','cliente','taxa_desconto'])
        except:
            response_dict = response_format_error_message(False)

    else:
        response_dict = response_format_error_message(False)

    return HttpResponse(json.dumps(response_dict))


def alterar_boolean_indicacao(request):
    empresa = request.POST['empresa']
    indicacao_bd = Indicacao.objects.get(indicacao=empresa)
    status = not indicacao_bd.indicacao_ativa
    try:
        Indicacao.objects.filter(indicacao=empresa).update(indicacao_ativa= status)
        response_dict = response_format_success_message(indicacao_bd, ['indicacao','indicacao_ativa'])
    except:
        response_dict = response_format_error_message(False)
    return HttpResponse(json.dumps(response_dict))


def deletar_indicacao (request):
    empresa = request.POST['empresa']
    indicacao_bd = Indicacao.objects.get(indicacao=empresa)
    print()

    try :
        indicacao_bd.indicacao.delete()
        response_dict = response_format_success_message(indicacao_bd,[])
    except:
        response_dict = response_format_error_message(False)

    return HttpResponse(json.dumps(response_dict))


def company_was_indicated(company):
    indications = Indicacao.objects.filter(indicacao=company)
    if len(indications) > 0:
        return True
    else:
        return False


def salvar_contrato(request):
    result, form = filter_request(request,FormContrato)
    if result:
        contrato = form.form_to_object()
        cliente = entidade.objects.get(pk=int(request.POST['cliente']))
        contrato.cliente = cliente

        plano = Plano.objects.get(pk=int(request.POST['plano']))
        contrato.servicos_contratados = plano.servicos
        contrato.totalizar_honorario()
        contrato.save()
        response_dict = response_format_success_message(contrato,None)
    else:
        #print "VEJA OS ERROS: ",form.errors.items()
        #texto = ""
        #for item in form.errors.items():
        #    for erro in item[1]:
        #        texto = texto+'- '+str(erro)+'<br>'
        response_dict = response_format_error_message(form.errors)
    return HttpResponse(json.dumps(response_dict))


def alterar_contrato(request):
    result, form = filter_request(request,FormContrato)

    if result:
        contrato = form.form_to_object(int(request.POST['cliente']))
        plano = Plano.objects.get(pk=int(request.POST['plano']))
        #contrato.servicos_contratados = plano.servicos
        contrato.plano = plano
        contrato.totalizar_honorario()
        contrato.save()
        response_dict = response_format_success_message(contrato,None) #response_format_error_message("TESTANTADO.. ")#response_format_success_message(contrato,None)
    else:
        response_dict = response_format_error_message(form.errors)

    return HttpResponse(json.dumps(response_dict))

def atualizar_contrato(request):
    contrato = Contrato.objects.get(cliente_id=int(request.POST['cliente']))
    #plano = Plano.objects.get(pk=int(request.POST['plano']))
    #contrato.servicos_contratados = plano.servicos
    #contrato.plano = plano
    contrato.totalizar_honorario()
    contrato.save()
    response_dict = response_format_success_message(contrato, None)
    return HttpResponse(json.dumps(response_dict))


class ProventosController(BaseController):

    #login_required
    #user_passes_test(lambda u: u.permissions.can_view_entity(), login_url='/error/access_denied', redirect_field_name=None)

    #never_cache - Para usar esse decorador precisamos usar esse metodo com o self e consequentemente instancia-lo no urls.
    def filter_provents(self,request):
        cache_page = cache.has_key(request.get_raw_uri())
        return BaseController().filter(request, Proventos, queryset=Proventos.objects.filter(is_active=True).order_by('-id'))

    #login_required
    #user_passes_test(lambda u: u.permissions.can_insert_entity(), login_url='/error/access_denied', redirect_field_name=None)
    def save_provent(request):
        cache_page = cache.has_key('http://localhost:8020/api/provents')
        #print("VEJA SE TEM CACHE: ",cache_page)
        return BaseController().save(request, FormProventos)

    #login_required
    #user_passes_test(lambda u: u.permissions.can_update_entity(), login_url='/error/access_denied', redirect_field_name=None)
    def update_provent(request):
        return BaseController().update(request, FormProventos)

    def disable_provent(request):
        return BaseController().disable(request, Proventos)

"""
def get_lista_proventos_old(self,request):
    lista_proventos = Proventos.objects.filter(ativo=True).order_by('-id')

    response_dict = []
    for item in lista_proventos:
        response_object = {}
        response_object['id'] = item.id
        response_object['tipo'] = item.tipo
        response_object['nome'] = item.nome
        response_object['descricao'] = item.descricao
        response_object['valor'] = float(item.valor)
        response_object['data_cadastro'] = str(item.data_cadastro.strftime('%d/%m/%Y'))
        response_object['cadastrado_por'] = item.cadastrado_por.nome_razao
        response_object['ultima_alteracao'] = str(item.ultima_alteracao.strftime('%d/%m/%Y'))
        response_object['alterado_por'] = item.alterado_por.nome_razao
        response_object['selecionado'] = ""
        response_dict.append(response_object)
    return HttpResponse(json.dumps(response_dict))

def adicionar_provento_old(self,request):
    
    print("VEJA O QUE VEIO: ",request.POST['tipo'])
    result, form = filter_request(request, FormProventos)
    if result:
        provento = form.form_to_object()
        provento.save()
        response_dict = response_format_success_message(provento, None)
    else:
        texto = ""
        for item in form.errors.items():
            for erro in item[1]:
                texto = texto+'- '+str(erro)+'<br>'
        response_dict = response_format_error_message(form.errors)
    return HttpResponse(json.dumps(response_dict))
"""

"""
class ContratoAPI:

    def get_lista_contratos(request):
        lista_contratos = Contrato.objects.all()
        #response_dict = response_format_error("Formulário com dados inválidos.")
        return HttpResponse({'message':'Testando'})



    def register_user(request):
        resultado, form = AbstractAPI.filter_request(request, FormRegister)
        #print("VAMOS LA.. VEJA OS TESTS: ",request.POST)
        if resultado:
            #print("TA VALIDO")
            email = request.POST['email'].lower()
            senha = request.POST['password']
            if User.objects.check_available_email(email):
                #print("EMAIL TA DISPONIVEL")
                usuario = User.objects.create_contracting_user(email, senha)
                if usuario is not None:
                    activation_code = generate_activation_code(email)
                    send_generate_activation_code(email, activation_code)
                    response_dict = response_format_success(usuario, ['email'])
                else:
                    #print("USUARIO NAO TA CADASTRADO")
                    response_dict = response_format_error("Nao foi possivel criar objeto")
            else:
                #print("EMAIL TA INDISPONIVEL")
                response_dict = response_format_error("Email já cadastrado.")
        else:
            #print("FORMULARIO INCORRETO")
            response_dict = response_format_error("Formulário com dados inválidos.")
        return HttpResponse(json.dumps(response_dict))

    def register_delete(request, email):
        user = User.objects.get_user_email(email)
        if user is not None:
            user.delete()
            response_dict = response_format_error("Usuario deletado com sucesso.")
        else:
            response_dict = response_format_error("Usuario nao existe.")
        return HttpResponse(json.dumps(response_dict))
"""