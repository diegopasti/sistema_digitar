# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

import decimal
from django.contrib.auth.models import User
from modules.entidade.models import entidade
from modules.entidade.formularios import MENSAGENS_ERROS
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.signals import pre_save
from modules.servico.models import Plano
from django.db import models
from decimal import Decimal
import datetime


class Contrato(models.Model):
    plano = models.ForeignKey(Plano, default=1)

    cliente = models.ForeignKey(entidade, default=1)
    opcoes_tipos_clientes = (('PF', 'PESSOA FISICA'), ('PJ', 'PESSOA JURIDICA'),)
    tipo_cliente  = models.CharField("Tipo do Cliente:",max_length=2,null=False,default='PJ',choices = opcoes_tipos_clientes,error_messages=MENSAGENS_ERROS)

    vigencia_inicio = models.DateField(null=True)
    vigencia_fim    = models.DateField(null=True,blank=True)

    taxa_honorario  = models.DecimalField("Honorário:", max_digits=11, decimal_places=2, null=True,blank=True)
    valor_honorario = models.DecimalField("Valor:", max_digits=11, decimal_places=2, null=True,blank=False)
    valor_total = models.DecimalField("Total:", max_digits=11, decimal_places=2, null=True, blank=False)
    dia_vencimento  = models.CharField("Dia do Vencimento",null=True,blank=True,default=5,max_length=2)
    data_vencimento = models.DateField("Data de Vencimento",null=True,blank=True)

    desconto_temporario = models.DecimalField("Desconto Temporário:", max_digits=11,default=0, decimal_places=2, null=True,blank=True,validators=[MaxValueValidator(100),MinValueValidator(0)])
    desconto_temporario_ativo  = models.DecimalField("Desconto Temporário Ativo:", max_digits=11,default=0, decimal_places=2, null=True,blank=True,validators=[MaxValueValidator(100),MinValueValidator(0)])
    desconto_inicio = models.DateField(null=True,blank=True)
    desconto_fim    = models.DateField(null=True,blank=True)

    reembolso_arquivo_caixa = models.BooleanField(default=False)
    arquivos_caixa = models.IntegerField(default=0)

    desconto_indicacoes = models.DecimalField("Desconto por Indicações:", max_digits=7, decimal_places=2, default=0, null=True,blank=True)
    servicos_contratados = models.CharField("Serviços:",null=True,blank=True,max_length=100)
    cadastrado_por = models.ForeignKey(User,  related_name = "cadastrado_por",default=1)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    ultima_alteracao = models.DateTimeField(null=True, auto_now=True)
    alterado_por = models.ForeignKey(User, related_name = "alterado_por",default=1)
    ativo = models.BooleanField(default=True)

    #def save(self, *args, **kwargs):
    #    self.servicos_contratados = self.plano.servicos
    #    self.totalizar_honorario()
    #    super().save(self)
    #    #    print("SALVEI O CONTRATO!")
    #    #    models.Model.save(self, *args, **kwargs)
    #    #    #super(Contrato).save(self, *args, **kwargs)

    def serialize(self):
        serialized_values = {}

    def valor_honorario_float(self):
        return float(self.valor_honorario)

    def desconto_total_ativo(self):
        return float(self.desconto_temporario_ativo + self.desconto_indicacoes)

    def valor_total_float(self):
        return float(self.valor_total)

    def totalizar_honorario(self):
        desconto_temporario = self.calcular_desconto_temporario()
        desconto_fidelidade = self.calcular_desconto_fidelidade()
        self.desconto_temporario_ativo = desconto_temporario
        self.desconto_indicacoes = desconto_fidelidade
        desconto_total = Decimal(desconto_temporario)/100 + Decimal(desconto_fidelidade)/100
        self.valor_total = Decimal(self.valor_honorario)*(1-desconto_total)
        #self.save()

    def calcular_desconto_temporario(self, competencia=None):
        if self.desconto_temporario is not None:
            if self.verificar_validade_desconto_temporario(competencia,self.desconto_inicio,self.desconto_fim):
                desconto = self.desconto_temporario
                return Decimal(desconto)
        return Decimal(0)

    def verificar_validade_desconto_temporario(self,competencia=None, inicio=None,termino=None):
        if competencia is not None:
            month_dict_name = {'JAN':'01', 'FEV':'02', 'MAR':'03', 'ABR':'04', 'MAI':'05', 'JUN':'06', 'JUL':'07', 'AGO':'08', 'SET':'09', 'OUT':'10', 'NOV':'11', 'DEZ':'12'}
            competencia_parts = competencia.split('/')
            month_name = competencia_parts[0]
            year = competencia_parts[1]
            month = month_dict_name[month_name]
            day = '01'
            current_date = datetime.datetime.strptime(year+"-"+month+'-'+day, '%Y-%m-%d').date()
        else:
            current_date = datetime.datetime.now().date()

        if inicio is not None:
            if current_date < inicio:
                return False

        if termino is not None:
            if current_date > termino:
                return False
        return True

    def calcular_desconto_fidelidade(self):
        indicacoes = Indicacao.objects.filter(cliente=self.cliente).filter(indicacao_ativa=True)
        if len(indicacoes) == 0:
            return Decimal(0)
        else:
            desconto = Decimal(0)
            for item in indicacoes:
                if item.indicacao.ativo:
                    if(desconto + item.taxa_desconto > 30):
                        desconto = 30.0
                        break
                    else:
                        desconto = desconto + item.taxa_desconto
            return desconto

