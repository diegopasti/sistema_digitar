from django.core.management import call_command
import datetime
import dropbox
import shutil
import django
import re
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sistema_contabil.settings")

from sistema_contabil.settings import DBBACKUP_STORAGE_OPTIONS, DROPBOX_ROOT_PATH, DROPBOX_OAUTH2_TOKEN


class BackupManager:

    dropbox = None

    def __init__(self):
        pass

    def create_backup(self):
        self.dropbox = dropbox.Dropbox(DROPBOX_OAUTH2_TOKEN)
        start_timing_backup = datetime.datetime.now()
        django.setup()
        call_command('dbbackup', '-v', '1', '-z')
        backup = self.upload()
        link = backup['link']
        name = backup['file_name']
        size = backup['size']
        self.clear_temp_file()
        backup_duration = datetime.datetime.now() - start_timing_backup
        print("Backup gerado em",backup_duration.total_seconds(),"segundos")
        print("Arquivo disponivel em "+link)
        #print("Nome: "+name)
        #print("Disponivel em: "+link)
        #print("Tamanho em bytes: "+size)
        return backup

    def restore_backup(self):
        self.dropbox = dropbox.Dropbox(DROPBOX_OAUTH2_TOKEN)
        start_timing_backup = datetime.datetime.now()
        list_files = self.dropbox.files_list_folder(DROPBOX_ROOT_PATH)
        most_recent_backup = self.download(list_files.entries[-1].path_display)
        django.setup()
        call_command('dbrestore', '-v','0', '-i', 'temp.dump.gz', '-z', '-q','--noinput')
        self.clear_temp_file()
        backup_duration = datetime.datetime.now() - start_timing_backup
        print("Backup Restaurado em", backup_duration.total_seconds(), "segundos")
        return True

    def list_backup(self):
        print('\n')
        self.dropbox = dropbox.Dropbox(DROPBOX_OAUTH2_TOKEN)
        self.dt = self.dropbox.files_list_folder(DROPBOX_ROOT_PATH)
        self.data = []
        for entry in self.dt.entries:
            data = {}
            filename = entry.name
            path_name = entry.path_lower
            link = self.dropbox.sharing_create_shared_link(path_name)  # Mesmo estando obsoleto,esse é o único modo de retornar o link de arquivos já compartilhados...
            url = link.url
            dl_url = re.sub(r"\?dl\=0", "?dl=1", url)
            modified = entry.client_modified
            time = datetime.timedelta(hours=2)
            hora = datetime.datetime.strptime(str(modified), '%Y-%m-%d %H:%M:%S')
            now = hora - time
            data['file_name'] = filename
            data['link'] = dl_url
            data['client_modified'] = entry.client_modified
            data['size'] = str(entry.size)+" bytes"
            size = str(entry.size)
            display = entry.name
            print(display, now , size, '\n'+dl_url)
            self.data.append(data)
        #print(self.data)
        return self.data


    def download(self, file):
        self.file = (file)
        self.file.replace('/backup/', '')
        try:
            metadata, res = self.dropbox.files_download(self.file)
        except Exception as erro:
            print("Erro! ", erro)

        final_path = DBBACKUP_STORAGE_OPTIONS['location'] + '/temp.dump.gz'
        f = open(final_path, "wb")
        f.write(res.content)
        f.close()
        return final_path

    def upload(self):
        self.data = []
        data = {}
        temp_file = DBBACKUP_STORAGE_OPTIONS['location']+'/temp.dump.gz'
        shutil.copy(temp_file,'data/backup/last_backup.dump.gz')
        time = datetime.datetime.now()
        export_name = DROPBOX_ROOT_PATH+'/'+time.strftime("%Y%m%d%H%M%S")+'.dump.gz'

        with open(temp_file, 'rb') as f:
            self.dropbox.files_upload(f.read(), export_name)
        link = self.dropbox.sharing_create_shared_link_with_settings(export_name)
        url = link.url
        dl_url = re.sub(r"\?dl\=0", "?dl=1", url)
        data['file_name'] = link.name
        data['link'] = dl_url
        data['client_modified'] = link.client_modified
        data['size'] = int(link.size)

        return data
        #return dl_url

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

