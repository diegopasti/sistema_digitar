# -*- encoding: utf-8 -*-
import datetime, json, os
from decimal import Decimal
from django.contrib import messages
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from django.http.response import Http404,HttpResponse, HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.shortcuts import render
from libs.default.core import BaseController
from libs.default.decorators import request_ajax_required, permission_level_required
from modules.entidade.models import informacoes_juridicas, informacoes_tributarias, AtividadeEconomica, localizacao_simples, Documento  # , localizacao , Endereco, Municipio, Bairro, Logradouro,
from modules.entidade.models import entidade, contato
from modules.entidade.service import consultar_codigo_postal_viacep  # consultar_codigo_postal_default
from modules.entidade.utilitarios import remover_simbolos  # formatar_codificacao,
from modules.entidade.formularios import formulario_cadastro_entidade_completo, formulario_justificar_operacao


def verificar_cadastro_empresa():
    registros = entidade.objects.count()
    if registros == 0:
        from modules.nucleo.initial_data import precarregar_dados_digitar, precarregar_referencias_documentos
        precarregar_dados_digitar()
        precarregar_referencias_documentos()
        return True
    else:
        return True

@login_required
def index(request):
    if verificar_cadastro_empresa():
        #from modules.core.services import NotificationsControl
        #NotificationsControl().generate_notifications()
        return render(request,"blank.html")
    else:
        return HttpResponseRedirect('/cadastrar_empresa')


def buscar_fontes(request):
    return render(request,"index.html")

@login_required
#permission_level_required(3,'/error/access_denied')
def cadastro_entidades(request):
    usuario_admin = False
    dados = entidade.objects.exclude(id=1).exclude(ativo=False).order_by('nome_razao')
    if (request.method == "POST"):

        """
        COM A EXCLUSÃO EM AJAX A FLUIDEZ MELHOROU MUITO E ESSE CODIGO JA NAO É MAIS NECESSARIO.

        form_desativar = formulario_justificar_operacao(request.POST, request.FILES)
        if form_desativar.is_valid():



            tipo_operacao = form_desativar['operacao'].value()
            operacao_tabela = form_desativar['tabela'].value()
            operacao_user = form_desativar['user'].value()

            operacao_cliente = int(form_desativar['cliente'].value())
            operacao_descricao = form_desativar['descricao'].value()
            operacao_justificativa = form_desativar['justificativa'].value().upper()

            cliente = entidade.objects.get(pk=operacao_cliente)

            print("olha o cliente: ",cliente)


            operacao = OperacaoRestrita()

            operacao.user = None
            operacao.tipo = tipo_operacao

            operacao.tabela = operacao_tabela
            operacao.descricao = operacao_descricao
            operacao.entidade = cliente
            operacao.justificativa = operacao_justificativa

            #operacao.save()
            messages.add_message(request, messages.SUCCESS, "Registro desativado com sucesso!")
            form_desativar = formulario_justificar_operacao()

        else:
            msg = verificar_erro(form_desativar)
            messages.add_message(request, messages.SUCCESS,msg)

        """

    else:
        form_desativar = formulario_justificar_operacao()
        # formulario_contato  = form_adicionar_contato()

    return render(request,"entidade/cadastro_entidades.html",{'dados': dados, 'form_desativar': form_desativar, 'erro': False})

class EntityController (BaseController):
    @request_ajax_required
    @method_decorator(login_required)
    def desativar_cliente(self,request):
        return self.disable(request,entidade)

        '''if request.is_ajax():
            cliente = entidade.objects.get(pk=int(cliente))
            operacao = RestrictedOperation()
            operacao.tipo = "DES"
            operacao.tabela = "ENTIDADE"
            operacao.entidade = cliente
    
            if request.user.is_anonymous():
                operacao.user = None
            else:
                operacao.user = request.user
    
            # POR ENQUANTO NAO PODEMOS UTILIZAR ACENTUAÇÃO NESSA DESCRICAO
            operacao.descricao = "DESATIVACAO DO CLIENTE "+cliente.nome_razao+" ("+cliente.cpf_cnpj+") DO SISTEMA."
            operacao.justificativa = list(request.GET)[0].upper()
    
            #print("Tentano excluir: ", operacao.descricao,operacao.justificativa)
    
            try:
                operacao.save()
                cliente.ativo = False
                cliente.save()
                data = json.dumps("sucesso")
            except:
                data = None
    
            return HttpResponse(data, content_type='application/json')
    
        else:
            raise Http404
            '''

@login_required
def novo_buscar_lista_clientes(request):
    #if request.is_ajax():
    clientes = entidade.objects.all().filter(ativo=True)#.exclude(id=1).order_by('-id')
    dados = []
    for item in clientes:
        nome_cliente = str(item.id)+" - "+item.nome_razao
        if item.nome_filial != None and item.nome_filial != "":
            nome_cliente = nome_cliente + " (" + item.nome_filial + ")"

        registro = {}
        registro["id"] = str(item.id)
        registro["name"] = nome_cliente.upper()
        dados.append(registro)

    data = json.dumps(dados)
    return HttpResponse(data, content_type='application/json')
    #else:
    #    raise Http404

