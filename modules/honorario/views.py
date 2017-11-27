from django.shortcuts import render_to_response
from django.template import RequestContext
from modules.honorario.forms import FormContrato, FormIndicacao, FormProventos


def honorario_page(request):
    form_contrato = FormContrato()
    form_indicacao = FormIndicacao()
    return render_to_response("honorario/honorario.html",{'formulario_contrato':form_contrato, 'formulario_indicacao':form_indicacao},context_instance=RequestContext(request))


def proventos_page(request):
    form_contrato = FormContrato()
    form_proventos = FormProventos()
    return render_to_response("honorario/cadastro_proventos.html",{'formulario_contrato':form_contrato, 'formulario_proventos':form_proventos},context_instance=RequestContext(request))


def contrato_page(request):
    form_contrato = FormContrato()
    return render_to_response("honorario/contrato.html",{'formulario_contrato':form_contrato},context_instance=RequestContext(request))