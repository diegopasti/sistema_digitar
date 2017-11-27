# -*- encoding: utf-8 -*-
from modules.entidade.models import contato, localizacao_simples, entidade
from modules.protocolo.models import documento


def precarregar_dados_digitar():
	registro = entidade()
	registro.cpf_cnpj = "08265538000130"
	registro.nome_razao = "DIGITAR ASSESSORIA CONTABIL LTDA ME"
	registro.apelido_fantasia = "DIGITAR"
	registro.tipo_registro = "E"
	registro.endereco_id = 1

	localizacao = localizacao_simples()
	localizacao.cep = "29056220"
	localizacao.logradouro = "RUA CAPITÃO DOMINGOS CORRÊA DA ROCHA"
	localizacao.numero = "60"
	localizacao.complemento = "SALAS 213/214"
	localizacao.bairro = "SANTA LUCIA"
	localizacao.codigo_ibge = "2900000"
	localizacao.municipio = "VITÓRIA"
	localizacao.estado = "ES"
	localizacao.pais = "BRASIL"
	localizacao.save()

	registro_contato = contato()
	registro_contato.tipo_contato = "COMERCIAL"
	registro_contato.numero = "(27) 3022-1223"
	registro_contato.nome_contato = "MARCELO BORGNIGON"
	registro_contato.cargo_setor = "marcelo@digitar-es.com.br"

	registro.endereco = localizacao
	registro.save()

	registro_contato.entidade = registro
	registro_contato.save()

def precarregar_referencias_documentos():
    for item in protocolo.referencias_documentos:
        novo_documento = documento()
        novo_documento.nome = item
        novo_documento.save()