def buscar_entidades(request):
    resultado = entidade.objects.all()
    results = []
    for item in resultado:
        dado = {}
        dado['cliente'] = item.nome_razao
        results.append(dado)
        
    texto = json.dumps(results)

    return HttpResponse(texto)


def formatar_cep(cep):
    novo_cep = cep[:2]+"."+cep[2:5]+"-"+cep[5:]    
    return novo_cep

def formatar_cpf(cpf):
    novo_cpf = cpf[:3]+"."+cpf[3:6]+"."+cpf[6:9]+"-"+cpf[9:]
    return novo_cpf

def formatar_cpfcnpj(codigo):
    if len(codigo) == 11:
        return formatar_cpf(codigo)
    else:
        return formatar_cnpj(codigo)

def formatar_cnpj(cnpj):
    novo_cnpj = cnpj[:2]+"."+cnpj[2:5]+"."+cnpj[5:8]+"/"+cnpj[8:12]+"-"+cnpj[12:]
    return novo_cnpj

def construir_endereco(localizacao):
    comp = localizacao.complemento
    num  = localizacao.numero

    localizacao = localizacao_simples.objects.get(pk=localizacao.cep_id)
    rua = localizacao.logradouro
    bairro = localizacao.bairro #Bairro.objects.get(pk=rua.bairro_id)
    cidade = localizacao.municipio #Municipio.objects.get(pk=Bairro.municipio_id)
    estado = localizacao.estado #""#Estado.objects.get(pk=Cidade.estado_id)
    
    
    endereco_completo = rua.nome+", "+num+", "+comp+", "+bairro+", "+cidade+", "+estado+" - "+formatar_cep(rua.cep)
    return endereco_completo


def gerar_pdf(request):
    from django.template import Context# loader,, Template
    #from xhtml2pdf import pisa
   
    parametros = {'emissor':"Digitar Contabilidade",
                          'destinatario':"HELDER PASTI",
                          'endereco_destinatario':"Rua demósthenes Nunes Vieira, 60, Alto Lage, Cariacica - ES",
                          'endereco_emissor':"Reta da Penha, Vitória - ES",
                          'codigo_protocolo':"P102",
                          'documentos':[
                                            ["33","IMPOSTO DE RENDA","2015","","R$ 285,50"],
                                            ["8","EMISSÃO DE CERTIFICADO DIGITAL","","31/12/2018","R$ 175,10"],
                                            ["14","CONTRATO - PLANO COMPLETO","","31/12/2018","R$ 475,00"],
                                        ],
                          'formulario_protocolo':"Nada por enquanto",
                           'erro':"sem erros tambem"}
    
    c = Context(parametros)#{'message': 'Your message'})
    from django_xhtml2pdf.utils import generate_pdf
    resp = HttpResponse(content_type='application/pdf')
    result = generate_pdf('protocolo/novo_protocolo.html', file_object=resp,context=c)
    return result
"""
def link_callback(uri, rel):
    
    #Convert HTML URIs to absolute system paths so xhtml2pdf can access those
    #resources
    
    # use short variable names
    sUrl = settings.STATIC_URL      # Typically /static/
    sRoot = settings.STATIC_ROOT    # Typically /home/userX/project_static/
    mUrl = settings.MEDIA_URL       # Typically /static/media/
    mRoot = settings.MEDIA_ROOT     # Typically /home/userX/project_static/media/

    # convert URIs to absolute system paths
    if uri.startswith(mUrl):
        path = os.path.join(mRoot, uri.replace(mUrl, ""))
    elif uri.startswith(sUrl):
        path = os.path.join(sRoot, uri.replace(sUrl, ""))
    else:
        return uri  # handle absolute uri (ie: http://some.tld/foo.png)

    # make sure that file exists
    if not os.path.isfile(path):
            raise Exception(
                'media URI must start with %s or %s' % (sUrl, mUrl)
            )
    return path
"""    

def validar_objeto(registro):
    print("Campo: ",registro)
    
    print(registro.documento,",",registro.referencia,",",registro.vencimento,",",registro.valor,",",registro.protocolo.emissor.nome_razao)
    
    try:
        registro.full_clean()
        print("passei aqui")
        return True     

    except Exception as e:
        print("Deu pau..",e.message_dict)
        return e.message

@login_required
def consultar_entidade(request,entidade_id):
    
    registro_entidade = entidade.objects.get(pk=entidade_id)
    
    if (request.method == "POST"):
        formulario = formulario_cadastro_entidade_completo()
    else:
        
        dados = {'cpf_cnpj':registro_entidade.cpf_cnpj,
                 'nome_razao':registro_entidade.nome_razao,
                 'apelido_fantasia':registro_entidade.apelido_fantasia,
                 'tipo_registro':registro_entidade.tipo_registro,
                 'nascimento_fundacao':registro_entidade.nascimento_fundacao
                }
        
        formulario = formulario_cadastro_entidade_completo(dados)
        
        
        
    return render(request,"consultar_entidade.html",{'dados':registro_entidade,'formulario':formulario,'erro':False})








