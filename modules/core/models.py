from django.db import models

from modules.core.config import ERRORS_MESSAGES, BaseConfiguration
#from modules.entity.models import BaseModel


#class Backup(models.Model):
#    created_date = models.DateTimeField(auto_now_add=True, null=False)
#    backup_file_name = models.CharField("Nome do Arquivo", null=False, blank=False, max_length=100, validators=[],error_messages=ERRORS_MESSAGES)
#    backup_size = models.PositiveIntegerField("Tamanho do Arquivo", null=False, error_messages=ERRORS_MESSAGES)
#    backup_link = models.CharField("Endereço", null=False, blank=False, max_length=100, validators=[], error_messages=ERRORS_MESSAGES)