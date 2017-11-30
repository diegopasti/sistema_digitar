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
from django.contrib import admin
from django.conf.urls import url, include
from modules.nucleo import views as nucleo_views
from modules.entidade import views as entidade_views
from modules.protocolo import views as protocolo_views
from modules.servico import views as servico_views
from modules.honorario import views as honorario_views
from modules.honorario import api as honorario_api
from modules.preferencias import views as preferencias_views
from modules.honorario.api import ProventosController
from modules.user import views as view_usuario

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', view_usuario.login_page),
    url(r'^$', entidade_views.index), # entidade.views.index),
    url(r'^cadastrar_empresa$', nucleo_views.cadastrar_empresa), #url(r'teste/$', "endereco.views.teste),
    url(r'^index/$',  entidade_views.index),
    url(r'^gerar_pdf/$', protocolo_views.gerar_pdf),
    url(r'^protocolo/$', protocolo_views.cadastro_protocolo),
    url(r'^protocolo/(?P<protocolo_id>\d+)/$', protocolo_views.cadastro_protocolo),
    url(r'^protocolo/get_detalhes_protocolo/(?P<protocolo_id>\d+)/$', protocolo_views.get_detalhes_protocolo),
    url(r'^protocolo/visualizar/(?P<protocolo_id>\d+)/$', protocolo_views.visualizar_protocolo),
    
    url(r'^protocolo/emitir_protocolo/$', protocolo_views.novo_emitir_protocolo),
    url(r'^protocolo/emitir_protocolo/(?P<operador>\w+)/$', protocolo_views.emitir_protocolo_identificado),
    url(r'^emitir_protocolo/excluir/(?P<numero_item>\d+)/$', protocolo_views.emitir_protocolo),

    url(r'^preferencias/protocolo/documentos/$', protocolo_views.cadastro_documentos),
    url(r'^protocolo/documento/(?P<id>\d+)/$', protocolo_views.get_documento),
    url(r'^protocolo/documento/excluir/(?P<id>\d+)/$', protocolo_views.excluir_documento),
    url(r'^api/protocolo/salvar$', protocolo_views.salvar_protocolo),

    url(r'^consultar_cep/(?P<codigo_postal>\d+)/$', entidade_views.consultar_cep),

    
    #url(r'^consultar_cep/(?P<cep>\d+\.\d+-\d+)/$', entidade_views.consultar_cep),
    url(r'^entidade/$', entidade_views.cadastro_entidades),
    url(r'^entidade/adicionar/$', entidade_views.adicionar_entidade),
    url(r'^entidade/desativar/(?P<cliente>\d+)/$', entidade_views.desativar_cliente),
    url(r'^entidade/visualizar/(?P<id>\d+)/$', entidade_views.visualizar_entidade),
    url(r'^api/entidade/lista_clientes/$', entidade_views.novo_buscar_lista_clientes),
    
    #url(r'^protocolo/$', entidade_views.protocolo),
    
    url(r'^adicionar_entidade/$', entidade_views.adicionar_entidade),
    url(r'^consultar_entidade/(?P<entidade_id>\d+)/$',entidade_views.consultar_entidade),

    url(r'^preferencias/servicos/$', servico_views.cadastro_servico),
    url(r'^api/preferencias/servicos/$', servico_views.consultar_servicos),
    url(r'^api/preferencias/novo_servico$', servico_views.adicionar_servico),
    url(r'^api/preferencias/alterar_servico/(?P<servico_id>\d+)/$', servico_views.alterar_servico),
    url(r'^api/preferencias/excluir_servico/(?P<servico_id>\d+)/$', servico_views.excluir_servico),

    url(r'^planos/$', servico_views.cadastro_planos),
    url(r'^api/planos/$', servico_views.consultar_planos),
    url(r'^api/planos/adicionar$', servico_views.adicionar_plano),
    url(r'^api/planos/atualizar', servico_views.atualizar_plano),
    url(r'^api/planos/excluir', servico_views.excluir_plano),

    url(r'^honorario/$', honorario_views.honorario_page),
    url(r'^honorario/contrato$', honorario_views.contrato_page),
    url(r'^api/honorario/lista_contratos$', honorario_api.get_lista_contratos),
    url(r'^api/honorario/salvar_contrato', honorario_api.salvar_contrato),
    url(r'^api/honorario/alterar_contrato', honorario_api.alterar_contrato),
    url(r'^api/honorario/atualizar_contrato', honorario_api.atualizar_contrato),
    url(r'^api/honorario/carregar_servicos_contratados/(?P<cliente_id>\d+)/(?P<plano_id>\d+)/', honorario_api.carregar_servicos_contratados),
    url(r'^api/honorario/atualizar_servicos', honorario_api.atualizar_servicos),


    url(r'^api/honorario/lista_indicacao/(?P<cliente_id>\d+)/', honorario_api.get_lista_indicacoes),
    url(r'^api/honorario/salvar_indicacao/', honorario_api.salvar_indicacao),
    url(r'^api/honorario/alterar_indicacao/', honorario_api.alterar_indicacao),
    url(r'^api/honorario/alterar_boolean_indicacao/', honorario_api.alterar_boolean_indicacao),
    url(r'^api/honorario/deletar_indicacao/', honorario_api.deletar_indicacao),

    url(r'^proventos/$', honorario_views.proventos_page),
    url(r'^api/proventos$', ProventosController.filter),#"honorario.api.ProventosController().get_lista_proventos),
    url(r'^api/proventos/adicionar$', ProventosController.save),
    #url(r'^api/preferencias/alterar_salario/(?P<id>\d+)/$', "preferencias.views.alterar_salario),
    #url(r'^api/preferencias/excluir_salario/(?P<id>\d+)/$', "preferencias.views.excluir_salario),
    #url(r'^api/preferencias/salario_vigente/$', "preferencias.views.get_salario_vigente),

    url(r'^preferencias/$', preferencias_views.controle_preferencias),
    url(r'^api/preferencias/salarios$', preferencias_views.listar_salarios),
    url(r'^api/preferencias/novo_salario$', preferencias_views.adicionar_salario),
    url(r'^api/preferencias/alterar_salario/(?P<id>\d+)/$', preferencias_views.alterar_salario),
    url(r'^api/preferencias/excluir_salario/(?P<id>\d+)/$', preferencias_views.excluir_salario),
    url(r'^api/preferencias/salario_vigente/$', preferencias_views.get_salario_vigente),

    url(r'^api/working/register/$', nucleo_views.working),


]