def validar_registro(registro):
    msg = ""
    try:
        registro.full_clean()
        msg = "SUCESSO"
    
    except ValidationError as excecao:   
        msg = "Erro! "+excecao.message
        
    except IntegrityError as excecao:
        if "cpf_cnpj" in excecao.message:
            msg = "Erro! cpf ou cnpj já existe no cadastro!"
        
        else:
            msg = excecao.message

        return msg,""
    
    finally:
        return False,""

@login_required
def visualizar_entidade(request,id):
    print("QUERO PEGAR OS CONTATOS DO CLIENTE: ",id)
    cliente = entidade.objects.get(pk=id)
    meus_contatos = contato.objects.filter(entidade=cliente)
    print("VEJA OS CONTATOS: ",meus_contatos)
    minhas_atividades = AtividadeEconomica.objects.filter(entidade=cliente)
    #contatos_serializado = serializar_contatos(meus_contatos)
    #atividades_serializadas = serializar_atividades(minhas_atividades)
    meus_documentos = Documento.objects.filter(entidade=cliente)
    url = request.get_full_path()
    print(url)
    tab = os.path.basename(url)
    print(tab)

    if 'contatos' == tab:
        tab_active = 'tab_contatos'
    elif 'atividades' == tab:
        tab_active = 'tab_cnae'
    elif 'controles' == tab:
        tab_active = 'tab_servicos'
    else:
        tab_active = 'tab_client'

    if (request.method == "POST"):
        from modules.entidade.models import localizacao_simples
        formulario = formulario_cadastro_entidade_completo(request.POST, request.FILES)
        try:
            endereco = localizacao_simples.objects.get(id=cliente.endereco.id)
        except:
            endereco = localizacao_simples()

        if formulario.is_valid():
            #print("olha, estou querendo alterar:")
            #lista_objetos = load_objects_from_form(formulario,cliente,cliente.endereco,meus_contatos,minhas_atividades)

            cliente.cpf_cnpj = remover_simbolos(formulario.cleaned_data['cpf_cnpj'])
            cliente.nome_razao = formulario.cleaned_data['nome_razao'].upper()
            cliente.apelido_fantasia = formulario.cleaned_data['apelido_fantasia'].upper()
            cliente.tipo_registro = "C"
            cliente.nascimento_fundacao = formulario.cleaned_data['nascimento_fundacao']
            cliente.registro_geral = formulario.cleaned_data['registro_geral']

            cliente.inscricao_estadual = formulario.cleaned_data['inscricao_estadual']
            cliente.inscricao_municipal = formulario.cleaned_data['inscricao_municipal']
            cliente.inscricao_produtor_rural = formulario.cleaned_data['inscricao_produtor_rural']
            cliente.inscricao_imovel_rural = formulario.cleaned_data['inscricao_imovel_rural']

            cliente.nome_filial = formulario.cleaned_data['nome_filial']
            cliente.natureza_juridica = formulario.cleaned_data['natureza_juridica']
            cliente.regime_apuracao = formulario.cleaned_data['regime_apuracao']
            cliente.regime_desde = formulario.cleaned_data['regime_desde']
            cliente.tipo_vencimento_iss = formulario.cleaned_data['tipo_vencimento']
            cliente.data_vencimento_iss = formulario.cleaned_data['data_vencimento_iss']
            cliente.dia_vencimento_iss = formulario.cleaned_data['dia_vencimento_iss']
            cliente.taxa_iss = formulario.cleaned_data['taxa_iss']
            cliente.inscricao_junta_comercial = formulario.cleaned_data['inscricao_junta_comercial']
            try:
                cliente.taxa_iss = Decimal(formulario.cleaned_data['taxa_iss'].replace('.','').replace(',','.'))
            except:
                cliente.taxa_iss = formulario.cleaned_data['taxa_iss']

            cliente.responsavel_cliente = formulario.cleaned_data['responsavel_cliente']
            cliente.supervisor_cliente = formulario.cleaned_data['supervisor_cliente']

            cliente.notificacao_email = formulario.cleaned_data['notificacao_email'].lower()
            cliente.notificacao_responsavel = formulario.cleaned_data['notificacao_responsavel'].upper()
            cliente.notificacao_envio = formulario.cleaned_data['notificacao_envio']
            cliente.observacoes = formulario.cleaned_data['observacoes'].upper()

            endereco.cep         = formulario.cleaned_data['cep']
            endereco.codigo_ibge = formulario.cleaned_data['codigo_municipio']
            endereco.complemento = formulario.cleaned_data['complemento']
            endereco.logradouro  = formulario.cleaned_data['endereco']
            endereco.numero      = formulario.cleaned_data['numero_endereco']
            endereco.bairro      = formulario.cleaned_data['bairro']
            endereco.municipio   = formulario.cleaned_data['municipio']
            endereco.estado      = formulario.cleaned_data['estado']
            endereco.pais        = formulario.cleaned_data['pais']
            endereco.save()

            cliente.save()

            contatos = formulario.cleaned_data['contatos']
            contatos = contatos.split("#")

            for item in contatos:
                item = item.replace("undefined", "")
                if "|" in item:
                    dados = item.split("|")
                    #print("OLHA OS CAMPOS NA HORA DE CONSTRUIR O CONTATO:", dados)

                    if "+" in dados[0]:
                        registro = contato(
                            nome_contato=cliente.nome_razao,
                            tipo_contato=dados[1],
                            numero=dados[2],
                            cargo_setor=dados[4].upper(),
                            email=dados[5].lower(),
                            entidade=cliente
                        )
                        registro.save()

                    elif "-" in dados[0]:
                        if dados[1] != "-":
                            excluir_id = int(dados[0].replace("-","")) # int(dados[0][1:])

                            try:
                                contato_excluir = contato.objects.get(id=excluir_id)
                                contato_excluir.delete()
                            except:
                                #print("Erro! Não foi possivel excluir o contato %s, tente novamente."%(str(excluir_id)))
                                msg = "Erro! Não foi possivel excluir o contato %s, tente novamente."%(str(contato.objects.get(id=excluir_id)))
                        else:
                            pass#print("O usuario pode ter apagado muitos contatos de vez..")
                    else:
                        pass#print("MANTER")

            atividades = formulario.cleaned_data['atividade_economica']
            if atividades != "":
                atividades = atividades.split("#")
                for item in atividades:
                    item = item.replace("undefined", "")
                    dados = item.split("|")

                    if "+" in dados[0]:
                        registro = AtividadeEconomica()
                        registro.atividade = dados[1]
                        registro.entidade = cliente

                        try:
                            data = dados[2]
                            registro.desde = data
                            registro.desde = datetime.datetime.strptime(data, "%d/%m/%Y").date()
                        except:
                            registro.desde = None

                        registro.save()

                    elif "-" in dados[0]:
                        excluir_id = int(dados[0][1:])
                        try:
                            atividade_excluir = AtividadeEconomica.objects.get(id=excluir_id)
                            atividade_excluir.delete()
                        except:
                            # print("Erro! Não foi possivel excluir o contato %s, tente novamente."%(str(excluir_id)))
                            msg = "Erro! Não foi possivel excluir o contato %s, tente novamente." % (
                            str(atividade_excluir.objects.get(id=excluir_id)))


                    else:
                        pass  # print("MANTER")

            documentos = formulario.cleaned_data['tabela_documentos']

            if documentos != "":
                documentos = documentos.split("#")
                #print("VEJA O QUE CHEGOU: ")
                for item in documentos:
                    dados = item.split("|")
                    #print(">>>",dados)

                    if "+" in dados[0] or "@" in dados[0]:
                        registro = Documento()
                        registro.tipo = dados[1].upper()
                        registro.nome = dados[2].upper()
                        registro.tipo_vencimento = dados[3].upper()
                        registro.senha = dados[5]
                        if dados[6] == "SIM":
                            registro.notificar_cliente = True
                        else:
                            registro.notificar_cliente = False

                        if dados[7] == "":
                            registro.prazo_notificar = None
                        else:
                            registro.prazo_notificar = dados[7]
                        registro.criado_por = request.user
                        #registro.vencimento = dados
                        registro.entidade = cliente

                        if "@" in dados[0]:
                            registro.ativo = False
                            registro.data_finalizado = datetime.datetime.now()
                            registro.finalizado_por = request.user

                        try:
                            registro.vencimento = datetime.datetime.strptime(dados[4], "%d/%m/%Y").date()
                        except:
                            registro.vencimento = None

                        registro.save()

                    elif "-" in dados[0]:

                        excluir_id = int(dados[0][1:])
                        try:
                            registro_excluir = Documento.objects.get(id=excluir_id)
                            registro_excluir.delete()
                        except:
                            # print("Erro! Não foi possivel excluir o contato %s, tente novamente."%(str(excluir_id)))
                            msg = "Erro! Não foi possivel excluir o documento, tente novamente."

                    elif "*" in dados[0]:
                        try:
                            registro = Documento.objects.get(pk=int(dados[0][1:]))
                        except:
                            registro = None

                        if registro is not None:
                            #from django.utils.timezone import now, localtime
                            registro.ativo = False
                            registro.data_finalizado = datetime.datetime.now() #localtime(now())
                            registro.finalizado_por = request.user
                            registro.save()
                        pass


                    else:
                        # nenhuma alteracao no item da tabela.
                        pass


            else:
                print("Nao tem documentos pra monitorar")

            #for cnae in registro_cnae:
            #    cnae.entidade = registro_entidade
            #    cnae.save()

            msg = "Cliente alterado com sucesso!"
            messages.add_message(request, messages.SUCCESS, msg)

            return HttpResponseRedirect('/entidade')

        else:
            msg = verificar_erro(formulario)

        #print("vim pra ca..")
        messages.add_message(request, messages.SUCCESS, msg)

    else:
        cliente = entidade.objects.get(pk=id)
        meus_contatos = contato.objects.filter(entidade=cliente)
        minhas_atividades = AtividadeEconomica.objects.filter(entidade=cliente)
        meus_documentos = Documento.objects.filter(entidade=cliente)
        contatos_serializado = serializar_contatos(meus_contatos)
        print("VEJA SO OS CONTATOS SERIALIZADO JOVEM: ",contatos_serializado)
        atividades_serializadas = serializar_atividades(minhas_atividades)
        documentos_serializados = serializar_documentos(meus_documentos)
        #print("olha minhas atividades:",minhas_atividades)


        if cliente.responsavel_cliente != None:
            responsavel_cliente = cliente.responsavel_cliente.id
        else:
            responsavel_cliente = None

        if cliente.supervisor_cliente != None:
            supervisor_cliente = cliente.supervisor_cliente.id
        else:
            supervisor_cliente = None

        #formulario_contrato = FormularioContrato()

        formulario = formulario_cadastro_entidade_completo(initial={
                        'cpf_cnpj':cliente.cpf_cnpj,
                        'nome_razao':cliente.nome_razao,
                        'apelido_fantasia':cliente.apelido_fantasia,
                        'nascimento_fundacao':cliente.nascimento_fundacao,
                        'natureza_juridica':cliente.natureza_juridica,
                        'regime_apuracao':cliente.regime_apuracao,
                        'regime_desde': cliente.regime_desde,
                        'nome_filial': cliente.nome_filial,
                        'inscricao_estadual': cliente.inscricao_estadual,
                        'inscricao_municipal': cliente.inscricao_municipal,
                        'inscricao_junta_comercial': cliente.inscricao_junta_comercial,
                        'inscricao_produtor_rural': cliente.inscricao_produtor_rural,
                        'inscricao_imovel_rural' : cliente.inscricao_imovel_rural,
                        'cep': cliente.endereco.cep,
                        'endereco': cliente.endereco.logradouro,
                        'bairro': cliente.endereco.bairro,
                        'municipio': cliente.endereco.municipio,
                        'estado': cliente.endereco.estado,
                        'pais':cliente.endereco.pais,
                        'numero_endereco': cliente.endereco.numero,
                        'complemento':cliente.endereco.complemento,
                        'codigo_municipio': cliente.endereco.codigo_ibge,

            'contatos': contatos_serializado,
            'atividade_economica':atividades_serializadas,

            'tipo_vencimento': cliente.tipo_vencimento_iss,
            'data_vencimento_iss': cliente.data_vencimento_iss,
            'dia_vencimento_iss': cliente.dia_vencimento_iss,
            'taxa_iss':cliente.taxa_iss,

            'responsavel_cliente': responsavel_cliente,
            'supervisor_cliente':supervisor_cliente,

            'notificacao_email': cliente.notificacao_email,
            'notificacao_envio': cliente.notificacao_envio,
            'notificacao_responsavel': cliente.notificacao_responsavel,
            'tabela_documentos':documentos_serializados,
            'observacoes':cliente.observacoes

            }
        )

    return render(request,"entidade/adicionar_entidade.html",
                          {'dados': [],
                            'formulario_entidade': formulario,
                            'meus_contatos':meus_contatos,
                            'minhas_atividades':minhas_atividades,
                            'meus_documentos':meus_documentos,
                            'naturezas_juridicas':informacoes_juridicas.natureza_juridica,
                            'atividades_economicas':informacoes_tributarias.atividades_economicas,
                            'tab_active':tab_active,
                            'erro': False},
                          )

