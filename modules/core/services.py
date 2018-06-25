import datetime

from django.contrib.auth.models import User
from modules.entidade.models import Documento
from modules.honorary.models import Contrato
from modules.nucleo.models import Notification
from modules.protocolo.models import protocolo


class NotificationsControl:

    def __init__(self):
        self.notifications_list = [EntityNotifications(),ContractNotifications(),ProtocolNotifications()]

    def generate_notifications(self):
        for item in self.notifications_list:
            item.generate_notifications()


class ProtocolNotifications:

    def generate_notifications(self):
        self.create_open_protocols()

    def create_open_protocols(self):
        corrigir_operador_emissor_protocolo()
        protocols_list = protocolo.objects.filter(situacao=False)
        current_date = datetime.datetime.now().date()
        current_year = current_date.year
        current_month = current_date.month - 1
        month_name = {0: 'JAN', 1: 'FEV', 2: 'MAR', 3: 'ABR', 4: 'MAI', 5: 'JUN', 6: 'JUL', 7: 'AGO', 8: 'SET', 9: 'OUT', 10: 'NOV', 11: 'DEZ'}
        competence = month_name[current_month] + "/" + str(current_year)
        max_days_open_protocols = 7

        for item in protocols_list:
            opened_days = item.calcular_dias_atraso()
            if opened_days > max_days_open_protocols:
                notification = Notification()
                notification.module = "PROTOCOL"
                notification.group = "PROTOCOL"
                notification.tag = "OPEN_PROTOCOL"
                notification.type = "INFO"
                notification.related_model = 'modules.protocolo.models.protocolo'
                notification.related_object = item.id
                notification.competence = competence
                notification.related_users = "1;2"
                if item.emissor_id != 1:
                    notification.related_users = notification.related_users+";"+str(item.emissor_id)

                notification.related_entity = item.destinatario
                notification.get_related_user_names()
                notification.title = "PROTOCOLO EM ABERTO POR MAIS TEMPO QUE O PERMITIDO"
                if item.destinatario is not None:
                    notification.message = "Protocolo "+item.numeracao_destinatario+" do(a) cliente " + title_especial(item.destinatario.nome_razao) + " aberto há "+str(opened_days)+" dias."
                else:
                    notification.message = "Protocolo avulso do(a) cliente "+title_especial(item.nome_avulso)+" aberto há "+str(opened_days)+" dias."

                try:
                    notification.save()
                    #notification.show_details()
                except:
                    pass


def corrigir_operador_emissor_protocolo():
    protocols_list = protocolo.objects.all()
    for item in protocols_list:
        if item.emitido_por == "MARCELO":
            item.emitido_por = "MARCELO BOURGUIGNON"
            item.save()
        else:

            if item.emissor.first_name in item.emitido_por:
                #print("VEJA O NOME DO OPERADOR: ", item.emitido_por, "  - ID: ", item.emissor,' - OK')
                pass

            else:
                #print("VEJA O NOME DO OPERADOR: ", item.emitido_por, "  - ID: ", item.emissor, ' - CORRIGIR')
                #print("PROCURAR: ",item.emitido_por.split(' ')[0])
                edited_user = User.objects.get(first_name=item.emitido_por.split(' ')[0])
                item.emissor = edited_user
                item.save()
                #print("TROQUEI")


class ContractNotifications:

    def generate_notifications(self):
        contract_list = Contrato.objects.filter(ativo=True)
        current_date = datetime.datetime.now().date()
        current_year = current_date.year
        current_month = current_date.month - 1
        month_name = {0: 'JAN', 1: 'FEV', 2: 'MAR', 3: 'ABR', 4: 'MAI', 5: 'JUN', 6: 'JUL', 7: 'AGO', 8: 'SET', 9: 'OUT', 10: 'NOV', 11: 'DEZ'}
        competence = month_name[current_month] + "/" + str(current_year)

        contract_deadline_days = [60, 30, 15, 7, 3, 2, 1]
        discount_deadline_days = [30, 15, 7, 3, 2, 1]

        for contract in contract_list:
            if contract.vigencia_fim is not None:
                days_to_expiration, message = self.check_expiration_days(expiration_date=contract.vigencia_fim, current_date=current_date,deadline_days=contract_deadline_days, notify_days_exceeded=False)
                if days_to_expiration is not None:
                    self.create_closing_contract_notification(contract, competence, message)

            if contract.desconto_fim is not None:
                days_to_expiration, message = self.check_expiration_days(expiration_date=contract.desconto_fim, current_date=current_date,deadline_days=discount_deadline_days, notify_days_exceeded=False)
                if days_to_expiration is not None:
                    self.create_closing_discount_notification(contract, competence, message)

    def create_closing_contract_notification(self, contract, competence, message):
        notification = Notification()
        notification.module = "HONORARY"
        notification.group = "CONTRACT"
        notification.tag = "CONTRACT_CLOSING"
        notification.type = "INFO"
        notification.related_model = 'modules.honorary.models.Contrato'
        notification.related_object = contract.id
        notification.competence = competence
        notification.related_users = "1;2"
        notification.related_entity = contract.cliente
        notification.get_related_user_names()
        notification.title = "VIGÊNCIA DE CONTRATO ENCERRANDO"
        notification.message = "Contrato do(a) cliente " + title_especial(contract.cliente.nome_razao) + " " + message

        try:
            notification.save()
            notification.show_details()
        except:
            pass

    def create_closing_discount_notification(self, contract, competence, message):
        notification = Notification()
        notification.module = "HONORARY"
        notification.group = "CONTRACT"
        notification.tag = "DISCOUNT_CLOSING"
        notification.type = "INFO"
        notification.related_model = 'modules.honorary.models.Contrato'
        notification.related_object = contract.id
        notification.competence = competence
        notification.related_users = "1;2"
        notification.related_entity = contract.cliente
        notification.get_related_user_names()
        notification.title = "VIGÊNCIA DO DESCONTO TEMPORÁRIO DO CONTRATO ENCERRANDO"
        notification.message = "Desconto Temporário do contrato do(a) cliente " + title_especial(contract.cliente.nome_razao) + " " + message

        try:
            notification.save()
            notification.show_details()
        except:
            pass

    def check_expiration_days(self, expiration_date=None, current_date=None, deadline_days=None, notify_days_exceeded=True):
        days_to_expiration = expiration_date - current_date
        days_to_expiration = days_to_expiration.days
        message = "" #title_especial(document.nome) + " do(a) cliente "+title_especial(document.entidade.nome_razao)

        if (days_to_expiration <= deadline_days[0]):
            if days_to_expiration > 0:
                for item in deadline_days:
                    if days_to_expiration == item:
                        if item == 1:
                            message = message + " vence amanha."
                        else:
                            message = message + " vence em "+str(item)+" dias."

            elif days_to_expiration == 0:
                message = message + " vence hoje."

            else:
                if notify_days_exceeded:
                    if days_to_expiration == -1:
                        message = message + " venceu ontem."
                    else:
                        message = message + " vencido há " + str( -1 * days_to_expiration) + " dias."
                else:
                    message = None
                    days_to_expiration = None
        else:
            message = None
            days_to_expiration = None

        return days_to_expiration, message


