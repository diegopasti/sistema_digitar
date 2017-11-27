#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
from django.conf import settings

__version__ = "0.1"

import re
import os
import sys
import gzip
import shutil
import dropbox
import datetime
from dropbox import Dropbox
from django.core.files.storage import Storage
from django.core.exceptions import ImproperlyConfigured
from django.core.management import execute_from_command_line

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sistemaweb.settings")

from dbbackup.management.commands import dbbackup

DROPBOX_OAUTH2_TOKEN = 'r2VjuxIaDQAAAAAAAAAAD7YKqJlAJSdXsRz3IWYGHs2Q_BEnim1nOc3-LA1PspKi'
DROPBOX_ROOT_PATH = '/sistemaweb/backup'
DROPBOX_ROOT_PATH_NEW = '/sistemaweb/backup'
ROOT_DIR = settings.BASE_DIR
FILEPATH = dbbackup.get_connector().settings['NAME']


class DropBoxStorage(Storage):
    """DropBox Storage class for Django pluggable storage system."""

    CHUNK_SIZE = 4 * 1024 * 1024

    def __init__(self, oauth2_access_token=None, root_path=None):
        oauth2_access_token = DROPBOX_OAUTH2_TOKEN
        self.root_path = DROPBOX_ROOT_PATH
        if oauth2_access_token is None:
            raise ImproperlyConfigured("Você deve configurar um token em DROPBOX_OAUTH2_TOKEN ou em settings.py")
        self.dbx = Dropbox(oauth2_access_token)

    def user_profile(self):
        self.dt = self.dbx.users_get_current_account()
        print(self.dt)

    def list_dir_and_files_all(self):
        try:
            self.dt = self.dbx.files_list_folder(self.root_path)
            print('DIRETÓRIOS\n')
            self.list_subdirs(self.dt)
        except:
            self.dt = self.dbx.files_get_metadata(self.root_path)
            print('ARQUIVOS\n')
            if (isinstance(self.dt, dropbox.files.FileMetadata)):
                print('FUNCIONA')
            file = self.list_files(self.dt)
            return file

    def list_subdirs(self, dt):
        for entry in self.dt.entries:
            i = entry.path_display
            print(i)

    def list_files(self):
        self.dt = self.dbx.files_get_metadata(self.root_path)
        file = self.dt.path_display
        print(file)
        return file

    def upload_file(self):
        #print('Uploading para pasta ', DROPBOX_ROOT_PATH_NEW)
        time = datetime.datetime.now()
        time = time.strftime("%Y%m%d%H%M%S")
        FILEPATH = self.simple_backup()



        with open(FILEPATH, 'rb') as f:
            self.dbx.files_upload(f.read(), DROPBOX_ROOT_PATH_NEW + '/' + time + '.dump')
        link = self.dbx.sharing_create_shared_link_with_settings(DROPBOX_ROOT_PATH_NEW + '/' + time + '.dump')
        url = link.url
        dl_url = re.sub(r"\?dl\=0", "?dl=1", url)
        return dl_url

    def upload_file_compress(self, filename=''):
        print('Uploading para pasta ', DROPBOX_ROOT_PATH_NEW)
        t = datetime.datetime.now()
        t.strftime("%Y%m%d%H%M%S")
        new_basename = os.path.basename(filename)
        with open(filename, 'rb') as f:
            self.dbx.files_upload(f.read(), DROPBOX_ROOT_PATH_NEW + '/' + new_basename)
        link = self.dbx.sharing_create_shared_link_with_settings(
            DROPBOX_ROOT_PATH_NEW + '/' + new_basename)
        url = link.url
        dl_url = re.sub(r"\?dl\=0", "?dl=1", url)
        return dl_url

    def download_file(self, file=''):
        self.file = (DROPBOX_ROOT_PATH + '/' + file)
        file_name = self.file.replace('/sistemaweb/backup/', '')
        print('\nDownloading... /data/backup/' + file_name)
        try:
            metadata, res = self.dbx.files_download(self.file)
        except:
            pass
            metadata, res = self.dbx.files_download(file)
        final_path = ROOT_DIR + '/data/backup/' + file_name
        f = open(final_path, "wb")
        f.write(res.content)
        f.close()
        if '.zip' in final_path or '.gz' in final_path:
            print('Arquivo compactado...efetuando descompressão de dados.')
            self.uncompress_file(final_path)
            new_basename = os.path.basename(final_path).replace('.gz', '')
            return new_basename
        return final_path

    def list_dirs_root_path(self):
        self.dt = self.dbx.files_list_folder(self.root_path)
        #print('ARQUIVOS ENCONTRADOS SERÃO LISTADOS ABAIXO:\n')
        dir = self.download_file(self.dt.entries[-1].path_display) #self.list_files_root_path(self.dt)
        return dir

    def list_files_all(self):
        self.dt = self.dbx.files_list_folder(self.root_path)
        #print('ARQUIVOS ENCONTRADOS SERÃO LISTADOS ABAIXO:\n')
        self.data = []
        for entry in self.dt.entries:
            data = {}
            data['backup_link']
            data['client_modified'] = entry.client_modified
            data['size'] = str(entry.size)+" bytes"
            t = entry.client_modified
            time = datetime.timedelta(hours=2)
            hora = datetime.datetime.strptime(str(t), '%Y-%m-%d %H:%M:%S')
            now = hora - time
            size = entry.size
            size = str(size)+' bytes'
            display = entry.path_display
            print(display, now , size)
            self.data.append(data)
        return self.data

    def simple_backup(self):
        g = dbbackup.get_connector()
        execute_from_command_line(["manage.py", "dbbackup", "-v", "1"])
        filename = (ROOT_DIR + '/data/backup/' + g.generate_filename())
        #print(filename)
        return filename

    def compress_file(self, filename='', n=''):
        if n == '':
            self.compress_all(filename)
        elif n == '1':
            file = self.compress_all(filename)
            action = self.upload_file_compress(file)
            return action

    def compress_all(self, filename):
        if 'C:' in filename:
            new_basename = os.path.basename(filename)
            file = (ROOT_DIR + '/data/backup/' + new_basename + '.gz')
            f = open(filename, 'rb')
            data = f.read()
            f = gzip.open(file, 'wb')
            f.write(data)
            f.close()
            #print('Arquivo compactado com sucesso!!!')
            return file
        else:
            filepath = (ROOT_DIR + '/data/backup/' + filename)
            file = (ROOT_DIR + '/data/backup/' + filename + '.gz')
            f = open(filepath, 'rb')
            data = f.read()
            f = gzip.open(file, 'wb')
            f.write(data)
            f.close()
            #print('Arquivo compactado com sucesso!!!')
            return file

    def uncompress_file(self, filename):
        if 'C:' in filename:
            new_basename = os.path.basename(filename).replace('.gz', '')
            local_file = (ROOT_DIR + '/data/backup/' + new_basename)
            f = gzip.open(filename, 'rb')
            data = f.read()
            f.close()
            f = open(local_file, 'wb')
            f.write(data)
            f.close()
            print('Arquivo descomprimido com sucesso!!!')
        else:
            local_file = (ROOT_DIR + '/data/backup/' + filename)
            new_basename = os.path.basename(filename).replace('.gz', '')
            file = (ROOT_DIR + '/data/backup/' + new_basename)
            f = gzip.open(local_file, 'rb')
            data = f.read()
            f.close()
            f = open(file, 'wb')
            f.write(data)
            f.close()
            print('Arquivo descomprimido com sucesso!!!')

    def restore_db(self, filepath=''):
        print("VEJA O FILEPATH: ",filepath)
        execute_from_command_line(["manage.py", "dbrestore", "-v", "1", "--noinput", "-i", filepath])

    def restore(self):  # faz a restauração do banco de dados a partir de um backup salvo na dropbox.
        file_name = DropBoxStorage().list_dirs_root_path()
        new_basename = file_name
        if '/' in file_name:
            basename = shutil.copy(file_name, ROOT_DIR + '/data/backup/')
            new_basename = os.path.basename(basename)
        DropBoxStorage().restore_db(new_basename)

        from django.core.management import call_command
        import django
        django.setup()

        call_command('dbrestore', '-v', '1',  "--noinput", "-i", new_basename)

        #execute_from_command_line(["manage.py", "dbrestore", "-v", "1", "--noinput", "-i", new_basename])

        """
        print("VEJA O ARG: ",arg)
        if '/' in new_basename:
            basename = shutil.copy(new_basename, ROOT_DIR + '/data/backup/')
            new_basename = os.path.basename(basename)
            self.restore_db(new_basename)
        else:
            print("VEJA O CAMINHO PRA COPIAR O ARQuivO:",ROOT_DIR + '/data/backup/')
            basename = shutil.copy(new_basename, ROOT_DIR + '/data/backup/')
            print("CONSEGUI O BASENAME: ",basename)
            new_basename = os.path.basename(basename)
            self.restore_db(new_basename)
        """