@login_required
def adicionar_entidade(request):
    url = request.get_full_path()
    print(url)
    tab = os.path.basename(url)
    print(tab)

    if 'contatos' == tab:
        tab_active = 'tab_contatos'
    elif 'atividades' == tab:
        tab_active = 'tab_cnae'
    elif 'controles' == tab:
        tab_active = 'tab_servicos'
    else:
        tab_active = 'tab_client'

    if (request.method == "POST"):
        #print("VEJA O QUE VEIO: ",request.POST)
        formulario = formulario_cadastro_entidade_completo(request.POST, request.FILES)
        #formulario_contrato = FormularioContrato(request.POST, request.FILES)

        #if formulario_contrato.is_valid():
        #    print("OLHA O FORMULARIO DO CONTRATO TA OK")
        #else:
        #    print("VEJA OS CAMPOS LIMPOS: ",formulario_contrato.cleaned_data)
        #    print("VEJA OS ERROS: ",formulario_contrato.errors)

        erro = False
        msg  = ""

        #print("olha o documento:",formulario.documentos)

        if formulario.is_valid():
            registro_entidade    = formulario.get_entidade(formulario)
            registro_contato     = formulario.get_contatos(formulario, registro_entidade)
            registro_localizacao = formulario.get_localizacao(formulario)
            #print("OLHA O FORM DE LOCALIZAÇÃO:",registro_localizacao)
            registro_cnae        = formulario.get_cnae(formulario)

            registro_documentos  = formulario.get_documentos(formulario)
            registro_contrato    = formulario.get_contrato(formulario)
            #print("Olha os contrato: ",registro_contrato)

            #print("Tentar validar o contrato: ",validar_registro(registro_contrato))

            #print("Olha as validacoes: ", registro_entidade, "-", registro_contato, "-", registro_localizacao)
            if validar_registro(registro_entidade) and validar_registro(registro_contato) and validar_registro(registro_localizacao) and validar_registro(registro_cnae):
                try:
                    registro_localizacao.save()
                    registro_entidade.endereco = registro_localizacao
                    registro_entidade.save()

                    for contato in registro_contato:
                        contato.entidade = registro_entidade
                        contato.save()

                    for cnae in registro_cnae:
                        cnae.entidade = registro_entidade
                        cnae.save()

                    for documento in registro_documentos:
                        documento.entidade = registro_entidade
                        documento.save()
                        #print("Salvei um documento?",documento.nome)


                    msg = "Cliente cadastrado com sucesso!"
                    #formulario = formulario_cadastro_entidade_completo()
                    return HttpResponseRedirect('/entidade')

                except Exception as e:
                    msg = 'Erro! Exceção:' + str(e)
                    print("Erro! Excecao:",msg)

            else:
                #print("deu pau na validacao")
                msg = "Erro! Existem Campos preenchidos incorretamente."

        else:
            msg = verificar_erro(formulario)
            if "Contatos: Precisa ser Informado!" in msg:
                msg = "Erro! Pelo menos um contato deve ser informado."
            print(msg)

        messages.add_message(request, messages.SUCCESS,msg)
    else:
        formulario = formulario_cadastro_entidade_completo()
        #formulario_contrato = FormularioContrato()

    return render(request,"entidade/adicionar_entidade.html",
                              {'dados': [], 'formulario_entidade': formulario, 'naturezas_juridicas':informacoes_juridicas.natureza_juridica, 'atividades_economicas':informacoes_tributarias.atividades_economicas, 'tab_active': tab_active, 'erro': False},
                              )

