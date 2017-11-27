from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied, ValidationError
from sistemaweb import settings
from functools import wraps


def validate_formulary(view):
    @wraps(view)
    def _wrapped_view(controller, request, formulary, *args, **kwargs):
        """ request via ajax verifiy need settings.DEBUG=True for running view tests."""
        form = formulary(request.POST)
        if not form.is_valid():
            #print("DA UMA VERIFICADA NO FORM: ",form.errors)
            controller.object = form.get_object()
            controller.get_exceptions(controller.object, form)
        else:
            controller.object = form.get_object()
            controller.get_exceptions(controller.object, form)
            #print("FORMULARIO TA VALIDO MAS QUERO VER TBM O MODELO: ", controller.full_exceptions)
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