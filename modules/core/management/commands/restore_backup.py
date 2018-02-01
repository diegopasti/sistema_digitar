from django.core.management.base import BaseCommand, CommandError
from modules.nucleo.models import Backup
from libs.backup.backup import BackupManager


class Command(BaseCommand):
    help = 'Print hello world'

    def handle(self, **options):

        #self.stdout.write('Hello World')
        restore = BackupManager().restore_backup()
        print(restore)
