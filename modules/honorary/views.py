from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from libs.default.decorators import permission_level_required
from modules.entidade.formularios import formulario_justificar_operacao
from modules.honorary.forms import FormContrato, FormIndicacao, FormProventos, FormHonoraryItem


@login_required
@permission_level_required(1,'/error/access_denied')
def honorary_page(request):
    form_contrato = FormContrato()
    form_indicacao = FormIndicacao()
    form_honorary_item = FormHonoraryItem()
    return render(request,"honorario/honorary/honorary.html",{'formulario_contrato':form_contrato, 'formulario_indicacao':form_indicacao, 'formulario_proventos':form_honorary_item})

@login_required
@permission_level_required(2,'/error/access_denied')
def proventos_page(request):
    form_proventos = FormProventos()
    form_desativar = formulario_justificar_operacao()
    return render(request,"honorario/provents.html",{'formulario_proventos':form_proventos, 'form_desativar':form_desativar})

@login_required
@permission_level_required(1,'/error/access_denied')
def contract_page(request):
    form_contrato = FormContrato()
    form_indicacao = FormIndicacao()
    return render(request, "honorario/contract.html", {'formulario_contrato': form_contrato, 'formulario_indicacao': form_indicacao})