def load_objects_from_form(formulario,cliente,endereco,contatos,cnaes):
    registro_localizacao = formulario.get_localizacao(formulario,endereco)
    print("VALIDANDO A LOCALIZACAO:", validar_objeto(registro_localizacao))

    registro_entidade = formulario.get_entidade(formulario,cliente)
    print("VALIDANDO A ENTIDADE:", validar_objeto(registro_entidade))

    registro_contatos = formulario.get_contatos(formulario, cliente)
    print("VALIDANDO OS CONTATOS:", validar_objeto(registro_entidade))

    registro_entidade = formulario.get_cnae(formulario, cliente)
    print("VALIDANDO OS CNAES:", validar_objeto(registro_entidade))

def create_objects_from_form(formulario):
    registro_localizacao = formulario.get_localizacao(formulario)
    print("VALIDANDO A LOCALIZACAO:", validar_objeto(registro_localizacao))

    registro_entidade    = formulario.get_entidade(formulario)
    print("VALIDANDO A ENTIDADE:",validar_objeto(registro_entidade))

    registro_contato     = formulario.get_contatos(formulario, registro_entidade)

    for item in registro_contato:
        print("VALIDANDO OS CONTATOS:", validar_objeto(item))

    registro_cnae        = formulario.get_cnae(formulario)
    for item in registro_cnae:
        print("VALIDANDO OS CNAES:", validar_objeto(item))

    registros = [registro_entidade,registro_contato,registro_localizacao,registro_cnae]
    return registros

