from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from libs.default.core import BaseController
from libs.default.decorators import request_ajax_required
from modules.entidade.models import Documento, entidade


class EntityController(BaseController):

    def close_document(self, request):
        self.start_process(request)
        try:
            documento = Documento.objects.get(pk=int(request.POST['document_id']))
        except:
            documento = None
        if documento is not None:
            from django.utils.timezone import now, localtime
            documento.ativo = False
            documento.data_finalizado = localtime(now())
            documento.finalizado_por = request.user
            response_dict = self.execute(documento, documento.save)

        else:
            response_dict = {}
            response_dict['result'] = False
            response_dict['object'] = None
            response_dict['message'] = "Erro! Documento informado não existe."
        return self.response(response_dict)

    @request_ajax_required
    @method_decorator(login_required)
    def desativar_cliente(self, request):
        return self.disable(request, entidade)