# -*- encoding: utf-8 -*-
from decimal import Decimal

import os

from modules.honorary.models import Contrato, Indicacao, Proventos, Honorary, HonoraryItem
from modules.honorary.forms import FormContrato, FormProventos, FormHonoraryItem
from django.contrib.auth.decorators import login_required, permission_required
from libs.default.decorators import request_ajax_required
from django.utils.decorators import method_decorator

from modules.protocolo.views import formatar_cpf_cnpj
from modules.servico.models import Plano, Servico
from django.http import HttpResponse, Http404
from libs.default.core import BaseController
from modules.entidade.models import entidade, contato
from sistema_contabil import settings
from django.core import serializers
from django.core.cache import cache
from django.utils import timezone
import datetime
import json

from sistema_contabil.settings import BASE_DIR


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



def company_was_indicated(company):
    indications = Indicacao.objects.filter(indicacao=company)
    if len(indications) > 0:
        return True
    else:
        return False


class ContractController(BaseController):

    @method_decorator(login_required)
    def salvar_contrato(self, request):
        save_response = self.save(request, FormContrato, extra_fields=['plano__nome'], is_response=False)
        print("SALVEI: ")
        if save_response['result']:
            contrato = Contrato.objects.get(pk=int(save_response['object']['id']))
            contrato.servicos_contratados = contrato.plano.servicos
            contrato.totalizar_honorario()
            contrato.save()

            honoraries = Honorary.objects.filter(contract=contrato)
            for honorary in honoraries:
                honorary = Honorary().update_honorary(honorary, contract=contrato)
                honorary.updated_by = request.user
                honorary.updated_by_name = request.user.get_full_name()
                honorary.save()

            return self.response(super().object(request, Contrato, contrato.id, extra_fields=['plano__nome']))
        else:
            return self.response(save_response)

        """
        result, form = filter_request(request, FormContrato)
        if result:
            contrato = form.form_to_object()
            cliente = entidade.objects.get(pk=int(request.POST['cliente']))
            contrato.cliente = cliente

            plano = Plano.objects.get(pk=int(request.POST['plano']))
            contrato.servicos_contratados = plano.servicos
            contrato.totalizar_honorario()
            contrato.save()
            response_dict = response_format_success_message(contrato, None)
        else:
            # print "VEJA OS ERROS: ",form.errors.items()
            # texto = ""
            # for item in form.errors.items():
            #    for erro in item[1]:
            #        texto = texto+'- '+str(erro)+'<br>'
            response_dict = response_format_error_message(form.errors)
        
            response_dict['result'] = False
            response_dict['object'] = None
            response_dict['message'] = "Erro! "+form.errors

        return self.response(response_dict)
        """

    @request_ajax_required
    @method_decorator(login_required)
    #method_decorator(permission_required('contrato.add_contrato',raise_exception=True))
    def get_lista_contratos(self, request):
        lista_clientes = entidade.objects.all().exclude(pk=1).order_by('-pk')
        response_dict = []
        for item in lista_clientes:
            response_cliente = {}
            response_cliente['cliente_id'] = item.id
            response_cliente['cliente_nome'] = item.nome_razao
            response_cliente['selecionado'] = False
            response_cliente['contrato'] = {}

            try:
                contrato = Contrato.objects.get(cliente_id=item.id)
                result = self.object(request, Contrato, contrato.id, extra_fields=['plano__nome'])
                response_cliente['contrato'] = result['object']
            except:
                response_cliente['contrato'] = None

            """
            #try:
            #    contrato = Contrato.objects.get(cliente=item.id)
            #except:
            #    contrato = {}
            
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

                if (contrato.vigencia_inicio): response_cliente['contrato']['vigencia_inicio'] = str(contrato.vigencia_inicio.strftime('%d/%m/%Y'))

                if (contrato.vigencia_fim): response_cliente['contrato']['vigencia_fim'] = str(contrato.vigencia_fim.strftime('%d/%m/%Y'))
                response_cliente['contrato']['taxa_honorario'] = contrato.taxa_honorario

                if (contrato.taxa_honorario): response_cliente['contrato']['taxa_honorario'] = float(contrato.taxa_honorario)
                if (contrato.valor_honorario): response_cliente['contrato']['valor_honorario'] = float(contrato.valor_honorario)

                response_cliente['contrato']['dia_vencimento'] = contrato.dia_vencimento
                response_cliente['contrato']['data_vencimento'] = contrato.data_vencimento

                # contrato.totalizar_honorario()

                response_cliente['contrato']['desconto_temporario'] = float(contrato.desconto_temporario)
                response_cliente['contrato']['desconto_temporario_ativo'] = float(contrato.desconto_temporario_ativo)
                response_cliente['contrato']['desconto_indicacoes'] = float(contrato.desconto_indicacoes)
                response_cliente['contrato']['valor_total'] = float(contrato.valor_total)

                if (contrato.desconto_inicio): response_cliente['contrato']['desconto_inicio'] = str(contrato.desconto_inicio.strftime('%d/%m/%Y'))
                if (contrato.desconto_fim): response_cliente['contrato']['desconto_fim'] = str(contrato.desconto_fim.strftime('%d/%m/%Y'))

                response_cliente['contrato']['cadastrado_por'] = contrato.cadastrado_por.get_full_name()
                response_cliente['contrato']['data_cadastro'] = str(contrato.data_cadastro.strftime('%d/%m/%Y'))
                response_cliente['contrato']['ultima_alteracao'] = str(contrato.ultima_alteracao.strftime('%d/%m/%Y'))
                response_cliente['contrato']['alterado_por'] = contrato.alterado_por.get_full_name()

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
            """

            response_dict.append(response_cliente)
        response_final = {}
        response_final['result'] = True
        response_final['object'] = response_dict
        response_final['message'] = str(len(response_dict))+" Contratos carregados com sucesso!"
        return self.response(response_final)

    @request_ajax_required
    @method_decorator(login_required)
    def alterar_contrato(self, request):
        update_response = self.update(request, FormContrato, extra_fields=['plano__nome'], is_response=False)
        if update_response['result']:
            contrato = Contrato.objects.get(pk=int(request.POST['id']))
            contrato.totalizar_honorario()
            contrato.save()

            honoraries = Honorary.objects.filter(contract=contrato)
            for honorary in honoraries:
                honorary = Honorary().update_honorary(honorary, contract=contrato)
                honorary.updated_by = request.user
                honorary.updated_by_name = request.user.get_full_name()
                honorary.save()

            return self.response(super().object(request, Contrato, contrato.id, extra_fields=['plano__nome']))
        else:
            return self.response(update_response)


        """
        result, form = filter_request(request, FormContrato)
        response_dict = {}
        if result:
            contrato = form.form_to_object(int(request.POST['cliente']))
            plano = Plano.objects.get(pk=int(request.POST['plano']))
            contrato.plano = plano
            contrato.totalizar_honorario()
            contrato.save()

            honoraries = Honorary.objects.filter(contract=contrato)
            for honorary in honoraries:
                honorary = Honorary().update_honorary(honorary, contract=contrato)
                honorary.updated_by = request.user
                honorary.updated_by_name = request.user.get_full_name()
                honorary.save()

            response_dict = self.notify.success(contrato)

        else:
            response_dict['result'] = False
            response_dict['object'] = None
            response_dict['message'] = "Erro! "+form.errors

        return self.response(response_dict)
        """

    @request_ajax_required
    @method_decorator(login_required)
    def close_contract(self, request):
        try:
            contrato = Contrato.objects.get(pk=int(request.POST['id']))
            contrato.ativo = False

            honoraries = Honorary.objects.filter(contract=contrato)
            for honorary in honoraries:
                honorary = Honorary().update_honorary(honorary, contract=contrato)
                honorary.updated_by = request.user
                honorary.updated_by_name = request.user.get_full_name()
                honorary.save()

        except Exception as e:
            contrato = None
            response_dict = self.notify.error(e)

        if contrato is not None:
            response_dict = self.execute(contrato, contrato.save, extra_fields=['plano__nome'])
            if(response_dict['result']):
                honoraries = Honorary.objects.filter(contract=contrato)
                for honorary in honoraries:
                    honorary = Honorary().update_honorary(honorary, contract=contrato)
                    honorary.updated_by = request.user
                    honorary.updated_by_name = request.user.get_full_name()
                    honorary.save()
            print("VEJA O RESULTADO: ",response_dict)
            return self.response(response_dict)
        else:
            return self.response(response_dict)


    @request_ajax_required
    @method_decorator(login_required)
    def atualizar_contrato(self, request):
        contract_selected = Contrato.objects.filter(cliente_id=int(request.POST['cliente']))
        response_dict = {}
        if contract_selected.count() == 0:
            response_dict['result'] = False
            response_dict['object'] = None
            response_dict['message'] = "Erro! Contrato não identificado."
        else:
            contract_selected = contract_selected[0]
            contract_selected.totalizar_honorario()
            contract_selected.save()
            response_dict = self.notify.success(contract_selected)
        return self.response(response_dict)

    @request_ajax_required
    @method_decorator(login_required)
    def carregar_servicos_contratados(self, request, cliente_id):
        response_dict = []
        cliente = entidade.objects.get(pk=int(cliente_id))
        contrato = Contrato.objects.filter(cliente=cliente).first()
        if contrato is not None:
            plano = contrato.plano
            servicos_plano = plano.servicos.split(';')

            for item in servicos_plano:
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

        response_final = {}
        response_final['result'] = True
        response_final['object'] = response_dict
        response_final['message'] = str(len(response_dict)) + " Serviços carregados com sucesso!"
        return self.response(response_final)

    @request_ajax_required
    @method_decorator(login_required)
    def atualizar_servicos(self, request):
        cliente_id = request.POST['cliente_id']
        contract_selected = Contrato.objects.filter(cliente_id=int(cliente_id))
        response_dict = {}
        if contract_selected.count() == 0:
            response_dict['result'] = False
            response_dict['object'] = None
            response_dict['message'] = "Erro! Contrato não identificado."
        else:
            contract_selected = contract_selected[0]
            contract_selected.servicos_contratados = request.POST['servicos']
            response_dict = self.execute(contract_selected, contract_selected.save)
        return self.response(response_dict)

    @request_ajax_required
    @method_decorator(login_required)
    def get_lista_indicacoes(self, request, cliente_id):
        id_cliente = int(cliente_id)
        #lista_indicacoes = Indicacao.objects.filter(cliente=id_cliente)

        lista_indicacoes = self.notify.datalist(Indicacao.objects.filter(cliente=id_cliente), extra_fields=['indication_name'])
        for item in lista_indicacoes:
            #print("EMPRESA INDICADA: ",item['indicacao'])
            indication_client = entidade.objects.get(id=int(item['indicacao']))
            item['indication_name'] = indication_client.nome_razao

        response_dict = {}
        if len(lista_indicacoes) == 0:
            response_dict['result'] = True
            response_dict['object'] = []
            response_dict['message'] = "Cliente não tem nenhuma indicação."
        else:
            response_dict['result'] = True
            response_dict['object'] = lista_indicacoes
            response_dict['message'] = str(len(lista_indicacoes))+" indicações cadastradas."
        print("VEJA O RESPONSE DICT: ",response_dict)
        return self.response(response_dict)

    @request_ajax_required
    @method_decorator(login_required)
    def salvar_indicacao(self,request):
        empresa = request.POST['empresa']
        taxa_desconto = float(request.POST['taxa_desconto'].replace('.','').replace(',','.'))
        cliente_id = request.POST['cliente_id']
        response_dict = {}
        if empresa == cliente_id:
            response_dict['result'] = False
            response_dict['object'] = None
            response_dict['message'] = "Erro! Não é possivel incluir uma indicação de uma empresa pra ela própria."
            return self.response(response_dict)

        if company_was_indicated(empresa) == False:
            cliente = entidade.objects.get(pk=int(cliente_id))
            if cliente is not None:
                indicacao = Indicacao()
                indicacao.cliente_id = int(cliente_id)
                indicacao.indicacao_id = int(empresa)
                indicacao.taxa_desconto = taxa_desconto

                indicacao.save()
                # response_dict = response_format_success_message(indicacao,['indicacao','cliente','taxa_desconto','data_cadastro'])

                contrato = Contrato.objects.get(cliente=cliente)
                contrato.totalizar_honorario()
                contrato.save()

                honoraries = Honorary.objects.filter(contract=contrato)
                for honorary in honoraries:
                    honorary = Honorary().update_honorary(honorary, contract=contrato)
                    honorary.updated_by = request.user
                    honorary.updated_by_name = request.user.get_full_name()
                    honorary.save()

                response_dict = self.notify.success(indicacao, extra_fields=['indication_name'])

                indication_client = entidade.objects.get(id=indicacao.indicacao_id)
                response_dict['object']['indication_name'] = indication_client.nome_razao

                #response_dict = response_format_success_message(indicacao, ['indicacao', 'cliente', 'taxa_desconto', 'data_cadastro'])
                # contrato.desconto_indicacoes = contrato.desconto_indicacoes + Decimal(taxa_desconto)

            else:
                response_dict['result'] = False
                response_dict['message'] = "Erro! Cliente não existe."
        else:
            response_dict['result'] = False
            response_dict['message'] = "Erro! Essa empresa foi indicada."
        return self.response(response_dict)

    @request_ajax_required
    @method_decorator(login_required)
    def alterar_indicacao(self,request):
        from django.utils.timezone import now, localtime
        client_id = int(request.POST['cliente_id'])
        indicated_company = request.POST['empresa']
        indicated_name = request.POST['empresa_nome']
        taxa_desconto = float(request.POST['taxa_desconto'].replace('.','').replace(',','.'))
        indicacao_bd = Indicacao.objects.get(indicacao=indicated_company)

        if (indicacao_bd.indicacao.nome_razao == indicated_name and indicacao_bd.taxa_desconto != taxa_desconto):
            indicacao_bd.taxa_desconto = taxa_desconto
            indicacao_bd.ultima_alteracao = localtime(now())
            try:
                indicacao_bd.save()
                response_dict = self.notify.success(indicacao_bd, extra_fields=['indication_name'])
                response_dict['object']['indication_name'] = indicacao_bd.indicacao.nome_razao

            except Exception as erro:
                response_dict = self.notify.error(erro)

            if response_dict['result']:
                #Indicacao.objects.filter(indicacao=indicated_company).update(taxa_desconto=taxa_desconto,ultima_alteracao = localtime(now()))
                contrato = Contrato.objects.get(cliente_id=client_id)
                contrato.totalizar_honorario()
                contrato.ultima_alteracao = localtime(now())
                contrato.save()

                honoraries = Honorary.objects.filter(contract=contrato, )
                for honorary in honoraries:
                    honorary = Honorary().update_honorary(honorary, contract=contrato)
                    honorary.last_update = localtime(now())
                    honorary.updated_by = request.user
                    honorary.updated_by_name = request.user.get_full_name()
                    honorary.save()
        else:
            response_dict = response_format_error_message(False)
        return self.response(response_dict)

    @request_ajax_required
    @method_decorator(login_required)
    def alterar_boolean_indicacao(self, request):
        from django.utils.timezone import now, localtime
        client_company_id = int(request.POST['cliente'])
        indicated_company_id = int(request.POST['indicated_company'])
        if(request.POST['indicacao_ativa']=='false'):
            status = True
        else:
            status = False

        indicacao = Indicacao.objects.get(indicacao_id=indicated_company_id)
        indicacao.indicacao_ativa = status
        indicacao.ultima_alteracao = localtime(now())#timezone.localtime(timezone.now())
        indicacao.alterado_por = request.user

        try:
            indicacao.save()
            response_dict = self.notify.success(indicacao, extra_fields=['indication_name'])

        except Exception as erro:
            response_dict = self.notify.error(erro)

        if response_dict['result']:
            indication_client = entidade.objects.get(id=indicated_company_id)
            response_dict['object']['indication_name'] = indication_client.nome_razao

            contrato = Contrato.objects.get(cliente_id=int(client_company_id))
            contrato.totalizar_honorario()
            contrato.ultima_alteracao = now #timezone.localtime(timezone.now())
            contrato.alterado_por = request.user
            contrato.save()

            honoraries = Honorary.objects.filter(contract=contrato)
            for honorary in honoraries:
                honorary = Honorary().update_honorary(honorary, contract=contrato)
                honorary.updated_by = request.user
                honorary.updated_by_name = request.user.get_full_name()
                honorary.save()
        return self.response(response_dict)

    @request_ajax_required
    @method_decorator(login_required)
    def deletar_indicacao(self, request):
        empresa = request.POST['indicated_company']
        indicacao_bd = Indicacao.objects.get(indicacao_id=int(empresa))
        response_final = {}
        try:
            indicacao_bd.delete()
            response_final['result'] = True
            response_final['message'] = "Indicação excluida com sucesso!"

            contrato = Contrato.objects.get(cliente_id=int(empresa))
            contrato.totalizar_honorario()
            contrato.save()

            honoraries = Honorary.objects.filter(contract=contrato)
            for honorary in honoraries:
                honorary = Honorary().update_honorary(honorary, contract=contrato)
                honorary.updated_by = request.user
                honorary.updated_by_name = request.user.get_full_name()
                honorary.save()

        except:
            response_final['result'] = False
            response_final['message'] = "Erro! Não foi possivel excluir essa indicação."

        response_final['object'] = None
        return self.response(response_final)


