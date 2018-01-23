from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
import os
import pip
import django

REQUIREMENTS = r'requirements\requirements.txt'

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sistema_contabil.settings")


class Command(BaseCommand):

    help = 'Print hello world'

    def handle(self, **options):
        django.setup()
        pip.main(['install', '-r', REQUIREMENTS])
        call_command('bower', 'install')
        call_command('makemigrations')
        call_command('migrate')