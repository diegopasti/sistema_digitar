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
        link_folder = backup['folder_link']
        self.clear_temp_file()
        backup_duration = datetime.datetime.now() - start_timing_backup
        print("Backup gerado em",backup_duration.total_seconds(),"segundos")
        #print("Arquivo disponivel em "+link)
        #print("Nome: "+name)
        #print("Tamanho em bytes: "+str(size))
        #print("Pasta compartilhada: "+link_folder)
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
        metadata = []
        for entry in self.dt.entries:
            data = {}
            filename = entry.name
            display = entry.name
            path_name = entry.path_lower
            size = entry.size
            filesize = '{0:.2f}'.format(size/1024)
            #print(filesize)
            #print(int(float(filesize)))
            link = self.dropbox.sharing_create_shared_link(path_name)  # Mesmo estando obsoleto,esse é o único modo de retornar o link de arquivos já compartilhados...
            url = link.url
            #dl_url = re.sub(r"\?dl\=0", "?dl=1", url)
            modified = entry.client_modified
            time = datetime.timedelta(hours=2)
            hora = datetime.datetime.strptime(str(modified), '%Y-%m-%d %H:%M:%S')
            now = hora - time
            print(display, now , filesize, '\n'+url)
            data['file_name'] = filename
            data['link'] = url
            data['client_modified'] = entry.client_modified
            data['size'] = filesize
            metadata.append(data)
            #print(metadata)
            #print(data)
        return metadata


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

    def shared_folder(self):
        #self.data = []
        #data = {}
        self.dropbox = dropbox.Dropbox(DROPBOX_OAUTH2_TOKEN)
        #link = self.dropbox.sharing_create_shared_link_with_settings(DROPBOX_ROOT_PATH)
        link = self.dropbox.sharing_create_shared_link(DROPBOX_ROOT_PATH)  # Mesmo estando obsoleto,esse é o único modo de retornar o link de arquivos já compartilhados...
        shared_link = link.url
        print('\n',shared_link)
        return shared_link
        #data['folder_link'] = link.url
        #return data


    def upload(self):
        self.data = []
        data = {}
        temp_file = DBBACKUP_STORAGE_OPTIONS['location']+'/temp.dump.gz'
        time = datetime.datetime.now()
        shutil.copy(temp_file,'data/backup/'+time.strftime("%Y%m%d%H%M%S")+'.dump.gz')
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
        data['folder_link'] = self.shared_folder()

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
    elif "shared" in arguments:
        backup_manage.shared_folder()
    else:
        pass

