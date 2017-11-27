'''
Created on 8 de abr de 2016

@author: Win7
'''

import sqlite3

class database_manager():
    
    conexao = None
    cursor  = None
    banco   = None
    
    def conectar_banco(self,banco):
        self.banco = banco
        try:
            self.conexao = sqlite3.connect(banco)
            self.cursor = self.conexao.cursor()    
                
        except sqlite3.Error, e:
            print "Error %s:" % e.args[0]
            
    def inserir(self,tabela,campos,valores):
        query = "INSERT INTO "+tabela+" ("+campos+") VALUES ("+valores+")"
        print query
        self.execute(query)
        
    def selecionar(self,tabela,campos,condicao):
        query = "SELECT "+campos+" FROM "+tabela
        
        if condicao != "":
            query = query+" WHERE ("+condicao+")"
        
        print query
        return self.cursor.execute(query)
    
    def execute(self,query):
        try:
            self.cursor.execute(query)
            self.conexao.commit()
        except:
            print "Erro na execucao da query: ",query
            self.conexao.rollback()