def validar_objetos_formulario(lista_objetos):
    lista_erros = []
    resultado_geral = True
    for item in lista_objetos:
        print("Olha o que eu quero validar: ",item,type(item))
        if type(item) == list:
            for elemento in item:
                resultado, problemas = validar_objeto(elemento)
                if resultado == False:
                    print("Subitem com problemas:",elemento,problemas)
                    lista_erros = lista_erros + problemas
                    resultado_geral = resultado
        else:
            resultado, problemas = validar_objeto(item)

        if resultado == False:
            print (item)
            lista_erros.append(problemas)
            resultado_geral = resultado

    return resultado_geral,lista_erros


def validar_objeto(registro):
    try:
        registro.full_clean()
        return True,""

    except ValidationError as excecao:
        lista_problemas = dict(excecao).items()
        #for item in lista_problemas:
        #    print("Veja o problema:",item)
        #print("o erro:",list())
        return False, lista_problemas


    """except ValidationError as excecao:
        msg = "Erro! " + excecao.message

    except IntegrityError as excecao:
        if "cpf_cnpj" in excecao.message:
            msg = "Erro! cpf ou cnpj já existe no cadastro!"

        else:
            msg = excecao.message

        return msg, ""

    finally:
        return False, ""

    """

def salvar_atividades(registro_contato,registro_entidade):
    try:
        for contato in registro_contato:
            contato.entidade = registro_entidade
            contato.save()
        return True
    except:
        return False

def salvar_contatos(registro_cnae,registro_entidade):
    try:
        for cnae in registro_cnae:
            cnae.entidade = registro_entidade
            cnae.save()
        return True
    except:
        return False

