from django.core.management.base import BaseCommand, CommandError
from libs.backup.backup import BackupManager
from django.core.management import call_command
from dbbackup.db.sqlite import SqliteConnector, SqliteCPConnector
from django.utils.six import BytesIO
import django
import gzip
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sistema_contabil.settings")


class Command(BaseCommand):
    help = 'Print hello world'

    def handle(self, **options):

        '''
            path = 'data/backup/temp.dump'
            path_zip = 'data/backup/temp.dump.gz'
            connector = SqliteCPConnector()
            dump = connector.create_dump()
            with open(path, 'wb') as f:
                f.write(dump.read())
            with open(path, 'rb') as f:
                data = f.read()
            with gzip.open(path_zip, 'wb') as f:
                f.write(data)
                f.close()
            #file_dump = BackupManager().download_last_file()
            #print(file_dump)
            with gzip.open(path_zip, 'rb') as f:
                file_content = BytesIO(f.read())
            connector.restore_dump(file_content)
        '''

        django.setup()
        #call_command('flush', '--no-input')
        restore = BackupManager().restore_backup()
        print(restore)
