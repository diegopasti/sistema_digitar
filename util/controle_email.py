#import mimetypes
import os
import mimetypes
import smtplib
from email import encoders
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

class Email(MIMEMultipart,object):

    dispatcher = None
    receivers  = None
    message    = None

    def __init__(self,dispatcher):
        super(Email,self).__init__()
        self.dispatcher = dispatcher
        self.receivers = []

    def set_message(self, msg):
        self.message = msg
        self.attach(MIMEText(msg, 'html', 'utf-8'))

    def get_message(self):
        return self.message

    def attach_file(self,filename):
        if not os.path.isfile(filename):
            return

        ctype, encoding = mimetypes.guess_type(filename)

        if ctype is None or encoding is not None:
            ctype = 'application/octet-stream'

        maintype, subtype = ctype.split('/', 1)

        if maintype == 'text':
            with open(filename) as f:
                mime = MIMEText(f.read(), _subtype=subtype)
        elif maintype == 'image':
            with open(filename, 'rb') as f:
                mime = MIMEImage(f.read(), _subtype=subtype)
        elif maintype == 'audio':
            with open(filename, 'rb') as f:
                mime = MIMEAudio(f.read(), _subtype=subtype)
        else:
            with open(filename, 'rb') as f:
                mime = MIMEBase(maintype, subtype)
                mime.set_payload(f.read())

            encoders.encode_base64(mime)

        mime.add_header('Content-Disposition', 'attachment', filename=filename)
        self.attach(mime)

    def add_receiver(self,receiver):
        self.receivers.append(receiver)

    def get_receivers(self):
        #self['To'] = self.receivers
        self['To'] = ', '.join(self.receivers)
        #print self["To"],type(self["To"])
        return self['To']

    def set_sender(self,sender):
        self["From"] = sender

    def get_sender(self):
        return self["From"]

    def set_subject(self,subject):
        self["Subject"] = subject

    def get_subject(self):
        return self["Subject"]

    def send(self):
        self.dispatcher.send_email(self)



class EmailController():

    service  = None
    account  = None
    password = None
    username = None
    smtp     = None

    def __init__(self,service,account,password,username):
        self.account = account
        self.password = password
        self.username     = username
        self.setup_service(service)

    def setup_service(self,service):
        self.service = service
        if self.service == "GMAIL":
            self.smtp = smtplib.SMTP_SSL('smtp.gmail.com', 465)

        elif self.service == "HOTMAIL":
            self.smtp = smtplib.SMTP_SSL('smtp.live.com', 465)

        elif self.service == "MAIL":
            self.smtp = smtplib.SMTP_SSL('smtp.mail.com', 465)

        elif self.service == "YAHOO":
            self.smtp = smtplib.SMTP_SSL('smtp.mail.yahoo.com 	', 465)

        else:
            self.smtp = smtplib.SMTP_SSL('smtp.gmail.com', 465)

    def new_email(self):
        email = Email(self)
        email.set_sender(self.username)
        return email

    def send_email(self,email):
        raw = email.as_string()
        self.smtp.login(self.account, self.password)
        self.smtp.sendmail(email.get_sender(), email["To"], raw)

    def close(self):
        self.smtp.quit()

if __name__=="__main__":
    service = "GMAIL"
    account = "diegopasti@gmail.com"
    password = "61109119di"
    username = "Diego Pasti"

    email_controller = EmailController(service, account, password, username)
    email = email_controller.new_email()

    """
        Por enquanto eh necessario definir a lista de destinatarios
        atribuindo diretamente ao parametro "To" do email. Por algum
        motivo utilizar o helper "add_receiver" faz com que o destinatario
        seja informado como com copia oculto (CCO).

    """
    email["To"] = 'diegopasti@gmail.com ,helder@pcns.com.br'
    # email.add_receiver("diegopasti@gmail.com")
    # email.add_receiver("helder@pcns.com.br")

    email.set_subject("Teste com novo controle de emails")
    email.set_message("Novo mecanismo de envio de mensagens")
    email.send()
    email_controller.close()
    print "Email de teste enviado com sucesso"




"""
def adicionar_anexo(msg, filename):
    if not os.path.isfile(filename):
        return

    ctype, encoding = mimetypes.guess_type(filename)

    if ctype is None or encoding is not None:
        ctype = 'application/octet-stream'

    maintype, subtype = ctype.split('/', 1)

    if maintype == 'text':
        with open(filename) as f:
            mime = MIMEText(f.read(), _subtype=subtype)
    elif maintype == 'image':
        with open(filename, 'rb') as f:
            mime = MIMEImage(f.read(), _subtype=subtype)
    elif maintype == 'audio':
        with open(filename, 'rb') as f:
            mime = MIMEAudio(f.read(), _subtype=subtype)
    else:
        with open(filename, 'rb') as f:
            mime = MIMEBase(maintype, subtype)
            mime.set_payload(f.read())

        encoders.encode_base64(mime)

    mime.add_header('Content-Disposition', 'attachment', filename=filename)
    msg.attach(mime)
"""

"""
de = 'seumail@gmail.com'
para = ['outroemail@gmail.com']

msg = MIMEMultipart()
msg['From'] = de
msg['To'] = ', '.join(para)
msg['Subject'] = 'Buteco Open Source'

# Corpo da mensagem
msg.attach(MIMEText('Exemplo de email HTML com anexo do &lt;b&gt;Buteco Open Source&lt;b/&gt;.', 'html', 'utf-8'))

# Arquivos anexos.
adicionar_anexo(msg, 'texto.txt')
adicionar_anexo(msg, 'imagem.jpg')

raw = msg.as_string()

smtp = smtplib.SMTP_SSL('smtp.gmail.com', 465)
smtp.login('seumail@gmail.com', 'suasenha')
smtp.sendmail(de, para, raw)
smtp.quit()
"""