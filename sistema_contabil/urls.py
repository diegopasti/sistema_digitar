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

from modules.core.api import ConfigurationsController
from modules.entidade.views import EntityController
from modules.nucleo import views as nucleo_views
from modules.core import views as core_views
from modules.entidade import views as entidade_views
from modules.protocolo import views as protocolo_views
from modules.servico import views as servico_views
from modules.honorary import views as honorario_views
from modules.honorary import api as honorario_api
from modules.preferencias import views as preferencias_views
from modules.honorary.api import ProventosController, HonoraryController, ContractController
from modules.user import views as view_usuario
from modules.user.api import UserController
#from filebrowser.sites import site
#site.directory = "data/backup/"
handler403 = 'modules.core.views.access_denied'

urlpatterns = [

    url(r'admin/register/first_user',view_usuario.register_first_user),
    url(r'^$', entidade_views.index),
    #url(r'^admin/filebrowser/', include(site.urls)),
    #url(r'^adminurl/filebrowser/', include(site.urls)),
    #url(r'^grappelli/', include('grappelli.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', view_usuario.login_page),
    url(r'^logout', view_usuario.logout_page),
    url(r'^profile/',view_usuario.profile),
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
    url(r'^entidade/desativar/$', EntityController().desativar_cliente),
    url(r'^entidade/visualizar/(?P<id>\d+)/$', entidade_views.visualizar_entidade),
    url(r'^adicionar_entidade/$', entidade_views.adicionar_entidade),
    url(r'^consultar_entidade/(?P<entidade_id>\d+)/$',entidade_views.consultar_entidade),
    url(r'^api/entidade/lista_clientes/$', entidade_views.novo_buscar_lista_clientes),


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

    url(r'^contract/$', honorario_views.contract_page),
    url(r'^api/contract/lista_contratos$', ContractController().get_lista_contratos),
    url(r'^api/contract/salvar_contrato', ContractController().salvar_contrato),
    url(r'^api/contract/alterar_contrato', ContractController().alterar_contrato),
    url(r'^api/contract/close', ContractController().close_contract),
    url(r'^api/contract/atualizar_contrato', ContractController().atualizar_contrato),
    url(r'^api/contract/carregar_servicos_contratados/(?P<cliente_id>\d+)/(?P<plano_id>\d+)/', ContractController().carregar_servicos_contratados),
    url(r'^api/contract/atualizar_servicos', ContractController().atualizar_servicos),
    url(r'^api/contract/lista_indicacao/(?P<cliente_id>\d+)/', ContractController().get_lista_indicacoes),
    url(r'^api/contract/salvar_indicacao/', ContractController().salvar_indicacao),
    url(r'^api/contract/alterar_indicacao/', ContractController().alterar_indicacao),
    url(r'^api/contract/alterar_boolean_indicacao/', ContractController().alterar_boolean_indicacao),
    url(r'^api/contract/deletar_indicacao/', ContractController().deletar_indicacao),

    url(r'^provents/$', honorario_views.proventos_page),
    url(r'^api/provents$', ProventosController().filter_provents),
    url(r'^api/provents/save$', ProventosController.save_provent),
    url(r'^api/provents/update$', ProventosController.update_provent),
    url(r'^api/provents/disable$', ProventosController.disable_provent),

    url(r'^honorary/$', honorario_views.honorary_page),
    url(r'^api/honorary$', HonoraryController().filter),
    url(r'^api/honorary/competences$', HonoraryController().generate_honoraries),
    url(r'^api/honorary/competences/current/close$', HonoraryController().close_current_competence),

    #url(r'^api/preferencias/alterar_salario/(?P<id>\d+)/$', "preferencias.views.alterar_salario),
    #url(r'^api/preferencias/excluir_salario/(?P<id>\d+)/$', "preferencias.views.excluir_salario),
    #url(r'^api/preferencias/salario_vigente/$', "preferencias.views.get_salario_vigente),

    url(r'^preferencias/$', preferencias_views.controle_preferencias),
    url(r'^api/preferencias/salarios$', preferencias_views.listar_salarios),
    url(r'^api/preferencias/novo_salario$', preferencias_views.adicionar_salario),
    url(r'^api/preferencias/alterar_salario/(?P<id>\d+)/$', preferencias_views.alterar_salario),
    url(r'^api/preferencias/excluir_salario/(?P<id>\d+)/$', preferencias_views.excluir_salario),
    url(r'^api/preferencias/salario_vigente/$', preferencias_views.get_salario_vigente),

    #url(r'^api/core/', include('modules.nucleo.urls')),

    url(r'^api/working/register/$', nucleo_views.working),
    url(r'^system/configurations', core_views.system_configurations),
    url(r'configurations/backup$', ConfigurationsController().load_backups),
    url(r'configurations/backup/info$', ConfigurationsController().check_available_space),
    url(r'configurations/backup/create$', ConfigurationsController().create_backup),
    url(r'configurations/backup/restore$', ConfigurationsController().restore_backup),
    url(r'configurations/version/info$', ConfigurationsController().version_update),
    url(r'configurations/version/update$', ConfigurationsController().update),
    url(r'configurations/backup/share$', ConfigurationsController().shared_folder),
    url(r'configurations/backup/restore$', ConfigurationsController().restore_backup),
    url(r'configurations/backup/backups$', ConfigurationsController().list_backups),
    url(r'configurations/backup/manager$', ConfigurationsController().manager_dropbox),

    #'''POR HORA FICA AQUI DEPOIS ARRUMO'''
    url(r'users/',view_usuario.user_page),
    url(r'^api/user/', include('modules.user.urls')),
    # User Administration
    url(r'session_security/', include('session_security.urls')),
    url(r'error/access_denied',core_views.access_denied),

]
