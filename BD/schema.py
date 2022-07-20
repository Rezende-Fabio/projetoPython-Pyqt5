import sqlite3
import time
import os
from sqlite3 import Error


class Conexao:
    
    def __init__(self):
        self.database = "Scanawe.db"
        self.conn = None
        self.cur = None
        self.connected = None
    
    def creatDb(self):
        try:
            self.conn = sqlite3.connect(self.database)
        except Exception as e:
            print(e)

    def connect(self):
        try:
            self.conn = sqlite3.connect(self.database)
            self.cur = self.conn.cursor()
            self.connected = True
        except Exception as e:
            print(e)
    
    def execute(self, sql, parms = None):
        if self.connected:
            if parms == None:
                self.cur.execute(sql)
            else:
                self.cur.execute(sql, parms)
            return True
        else:
            return False
    
    def fetchall(self):
        return self.cur.fetchall()

    def commit(self):
        self.conn.commit()
        
    def table(self):

        try:
            self.cur.execute("""
                CREATE TABLE IF NOT EXISTS PERFIL(
                    permissao INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT DEFAULT 3,
                    descricaoPerfil TEXT (15) NOT NULL   
                    );""")
        except Error as e:
            print (f"ERRO {e} na tabela PERFIL")

    #------------------------------------------------------------------------

        try:
            self.cur.execute("""
                CREATE TABLE IF NOT EXISTS TOKEN(
                    idToken INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    token TEXT (10) NOT NULL	   
                    );""")
        except Error as e:
            print (f"ERRO {e} na tabela TOKEN")

        #------------------------------------------------------------------------

        try:
            self.cur.execute("""
                CREATE TABLE IF NOT EXISTS ENDERECO(
                    idEndereco INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    estado TEXT (5) NOT NULL,
                    cidade TEXT (25) NOT NULL,
                    bairro TEXT (25) NOT NULL,
                    rua TEXT (25) NOT NULL,
                    numero INTEGER NOT NULL,
                    complemento TEXT (25),
                    cep	TEXT (8) NOT NULL
                    );""")
        except Error as e:
            print (f"ERRO {e} na tabela ENDERECO")

        #------------------------------------------------------------------------

        try:
            self.cur.execute("""
                CREATE TABLE IF NOT EXISTS EMPRESA(
                    siglaEmpresa TEXT (5) NOT NULL PRIMARY KEY, 
                    nomeEmpresa TEXT (50) NOT NULL,   
                    cnpj TEXT (50) NOT NULL,
                    idEndereco INTEGER NOT NULL,
                    FOREIGN KEY (idEndereco) REFERENCES ENDERECO (idEndereco)
                    ON DELETE CASCADE ON UPDATE CASCADE
                    );""")
        except Error as e:
            print (f"ERRO {e} na tabela EMPRESA")

        #------------------------------------------------------------------------

        try:
            self.cur.execute("""
                CREATE TABLE IF NOT EXISTS SETOR(
                    siglaSetor TEXT (5) NOT NULL PRIMARY KEY,
                    nomeSetor TEXT (25) NOT NULL, 
                    localizacao TEXT (25) NOT NULL,
                    ramal TEXT (25),	
                    setorPai TEXT (5),
                    descricaoSetor TEXT (100),
                    siglaEmpresa TEXT(5) NOT NULL,
	                FOREIGN KEY(siglaEmpresa) REFERENCES EMPRESA(siglaEmpresa)
                    ON DELETE CASCADE ON UPDATE CASCADE
                    );""")
        except Error as e:
            print (f"ERRO {e} na tabela SETOR")

        #------------------------------------------------------------------------

        try:
            self.cur.execute("""
                CREATE TABLE IF NOT EXISTS PESSOA(
                    idPessoa INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    nomePessoa TEXT (50) NOT NULL, 
                    email TEXT (50) NOT NULL,
                    telefone TEXT (11),
                    cargo TEXT (20) NOT NULL,
                    cpf TEXT (11) NOT NULL,
                    idToken INTEGER,
                    permissao INTEGER NOT NULL,
                    siglaSetor TEXT (5),
                    siglaEmpresa TEXT(5),
                    FOREIGN KEY (idToken) REFERENCES TOKEN (idToken)
                    ON DELETE CASCADE ON UPDATE CASCADE,
                    FOREIGN KEY (permissao) REFERENCES PERFIL (permissao)
                    ON DELETE CASCADE ON UPDATE CASCADE,
                    FOREIGN KEY (siglaSetor) REFERENCES SETOR (siglaSetor)
                    ON DELETE CASCADE ON UPDATE CASCADE
                    FOREIGN KEY(siglaEmpresa) REFERENCES EMPRESA (siglaEmpresa)
                    ON DELETE CASCADE ON UPDATE CASCADE	   
                    );""")
        except Error as e:
            print (f"ERRO {e} na tabela PESSOA")

        #------------------------------------------------------------------------

        try:
            self.cur.execute("""
                CREATE TABLE IF NOT EXISTS LOGIN(
                    idLogin INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    login TEXT (50) NOT NULL,
                    senha TEXT (25) NOT NULL,
                    idPessoa INTEGER NOT NULL,
                    FOREIGN KEY (idPessoa) REFERENCES PESSOA (idPessoa)
                    ON DELETE CASCADE ON UPDATE CASCADE	   
                    );""")
        except Error as e:
            print (f"ERRO {e} na tabela LOGIN")

        #------------------------------------------------------------------------

        try:
            self.cur.execute("""
                CREATE TABLE IF NOT EXISTS RELATORIO(
                    siglaRelatorio TEXT (5) NOT NULL PRIMARY KEY,
                    tituloRelatorio TEXT (25) NOT NULL,
                    data date NOT NULL	   
                    );""")
        except Error as e:
            print (f"ERRO {e} na tabela RELATORIO")

        #------------------------------------------------------------------------
        try:
            self.cur.execute("""
                CREATE TABLE IF NOT EXISTS QUESTIONARIO(
                    siglaQuestionario TEXT (5) NOT NULL PRIMARY KEY,
                    tituloQuestionario TEXT (50) NOT NULL,
                    dataInicio TEXT (25) NOT NULL,
                    dataFinal INTEGER NOT NULL,
                    siglaEmpresa TEXT (5) NOT NULL,
                    siglaRelatorio TEXT (5),	    
                    FOREIGN KEY (siglaEmpresa) REFERENCES EMPRESA (siglaEmpresa)
                    ON DELETE CASCADE ON UPDATE CASCADE,	
                    FOREIGN KEY (siglaRelatorio) REFERENCES RELATORIO (siglaRelatorio)
                    ON DELETE CASCADE ON UPDATE CASCADE
                    );""")
        except Error as e:
            print (f"ERRO {e} na tabela QUESTIONARIO")

        #------------------------------------------------------------------------

        try:
            self.cur.execute("""
                CREATE TABLE IF NOT EXISTS QUESTAO(
                    idQuestao INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    tipo TEXT (25) NOT NULL,
                    descricaoQuestao TEXT (50) NOT NULL,
                    siglaQuestionario TEXT (5) NOT NULL,
                    FOREIGN KEY (siglaQuestionario) REFERENCES QUESTIONARIO (siglaQuestionario)
                    ON DELETE CASCADE ON UPDATE CASCADE	   
                    );""")
        except Error as e:
            print (f"ERRO {e} na tabela QUESTAO")

        #------------------------------------------------------------------------

        try:
            self.cur.execute("""
                CREATE TABLE IF NOT EXISTS RESPOSTA(
                    idResposta INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    descricaoResposta TEXT (50) NOT NULL,
                    idQuestao INTEGER NOT NULL,
                    FOREIGN KEY (idQuestao) REFERENCES QUESTAO (idQuestao)
                    ON DELETE CASCADE ON UPDATE CASCADE	   
                    );""")
        except Error as e:
            print (f"ERRO {e} na tabela RESPOSTA")

        #------------------------------------------------------------------------