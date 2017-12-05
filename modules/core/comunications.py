from conf.configurations import SystemVariables
from modules.core.utils import send_email


def send_generate_activation_code(email,activation_code):
    html_content = SystemVariables.messages_email.confirmation_user_email
    url_confirmation = "http://localhost:8000/register/activate/"+email+"/"+activation_code+"/"
    html_content = html_content.replace('{{ CONFIRMATION_URL }}',url_confirmation)
    return send_email(to_address=email, title="Melinux Sistema - Confirmação de email", message=html_content)


def resend_generate_activation_code(email,activation_code):
    html_content = SystemVariables.messages_email.resend_activation_code_email
    url_confirmation = "http://localhost:8000/register/activate/"+email+"/"+activation_code+"/"
    html_content = html_content.replace('{{ CONFIRMATION_URL }}',url_confirmation)
    return send_email(to_address=email, title="Melinux Sistema - Confirmação de email", message=html_content)


def send_reset_password(senha, email):
    html_content = SystemVariables.messages_email.reset_password_email
    html_content = html_content.replace('{{ NEW_PASSWORD }}', senha)
    return send_email(to_address=email, title="Melinux Sistema - Recuperar Acesso", message=html_content)
