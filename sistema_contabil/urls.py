"""sistema_contabil URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

from modules.honorario.api import ProventosController

urlpatterns = [

    url(r'^$', "modules.entidade.views.index"),
    
    url(r'^cadastrar_empresa$', "modules.nucleo.views.cadastrar_empresa"),
    
    
    url(r'^admin/', include(admin.site.urls)),
    url(r'teste/$', "endereco.views.teste"),
    
    url(r'^index/$', "modules.entidade.views.index"),
    
    url(r'^gerar_pdf/$', "modules.protocolo.views.gerar_pdf"),
    url(r'^protocolo/$', "modules.protocolo.views.cadastro_protocolo"),
    url(r'^protocolo/(?P<protocolo_id>\d+)/$', "modules.protocolo.views.cadastro_protocolo"),
    url(r'^protocolo/get_detalhes_protocolo/(?P<protocolo_id>\d+)/$', "modules.protocolo.views.get_detalhes_protocolo"),
    url(r'^protocolo/visualizar/(?P<protocolo_id>\d+)/$', "modules.protocolo.views.visualizar_protocolo"),
    
    url(r'^protocolo/emitir_protocolo/$', "modules.protocolo.views.novo_emitir_protocolo"),
    url(r'^protocolo/emitir_protocolo/(?P<operador>\w+)/$', "modules.protocolo.views.emitir_protocolo_identificado"),
    url(r'^emitir_protocolo/excluir/(?P<numero_item>\d+)/$', "modules.protocolo.views.emitir_protocolo"),

    url(r'^preferencias/protocolo/documentos/$', "modules.protocolo.views.cadastro_documentos"),
    url(r'^protocolo/documento/(?P<id>\d+)/$', "modules.protocolo.views.get_documento"),
	url(r'^protocolo/documento/excluir/(?P<id>\d+)/$', "modules.protocolo.views.excluir_documento"),
    url(r'^api/protocolo/salvar$', "modules.protocolo.views.salvar_protocolo"),

    url(r'^consultar_cep/(?P<codigo_postal>\d+)/$', "modules.entidade.views.consultar_cep"),

    
    #url(r'^consultar_cep/(?P<cep>\d+\.\d+-\d+)/$', "modules.entidade.views.consultar_cep"),
    url(r'^entidade/$', "modules.entidade.views.cadastro_entidades"),
    url(r'^entidade/adicionar/$', "modules.entidade.views.adicionar_entidade"),
    url(r'^entidade/desativar/(?P<cliente>\d+)/$', "modules.entidade.views.desativar_cliente"),
	url(r'^entidade/visualizar/(?P<id>\d+)/$', "modules.entidade.views.visualizar_entidade"),
    url(r'^api/entidade/lista_clientes/$', "modules.entidade.views.novo_buscar_lista_clientes"),
    
    #url(r'^protocolo/$', "modules.entidade.views.protocolo"),
    
    url(r'^adicionar_entidade/$', "modules.entidade.views.adicionar_entidade"),
    url(r'^consultar_entidade/(?P<entidade_id>\d+)/$',"modules.entidade.views.consultar_entidade"),

    url(r'^preferencias/servicos/$', "modules.servico.views.cadastro_servico"),
    url(r'^api/preferencias/servicos/$', "modules.servico.views.consultar_servicos"),
    url(r'^api/preferencias/novo_servico$', "modules.servico.views.adicionar_servico"),
    url(r'^api/preferencias/alterar_servico/(?P<servico_id>\d+)/$', "modules.servico.views.alterar_servico"),
    url(r'^api/preferencias/excluir_servico/(?P<servico_id>\d+)/$', "modules.servico.views.excluir_servico"),

    url(r'^planos/$', "modules.servico.views.cadastro_planos"),
    url(r'^api/planos/$', "modules.servico.views.consultar_planos"),
    url(r'^api/planos/adicionar$', "modules.servico.views.adicionar_plano"),
    url(r'^api/planos/atualizar', "modules.servico.views.atualizar_plano"),
    url(r'^api/planos/excluir', "modules.servico.views.excluir_plano"),

    url(r'^honorario/$', "modules.honorario.views.honorario_page"),
    url(r'^honorario/contrato$', "modules.honorario.views.contrato_page"),
    url(r'^api/honorario/lista_contratos$', "modules.honorario.api.get_lista_contratos"),
    url(r'^api/honorario/salvar_contrato', "modules.honorario.api.salvar_contrato"),
    url(r'^api/honorario/alterar_contrato', "modules.honorario.api.alterar_contrato"),
    url(r'^api/honorario/atualizar_contrato', "modules.honorario.api.atualizar_contrato"),
    url(r'^api/honorario/carregar_servicos_contratados/(?P<cliente_id>\d+)/(?P<plano_id>\d+)/', "modules.honorario.api.carregar_servicos_contratados"),
    url(r'^api/honorario/atualizar_servicos', "modules.honorario.api.atualizar_servicos"),


    url(r'^api/honorario/lista_indicacao/(?P<cliente_id>\d+)/', "modules.honorario.api.get_lista_indicacoes"),
    url(r'^api/honorario/salvar_indicacao/', "modules.honorario.api.salvar_indicacao"),
    url(r'^api/honorario/alterar_indicacao/', "modules.honorario.api.alterar_indicacao"),
    url(r'^api/honorario/alterar_boolean_indicacao/', "modules.honorario.api.alterar_boolean_indicacao"),
    url(r'^api/honorario/deletar_indicacao/', "modules.honorario.api.deletar_indicacao"),

    url(r'^proventos/$', "modules.honorario.views.proventos_page"),
    url(r'^api/proventos$', ProventosController().get_lista_proventos),#"honorario.api.ProventosController().get_lista_proventos"),
    url(r'^api/proventos/adicionar$', ProventosController().adicionar_provento),
    #url(r'^api/preferencias/alterar_salario/(?P<id>\d+)/$', "preferencias.views.alterar_salario"),
    #url(r'^api/preferencias/excluir_salario/(?P<id>\d+)/$', "preferencias.views.excluir_salario"),
    #url(r'^api/preferencias/salario_vigente/$', "preferencias.views.get_salario_vigente"),

    url(r'^preferencias/$', "modules.preferencias.views.controle_preferencias"),
    url(r'^api/preferencias/salarios$', "modules.preferencias.views.listar_salarios"),
    url(r'^api/preferencias/novo_salario$', "modules.preferencias.views.adicionar_salario"),
    url(r'^api/preferencias/alterar_salario/(?P<id>\d+)/$', "modules.preferencias.views.alterar_salario"),
    url(r'^api/preferencias/excluir_salario/(?P<id>\d+)/$', "modules.preferencias.views.excluir_salario"),
    url(r'^api/preferencias/salario_vigente/$', "modules.preferencias.views.get_salario_vigente"),


    url(r'^api/working/register/$', "modules.nucleo.views.working"),


]
