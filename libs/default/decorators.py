from django.contrib.auth.decorators import user_passes_test
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
                print("VOU PEGAR O OBJETO QUE JA EXISTE")
                controller.object = form.get_object(int(request.POST['id']))
            else:
                print("VOU CRIRA UM OBJETO")
                controller.object = form.get_object()
        else:
            if 'id' in request.POST:
                print("FORM VALID: VOU PEGAR O OBJETO QUE JA EXISTE")
                controller.object = form.get_object(int(request.POST['id']))
            else:
                print("FORM VALID: CRIAR OBJETO")
                controller.object = form.get_object()

        '''
        if hasattr(controller.object,'cadastrado_por'): controller.object.cadastrado_por = request.user
        elif hasattr(controller.object, 'created_by'): controller.object.created_by = request.user
        else: pass

        if hasattr(controller.object, 'alterado_por'): controller.object.alterado_por = request.user
        elif hasattr(controller.object, 'updated_by'): controller.object.updated_by = request.user
        else: pass
        '''

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


def permission_level_required(nivel_requerido, login_url=None, raise_exception=False):

    '''
    Decorador View
    Um usuário só pode ter no máximo um grupo, dessa forma eu pego o id do grupo e filtro o acesso
    de acordo com esse numero, o nível hierarquico é Administrador, Supervisor e Operador, Com isso
    temos respectivamente 1,2,3 quanto menor o numero maior as suas permissões, assim sempre perguntamos
    se o nivel do grupo é menor ou igual para assim permitirmos ou não seu acesso
    '''

    def check_perms(user):
        nivel = user.groups.values_list('id',flat=True)
        if (int(nivel[0]) <= nivel_requerido):
            return True
        if raise_exception:
            raise PermissionDenied
        return False
    return user_passes_test(check_perms, login_url=login_url)

