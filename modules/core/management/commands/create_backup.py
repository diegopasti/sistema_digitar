from django.core.management.base import BaseCommand, CommandError
from modules.nucleo.models import Backup
from libs.backup.backup import BackupManager


class Command(BaseCommand):
    help = 'Print hello world'

    def handle(self, **options):

        #self.stdout.write('Hello World')
        backup_paramters = BackupManager().create_backup()
        try:
            backup = Backup.objects.get(backup_file_name=backup_paramters['file_name'])
            print("JA EXISTE")
        except:
            backup = Backup()
            print("VOU CRIAR")

        backup.backup_file_name = backup_paramters['file_name']
        backup.backup_link = backup_paramters['link']
        backup.backup_size = backup_paramters['size']
        backup.save()