class protocolo:
    referencias_documentos = [
                    'RECIBO DE PAGAMENTO DE SALÁRIO MENSAL',
                    'RECIBO DE PAGAMENTO DE SALÁRIO MENSAL (EMPREGADA DOMÉSTICA)',
                    'RECIBO DE PAGAMENTO AUTÔNOMO - RPA',
                    'RECIBO DE PAGAMENTO DE PRÓ-LABORE',
                    'RECIBO PAGAMENTO 13º SALÁRIO',
                    'FGTS',
                    'DASN',
                    'DARF 1708',
                    'DARF 5952',
                    'DARF 0210',
                    'DARF 0588',
                    'DARF 3551',
                    'DARF 8301 - PIS SOBRE FOLHA',
                    'DARF 2089 IRPJ',
                    'DARF 2372 CSLL',
                    'DARF 8109 PIS',
                    'DARF 2172 COFINS',
                    'DARF 4737',
                    'DARF 0561',
                    'DARF 4750',
                    'DARF 0211 - CARNÊ LEÃO',
                    'DARF 0190',
                    'DARF 1070 - ITR',
                    'GPS 2208 - EMPRESAS EM GERAL - CEI',
                    'GPS 2100 - EMPRESA EM GERAL - CNPJ',
                    'GPS 1600 - EMPREGADA DOMÉSTICA',
                    'GPS 1007 - AUTONÔMO INDIVIDUAL',
                    'GPS 2216 - EMPRESAS EM GERAL - CEI (OUTRAS ENTIDADES)',
                    'GPS 2003',
                    'CARTÃO VALE TRANSPORTE',
                    'VALE TRANSPORTE',
                    'HONORÁRIOS CONTÁBEIS',
                    'ISS SOBRE FATURAMENTO',
                    'CONTRIBUIÇÃO SINDICAL EMPREGADO',
                    'CONTRIBUIÇÃO SINDICAL PATRONAL - GRCSU',
                    'CONTRIBUIÇÃO ASSISTENCIAL',
                    'CARTEIRA DE TRABALHO',
                    'AVISO E RECIBO DE FÉRIAS',
                    'REQUERIMENTO ELETRONICO',
                    'MOVIMENTAÇÃO DE FÉRIAS',
                    'REQUERIMENTO SEGURO DESEMPREGO',
                    'CHAVE IDENTIFICAÇÃO TRABALHADOR',
                    'PERFIL PROFISSIOGRÁFICO PREVIDENCIÁRIO',
                    'TAXA ALVARÁ CORPO DE BOMBEIROS',
                    'TAXA ALVARÁ SANITÁRIO',
                    'TAXA PRÉVIA ALVARÁ LOCALIZAÇÃO E FUNCIONAMENTO',
                    'TAXA LICENÇA AMBIENTAL',
                    'ALVARÁ CORPO DE BOMBEIROS',
                    'LICENÇA AMBIENTAL',
                    'ALVARÁ SANITÁRIO',
                    'ALTERAÇÃO CONTRATUAL ORIGINAL',
                    'LIVRO DIÁRIO',
                    'BALANCETE',
                    'DOCUMENTO BÁSICO DE ENTRADA',
                    'CERTIFICADO DIGITAL',
                    'TAXA LIVRO DIÁRIO',
                    'CADERNO PROTOCOLO',
                    'DECLARAÇÃO DE FATURAMENTO',
                    'COMPROVANTE DE RENDIMENTOS',
                    'CRM E CRT ORIGINAIS',
                    'CIRCULAR',
                    'ISS FIXO COTA ÚNICA',
                    'ISS FIXO COTA 1',
                    'ISS FIXO COTA 2',
                    'ISS FIXO COTA 3',
                    'ISS FIXO COTA 4',
                    'DECLARAÇÃO DE BENEFICIÁRIO DE VALE TRANSPORTE',
                    'CONTRATO DE TRABALHO',
                    'DECLARAÇÃO CONTADOR DE CONTRIBIÇÃO INSS AUTONOMA',
                    'DECLARAÇÃO DE RETENÇÃO DE INSS',
                    'LIVRO DE REGISTRO DE EMPREGADOS',
                    'BOLETO TICKET SERVIÇOS',
                    'PROCURAÇÃO CARTÓRIO',
                    'PROCURAÇÃO ELETRONICA',
                    'FOLHAS DE PONTO FUNCIONÁRIOS',
                    'DAS - SIMPLES NACIONAL',
                    'ETIQUETA DE DEMISSÃO PARA CARTEIRA DE TRABALHO',
                    'GUIA DAE',
                    'DEMONSTRATIVO DA APURAÇÃO DOS GANHOS DE CAPITAL',
                    'REQUERIMENTO SEGURO DESEMPREGO',
                    'TERMO DE TITULARIDADE - CERTIFICADO CORREIOS',
                    'ATESTADO DE SAÚDE OCUPACIONAL - DEMISSIONAL',
                    'BOLETO CONSELHO REGIONAL DE MEDICINA - CRM',
                    'CONCESSÃO EMPRESTIMO AO EMPREGADO',
                    'GUIA DE GRRF',
                    'LIVRO CAIXA',
                    'DECORE',
                    'PARCELAMENTO PREVIDENCIARIO',
                    'ISS - PARCELAMENTO',
                    'NOTIFICAÇÃO',
                    'CONTRATO DE LOCAÇÃO',
                    'CONTRATO DE PRESTAÇÃO DE SERVIÇOS CONTÁBEIS',
                    'EXTRATO FINS RESCISÓRIOS',
                    'CARTA PREPOSTO AUTORIZAÇÃO',
                    'AVISO DE DISPENSA NO CONTRATO DE EXPERIÊNCIA',
                    'CARTA DE REFERÊNCIA',
                    'GRCS - GUIA DE RECOLHIMENTO DA CONTRIBUIÇÃO SINDICAL',
                    'DECLARAÇÃO DE FATURAMENTO',
                    'ISS S/SERVIÇOS TOMADOS',
                    'GUIA DE RECOLHIMENTO MENSAL SINTRASADES',
                    'TAXA ANUAL PODER DE POLICIA COTA ÚNICA',
                    'TAXA PODER DE POLÍCIA PARCELA ÚNICA',
                    'TAXA PODER DE POLÍCIA 1ª PARCELA',
                    'TAXA PODER DE POLÍCIA 2ª PARCELA',
                    'TAXA PODER DE POLÍCIA 3ª PARCELA'
    ]