if __name__ == '__main__':

    import getopt


    def usage():
        print(' --list <list files> - Lista os arquivos da pasta;')
        print(' --upload <upload file> - Faz o upload de um backup;')
        print(' --download <download file> - Restaura do último backup realizado;')
        print(' --path - Indique o local de um arquivo;')
        print(' --version - Informações sobre a versão do script;')
        print(' --help - Ajuda!!!')


    def version():
        print(__version__)


    try:
        opts, args = getopt.getopt(sys.argv[1:], "dpc:nuv", [  # arguments
                                                                'list',
                                                                'upload',
                                                                'version',
                                                                'help',
                                                                'backup',
                                                                'restore',
                                                                'download=',
                                                                'compress',
                                                                'uncompress=',
                                                                'dbcompress',
                                                                'dbuncompress',
                                                                'db=',
                                                                'path='])
    except getopt.GetoptError:
        usage()
        sys.exit(1)
    for opt, arg in opts:
        print(opt)
        print(arg)
        if opt in ('-h', '--help'):
            usage()
        elif opt in ('-v', '--version'):
            version()
        elif opt in ('-d', '--download'):
            if opt == '-d':
                DropBoxStorage().list_dirs_root_path()
            elif opt == '--download':
                print(arg)
                DropBoxStorage().download_file(arg)
        elif opt in '--backup':
            sp = DropBoxStorage().simple_backup()
        elif opt in '--restore':
            arg = DropBoxStorage().list_dirs_root_path()
            new_basename = (arg)
            print(new_basename)
            if '/' in new_basename:
                basename = shutil.copy(new_basename, ROOT_DIR + '/data/backup/')
                new_basename = os.path.basename(basename)
                print(new_basename)
            restore = DropBoxStorage().restore_db(new_basename)
        elif opt in '--upload':
            link = DropBoxStorage().upload_file()
            print(link)
        elif opt in '--list':
            DropBoxStorage().list_files_all()
        elif opt in ('-c', '--compress'):
            if opt == '-c':
                DropBoxStorage().compress_file(arg)
            elif opt == '--compress':
                arg = DropBoxStorage().simple_backup()
                try:
                    DropBoxStorage().compress_file(arg)
                except:
                    pass
                try:
                    DropBoxStorage().compress_file(sp)
                except:
                    pass
                    #usage()
        elif opt in '--uncompress':
            action = DropBoxStorage().uncompress_file(arg)
        elif opt in '--db':
            DropBoxStorage().compress_file(arg, n='1')
        elif opt in '--dbcompress':
            arg = DropBoxStorage().simple_backup()
            link = DropBoxStorage().compress_file(arg, n='1')
            print(link)
        elif opt in '--dbuncompress':
            arg = DropBoxStorage().list_dirs_root_path()


    def backup_file():  # faz backup simples local.
        DropBoxStorage().simple_backup()


    def list_files_dropbox():  # lista os arquivos de backup da dropbox.
        DropBoxStorage().list_files_all()


    def backup_for_dropbox():  # faz upload de arquivos para a dropbox e retorna um link para download.
        arg = DropBoxStorage().simple_backup()
        link = DropBoxStorage().compress_file(arg, n='1')
        print(link)


    def restore_db():  # faz a restauração do banco de dados a partir de um backup salvo na dropbox.
        arg = DropBoxStorage().list_dirs_root_path()
        new_basename = (arg)
        if '/' in new_basename:
            basename = shutil.copy(new_basename, ROOT_DIR + '/data/backup/')
            new_basename = os.path.basename(basename)
        DropBoxStorage().restore_db(new_basename)