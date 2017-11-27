'''
Created on 16 de set de 2015

@author: Diego
'''
import cgi
import urllib


def consultar_codigo_postal(cep):
    cep = cep.replace(".","")
    cep = cep.replace("-","")
    cep_busca   = cep;  
        
    url         = "http://cep.republicavirtual.com.br/web_cep.php?cep=" + cep_busca + "&formato=query_string"  
    pagina      = urllib.urlopen(url)  
    conteudo    = pagina.read();  
    resultado   = cgi.parse_qs(conteudo);
    
    if resultado['resultado'][0] == '1':
        #print "Endereco com cidade de CEP unico: "  
        Endereco = resultado['tipo_logradouro'][0].upper()+" "+resultado['logradouro'][0].upper()
        bairro = resultado['bairro'][0].upper()
        cidade = resultado['cidade'][0].upper()
        uf     = resultado['uf'][0].upper()
        print "olha o cep c tem pais:",resultado
        resultado = [Endereco,bairro,cidade,uf,]
        
    elif resultado['resultado'][0] == '2':
        #print "Endereco com cidade de CEP unico: "  
        cidade = resultado['cidade'][0].upper()  
        uf     = resultado['uf'][0].upper() 
        resultado = ["","",cidade,uf,]
    else:  
        resultado = None
        
    return resultado

def enviar_email():
    