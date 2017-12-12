from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import Http404
from django.utils.decorators import method_decorator

from libs.backup.backup import BackupManager
#from libs.backup.pygit import check_update
from libs.default.core import BaseController
from modules.core.models import Backup
#from modules.user.models import User
from sistema_contabil import settings

class ConfigurationsController(BaseController):

    #method_decorator(login_required)
    #user_passes_test(lambda u: u.permissions.can_view_entity(), login_url='/error/access_denied', redirect_field_name=None)
    def load_backups(self, request):
        x = BaseController().filter(request, model=Backup)
        print("VEJA O QUE TENHO QUE ENVIAR: ",x)
        return BaseController().filter(request, model=Backup)

    def create_backup(self,request):
        self.start_process(request)
        backup_paramters = BackupManager().create_backup()
        backup = Backup()
        backup.backup_file_name = backup_paramters['file_name']
        backup.backup_link = backup_paramters['link']
        backup.backup_size = backup_paramters['size']
        self.get_exceptions(backup, None)
        if self.full_exceptions == {}:
            response_dict = self.execute(backup, backup.save)
        else:
            response_dict = self.notify.error(self.full_exceptions)
        return self.response(response_dict)

    def restore_backup(self,request):
        self.start_process(request)
        backup_paramters = BackupManager().create_backup()
        backup = Backup()
        backup.backup_file_name = backup_paramters['file_name']
        backup.backup_link = backup_paramters['link']
        backup.backup_size = backup_paramters['size']

        self.get_exceptions(backup, None)
        if self.full_exceptions == {}:
            response_dict = self.execute(backup, backup.save)
        else:
            response_dict = self.notify.error(self.full_exceptions)
        return self.response(response_dict)

    def check_available_space(self,request):
        self.start_process(request)
        backup_list = BackupManager().list_backup()
        response_dict = {}
        response_dict['result'] = True
        response_dict['message'] = ""
        response_dict['object'] = {}
        response_dict['object']['total_files'] = len(backup_list)
        response_dict['object']['total_space'] = 2000000000
        response_dict['object']['used_space'] = 0
        response_dict['object']['last_update'] = None
        for item in backup_list:
            response_dict['object']['used_space'] = response_dict['object']['used_space'] + float(item['size'])
        response_dict['object']['used_percent_space'] = round((response_dict['object']['used_space'] / response_dict['object']['total_space']) * 100, 2)
        print("PERCENTUAL: ",response_dict['object']['used_space'] / response_dict['object']['total_space'])
        print("ESPACO DE ARMAZENAMENTO: ",response_dict)
        return self.response(response_dict)

    def version_update(self,request):
        self.start_process(request)
        version_check = check_update()
        print('DICT VERSION:',version_check)
        response_dict = {}
        response_dict['result'] = True
        response_dict['message'] = ""
        response_dict['object'] = {}
        if version_check['local'] != version_check['remote']:
            response_dict['object']['available_update'] = True
        else:
            response_dict['object']['available_update'] = False
        response_dict['object']['local'] = version_check['local']
        response_dict['object']['remote'] = version_check['remote']
        print("VEJA A VERSÃO: ",response_dict)
        return self.response(response_dict)

    def update(self,request):
        self.start_process(request)
        updating = update()
        print('DICT VERSION:',updating)

    """def shared_folder(self,request):
        self.start_process(request)
        backup_paramters = BackupManager().shared_folder()
        backup = Backup()
        backup.backup_link_folder = backup_paramters['folder_link']
        self.get_exceptions(backup, None)
        if self.full_exceptions == {}:
            response_dict = self.execute(backup, backup.save)
        else:
            response_dict = self.notify.error(self.full_exceptions)
        return self.response(response_dict)
        """








class AbstractAPI:

    def filter_request(request, formulary=None):
        if request.is_ajax() or settings.DEBUG:
            if formulary is not None:
                form = formulary(request.POST)
                if form.is_valid():
                    return True, form
                else:
                    return False, form
            else:
                return True,True
        else:
            raise Http404
