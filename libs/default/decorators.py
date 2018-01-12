from django.core.exceptions import PermissionDenied
from sistema_contabil import settings
from functools import wraps


def validate_formulary(view):
    @wraps(view)
    def _wrapped_view(controller, request, formulary, *args, **kwargs):
        """ request via ajax verifiy need settings.DEBUG=True for running view tests."""
        form = formulary(request.POST)
        form.request = request
        if not form.is_valid():
            if 'id' in request.POST:
                controller.object = form.get_object(int(request.POST['id']))
            else:
                controller.object = form.get_object()
        else:
            if 'id' in request.POST:
                controller.object = form.get_object(int(request.POST['id']))
            else:
                controller.object = form.get_object()

        #print("VAMOS VER O OBJETO: ",dir(controller.object))
        if hasattr(controller.object,'cadastrado_por'):
            controller.object.cadastrado_por = request.user
        elif hasattr(controller.object, 'created_by'):
            print("TEM O CREATED")
            controller.object.created_by = request.user
        else:
            print("NAO TEM CRIADO NEM CREATED?")

        if hasattr(controller.object, 'alterado_por'): controller.object.alterado_por = request.user
        elif hasattr(controller.object, 'updated_by'):
            controller.object.updated_by = request.user
            print("TEM O UPDATED")
        else: pass


        controller.get_exceptions(controller.object, form)
        return view(controller, request, formulary, *args, **kwargs)
    return _wrapped_view


def request_ajax_required(view):
    @wraps(view)
    def _wrapped_view(controller, request, formulary=None, *args, **kwargs):
        """ request via ajax verifiy need settings.DEBUG=True for running view tests."""
        if request.is_ajax() or settings.DEBUG:
            controller.start_process(request)
            controller.request = request
            if formulary is None:
                return view(controller, request, *args, **kwargs)
            else:
                return view(controller, request, formulary, *args, **kwargs)
        else:
            raise PermissionDenied()
    return _wrapped_view


def request_get_required(view):
    @wraps(view)
    def _wrapped_view(request, *args, **kwargs):
        if request.method == 'GET':
            return view(request, *args, **kwargs)
        else:
            raise PermissionDenied()
    return _wrapped_view


def request_post_required(view):
    @wraps(view)
    def _wrapped_view(request, *args, **kwargs):
        if request.method == 'POST':
            return view(request, *args, **kwargs)
        else:
            raise PermissionDenied()
    return _wrapped_view