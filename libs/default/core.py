from libs.default.decorators import request_ajax_required, validate_formulary
from django.core.exceptions import ValidationError

#from modules.core.comunications import send_generate_activation_code
from modules.nucleo.config import ERRORS_MESSAGES
from datetime import date, datetime, timedelta
from django.http import Http404, HttpResponse

#from modules.core.utils import generate_activation_code
from django.contrib.auth import login
from django.db import IntegrityError
from django.core import serializers

from modules.nucleo.models import RestrictedOperation
from django.contrib.auth.models import Permission, User, Group
from django.contrib.auth import authenticate, login
from modules.user.models import Session
from sistema_contabil import settings
import datetime
import json
import sys


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""
    print(obj, type(obj))
    if isinstance(obj, date):
        return obj.isoformat()
    if isinstance(obj, datetime):
        return obj.isoformat()
    if isinstance(obj, timedelta):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))


class Notify:

    def datalist(self, datalist, list_fields=None, extra_fields=None):
        response_dict = []
        for item in datalist:
            response_data = self.__format_serialized_model(item, list_fields, extra_fields)
            response_dict.append(response_data)
        return response_dict

    def success(self, object, message='', list_fields=None, extra_fields=None):
        return self.__response_format(True, message, object, list_fields, extra_fields)

    def error(self, exceptions):
        return self.__response_format(False,self.__format_exceptions(exceptions),None, None)

    def __response_format(self,result, message, obj=None, list_fields=None, extra_fields=None):
        response_dict = {}
        response_dict['result'] = result
        response_dict['message'] = message
        if result:
            response_dict['object'] = self.__format_serialized_model(obj, list_fields, extra_fields)
        else:
            response_dict['object'] = None
        return response_dict

    def __format_serialized_model(self,object,list_fields, extra_fields=None):
        if list_fields is not None:
            response_model = serializers.serialize('json', [object], fields=tuple(list_fields))
        else:
            response_model = serializers.serialize('json', [object])

        response_model = json.loads(response_model)[0]
        response_model = response_model['fields']

        if extra_fields is not None:
            for item in extra_fields:
                metodo = getattr(object, item, None)
                if (metodo is not None):
                    if callable(metodo):
                        result = metodo()
                    else:
                        result = metodo

                else:
                    if "__" in item:
                        related_field_parts = item.split("__")
                        related_field = object
                        for element in related_field_parts:
                            related_field = getattr(related_field, element, None)
                        result = related_field
                    else:
                        result = ''

                response_model[item] = result
        response_model['id'] = object.id
        response_model['selected'] = ''
        return response_model

    def __format_exceptions(self,exceptions):
        message_dict = {}

        if type(exceptions) == dict:
            message_dict = exceptions

        elif isinstance(exceptions,ValidationError):
            try:
                for item in exceptions.error_dict:
                    field = item
                    exception = exceptions.error_dict[field][0]
                    error_code = exception.code
                    value = exception.args[0]
                    if ': ' in value:
                        value = value.split(": ")[1]
                    message_dict[field] = ERRORS_MESSAGES[error_code]#value
            except Exception as error:
                print("ERRO INTERNO: ",error)
                message_dict = error

        elif isinstance(exceptions,IntegrityError):
            params = exceptions.args[0].split(": ")
            field = params[1].split('.')[1]
            value = ERRORS_MESSAGES["unique"]
            message_dict[field] = value

        else:
            print("ERRO! VERIFIQUE A EXCESSAO: ",exceptions, type(exceptions))
            #paramters = exceptions.args[0].split(': ')
            #code_status = exceptions.args[1]
            #field = paramters[0]
            # value = paramters[1]
            #message_dict[field] = ERRORS_MESSAGES[code_status]
            message_dict = exceptions.args[0]
        return message_dict