def serializar_contatos(dados):
    resultado = ''
    print("VEJA MEUS CONTATOS: ",dados)
    for item in dados:
        resultado = resultado + str(item.id)+'|'+item.tipo_contato +'|'+item.numero+'|'+item.nome_contato+'|'+item.cargo_setor+'|'+item.email+'#'
        #u'RESIDENCIAL|(27) 3043-0703|undefined|undefined#'
        #print("serializar: ",item)
    return resultado

def serializar_documentos(dados):
    resultado = ''
    for item in dados:

        if item.vencimento == None:
            vencimento = ""
        else:
            vencimento = str(item.vencimento.strftime('%d/%m/%Y'))

        if item.notificar_cliente:
            notificar_cliente = 'SIM'
        else:
            notificar_cliente = 'NAO'

        registro = str(item.id) + '|' + item.tipo + '|' +item.nome + '|' + vencimento + "|"+ item.senha +'|'+notificar_cliente+'|'+str(item.prazo_notificar)+'#'
        resultado = resultado + registro
    return resultado

def serializar_atividades(dados):
    resultado = ''
    #print("olha os cnaes: ",dados)
    for item in dados:
        if item.desde == None:
            desde = ""
        else:
            desde = str(item.desde.strftime('%d/%m/%Y'))

        resultado = resultado + str(item.id)+'|'+item.atividade +'|'+desde+'#'
        #u'RESIDENCIAL|(27) 3043-0703|undefined|undefined#'
        #print("serializar: ",item)
    return resultado


def verificar_erro(formulario):
    msg = ""
    for campo in formulario:
        print("VEJA O CAMPO: ",campo.data,campo.name,campo.value(),campo.errors, campo.field)

        """
        ['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', 
        '__ge__', '__getattribute__', '__getitem__', '__gt__', '__hash__', '__html__', 
        '__init__', '__init_subclass__', '__iter__', '__le__', '__len__', '__lt__', 
        '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', 
        '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 
        'as_hidden', 'as_text', 'as_textarea', 'as_widget', 'auto_id', 'build_widget_attrs', 
        'css_classes', 'data', 'errors', 'field', 'form', 'help_text', 'html_initial_id', 
        'html_initial_name', 'html_name', 'id_for_label', 'initial', 'is_hidden', 'label', 
        'label_tag', 'name', 'subwidgets', 'value']
        """

        #erros_json = campo.errors.as_json()
        erros = campo.errors.as_data()
        if erros != []:
            if campo.name == 'contatos':
                msg = "Erro! Pelo menos um contato deve ser informado."
            else:
                erro = erros[0][0]
                msg = campo.label + " " + erro

            """if 'email' in erro:
                msg = "Erro! " + unicode(erro)

            elif 'data' in erro:
                msg = "Erro! " + unicode(erro)

            else:
                msg = campo.label + " " + erro

            print campo.label,"olha o err:",erro
            msg = campo.label + " " + erro"""
            return msg

    """
    if request.POST:
        form = formulario_cadastro_entidade_completo(request.POST, request.FILES)
        if form.is_valid():
            print("deu certo!"

    else:
        form = formulario_cadastro_entidade_completo()

    #return render(request,request, 'contact/form.html', {'form':form})
    
    return render(request,"cadastro_entidades.html",{'formulario':form})
    """

def verificar_erros_formulario(formulario):
    msg = ""            
    for campo in formulario:
        erros = campo.errors.as_data()
                
        if erros != []:
            
            erro = erros[0][0]
                        
            if 'email' in erro:
                msg = "Erro! "+u''+erro
            
            elif 'data' in erro:          
                msg = "Erro! "+u''+erro
            
            else:
                msg = campo.label+" "+u''+erro
            
            return msg
    
          

def consultar_cep(request,codigo_postal):
    from modules.entidade.models import localizacao_simples
    if request.is_ajax():
        
        codigo_postal = codigo_postal.replace(".","")
        codigo_postal = codigo_postal.replace("-","")
        
        resultado = localizacao_simples.objects.filter(cep=codigo_postal)
        resultado = consultar_codigo_postal_viacep(codigo_postal)
        """
        if True: #resultado.count() == 0:
            #print("Nao achei na base de dados"
            
            #return HttpResponse(resultado, content_type='application/json')
            #resultado = [resultado['logradouro'],resultado['bairro'],resultado['municipio'],resultado['estado'],resultado['codigo_municipio'],resultado['pais']]
            
            ""
            if resultado != None:
                resultado[0] = formatar_codificacao(resultado[0])
                resultado[1] = formatar_codificacao(resultado[1])
                resultado[2] = formatar_codificacao(resultado[2])
                                                                  
                registro_estado    = Estado.objects.get(sigla=resultado[3])            
                registro_pais      = registro_estado.Pais.nome
                registro_municipio = Municipio.objects.select_related().get(Estado=registro_estado,nome=resultado[2])
                codigo_municipal   = registro_municipio.codigo_ibge
                resultado.append(codigo_municipal)
                resultado.append(registro_pais)
                
                print("ate aqui eu consegui.."          
                registro_bairro = Bairro.objects.select_related().get(municipio=registro_municipio,nome=resultado[1])
                
                print("achei o bairro?"                       
                registro_endereco = Endereco(
                                     cep = codigo_postal,
                                     Bairro = registro_bairro,
                                     nome = resultado[0]
                                    )
                
                try:             
                    print("salvei um novo Endereco"       
                    registro_endereco.save()

                except Exception as excecao:
                    print("deu problema",excecao.message
                    
            else:
                resultado = ["","","","","",""]
            ""
            
        #else:
        #    registro_endereco = resultado[0]
        #    registro_bairro = Bairro.objects.get(id=registro_endereco.bairro_id)
        #    registro_cidade = registro_bairro.municipio 
        #    registro_estado = registro_cidade.estado    
        #    resultado = [registro_endereco.nome,registro_bairro.nome,registro_cidade.nome,registro_estado.sigla,registro_cidade.codigo_ibge,registro_estado.pais.nome]
        """
        data = json.dumps(resultado)
        print("VEJA A CONSULTA  O  QUE VEIO: ",data)
        return HttpResponse(data, content_type='application/json')
    
    else:
        raise Http404




