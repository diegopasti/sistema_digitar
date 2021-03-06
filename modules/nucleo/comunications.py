from conf.configurations import SystemVariables
from modules.nucleo.utils import send_email
from sistema_contabil.settings import SERVER_ADDRESS


def send_generate_activation_code(email,activation_code):
    html_content = SystemVariables.messages_email.confirmation_user_email
    url_confirmation = "http://"+SERVER_ADDRESS+"/register/activate/"+email+"/"+activation_code+"/"
    html_content = html_content.replace('{{ CONFIRMATION_URL }}',url_confirmation)
    return send_email(to_address=email, title="Sistema Digitar - Confirmação de email", message=html_content)


def resend_generate_activation_code(email,activation_code):
    html_content = SystemVariables.messages_email.resend_activation_code_email
    url_confirmation = "http://"+SERVER_ADDRESS+"/register/activate/"+email+"/"+activation_code+"/"
    html_content = html_content.replace('{{ CONFIRMATION_URL }}',url_confirmation)
    return send_email(to_address=email, title="Sistema Digitar - Confirmação de email", message=html_content)


def send_reset_password(senha, email, username):
    html_content = SystemVariables.messages_email.reset_password_email
    html_content = html_content.replace('{{ NEW_PASSWORD }}', senha)
    html_content = html_content.replace('{{ LOGIN }}', username)
    return send_email(to_address=email, title="Sistema Digitar - Recuperar Acesso", message=html_content)