#def pre_save_contract(sender, instance, **kwargs):
#    instance.servicos_contratados = instance.plano.servicos
#    instance.totalizar_honorario()
#    #instance.save()
#    print("SALVEI O CONTRATO CALCULADO")
#pre_save.connect(pre_save_contract, sender=Contrato)

class Indicacao (models.Model):
    cliente = models.ForeignKey(entidade, related_name = "cliente")
    indicacao = models.ForeignKey(entidade,related_name = "indicacao")
    taxa_desconto = models.DecimalField("Taxa Desconto",max_digits=5, decimal_places=2, default=0)
    indicacao_ativa = models.BooleanField(default=True)
    cadastrado_por = models.ForeignKey(User, related_name="indicacao_cadastrado_por", default=1)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    ultima_alteracao = models.DateTimeField(null=True, auto_now=True)
    alterado_por = models.ForeignKey(User, related_name="indicacao_alterado_por", default=1)


class Proventos(models.Model):
    class Meta:
        db_table = 'honorary_provents'
        verbose_name = "Provento e Desconto"
        verbose_name_plural = "Proventos e Descontos"
    opcoes_tipos_provento = (('P', 'PROVENTO'), ('D', 'DESCONTO'), ('R', 'RESSARCIMENTO'))
    tipo = models.CharField("Tipo do Provento:", max_length=1, null=False, default='P', choices=opcoes_tipos_provento, error_messages=MENSAGENS_ERROS)
    nome = models.CharField("Nome:", max_length=100, null=False, error_messages=MENSAGENS_ERROS)
    descricao = models.CharField("Descrição:", max_length=500, null=True,blank=True, error_messages=MENSAGENS_ERROS)

    opcoes_tipos_valor = (('R', 'REAIS'), ('P', 'PERCENTUAL'))
    tipo_valor = models.CharField("Tipo do Valor:", max_length=1, null=False, default='R', choices=opcoes_tipos_valor, error_messages=MENSAGENS_ERROS)
    valor = models.CharField("Valor:", max_length=10, null=True, blank=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    cadastrado_por = models.ForeignKey(User, related_name='provento_cadastrado_por',  default=1)
    ultima_alteracao = models.DateTimeField(null=True, auto_now=True)
    alterado_por = models.ForeignKey(User, related_name='provento_alterado_por', default=1)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.nome+"     (R$"+str(self.valor)+")"


class Honorary(models.Model):
    class Meta:
        db_table = 'honorary'
        verbose_name = "Honorário"
        verbose_name_plural = "Honorários"
        unique_together = ("entity", "competence")

    entity = models.ForeignKey(entidade, default=1)
    entity_name = models.CharField("Cliente:", null=False, max_length=100)
    competence = models.CharField("Mês de Competencia:",null=False,max_length=8)

    competence_init_date = models.DateTimeField("Competencia inicia em", null=True)
    contract = models.ForeignKey(Contrato, null=True, related_name='contrato')
    initial_value_contract = models.DecimalField("Valor base do contrato", max_digits=11, default=0, decimal_places=2, null=True, blank=True)
    temporary_discount = models.DecimalField("Desconto temporário", max_digits=11,default=0, decimal_places=2, null=False,blank=True)
    fidelity_discount = models.DecimalField("Desconto fidelidade", max_digits=11, decimal_places=2, default=0, null=False,blank=True)
    contract_discount = models.DecimalField("Desconto total em contrato", max_digits=11, decimal_places=2, default=0, null=True,blank=True)
    final_value_contract = models.DecimalField("Valor final do contrato", max_digits=11, decimal_places=2, default=0, null=True, blank=True)
    number_debit_credit = models.IntegerField("Total de débitos e créditos", default=0)
    total_debit = models.DecimalField("Total à debitar", max_digits=11,decimal_places=2, default=0, null=True,blank=True)
    total_credit = models.DecimalField("Valor total à creditar", max_digits=11,decimal_places=2, default=0, null=True, blank=True)
    total_debit_credit = models.DecimalField("Valor total à creditar", max_digits=11, decimal_places=2, default=0, null=True, blank=True)
    total_repayment = models.DecimalField("Total à reembolsar", max_digits=11, decimal_places=2, default=0, null=True, blank=True)
    total_honorary = models.DecimalField("Honorário", max_digits=11, decimal_places=2, default=0, null=True, blank=True)

    created_date = models.DateTimeField(auto_now_add=True)

    opcoes_tipos_provento = (('A', 'EM ABERTO'), ('C', 'CONFERIDO'), ('E', 'ENCERRADO'))
    status = models.CharField("Situação do Honorário:", max_length=1, null=False, default='A', choices=opcoes_tipos_provento, error_messages=MENSAGENS_ERROS)

    #status = models.BooleanField("Situação do Honorário", default=False)
    conferred_date = models.DateTimeField("Honorário conferido em", null=True)
    conferred_by = models.ForeignKey(User, related_name="conferido_por", null=True)

    closed_date = models.DateTimeField("Honorário encerrado em", null=True)
    closed_by = models.ForeignKey(User, related_name="finalizado_por", null=True)
    last_update = models.DateTimeField("Ultima atualização", auto_now=True)
    updated_by = models.ForeignKey(User, related_name="atualizado_por", null=True)
    updated_by_name = models.CharField("Atualizado por:", null=True, max_length=100)
    is_received = models.BooleanField("Honorário recebido", default=False)
    received_by = models.ForeignKey(User, related_name="recebido_por", null=True)

    def initial_value_contract_float(self):
        return float(self.initial_value_contract)

    def total_contract_discount_float(self):
        return float((self.contract_discount/100)*self.initial_value_contract)

    def total_honorary_float(self):
        return float(self.total_honorary)

    def total_repayment_float(self):
        return float(self.total_repayment)

    def total_debit_float(self):
        return float(self.total_debit)

    def total_credit_float(self):
        return float(self.total_credit)

    def have_contract(self):
        if self.contract is not None:
            return True
        else:
            return False

    def create_honorary(self, entity, competence, contract=None):
        honorary = Honorary()
        honorary.entity = entity
        month_numbers = {'JAN':'01', 'FEV':'02','MAR':'03','ABR':'04','MAI':'05','JUN':'06','JUL':'07','AGO':'08','SET':'09','OUT':'10','NOV':'11','DEZ':'12'}
        competence_parts = competence.split('/')
        year = competence_parts[1]
        month = month_numbers[competence_parts[0]]

        honorary.competence_init_date = datetime.datetime.strptime("01/"+month+"/"+year+" 00:00:00", "%d/%m/%Y %H:%M:%S")
        honorary.entity_name = entity.nome_razao
        honorary.competence = competence
        if contract is not None:
            honorary = self.verify_contract_values(honorary, contract)
            honorary.verify_provents_values()
        return honorary

    def update_honorary(self, honorary, contract=None):
        if honorary.status != "E":
            if contract is not None:
                honorary = self.verify_contract_values(honorary, contract)
            honorary.verify_provents_values()
        return honorary

    def verify_provents_values(self):
        provent_list = HonoraryItem.objects.filter(honorary=self)
        self.number_debit_credit = 0
        self.total_debit_credit = 0
        self.total_repayment = 0
        self.total_debit = 0
        self.total_credit = 0

        if self.contract is None:
            self.total_honorary = 0
        else:
            self.total_honorary = self.final_value_contract
        for item in provent_list:
            self.number_debit_credit = self.number_debit_credit + 1
            new_value = Decimal(item.total_value)
            if item.type_item == 'P' or item.type_item == 'R':
                if item.type_item == 'P':
                    self.total_debit = self.total_debit + new_value
                else:
                    self.total_repayment = self.total_repayment + new_value
                self.total_debit_credit = self.total_debit_credit + new_value
                self.total_honorary = self.total_honorary + new_value

            else:
                self.total_credit = self.total_credit + new_value
                self.total_debit_credit = self.total_debit_credit - new_value
                self.total_honorary = self.total_honorary - new_value

    def verify_contract_values(self, honorary, contract):
        honorary.contract = contract
        if honorary.contract is not None and honorary.contract.ativo:
            generate_honorary = True
            if honorary.contract.dia_vencimento is None or honorary.contract.dia_vencimento == "":
                if honorary.contract.data_vencimento is not None and honorary.contract.data_vencimento != "":
                    honorary_competence = honorary.competence_init_date.strftime('%m/%Y')
                    contract_competence = honorary.contract.data_vencimento.strftime('%m/%Y')
                    if honorary_competence == contract_competence:
                        generate_honorary = True
                        #print("VOU GERAR ESSE HONORARIO ANUAL:",honorary_competence," - ",contract_competence)
                    else:
                        #print("CONTRATO COM VENCIMENTO ANUAL MAS NAO TA NO MES AINDA:", honorary_competence, " - ", contract_competence)
                        generate_honorary = False
                else:
                    pass
                    #print("EH MENSAL MESMO")
            else:
                #print("TEM DIA DE VENCIMENTO??")
                generate_honorary = True

            if generate_honorary:
                honorary.initial_value_contract = contract.valor_honorario
                honorary.temporary_discount = contract.calcular_desconto_temporario(honorary.competence)
                honorary.fidelity_discount = contract.calcular_desconto_fidelidade()
                honorary.contract_discount = honorary.temporary_discount + decimal.Decimal(honorary.fidelity_discount)
                honorary.final_value_contract = Decimal(honorary.initial_value_contract)*(1 - (honorary.contract_discount / 100))
                honorary.total_honorary = honorary.final_value_contract
                honorary.save()

                self.verify_discount_simples_nacional(honorary)
                self.verify_reembolso_arquivo_caixa(honorary)
                self.verify_provents(honorary)

                """
                if honorary.contract.reembolso_arquivo_caixa:
                    verificar_reembolso_ja_lançado = HonoraryItem.objects.filter(honorary=honorary,item_id=7)
                    if verificar_reembolso_ja_lançado.count() == 0:
                        honorary_item = HonoraryItem()
                        honorary_item.type_item = 'P'  #models.CharField("Tipo do Provento:", max_length=1, null=False, default='P', choices=opcoes_tipos_item, error_messages=MENSAGENS_ERROS)
                        honorary_item.type_value = 'R' #models.CharField("Tipo do Valor:", max_length=1, null=False, default='R', choices=opcoes_tipos_valores, error_messages=MENSAGENS_ERROS)
                        honorary_item.honorary = honorary
                        provento = Proventos.objects.get(pk=7)
                        honorary_item.item = provento
                        honorary_item.quantity = int(honorary.contract.arquivos_caixa)
                        honorary_item.unit_value = provento.valor
                        honorary_item.total_value = str(int(honorary.contract.arquivos_caixa)*Decimal(provento.valor))
                        honorary_item.created_by_id = 1
                        honorary_item.updated_by_id = 1
                        honorary_item.save()
                """
            else:
                #print("VOU RESETAR ESSE HONORARIO POIS NAO TA NO VENCIMENTO (ANUAL) OU NAO TEM DIA DE COBRANCA.")
                honorary.initial_value_contract = 0
                honorary.temporary_discount = 0
                honorary.fidelity_discount = 0
                honorary.contract_discount = 0
                honorary.final_value_contract = Decimal(0)
                honorary.total_honorary = Decimal(0)
                honorary.save()

                self.verify_discount_simples_nacional(honorary)
                self.verify_reembolso_arquivo_caixa(honorary)

        else:
            honorary.initial_value_contract = 0
            honorary.temporary_discount = 0
            honorary.fidelity_discount = 0
            honorary.contract_discount = 0
            honorary.final_value_contract = Decimal(0)
            honorary.total_honorary = Decimal(0)
        return honorary


    def verify_provents(self, honorary):
        honorary_itens = HonoraryItem.objects.filter(honorary=honorary)
        for item in honorary_itens:
            if item.type_value == "P":
                #print("AJUSTAR O ITEM:",item.item.nome,' PRECISA SER ATUALIZADO')
                provento = item.item
                item.item = provento
                item.quantity = Decimal(provento.valor)
                item.unit_value = honorary.initial_value_contract
                item.total_value = round((item.quantity / 100) * Decimal(item.unit_value), 2)
                item.created_by_id = 1
                item.updated_by_id = 1
                item.save()

    def verify_discount_simples_nacional(self, honorary):
        if honorary.entity.regime_apuracao == "SIMPLES_NACIONAL":
            verificar_desconto_ja_lançado = HonoraryItem.objects.filter(honorary=honorary, item_id=4)
            if verificar_desconto_ja_lançado.count() == 0:
                honorary_item = HonoraryItem()
                honorary_item.type_item = 'D'
                honorary_item.type_value = 'P'
                honorary_item.honorary = honorary
                provento = Proventos.objects.get(pk=4)
                honorary_item.item = provento
                honorary_item.quantity = Decimal(provento.valor)
                honorary_item.unit_value = honorary.initial_value_contract
                honorary_item.total_value = round((honorary_item.quantity / 100) * Decimal(honorary_item.unit_value), 2)
                honorary_item.created_by_id = 1
                honorary_item.updated_by_id = 1
                honorary_item.save()

            else:
                #print("JA TEM SIMPLES NACIONAL LANCADO.. VOU TER QUE ATUALIZAR:", verificar_desconto_ja_lançado)
                honorary_item = verificar_desconto_ja_lançado[0]
                honorary_item.type_item = 'D'
                honorary_item.type_value = 'P'
                honorary_item.honorary = honorary
                provento = Proventos.objects.get(pk=4)
                honorary_item.item = provento
                honorary_item.quantity = Decimal(provento.valor)
                honorary_item.unit_value = honorary.initial_value_contract
                honorary_item.total_value = round((honorary_item.quantity / 100) * Decimal(honorary_item.unit_value), 2)
                honorary_item.created_by_id = 1
                honorary_item.updated_by_id = 1
                honorary_item.save()

    def verify_reembolso_arquivo_caixa(self, honorary):
        if honorary.contract.reembolso_arquivo_caixa:
            verificar_reembolso_ja_lançado = HonoraryItem.objects.filter(honorary=honorary, item_id=7)
            if verificar_reembolso_ja_lançado.count() == 0:
                honorary_item = HonoraryItem()
                honorary_item.type_item = 'P'  # models.CharField("Tipo do Provento:", max_length=1, null=False, default='P', choices=opcoes_tipos_item, error_messages=MENSAGENS_ERROS)
                honorary_item.type_value = 'R'  # models.CharField("Tipo do Valor:", max_length=1, null=False, default='R', choices=opcoes_tipos_valores, error_messages=MENSAGENS_ERROS)
                honorary_item.honorary = honorary
                provento = Proventos.objects.get(pk=7)
                honorary_item.item = provento
                honorary_item.quantity = int(honorary.contract.arquivos_caixa)
                honorary_item.unit_value = provento.valor
                honorary_item.total_value = str(int(honorary.contract.arquivos_caixa) * Decimal(provento.valor))
                honorary_item.created_by_id = 1
                honorary_item.updated_by_id = 1
                honorary_item.save()

    """
    def set_contract_paramters(self, honorary, contract):
        honorary.contract = contract
        honorary.initial_value_contract = contract.valor_honorario
        honorary.temporary_discount = contract.calcular_desconto_temporario(honorary.competence)
        honorary.fidelity_discount = contract.calcular_desconto_fidelidade()
        honorary.contract_discount = honorary.temporary_discount + honorary.fidelity_discount
        honorary.final_value_contract = honorary.initial_value_contract * (1 - (honorary.contract_discount / 100))
        honorary.number_debit_credit = 0
        honorary.total_debit = 0
        honorary.total_credit = 0
        honorary.total_debit_credit = 0
        honorary.total_repayment = 0
        honorary.total_honorary = honorary.final_value_contract
        return honorary


    def update_honorary(self, entity, competence):
        honorary = Honorary.objects.filter(entity=entity, competence=competence)
        if honorary.count() != 0:
            honorary.contract = contract
            honorary.initial_value_contract = contract.valor_honorario
            honorary.temporary_discount = contract.calcular_desconto_temporario(competence)
            honorary.fidelity_discount = contract.calcular_desconto_fidelidade()
            honorary.contract_discount = honorary.temporary_discount + honorary.fidelity_discount
            honorary.final_value_contract = honorary.initial_value_contract * (1 - (honorary.contract_discount / 100))
            honorary.number_debit_credit = 0
            honorary.total_debit = 0
            honorary.total_credit = 0
            honorary.total_debit_credit = 0
            honorary.total_repayment = 0
            honorary.total_honorary = honorary.final_value_contract



    def create_honorary_without_contract(self, entity, competence):
        honorary = Honorary()
        honorary.entity = entity
        honorary.entity_name = entity.nome_razao
        honorary.competence = competence
        honorary.contract = None
        honorary.initial_value_contract = 0
        honorary.temporary_discount = 0
        honorary.fidelity_discount = 0
        honorary.contract_discount = 0
        honorary.final_value_contract = 0
        honorary.number_debit_credit = 0
        honorary.total_debit = 0
        honorary.total_credit = 0
        honorary.total_debit_credit = 0
        honorary.total_repayment = 0
        honorary.total_honorary = 0
        return honorary


    def create_honorary_with_contract(self, entity, competence, contract, honorary=None):
        if honorary is None:
            honorary = Honorary()
        if honorary.is_closed:
            return honorary
        honorary.entity = entity
        honorary.entity_name = entity.nome_razao
        honorary.competence = competence
        honorary.contract = contract
        honorary.initial_value_contract = contract.valor_honorario
        honorary.temporary_discount = contract.calcular_desconto_temporario(competence)
        honorary.fidelity_discount = contract.calcular_desconto_fidelidade()
        honorary.contract_discount = honorary.temporary_discount+honorary.fidelity_discount
        honorary.final_value_contract = honorary.initial_value_contract*(1-(honorary.contract_discount/100))
        honorary.number_debit_credit = 0
        honorary.total_debit = 0
        honorary.total_credit = 0
        honorary.total_debit_credit = 0
        honorary.total_repayment = 0
        honorary.total_honorary = honorary.final_value_contract
        return honorary
    """


class HonoraryItem(models.Model):
    class Meta:
        db_table = 'honorary_item'
        verbose_name = "Item do Honorário"
        verbose_name_plural = "Items do Honorário"

    opcoes_tipos_item = (('P', 'PROVENTO'), ('D', 'DESCONTO'), ('R', 'RESSARCIMENTO'))
    opcoes_tipos_valores = (('P', 'PERCENTUAL'), ('R', 'REAIS'))
    type_item = models.CharField("Tipo do Provento:", max_length=1, null=False, default='P', choices=opcoes_tipos_item, error_messages=MENSAGENS_ERROS)
    type_value = models.CharField("Tipo do Valor:", max_length=1, null=False, default='R', choices=opcoes_tipos_valores, error_messages=MENSAGENS_ERROS)
    honorary = models.ForeignKey(Honorary, default=1)
    item = models.ForeignKey(Proventos, default=1)
    complement = models.TextField("Complemento:", max_length=100, null=True, blank=True, error_messages=MENSAGENS_ERROS)
    quantity = models.DecimalField("Quantidade",null=True,blank=True, max_digits=11, decimal_places=2)
    unit_value = models.CharField("Valor unitário:", max_length=10, null=True, blank=True, default=1)
    total_value = models.CharField("Valor total:", max_length=10, null=False, blank=False)

    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, null=True, related_name="created_by")

    last_update = models.DateTimeField("Ultima atualização:", auto_now=True)
    updated_by = models.ForeignKey(User, null=True, related_name="updated_by")