'''
    COMENTEI O ANTIGO POIS ESTOU FECHANDO ROTAS ABERTAS
    def adicionar_entidade_antigo(request):
    
    dados = entidade.objects.all()
    
    if (request.method == "POST"):
                
        formulario = formulario_cadastro_entidade_completo(request.POST, request.FILES)        
        codigo_postal = remover_simbolos(formulario['cep'].value())
                
        if formulario.is_valid():
            
            registro_entidade = entidade()
            registro_entidade.cpf_cnpj = remover_simbolos(formulario.cleaned_data['cpf_cnpj'])
            registro_entidade.nome_razao = formulario.cleaned_data['nome_razao']
            registro_entidade.apelido_fantasia = formulario.cleaned_data['apelido_fantasia']
            registro_entidade.tipo_registro = formulario.cleaned_data['tipo_registro']
            registro_entidade.nascimento_fundacao = formulario.cleaned_data['nascimento_fundacao']
            
            validacao = False
            try:
                registro_entidade.save()
                validacao = True
                
            except IntegrityError as excecao:
                if "cpf_cnpj" in excecao.message:
                    msg = "Erro! cpf ou cnpj já existe no cadastro!"
                
                else:
                    msg = excecao.message
                    
            if validacao:
                registro_contato = contato(
                    entidade = registro_entidade,#entidade.objects.get(pk=registro_entidade.id),
                    nome_contato = registro_entidade.nome_razao,
                    tipo_contato = formulario.cleaned_data['tipo_contato'],
                    numero       = remover_simbolos(formulario.cleaned_data['numero_contato']),
                    cargo_setor  = formulario.cleaned_data['cargo_setor'],
                    email        = formulario.cleaned_data['email'],
                )                        
                #registro_contato.save()        
                            
                codigo_postal = remover_simbolos(formulario.cleaned_data['cep'])
                
                print("Tamo procurando o cep: ",codigo_postal)
                cep_id = Logradouro.objects.filter(cep=codigo_postal)
                print("Cep ID: ",cep_id)
                
                """
                registro_localizacao = localizacao(
                    cep_id      = cep_id,
                    numero      = formulario.cleaned_data['numero_endereco'],
                    complemento = formulario.cleaned_data['complemento'],
                    
                    )
                """
            
                #Endereco = formulario.cleaned_data['Endereco']
                
                bairro = formulario.cleaned_data['bairro']
                
                Municipio = formulario.cleaned_data['Municipio']
                codigo_municipio = remover_simbolos(formulario.cleaned_data['codigo_municipio'])
                Estado = formulario.cleaned_data['Estado']
                
                Pais = formulario.cleaned_data['Pais']
                tipo_contato = formulario.cleaned_data['tipo_contato']
                numero_contato = remover_simbolos(formulario.cleaned_data['numero_contato'])
                cargo_setor = formulario.cleaned_data['cargo_setor']
                email = formulario.cleaned_data['email']
            
                messages.add_message(request, messages.SUCCESS, "Registro salvo com sucesso!")
                
            else:
                messages.add_message(request, messages.SUCCESS, msg)
        
        else:
            
            msg = ""            
            for campo in formulario:
                erros = campo.errors.as_data()
                
                
                if erros != []:
                    
                    erro = erros[0][0]
                    
                    if 'email' in erro:
                        msg = "Erro! "+u""+erro
                    else:
                        msg = campo.label+" "+erro
                    messages.add_message(request, messages.SUCCESS, msg)
                    break
            
            return render(request,"adicionar_entidade.html",{'dados':dados,'formulario':formulario})
    
    else:
        formulario = formulario_cadastro_entidade_completo()
        #formulario_contato  = form_adicionar_contato()
        
    return render(request,"adicionar_entidade.html",{'dados':dados,'formulario':formulario})
        
    #return render(request,"adicionar_entidade.html",{'formulario_entidade':formulario_entidade,'formulario_contato':formulario_contato})
        
'''