'''
Created on 29 de set de 2015

@author: Diego
'''


def converte_data_datetime(data):
    #print "Olha a data:",data," - ",type(data)
    if data != "" and data!= None:
        campos = data.split("/")
        return campos[2]+"-"+campos[1]+"-"+campos[0]
    return data

def converte_datetime_data(data):
    if data != "":
        campos = data.split("-")
        return campos[2]+"/"+campos[1]+"/"+campos[0]
    return data

def formatar_codificacao(texto):
    texto = u''+unicode(texto, "latin-1")   
    texto = texto.upper()
    return texto 

def remover_simbolos(texto):
    texto = texto.replace(".","")
    texto = texto.replace(",","")
    texto = texto.replace("-","")
    return texto