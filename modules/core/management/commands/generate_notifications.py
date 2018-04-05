from django.core.management.base import BaseCommand, CommandError
from modules.nucleo.models import Backup
from libs.backup.backup import BackupManager


class Command(BaseCommand):
    help = 'Comando para gerar notificações do sistema.'

    def handle(self, **options):
        from modules.core.services import NotificationsControl
        NotificationsControl().generate_notifications()
        print("Notificações carregadas com sucesso!")
        #backup_paramters = BackupManager().create_backup()
        #try:
        #    backup = Backup.objects.get(backup_file_name=backup_paramters['file_name'])
        #except:
        #    backup = Backup()

        #backup.backup_file_name = backup_paramters['file_name']
        #backup.backup_link = backup_paramters['link']
        #backup.backup_size = backup_paramters['size']
        #backup.save()
