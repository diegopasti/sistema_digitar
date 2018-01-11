from django.conf.urls import url
from modules.user.api import UserController

urlpatterns = [

    url(r'save/register',UserController().salvar_registro),
    url(r'login/autentication$', UserController().login_autentication),
    url(r'update/$',UserController().upate_user),
    url(r'reset_password/$', UserController().reset_password),
    url(r'change_password/$', UserController().change_password),
    url(r'reactivate$', UserController().resend_activation_code),
    url(r'change_personal_info/$',UserController().change_personal_info),

    # User Administration
    url(r'filter/', UserController().filter_users),
    url(r'save/first/register/', UserController().save_first_register),
    # APIs administrativas
    url(r'chage_active/$', UserController().change_active),
]
