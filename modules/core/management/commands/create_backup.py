import datetime
import re
import shutil

import django
import sys

from datetime import date

import dropbox as dropbox
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from dropbox import dropbox

from modules.nucleo.models import Backup
from libs.backup.backup import BackupManager
from django.conf import settings
from sistema_contabil.settings import BACKUP_FILE, BASE_DIR, DROPBOX_ROOT_PATH, DROPBOX_OAUTH2_TOKEN
import tarfile


class Command(BaseCommand):
    help = 'Print hello world'

    def handle(self, **options):
        start_timing_backup = datetime.datetime.now()
        data = BackupManager().novo_backup()

        backup_duration = datetime.datetime.now() - start_timing_backup
        print("Backup gerado em", backup_duration.total_seconds(), "segundos")

        try:
            backup = Backup.objects.get(backup_file_name=data['file_name'])
        except:
            backup = Backup()


        backup.backup_file_name = data['file_name']
        backup.backup_link = data['link']
        backup.backup_size = data['size']
        backup.save()

        #backup_paramters = BackupManager().create_backup()
        """start_timing_backup = datetime.datetime.now()
        django.setup()
        sysout = sys.stdout
        sys.stdout = open(BACKUP_FILE, 'w+')
        call_command('dumpdata')

        sys.stdout = sysout

        time = datetime.datetime.now()
        now = time.strftime("%p")
        if now == 'AM':
            now = 'mat'
        elif now == 'PM':
            now = 'vesp'
        dias = ('seg', 'ter', 'qua', 'qui', 'sex', 'sab', 'dom')
        hj = date.today()
        dia = dias[hj.weekday()]

        final_name = time.strftime(dia + "_" + now) + ".dump.tar.gz"

        tar_file = BACKUP_FILE.replace('dump.json',final_name)
        tar = tarfile.open(tar_file, "w:gz")
        tar.add(BACKUP_FILE)
        tar.close()


        # shutil.copy(temp_file,'data/backup/'+time.strftime("%a"+"_"+"%Y%m%d%I%M%S"+"_"+"%p")+".dump.gz")
        # export_name = DROPBOX_ROOT_PATH+'/'+time.strftime("%a"+"_"+"%Y%m%d%I%M%S"+"_"+"%p")+".dump.gz"


        data = {}
        temp_file = 'dump.tar.gz'
        root_path = BASE_DIR
        dp = dropbox.Dropbox(DROPBOX_OAUTH2_TOKEN)
        # self.dt = dropbox.users_get_current_account()
        share_folder = dp.sharing_share_folder(DROPBOX_ROOT_PATH)
        # print(self.dt)
        print(share_folder)

        final_file = BACKUP_FILE.replace('dump.json',final_name)
        export_name = DROPBOX_ROOT_PATH+"/"+final_name
        print("VEJA A PORCARIA DO FINAL NAME: ",export_name)
        with open(final_file, 'rb') as f:
            dropbox.files_upload(f.read(), export_name, mode=dp.files.WriteMode('overwrite'))
        try:
            link = dp.sharing_create_shared_link_with_settings(export_name)
        except:
            link = dp.sharing_create_shared_link(export_name)
        file_metadata = dp.files_get_metadata(export_name)
        print(file_metadata)
        url = link.url
        dl_url = re.sub(r"\?dl\=0", "?dl=1", url)
        data['file_name'] = file_metadata.name
        data['link'] = dl_url
        data['client_modified'] = file_metadata.client_modified
        data['size'] = int(file_metadata.size)
        data['folder_link'] = self.shared_folder()

        #self.clear_temp_file()
        """