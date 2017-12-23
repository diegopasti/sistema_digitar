from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from modules.entidade.formularios import formulario_justificar_operacao
from modules.honorary.forms import FormContrato, FormIndicacao, FormProventos

@login_required
def honorary_page(request):
    form_contrato = FormContrato()
    form_indicacao = FormIndicacao()
    return render(request,"honorario/honorary/honorary.html",{'formulario_contrato':form_contrato, 'formulario_indicacao':form_indicacao})

@login_required
def proventos_page(request):
    form_proventos = FormProventos()
    form_desativar = formulario_justificar_operacao()
    return render(request,"honorario/provents.html",{'formulario_proventos':form_proventos, 'form_desativar':form_desativar})

@login_required
def contract_page(request):
    form_contrato = FormContrato()
    form_indicacao = FormIndicacao()
    return render(request, "honorario/honorario.html", {'formulario_contrato': form_contrato, 'formulario_indicacao': form_indicacao})