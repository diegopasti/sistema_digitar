from django.shortcuts import render_to_response, render
from django.template import RequestContext
from modules.honorario.forms import FormContrato, FormIndicacao, FormProventos


def honorario_page(request):
    form_contrato = FormContrato()
    form_indicacao = FormIndicacao()
    return render(request,"honorario/honorario.html",{'formulario_contrato':form_contrato, 'formulario_indicacao':form_indicacao})


def proventos_page(request):
    form_proventos = FormProventos()
    return render(request,"honorario/provents.html",{'formulario_proventos':form_proventos})


def contrato_page(request):
    form_contrato = FormContrato()
    return render(request,"honorario/contrato.html",{'formulario_contrato':form_contrato})