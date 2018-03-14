import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sistema_contabil.settings")
django.setup()

#from notifications.signals import notify
from django.contrib.auth.models import User
from django.test.utils import override_settings

i = User.objects.all()
print(i)
user = User.objects.get(pk=i)
print(user)


@override_settings(SITE_ID=1)
def notify_send():
    pass
    #notify.send(user, recipient=i, verb='TUDO FUNCIONANDO DE BOAS AQUI')


if __name__=='__main__':
    notify_send()