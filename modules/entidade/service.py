# -*- encoding: utf-8 -*-
'''
Created on 12 de abr de 2016

@author: Win7
'''

import cgi
import json
import urllib
#import urllib2

import requests
from django.http.response import HttpResponse

from modules.entidade.models import Logradouro, endereco_serializer


def consultar_codigo_postal(cep):
    resultado = Logradouro.objects.filter(cep=cep)
    if resultado.count() != 0:
        logradouro = resultado[0]
        #print(logradouro.nome)
        
    else:
        print("Endereco nao Cadastro! Realizando consulta externa.")
        resultado = json.load(urllib.urlopen("http://127.0.0.1:8081/api/consultar_cep/"+cep+"/"))
        
        print(resultado)
        pais = consultar_pais(resultado['pais'])
        estado  = consultar_estado(resultado['estado'])
        municipio  = consultar_municipio(resultado['municipio'],resultado['codigo_municipio'],estado)
        bairro = consultar_bairro(resultado['bairro'],resultado['codigo_bairro'], municipio)
        
        logradouro = Logradouro()
        logradouro.nome = resultado['logradouro'].upper()
        logradouro.cep = cep
        logradouro.bairro = bairro
        logradouro.save()
                
    Endereco = formatar_resposta(logradouro)
    serializer = endereco_serializer(Endereco)
    return HttpResponse(serializer.data, content_type='application/json')

    #return JsonResponse(serializer.data)

    
def formatar_resposta(logradouro):
    from modules.entidade import Endereco
    Endereco = Endereco()
    Endereco.logradouro = logradouro.nome
    Endereco.bairro = logradouro.bairro.nome
    Endereco.codigo_bairro = logradouro.bairro.codigo_ibge
    Endereco.municipio = logradouro.bairro.municipio.nome
    Endereco.codigo_municipio = logradouro.bairro.municipio.codigo_ibge
    Endereco.estado = logradouro.bairro.municipio.estado.sigla
    Endereco.pais = logradouro.bairro.municipio.estado.pais.nome
    return Endereco

def consultar_bairro(nome,codigo_bairro,municipio):
    from modules.entidade import Bairro
    busca = Bairro.objects.filter(nome=nome)
    
    if busca.count() != 0:
        bairro = busca[0] 
        print("Bairro cadastrado.",bairro.id,bairro.nome)
        return bairro
    
    else:
        print("Bairro nao cadastrado.")
        novo_bairro = Bairro()
        novo_bairro.nome = nome
        novo_bairro.municipio = municipio
        novo_bairro.codigo_ibge = codigo_bairro
        novo_bairro.save()
        print(novo_bairro.nome,"salvo.. ")
        return novo_bairro
        
def consultar_municipio(nome,codigo_municipio,estado):
    from modules.entidade import Municipio
    busca = Municipio.objects.filter(nome=nome, estado=estado)
    
    if busca.count() != 0:
        Municipio = busca[0] 
        return Municipio
    
    else:
        #print("Municipio nao Cadastrado.")
        novo_municipio = Municipio()
        novo_municipio.nome = nome
        novo_municipio.estado = estado
        novo_municipio.codigo_ibge = codigo_municipio
        novo_municipio.save()
        #print("salvei um novo Municipio")
        return novo_municipio

def consultar_estado(sigla):
    from modules.entidade import Estado
    
    if Estado.objects.all().count() != 27:
        print("Reimportando os dados de estados")
        lista_siglas = ["AC","AL","AP","AM","BA","CE","DF","ES","GO","MA","MT","MS","MG","PA","PB","PR","PE","PI","RJ","RN","RS","RO","RR","SC","SP","SE","TO"]
        
        for item in lista_siglas:
            busca = Estado.objects.filter(sigla=item)
            if busca.count() == 0:        
                resultado = json.load(urllib2.urlopen("http://127.0.0.1:8081/api/consultar_estado/sigla/"+item+"/"))
                
                estado = Estado()
                estado.nome = resultado["nome"]
                estado.sigla = resultado["sigla"]
                estado.regiao = resultado["regiao"]
                estado.codigo_ibge = resultado["codigo_ibge"]
                estado.pais = consultar_pais(resultado["Pais"])
                estado.save()
    
    busca = Estado.objects.filter(sigla=sigla)
    if busca.count() != 0:
        return busca[0] 
     
    
def consultar_pais(sigla):
    from modules.entidade import Pais
    busca = Pais.objects.filter(sigla=sigla)
    if busca.count() != 0:
        return busca[0] 
    
    else:
        pais = Pais()
        pais.nome = "BRASIL"
        pais.sigla = "BR"
        pais.save()
        return pais
    


def consultar_codigo_postal_viacep(cep):

    url         = "https://viacep.com.br/ws/"+cep+"/json/unicode/"  
    #pagina      = urllib.urlopen(url)
    print("VEJA A URL: ",url)
    req = requests.get(url)
    print("VEJA O REQUEST: ",req)
    try:
        req = requests.get(url)
        dados_json = json.loads(req.text)
        
        endereco = dados_json["logradouro"].upper()
        bairro = dados_json["bairro"].upper()
        cidade = dados_json["localidade"].upper()
        estado = dados_json["uf"]
        codigo = dados_json["ibge"]
    
        resultado = [endereco,bairro,cidade,codigo,estado,"BRASIL"]
    
    except:
        resultado = ["","","","","","BRASIL"]
    print("OLHA O QUE O VIA CEP NOS TROUXE.. ",resultado)
    return resultado

def consultar_codigo_postal_default(cep):
    cep = cep.replace(".","")
    cep = cep.replace("-","")
    cep_busca   = cep;  
        
    url         = "http://cep.republicavirtual.com.br/web_cep.php?cep=" + cep_busca + "&formato=query_string"  
    pagina      = urllib.urlopen(url)  
    conteudo    = pagina.read();  
    resultado   = cgi.parse_qs(conteudo);
    
    #print(resultado)
    
    if resultado['resultado'][0] == '1':
        #print("Endereco com cidade de CEP unico: "  )
        endereco = resultado['tipo_logradouro'][0].upper()+" "+resultado['logradouro'][0].upper()
        bairro = u""+resultado['bairro'][0].upper().decode("latin-1")
        
        cidade = u""+resultado['cidade'][0].upper().decode("latin-1")
        
        uf     = resultado['uf'][0].upper()
        resultado = [endereco,bairro,cidade,uf]
        
    elif resultado['resultado'][0] == '2':
        #print("Endereco com cidade de CEP unico: "  )
        cidade = resultado['cidade'][0].upper()  
        uf     = resultado['uf'][0].upper() 
        resultado = ["","",cidade,uf]
    else:  
        resultado = None
        
    return resultado