class BaseController(Notify):
    request = None
    notify = Notify()
    server_startup_time_process = None
    server_terminate_time_process = None
    server_processing_time = None

    @request_ajax_required
    def login(self, request, formulary):
        form = formulary(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    response_dict = self.notify.success(user, list_fields=['username'])
                else:
                    response_dict = self.notify.error({'username': 'Usuário não autorizado.'})
            else:
                response_dict = self.notify.error({'username': 'Usuário e senha não conferem, ou não existem.'})
        else:
            response_dict = self.get_exceptions(None, form)

        return self.response(response_dict)

    @request_ajax_required
    def signup(self, request, formulary):
        form = formulary(request.POST)
        if form.is_valid():
            username = request.POST['username']
            email = request.POST['email'].lower()
            senha = request.POST['password']
            nome = request.POST['first_name'].upper()
            sobrenome = request.POST['last_name'].upper()
            grupo = request.POST['groups']

            user = User.objects._create_user(username, email, senha,first_name=nome, last_name=sobrenome)
            if user is not None:
                my_group = Group.objects.get(id=int(grupo))
                my_group.user_set.add(user)
                response_dict = self.notify.success(user, list_fields=['email','username','is_active','date_joined','first_name','last_name','id','groups'],extra_fields=['group_id'])
                response_dict['object']['group_id'] = my_group.id
            else:
                response_dict = self.notify.error({'username': 'Nao foi possivel criar objeto.'})


        else:
            response_dict = self.get_exceptions(None, form) #self.notify.error({'email': 'Formulário com dados inválidos.'})
        return self.response(response_dict)

    @request_ajax_required
    @validate_formulary
    def save(self, request, formulary=None, extra_fields=None, is_response=True):
        if self.full_exceptions == {}:
            response_dict = self.execute(self.object, self.object.save, extra_fields)
        else:
            response_dict = self.notify.error(self.full_exceptions)
        if is_response:
            return self.response(response_dict)
        else:
            return response_dict

    @request_ajax_required
    def filter(self, request, model, queryset=None, order_by="-id", list_fields=None, limit=None, extra_fields=None):
        if queryset is None:
            if limit is not None:
                model_list = model.objects.all().order_by(order_by)[:limit]
            else:
                model_list = model.objects.all().order_by(order_by)

        else:
            model_list = queryset

        print(model_list, len(model_list))

        response_dict = {}
        response_dict['result'] = True
        response_dict['object'] = self.notify.datalist(model_list, list_fields, extra_fields)
        response_dict['message'] = str(len(self.notify.datalist(model_list, list_fields)))+" Registros carregados com sucesso!"
        return self.response(response_dict)

    @request_ajax_required
    def object(self, request,model, pk, extra_fields=None, is_response=False):
        try:
            object = model.objects.get(pk=pk)
            response_dict = self.notify.success(object, extra_fields=extra_fields)
        except Exception as erro:
            response_dict = self.notify.error(erro)

        if is_response:
            return self.response(response_dict)
        else:
            return response_dict

    @request_ajax_required
    @validate_formulary
    def update(self, request, formulary, extra_fields=None, is_response=True):
        if self.full_exceptions == {}:
            response_dict = self.execute(self.object, self.object.save, extra_fields)
        else:
            response_dict = self.notify.error(self.full_exceptions)
        if is_response:
            return self.response(response_dict)
        else:
            return response_dict

    @request_ajax_required
    def delete(self, request, model, object_id):
        self.request = request
        print("Excluir: ", model, '[', object_id, ']')
        object = model.objects.filter(id=object_id)
        response_dict = self.execute(object, object.delete)
        return self.response(response_dict)

    @request_ajax_required
    def disable(self, request, model):
        object = model.objects.get(pk=int(request.POST['id']))
        object.is_active = False
        try:
            object.ativo = False
        except:
            pass
        response_dict = self.execute(object, object.save)
        if response_dict['result']:
            self.report_operation(request, model)
        return self.response(response_dict)

    @request_ajax_required
    def enable (self,request,model):
        object = model.objects.get(pk=int(request.POST['id']))
        object.is_active = True
        response_dict = self.execute(object, object.save)
        if response_dict['result']:
            self.report_operation(request, model)
        return self.response(response_dict)

    def report_operation(self, request, model):
        operation = RestrictedOperation()
        operation.user = request.user
        operation.set_type(request.POST['action_type'])
        operation.object_id = request.POST['id']
        operation.object_name = request.POST['action_object']
        operation.justify = request.POST['action_justify']
        operation.table = model._meta.db_table
        operation.save()
        return

    def execute(self, object, action, extra_fields=None):
        try:
            action()
            response_dict = self.notify.success(object, extra_fields=extra_fields)
        except Exception as e:
            response_dict = self.notify.error(e)
        return response_dict

    def get_exceptions(self, object, form):
        """
        Metodo responsavel por tentar capturar erro no formulario e modelo e retornar tudo junto
        """
        self.model_exceptions = {}
        if object is not None:
            try:
                object.full_clean()

            except Exception as exception:
                self.model_exceptions = exception.message_dict

        self.full_exceptions = {}
        if form is not None:
            self.form_exceptions = form.format_validate_response()
        else:
            self.form_exceptions = {}

        #print("FORM EXCEPTIONS: ", self.form_exceptions)
        #print("MODEL EXCEPTIONS: ", self.model_exceptions)

        self.full_exceptions.update(self.model_exceptions)
        self.full_exceptions.update(self.form_exceptions)
        return self.notify.error(self.full_exceptions)

    def __create_session(self, request, user):
        sessao = Session()
        sessao.user = user
        sessao.session_key = request.session.session_key
        sessao.internal_ip = request.POST['internal_ipv4']
        sessao.external_ip = request.POST['external_ip']
        sessao.country_name = request.POST['country_name']
        sessao.country_code = request.POST['country_code']
        sessao.region_code = request.POST['region_code']
        sessao.region_name = request.POST['region_name']
        sessao.city = request.POST['city']
        sessao.zip_code = request.POST['zip_code']
        sessao.time_zone = request.POST['time_zone']
        sessao.latitude = request.POST['latitude']
        sessao.longitude = request.POST['longitude']
        sessao.save()

    def start_process(self, request):
        self.__request_path = request.path
        self.__request_bytes = sys.getsizeof(request.body)
        self.server_startup_time_process = datetime.datetime.now()
        #print("Processo iniciado em ", self.server_startup_time_process)

    def terminate_process(self):
        self.server_terminate_time_process = datetime.datetime.now()
        self.server_processing_time = self.server_terminate_time_process - self.server_startup_time_process
        #print("Processo executado em", self.server_processing_time)  # ,"ou",self.server_processing_time.total_seconds())

    def response(self, response_dict):
        import sys
        self.terminate_process()
        response_dict['status'] = {}
        response_dict['status']['request_path'] = self.__request_path
        response_dict['status']['request_size'] = self.__request_bytes
        response_dict['status']['response_size'] = "RESPONSE_SIZE"
        response_dict['status']['server_processing_time_duration'] = self.server_processing_time.total_seconds()  # datetime.datetime.now()
        response_dict['status']['cliente_processing_time_duration'] = ''
        data = json.dumps(response_dict, default=json_serial)
        data = data.replace('RESPONSE_SIZE', str(sys.getsizeof(data) - 16))
        response = HttpResponse(data)  # after generate response noramlization reduce size in 16 bytes
        return response

    def filter_request(self, request, formulary=None):
        if request.is_ajax() or settings.DEBUG:
            if formulary is not None:
                form = formulary(request.POST)
                if form.is_valid():
                    return True, form
                else:
                    return False, form
            else:
                return True, True
        else:
            raise Http404


class BaseForm:

    model = None

    def format_validate_response(self):
        response_errors = {}
        if self.errors:
            errors = self.errors
            for campo in errors:
                response_errors[campo] = []
                for erro in errors[campo]:
                    erro_format = str(erro)
                    erro_format = erro_format.replace("['", "")
                    erro_format = erro_format.replace("']", "")
                    response_errors[campo].append(erro_format)
        return response_errors

    def get_object(self, object_id=None):
        if object_id is not None:
            object = self.model.objects.get(pk=int(object_id))
        else:
            object = self.model()

        for attribute in self.data:
            if attribute != 'csrfmiddlewaretoken' and attribute != 'undefined':
                if '[]' in attribute:
                    options_selected = self.request.POST.getlist(attribute)
                    if options_selected is not None:
                        value = ';'.join(map(str, self.request.POST.getlist(attribute)))
                    attribute = attribute.replace("[]", "")
                else:
                    if attribute != 'id':
                        if self.data[attribute] != "null":
                            field = self.fields[attribute]
                            value = field.to_python(self.data[attribute])
                        else:
                            value = None
                        setattr(object, attribute, value)
                    #else:
                    #    pass #value = int(self.data[attribute])

        return object