class EntityNotifications:

    def generate_notifications(self):
        self.check_documents_expiring()

    def check_documents_expiring(self):
        documents_list = Documento.objects.filter(ativo=True)
        current_date   = datetime.datetime.now().date()
        current_year = current_date.year
        current_month = current_date.month-1
        month_name = {0:'JAN',1:'FEV',2:'MAR',3:'ABR',4:'MAI',5:'JUN',6:'JUL',7:'AGO',8:'SET',9:'OUT',10:'NOV',11:'DEZ'}
        competence = month_name[current_month]+"/"+str(current_year)
        for document in documents_list:
            days_to_expiration, message = self.check_expiration_days(document=document, current_date=current_date)
            if days_to_expiration is not None:
                notification = Notification()
                notification.module = "ENTITY"
                notification.group = "DOCUMENT"
                notification.tag = "DOCUMENTS_CLOSING"
                notification.type = "INFO"
                notification.title = "VENCIMENTO DE DOCUMENTO SE APROXIMA"
                notification.message = message
                notification.related_model = 'modules.entity.documento'
                notification.related_object = document.id
                notification.competence = competence
                notification.related_users = "1;2;"
                notification.related_entity = document.entidade
                client = document.entidade

                if client.responsavel_cliente is not None:
                    nivel = client.responsavel_cliente.groups.values_list('id',flat=True)[0]
                    if nivel > 2:
                        notification.related_users = notification.related_users + str(client.responsavel_cliente_id) + ";"

                if client.supervisor_cliente is not None:
                    nivel = client.supervisor_cliente.groups.values_list('id', flat=True)[0]
                    if nivel > 2:
                        notification.related_users = notification.related_users + str(client.supervisor_cliente_id) + ";"

                notification.related_users = notification.related_users[:-1]
                notification.get_related_user_names()
                try:
                    notification.save()
                    notification.show_details()
                    #print("")
                except:
                    pass

    def check_expiration_days(self, document=None, current_date=None):
        days_to_expiration = document.vencimento - current_date
        days_to_expiration = days_to_expiration.days
        message = title_especial(document.nome) + " do(a) cliente "+title_especial(document.entidade.nome_razao)

        if (days_to_expiration > 45):
            days_to_expiration = None
            message = None

        elif (days_to_expiration == 45):
            message = message+" vence em 45 dias."

        elif (days_to_expiration == 30):
            message = message + " vence em 30 dias."

        elif (days_to_expiration == 15):
            message = message + " vence em 15 dias."

        elif (days_to_expiration == 7):
            message = message + " vence em 7 dias."

        elif (days_to_expiration == 3):
            message = message + " vence em 3 dias."

        elif (days_to_expiration == 2):
            message = message + " vence em 2 dias."

        elif (days_to_expiration == 1):
            message = message + " vence amanha."

        elif (days_to_expiration == 0):
            message = message + " vence hoje."

        else:
            days_to_expiration = -1*days_to_expiration
            message = message + " vencido há "+str(days_to_expiration)+" dia(s)."
        return days_to_expiration, message

def title_especial(text):
    text = text.lower()
    text_parts = text.split(' ')
    new_text = ""
    for item in text_parts:
        if len(item) <=3:
            new_text = new_text + item+" "
        else:
            new_text = new_text + item.title() +" "
    new_text = new_text[:-1]
    return new_text

