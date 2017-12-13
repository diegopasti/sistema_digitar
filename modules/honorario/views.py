from django.shortcuts import render

from modules.entidade.formularios import formulario_justificar_operacao
from modules.honorario.forms import FormContrato, FormIndicacao, FormProventos


def honorario_page(request):
    form_contrato = FormContrato()
    form_indicacao = FormIndicacao()
    return render(request,"honorario/honorario.html",{'formulario_contrato':form_contrato, 'formulario_indicacao':form_indicacao})


def proventos_page(request):
    form_proventos = FormProventos()
    form_desativar = formulario_justificar_operacao()
    return render(request,"honorario/provents.html",{'formulario_proventos':form_proventos, 'form_desativar':form_desativar})


def contrato_page(request):
    form_contrato = FormContrato()
    return render(request,"honorario/contrato.html",{'formulario_contrato':form_contrato})