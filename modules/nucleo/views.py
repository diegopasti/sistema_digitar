# -*- encoding: utf-8 -*-
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http.response import Http404, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render_to_response
from django.shortcuts import render
from django.template.context import RequestContext
from django.utils.decorators import method_decorator

from libs.default.decorators import permission_level_required
from modules.entidade.models import entidade, contato, localizacao_simples  # , Logradouro, Localizacao,
from modules.entidade.utilitarios import remover_simbolos

from modules.entidade.formularios import formulario_cadastro_entidade_completo
from modules.nucleo.working_api import WorkingManager

@login_required
@permission_level_required(1, raise_exception=HttpResponseForbidden())
def system_configurations(request):
    return render(request, "core/configurations/backup/configurations.html")


def cadastrar_empresa(request):  
    dados = entidade.objects.all()
    if (request.method == "POST"):
        #print("Temos uma submissao")
        #request.POST['tipo_registro'] = u'E'
        formulario = formulario_cadastro_entidade_completo(request.POST, request.FILES)        
        #codigo_postal = remover_simbolos(formulario['cep'].value())
        
        #print(type(request.POST['tipo_registro']))
        #print(formulario['cep'])
        #print(formulario['tipo_registro'],formulario['tipo_registro'].value(),type(formulario['tipo_registro'].value()))
        formulario['tipo_registro'].value = u"E"
        print("consegui alterar: ",formulario['tipo_registro'].value)
        
        
        if formulario.is_valid():
            print("Formulario foi validado..")
            
            #print(request.POST)

            endereco_valido = False
            entidade_valido = False
            contato_valido  = False
            
            registro_endereco = localizacao_simples()
            registro_endereco.cep         = formulario.cleaned_data['cep']
            registro_endereco.logradouro  = formulario.cleaned_data['endereco']
            registro_endereco.numero      = formulario.cleaned_data['numero_endereco']
            registro_endereco.complemento = formulario.cleaned_data['complemento']    
            registro_endereco.bairro      = formulario.cleaned_data['bairro']
            registro_endereco.codigo_ibge = formulario.cleaned_data['codigo_municipio']
            registro_endereco.municipio   = formulario.cleaned_data['municipio']
            registro_endereco.estado      = formulario.cleaned_data['estado']    
            registro_endereco.pais        = formulario.cleaned_data['pais']
            
            try:
                entidade_valida = registro_endereco.full_clean(validate_unique=True)
                #print("localizacao criada.. esta valido: ")
                endereco_valido = True
            except Exception as erro:
                #print("localizacao nao esta valida ainda..",erro)
                pass
                
            
            registro_entidade = entidade()
            registro_entidade.cpf_cnpj = remover_simbolos(formulario.cleaned_data['cpf_cnpj'])
            registro_entidade.nome_razao = formulario.cleaned_data['nome_razao'].upper()
            registro_entidade.apelido_fantasia = formulario.cleaned_data['apelido_fantasia'].upper()
            registro_entidade.tipo_registro = u"E"#formulario.cleaned_data['tipo_registro']
            registro_entidade.nascimento_fundacao = formulario.cleaned_data['nascimento_fundacao']
            registro_entidade.endereco = registro_endereco
            try:
                registro_entidade.full_clean(validate_unique=True)
                entidade_valido = True
                
            except Exception as erro:
                
                for item in erro:
                    campo = item[0]
                    descricao = item[1][0]
                    
                    if campo == "endereco" and "nulo" in descricao:
                        #print("tudo certo, so precisa ter a localizacao salva..")
                        entidade_valido = True

            registro_contato = contato(
                entidade = registro_entidade,#entidade.objects.get(pk=registro_entidade.id),
                nome_contato = registro_entidade.nome_razao,
                tipo_contato = formulario.cleaned_data['tipo_contato'],
                numero       = remover_simbolos(formulario.cleaned_data['numero_contato']),
                cargo_setor  = formulario.cleaned_data['cargo_setor'].upper(),
                email        = formulario.cleaned_data['email'].lower(),
            )      
            
            try:
                registro_contato.full_clean(validate_unique=True)
                
            except Exception as erro:
                for item in erro:
                    campo = item[0]
                    descricao = item[1][0]
                    
                    if campo == "entidade" and "nulo" in descricao:
                        contato_valido = True

            
            if endereco_valido and entidade_valido and contato_valido:
                registro_endereco.save()
                registro_entidade.endereco = registro_endereco
                registro_entidade.save()
                registro_contato.entidade = registro_entidade
                registro_contato.save()
                messages.add_message(request, messages.SUCCESS, "Sua empresa foi cadastrada com sucesso!")
                return HttpResponseRedirect('/cadastro_entidades')

                
            else:
                messages.add_message(request, messages.SUCCESS, "Erro! Empresa nao pode ser cadastrada.")
                return HttpResponseRedirect('/cadastro_entidades')
            
            """
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
                print("Consegui registrar a entidade.. vamos tentar o contato..")
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
                logradouro = Logradouro.objects.filter(cep=codigo_postal)
                print("Cep ID: ",logradouro)
                
                
                registro_localizacao = Localizacao(
                    logradouro_id = logradouro,
                    numero      = formulario.cleaned_data['numero_endereco'],
                    complemento = formulario.cleaned_data['complemento'],
                    )
                
            
                #endereco = formulario.cleaned_data['endereco']
                
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
                print("deu errado..")
                messages.add_message(request, messages.SUCCESS, msg)
            """
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
            
            return render_to_response("nucleo/cadastrar_empresa.html",{'dados':dados,'formulario':formulario},context_instance=RequestContext(request))
    
    else:
        formulario = formulario_cadastro_entidade_completo()
        #formulario_contato  = form_adicionar_contato()
        
    return render_to_response("nucleo/cadastrar_empresa.html",{'dados':dados,'formulario':formulario},context_instance=RequestContext(request))

def working(request):
    if request.is_ajax():
        print("TO INDO LA SALVAR")
        return WorkingManager().register_programming_frontend(request.GET['request_page'])
    else:
        raise Http404