class ProventosController(BaseController):

    #login_required
    #user_passes_test(lambda u: u.permissions.can_view_entity(), login_url='/error/access_denied', redirect_field_name=None)

    #never_cache - Para usar esse decorador precisamos usar esse metodo com o self e consequentemente instancia-lo no urls.
    @method_decorator(login_required)
    #method_decorator(permission_required('user.can_add'))
    def filter_provents(self, request):
        return BaseController().filter(request, Proventos, queryset=Proventos.objects.filter(is_active=True).order_by('-id'))

    #login_required
    #user_passes_test(lambda u: u.permissions.can_insert_entity(), login_url='/error/access_denied', redirect_field_name=None)
    @method_decorator(login_required)
    def save_provent(self, request):
        #cache_page = cache.has_key('http://localhost:8020/api/provents')
        #print("VEJA SE TEM CACHE: ",cache_page)
        return BaseController().save(request, FormProventos)

    #login_required
    #user_passes_test(lambda u: u.permissions.can_update_entity(), login_url='/error/access_denied', redirect_field_name=None)
    @method_decorator(login_required)
    def update_provent(self, request):
        return BaseController().update(request, FormProventos)

    @method_decorator(login_required)
    def disable_provent(self, request):
        return BaseController().disable(request, Proventos)


class HonoraryController(BaseController):

    @method_decorator(login_required)
    def get_object(self, request):
        return self.object(request, Honorary, int(request.POST['id']),is_response=True)

    @method_decorator(login_required)
    def filter(self,request):
        for item in range(4):
            competence = self.get_competence(datetime.datetime.now().month+item)
            if Honorary.objects.filter(competence=competence).count() == 0:
                entity_list = entidade.objects.filter(ativo=True).exclude(id=1)
                for entity in entity_list:
                    self.create_update_honorary(request, entity, competence)
        return BaseController().filter(request, Honorary, extra_fields=['honorary_itens'])

    @method_decorator(login_required)
    def generate_honoraries(self,request):
        current_month = datetime.datetime.now().month
        entity_list = entidade.objects.filter(ativo=True).exclude(id=1)
        for entity in entity_list:
            self.create_update_honorary(request, entity, self.get_competence(current_month))
            self.create_update_honorary(request, entity, self.get_competence(current_month + 1))
            self.create_update_honorary(request, entity, self.get_competence(current_month + 2))
            self.create_update_honorary(request, entity, self.get_competence(current_month + 3))
        return BaseController().filter(request, Honorary)

    @request_ajax_required
    @method_decorator(login_required)
    def close_current_competence(self, request):

        now = timezone.localtime(timezone.now())
        completed_competence = self.get_competence(datetime.datetime.now().month-1)
        exist_competence = Honorary.objects.filter(competence=completed_competence)
        closed_competences = Honorary.objects.filter(competence=completed_competence, is_closed=False).update(is_closed=True,closed_by=request.user, closed_date = now)
        response_dict = {}
        if closed_competences != 0:
            response_dict['result'] = True
            response_dict['object'] = None
            response_dict['message'] = str(closed_competences) + " Honorários de "+completed_competence+" finalizados com sucesso!"
        else:
            response_dict['result'] = False
            response_dict['object'] = None
            if exist_competence.count() == 0:
                response_dict['message'] = "Nenhum honorário de "+completed_competence+" encontrado!"
            else:
                response_dict['message'] = "Honorários de " + completed_competence + " já foram finalizado!"
        return self.response(response_dict)

    def get_competence(self, month_number):
        month_list_name = ['JAN', 'FEV', 'MAR', 'ABR', 'MAI', 'JUN', 'JUL', 'AGO', 'SET', 'OUT', 'NOV', 'DEZ']
        current_month = datetime.datetime.now().month
        current_year = datetime.datetime.now().year
        if month_number == 0:
            month_number = 12
            current_year = current_year - 1

        elif month_number > 12:
            month_number = month_number - 12
            current_year = current_year + 1
        else:
            pass

        return month_list_name[int(month_number)-1]+"/"+str(current_year)

    @method_decorator(login_required)
    def create_update_honorary(self, request, entity, competence):
        contract = Contrato.objects.filter(cliente=entity)
        if contract.count() == 0: contract = None
        else: contract = contract[0]

        honoraries = Honorary.objects.filter(entity=entity, competence=competence)
        if honoraries.count() == 0:
            honorary = Honorary().create_honorary(entity, competence, contract=contract)
            honorary.created_by = request.user
            honorary.updated_by = request.user
        else:
            honorary = Honorary().update_honorary(honoraries[0], contract=contract)
            honorary.updated_by = request.user

        honorary.save()
        return honorary

    @method_decorator(login_required)
    def save_honorary_item(self, request):
        print("VEJA O QUE VEIO: ",request.POST)
        try:
            honorary = Honorary.objects.get(pk=int(request.POST['honorary_id']))
        except:
            honorary = None
        if honorary is not None:
            response_dict = self.save(request, FormHonoraryItem, is_response=False, extra_fields=['item__nome','created_by__get_full_name','updated_by__get_full_name'])
            if response_dict['result']:
                honorary.number_debit_credit = honorary.number_debit_credit + 1
                new_value =  Decimal(request.POST['total_value'])
                if request.POST['type_item'] == "P":
                    honorary.total_debit = honorary.total_debit + new_value
                    honorary.total_debit_credit = honorary.total_debit_credit + new_value
                    honorary.total_honorary = honorary.total_honorary + new_value

                elif request.POST['type_item'] == "D":
                    honorary.total_credit = honorary.total_credit + new_value
                    honorary.total_debit_credit = honorary.total_debit_credit - new_value
                    honorary.total_honorary = honorary.total_honorary - new_value

                elif request.POST['type_item'] == "R":
                    honorary.total_repayment = honorary.total_repayment + new_value
                    honorary.total_debit_credit = honorary.total_debit_credit + new_value
                    honorary.total_honorary = honorary.total_honorary + new_value
                else:
                    pass

                honorary.updated_by_id = request.user.id
                honorary.updated_by_name = request.user.get_full_name()
                honorary_response = self.execute(honorary, honorary.save, extra_fields=['item__nome','created_by__get_full_name','updated_by__get_full_name'])
                if honorary_response['result']:
                    response_dict['message'] = 'Honorário salvo com sucesso!'
                else:
                    response_dict['message'] = 'Erro! Registro salvo mas houve uma falha ao tentar recalcular o honorário.'
        else:
            response_dict = {}
            response_dict['result'] = False
            response_dict['object'] = None
            response_dict['message'] = "Erro! Honorário informado não existe."
        print("VEJA O QUE SAI:",response_dict)
        return self.response(response_dict)

    @method_decorator(login_required)
    def update_honorary_item(self, request):
        try:
            honorary = Honorary.objects.get(pk=int(request.POST['honorary_id']))
        except:
            honorary = None

        if honorary is not None:
            response_dict = self.update(request, FormHonoraryItem, extra_fields=['item__nome','created_by__get_full_name','updated_by__get_full_name'],is_response=False)
            if response_dict['result']:
                honorary.number_debit_credit = honorary.number_debit_credit + 1
                new_value =  Decimal(request.POST['total_value'])
                if request.POST['type_item'] == "P":
                    honorary.total_debit = honorary.total_debit + new_value
                    honorary.total_debit_credit = honorary.total_debit_credit + new_value
                    honorary.total_honorary = honorary.total_honorary + new_value

                elif request.POST['type_item'] == "D":
                    honorary.total_credit = honorary.total_credit + new_value
                    honorary.total_debit_credit = honorary.total_debit_credit - new_value
                    honorary.total_honorary = honorary.total_honorary - new_value

                elif request.POST['type_item'] == "R":
                    honorary.total_repayment = honorary.total_repayment + new_value
                    honorary.total_debit_credit = honorary.total_debit_credit + new_value
                    honorary.total_honorary = honorary.total_honorary - new_value
                else:
                    pass

                honorary.updated_by_id = request.user.id
                honorary.updated_by_name = request.user.get_full_name()
                honorary_response = self.execute(honorary, honorary.save, extra_fields=['item__nome','created_by__get_full_name','updated_by__get_full_name'])
                if honorary_response['result']:
                    response_dict['message'] = 'Honorário salvo com sucesso!'
                else:
                    response_dict['message'] = 'Erro! Registro salvo mas houve uma falha ao tentar recalcular o honorário.'
            else:
                response_dict = {}
                response_dict['result'] = False
                response_dict['object'] = None
                response_dict['message'] = "Erro! Honorário informado não existe."

        print("VEJA A SAIDA: ",response_dict)
        return self.response(response_dict)

    @method_decorator(login_required)
    def delete_honorary_item(self, request):
        try:
            object = HonoraryItem.objects.get(pk=int(request.POST['id']))
            honorary = object.honorary
            response_dict = self.delete_object(request, object, is_response=False)
        except Exception as erro:
            response_dict = self.notify.error(erro)

        if response_dict['result']:
            honorary = honorary.verify_contract_values(honorary=honorary, contract=honorary.contract)
            honorary.verify_provents_values()
            honorary.updated_by_id = request.user.id
            honorary.updated_by_name = request.user.get_full_name()
            honorary_response = self.execute(honorary, honorary.save, extra_fields=['item__nome', 'created_by__get_full_name', 'updated_by__get_full_name'])
            if honorary_response['result']:
               response_dict['message'] = 'Honorário salvo com sucesso!'
            else:
               response_dict['message'] = 'Erro! Registro salvo mas houve uma falha ao tentar recalcular o honorário.'

        print("VEJA A SAIDA: ", honorary_response)
        return self.response(honorary_response)

    @method_decorator(login_required)
    def get_provent_options(self, request):
        queryset = Proventos.objects.filter(id__gt=3)
        return BaseController().filter(request,model=Proventos,queryset=queryset,order_by='-pk')

    @method_decorator(login_required)
    def get_honorary_item(self, request):
        self.start_process(request)
        queryset = HonoraryItem.objects.filter(honorary_id=int(request.POST['id']))
        return BaseController().filter(request, Honorary,queryset=queryset, extra_fields=['item__nome','created_by__get_full_name','updated_by__get_full_name'])

    @method_decorator(login_required)
    def generate_document(self, request, honorary_id):
        print("VEJA O REQUEST: ",request, honorary_id)
        path = os.path.join(BASE_DIR, "static/imagens/")

        #parametros_emissor = criar_parametro_entidade_para_protocolo(1)
        #protocolo_selecionado = protocolo.objects.get(pk=protocolo_id)

        #documentos = item_protocolo.objects.filter(protocolo_id=protocolo_id)

        """
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
        """


        """destinatario_nome = p.destinatario.nome_razao
            destinatario_endereco = p.destinatario.endereco.get_endereco()
            destinatario_cpf_cnpj = formatar_cpf_cnpj(p.destinatario.cpf_cnpj)
            destinatario_contatos = contatos
            destinatario_complemento = p.destinatario.endereco.complemento.title()
        """

        """
        if protocolo_selecionado.doc_receptor != None:
            documento_receptor = protocolo_selecionado.doc_receptor

        else:
            documento_receptor = ""
        """

        #linhas_extras = [1] * (10 - len(documentos))

        date_hour_emission = datetime.datetime.now().strftime('%d/%m/%Y ÀS %H:%M:%S')
        company = entidade.objects.get(pk=1)
        company_contacts = contato.objects.filter(entidade=company)[:2]

        honorary = Honorary.objects.get(pk=int(honorary_id))
        client = honorary.entity
        client_contacts = contato.objects.filter(entidade=client)[:2]

        documentos = HonoraryItem.objects.filter(honorary=honorary)


        valor_liquido = honorary.total_honorary - honorary.total_repayment

        if honorary.contract is not None:
            vencimento = honorary.contract.dia_vencimento
            data_atual = datetime.datetime.now().strftime('/%m/%Y')
            if len(vencimento) == 1:
                vencimento = "0"+str(vencimento)+data_atual
            else:
                vencimento = str(vencimento)+data_atual
        else:
             vencimento = " "

        contract_unit_value = None
        contract_temporary_discount_rate = None
        contract_temporary_discount_value = None

        contract_fidelity_discount_rate = None
        contract_fidelity_discount_value= None

        if honorary.contract is not None:
            if honorary.contract.ativo:
                if honorary.contract.valor_honorario != 0:
                    contract_unit_value = honorary.contract.valor_honorario

                if honorary.contract.desconto_temporario_ativo is not None and honorary.contract.desconto_temporario_ativo > 0:
                    contract_temporary_discount_rate = honorary.contract.desconto_temporario_ativo
                    contract_temporary_discount_value = round(float(contract_unit_value) * (float(contract_temporary_discount_rate)/100.0), 2)

                if honorary.contract.desconto_indicacoes is not None and honorary.contract.desconto_indicacoes > 0:
                    contract_fidelity_discount_rate = honorary.contract.desconto_indicacoes
                    contract_fidelity_discount_value = round(float(contract_unit_value) * (float(honorary.contract.desconto_indicacoes)/100.0), 2)

        linhas_extras = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        offset = 0
        if documentos.count() < 10:
            if contract_unit_value is not None:
                offset = offset + 1
            if contract_temporary_discount_rate is not None:
                offset = offset + 1
            if contract_fidelity_discount_rate is not None:
                offset = offset + 1
            linhas_extras = linhas_extras[documentos.count()+offset:10]

        else:
            linhas_extras = []

        #contrato = None
        #if honorary.contract is not None:
        #    if honorary.contract.ativo:
        #        if honorary.contract.valor_honorario != 0:
        #            contrato = {'description': 'HONORÁRIOS CONTÁBEIS CONF. CONTRATO - ' + Honorary.competence, 'quantity': '1,00', 'unit_value': honorary.contract.valor_honorario}








        parametros = {
            'emissor_nome': company.nome_razao, #parametros_emissor.nome,
            'emissor_cpf_cnpj': formatar_cpf_cnpj(company.cpf_cnpj), #parametros_emissor.nome,formatar_cpf_cnpj(parametros_emissor.cpf_cnpj),
            'emissor_endereco': company.endereco.get_endereco(), #parametros_emissor.nome,parametros_emissor.endereco,
            'emissor_complemento': company.endereco.complemento.title(), #parametros_emissor.nome,parametros_emissor.complemento,
            'emissor_contatos': company_contacts, #parametros_emissor.nome,parametros_emissor.contatos,
            'destinatario_nome': client.nome_razao, #parametros_emissor.nome,parametros_destinatario.nome,
            'destinatario_cpf_cnpj': formatar_cpf_cnpj(client.cpf_cnpj), #parametros_emissor.nome,formatar_cpf_cnpj(parametros_destinatario.cpf_cnpj),
            'destinatario_endereco': client.endereco.get_endereco(), #parametros_emissor.nome,parametros_destinatario.endereco,
            'destinatario_complemento': client.endereco.complemento.title(), #parametros_emissor.nome,parametros_destinatario.complemento,
            'destinatario_contatos': client_contacts, #parametros_emissor.nome,parametros_destinatario.contatos,
            'honorary': honorary,

            'contract_unit_value':contract_unit_value,
            'contract_temporary_discount_rate':contract_temporary_discount_rate,
            'contract_temporary_discount_value': contract_temporary_discount_value,
            'contract_fidelity_discount_rate':contract_fidelity_discount_rate,
            'contract_fidelity_discount_value':contract_fidelity_discount_value,


            'valor_liquido':valor_liquido,
            'vencimento':vencimento,


            'emitido_por': request.user.get_full_name(), #parametros_emissor.nome,protocolo_selecionado.emitido_por.title(),
            'data_emissao': date_hour_emission, #parametros_emissor.nome,protocolo_selecionado.data_emissao,

            'recebido_por': "", #parametros_emissor.nome,protocolo_selecionado.recebido_por,  # recebido_por,
            'identificacao': "", #parametros_emissor.nome,protocolo_selecionado.doc_receptor if protocolo_selecionado.doc_receptor != None else "",
            'data_entrega': "", #parametros_emissor.nome,protocolo_selecionado.data_recebimento,  # data_entrega,
            'hora_entrega': "", #parametros_emissor.nome,protocolo_selecionado.hora_recebimento,  # hora_entrega,

            'documentos': documentos, #parametros_emissor.nome,documentos,  # formulario.temporarios,
            'linhas_extras': linhas_extras,  # 'documentos':[
            #                  ["33","IMPOSTO DE RENDA","2015","","R$ 285,50"],
            #                  ["8","EMISSAO DE CERTIFICADO DIGITAL","","31/12/2018","R$ 175,10"],
            #                  ["14","CONTRATO - PLANO COMPLETO","","31/12/2018","R$ 475,00"],
            #              ],
            # 'formulario_protocolo':"Nada por enquanto",
            # 'erro':"sem erros tambem",
            # 'path':path,

            'path_imagens': path

            }

        from django_xhtml2pdf.utils import generate_pdf
        resp = HttpResponse(content_type='application/pdf')
        result = generate_pdf('honorario/honorary_report.html', file_object=resp, context=parametros)
        return result


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