from libs.backup.dbdropbox import DropBoxStorage
from django.core.management import call_command
import datetime
import dropbox
import django
import re
import os

from sistemaweb.settings import DBBACKUP_STORAGE_OPTIONS, DROPBOX_ROOT_PATH, DROPBOX_OAUTH2_TOKEN


class BackupManager:

    dropbox = None

    def __init__(self):
        self.dropbox = dropbox.Dropbox(DROPBOX_OAUTH2_TOKEN)

    def create_backup(self):
        start_timing_backup = datetime.datetime.now()
        django.setup()
        call_command('dbbackup', '-v', '1', '-z')
        backup_path = self.upload()
        self.clear_temp_file()
        backup_duration = datetime.datetime.now() - start_timing_backup
        print("Backup gerado em",backup_duration.total_seconds(),"segundos")
        print("Arquivo disponivel em "+backup_path)
        return backup_path

    def restore_backup(self):
        start_timing_backup = datetime.datetime.now()
        list_files = self.dropbox.files_list_folder(DROPBOX_ROOT_PATH)
        most_recent_backup = self.download(list_files.entries[-1].path_display)  # self.list_files_root_path(self.dt)
        django.setup()
        call_command('dbrestore', '-v','0', '-i', 'temp.dump.gz', '-z', '-q','--noinput')
        self.clear_temp_file()
        backup_duration = datetime.datetime.now() - start_timing_backup
        print("Backup Restaurado em", backup_duration.total_seconds(), "segundos")
        return True

    def list_backup(self):
        return DropBoxStorage().list_files_all()

    def download(self,file):
        self.file = (file)
        file_name = self.file.replace('/backup/', '')
        try:
            metadata, res = self.dropbox.files_download(self.file)
        except Exception as erro:
            print("Erro! ",erro)

        final_path = DBBACKUP_STORAGE_OPTIONS['location']+'/temp.dump.gz'
        f = open(final_path, "wb")
        f.write(res.content)
        f.close()
        return final_path

    def upload(self):
        temp_file = DBBACKUP_STORAGE_OPTIONS['location']+'/temp.dump.gz'
        time = datetime.datetime.now()
        export_name = DROPBOX_ROOT_PATH+'/'+time.strftime("%Y%m%d%H%M%S")+'.dump.gz'

        with open(temp_file, 'rb') as f:
            self.dropbox.files_upload(f.read(), export_name)
        link = self.dropbox.sharing_create_shared_link_with_settings(export_name)
        url = link.url
        dl_url = re.sub(r"\?dl\=0", "?dl=1", url)
        return dl_url

    def clear_temp_file(self):
        backup_file = DBBACKUP_STORAGE_OPTIONS['location'] + '/temp.dump.gz'
        if os.path.isfile(backup_file):
            os.remove(backup_file)

if __name__=='__main__':
    import sys
    arguments = sys.argv
    backup_manage = BackupManager()
    if "create" in arguments:
        backup_manage.create_backup()
    elif "restore" in arguments:
        backup_manage.restore_backup()
    elif "list" in arguments:
        backup_manage.list_backup()
    else:
        pass

