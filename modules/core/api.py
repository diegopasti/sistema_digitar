import os
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import Http404
from django.utils.decorators import method_decorator
from libs.backup.backup import BackupManager
from libs.backup.pygit import check_update, update, install, checkout
from libs.default.core import BaseController
from modules.nucleo.models import Backup, RestrictedOperation
from modules.user.models import User
from sistema_contabil import settings
# from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
# from selenium import webdriver

class RestrictedOperationCotroller (BaseController):
    def load_operations (self, request):
        self.start_process(request)
        list = BaseController().filter(request, RestrictedOperation, extra_fields=['username'], is_response=False)
        for operation in list['object']:
            try:
                user = User.objects.get(id=int(operation['user']))
                operation['username'] = user.get_full_name()
            except Exception as error:
                print('SOU ERRO', error)
        print(list['object'])
        return self.response(list)
        #print("Vindo aqui")
        '''response_dict = {}
        response_dict['result'] = False
        response_dict['object'] = None
        try:
            list_operations = RestrictedOperation.objects.all()
            for operation in list_operations:
                operation_dict = {}
                operation_dict['user']
        return'''

class ConfigurationsController(BaseController):

    #method_decorator(login_required)
    #user_passes_test(lambda u: u.permissions.can_view_entity(), login_url='/error/access_denied', redirect_field_name=None)
    def load_backups(self, request):
        x = BaseController().filter(request, model=Backup)
        #print("VEJA O QUE TENHO QUE ENVIAR: ",x)
        return BaseController().filter(request, model=Backup, limit=12)

    def create_backup_local(self, request):
        self.start_process(request)
        backup_paramters = BackupManager().create_backup_local()
        #print('BACKUP REALIZADO COM SUCESSO.')
        response_dict = {}
        response_dict['result'] = True
        response_dict['message'] = ""
        response_dict['object'] = True
        return self.response(response_dict)
    """ backup = Backup()
        backup.backup_file_name = backup_paramters['file_name']
        backup.backup_link = 'Null'
        backup.backup_size = backup_paramters['size']
        self.get_exceptions(backup, None)
        if self.full_exceptions == {}:
            response_dict = self.execute(backup, backup.save)
        else:
            response_dict = self.notify.error(self.full_exceptions)
        return self.response(response_dict)
        """

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
        backup_paramters = BackupManager().restore_backup()
        response_dict = {}
        response_dict['result'] = True
        response_dict['message'] = ""
        response_dict['object'] = backup_paramters
        if backup_paramters is True:
            pass
            #print('RESTAURAÇÃO REALIZADA COM SUCESSO')
        else:
            pass
            #print('ERRO',backup_paramters)
        return self.response(response_dict)

    def list_backups(self,request):
        self.start_process(request)
        backup_list = BackupManager().list_backup()
        new_list = []
        for item in reversed(backup_list):
            if len(new_list) == 10:
                break
            else:
                new_list.append(item)

        backup_list = new_list
        response_dict = {}
        response_dict['result'] = True
        response_dict['message'] = ""
        response_dict['object'] = backup_list
        #print("VEJA A LISTA:", backup_list)
        #for item in backup_list:
        #    response_data = {}
        #    response_data['object'] = {}
        #    response_dict['object']['file_name'] = item['file_name']
        #    response_dict['object']['link'] = item['link']
        #    response_dict['object']['size'] = item['size']
        #    response_dict['object']['date'] = item['client_modified']
        #    print('SOU RESPONSE',response_dict)
        return self.response(response_dict)


    def check_available_space(self,request):
        self.start_process(request)
        backup_list = Backup.objects.all()
        response_dict = {}
        response_dict['result'] = True
        response_dict['message'] = ""
        response_dict['object'] = {}
        response_dict['object']['total_files'] = len(backup_list)
        response_dict['object']['total_space'] = 2000000000
        response_dict['object']['used_space'] = 0

        for item in backup_list:
            response_dict['object']['used_space'] = response_dict['object']['used_space'] + item.backup_size
        response_dict['object']['used_percent_space'] = round((response_dict['object']['used_space'] / response_dict['object']['total_space']) * 100, 2)

        #print("ESPACO DE ARMAZENAMENTO: ",response_dict)
        return self.response(response_dict)

    def check_available_system_space(self,request):
        self.start_process(request)
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(settings.DBBACKUP_STORAGE_OPTIONS['location']):
            for f in filenames:
                filepath = os.path.join(dirpath, f)
                total_size += os.path.getsize(filepath)/1024
                file_count = len(filenames)
        #print(settings.DBBACKUP_STORAGE_OPTIONS['location'])
        #print(total_size)
        
        if total_size < 1024:
            total_size = '{0:.2f}'.format(total_size)
            suffix = ' Kb'
        elif total_size >= 1024:
            total_size = '{0:.1f}'.format(total_size/1024)
            suffix = ' Mb'
        elif total_size >= 1024*1024:
            total_size = '{0:.1f}'.format(total_size/1024)
            suffix = ' Gb'

        response_dict = {}
        response_dict['result'] = True
        response_dict['message'] = ""
        response_dict['object'] = {}
        response_dict['object']['total_files'] = file_count
        response_dict['object']['folder_size'] = total_size + suffix

        return self.response(response_dict)

    def check_available_space1(self,request):
        self.start_process(request)
        #backup_list = BackupManager().list_backup()
        backup_list = Backup.objects.all()

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
        response_dict['object']['used_space'] = '{0:.2f}'.format(response_dict['object']['used_space'])
        #print('RESPONSE:',(response_dict['object']['used_space']))
        response_dict['object']['used_percent_space'] = round((float(response_dict['object']['used_space']) / response_dict['object']['total_space']) * 100, 2)
        #print("PERCENTUAL: ",float(response_dict['object']['used_space']) / response_dict['object']['total_space'])
        #print("ESPACO DE ARMAZENAMENTO: ",response_dict)
        return self.response(response_dict)

    def version_update(self,request):
        self.start_process(request)
        version_check = check_update()
        response_dict = {}
        response_dict['result'] = True
        response_dict['message'] = ""
        response_dict['object'] = {}
        if version_check['local'] != version_check['remote']:
            response_dict['object']['available_update'] = True
        else:
            response_dict['object']['available_update'] = False
        response_dict['object']['local'] = version_check['local'][0:8]
        response_dict['object']['remote'] = version_check['remote'][0:8]
        response_dict['object']['last_update'] = version_check['last_update']
        #print("VEJA A VERSÃO: ",response_dict)
        return self.response(response_dict)

    def update(self,request):
        self.start_process(request)
        # check_index = checkout()
        updating = update()
        # print('DEU CERTO')
        try:
            install_pack = install()
            response_dict = {}
            response_dict['result'] = True
            response_dict['object'] = None
            response_dict['message'] = 'Atualização realizada com sucesso.'
        except Exception as error:
            response_dict = self.notify.error(error)

        return self.response(response_dict)

    def shared_folder(self,request):
        self.start_process(request)
        backup_link_folder = BackupManager().shared_folder()
        response_dict = {}
        response_dict['result'] = True
        response_dict['message'] = ""
        response_dict['object'] = backup_link_folder
        #print("OLHE A LISTA:", backup_link_folder)
        return self.response(response_dict)

    '''def manager_dropbox(self,request):
        drive = settings.SELENIUM_CHROMEDRIVER
        binary = FirefoxBinary(settings.MOZILLA_FIREFOX_TEST_PATH)
        capabilities = webdriver.DesiredCapabilities().FIREFOX
        capabilities["marionette"] = True
        admin = settings.ADM_DROPBOX
        key = settings.KEY_DROPBOX
        browser = webdriver.Firefox(firefox_binary=binary, executable_path=settings.SELENIUM_GECKODRIVER_MOZILLA,capabilities=capabilities)
        browser = webdriver.Chrome(executable_path=str(drive))
        browser.get("https://www.dropbox.com/home/backup")
        list_of_inputs = browser.find_elements_by_xpath("//div/input[starts-with(@id,'pyxl')]")
        list_of_inputs[0].send_keys(admin)
        list_of_inputs[1].send_keys(key)
        sign_in = browser.find_element_by_class_name("login-button").click()
        response_dict = {}
        response_dict['result'] = True
        response_dict['message'] = ""
        response_dict['object'] = True
        return self.response(response_dict)
    '''

    def last_backup(self, request):
        x = BaseController().filter(request, model=Backup)
        #print("VEJA O QUE TENHO QUE ENVIAR: ",x)
        return BaseController().filter(request, model=Backup, limit=1)

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
