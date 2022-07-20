from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.Qt import Qt
from PyQt5.QtCore import pyqtSlot, QPropertyAnimation
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap, QKeyEvent
from PyQt5.QtPrintSupport import *
import os, sys
from BD.classes import *
import requests
from time import sleep
from sqlite3 import Error

from Templates.Dashboard_Consultor import Ui_Dialog


class MenuConsultor(QDialog):
    def __init__(self, usuario, *args, **argvs):
        super(MenuConsultor,self).__init__(*args, **argvs)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.usuario = usuario
        self.ui.label_26.setFocus()
        #############################################################
        #Quantidade de Empresas Cadastradas
        self.empresas_cadastradas()
        #############################################################

        #############################################################
        #Frame Superior
        self.ui.btnHome.clicked.connect(lambda: self.ui.Paginas.setCurrentWidget(self.ui.PageHome))
        self.ui.NomeUsuario.setText(self.usuario)
        #############################################################

        #############################################################
        #Botões do Menu a esquerda
        self.ui.pushButton_2.clicked.connect(self.menu_esquerda)
        self.ui.btnEmpresas.clicked.connect(self.opcao_Empre)
        self.ui.bntSair.clicked.connect(self.sair)
        #self.ui.btnQuestionario.clicked.connect(lambda: self.ui.Paginas.setCurrentWidget(self.ui.GerarRelat))
        self.ui.btnRelat.clicked.connect(lambda: self.ui.Paginas.setCurrentWidget(self.ui.Questionario))
        #############################################################
        
        #############################################################
        #Botões do Frame Empresas
        self.ui.btnCadEmpresa.clicked.connect(lambda: self.ui.Paginas.setCurrentWidget(self.ui.EmpresaCad))
        self.ui.btnListEmpresa.clicked.connect(lambda: self.ui.Paginas.setCurrentWidget(self.ui.EmpresaList))
        #############################################################

        #############################################################
        #Botão tela Gerar token
        self.ui.btnToken.clicked.connect(self.tela_gerar_token)
        #############################################################

        #############################################################
        #Tela Listagem de Empresas
        self.lista_de_empresas()
        self.ui.btnPesqEmpresa.clicked.connect(self.lista_de_empresas_pesquisa)
        self.ui.btnAlteraEmpresa.clicked.connect(self.atualizar_empresa)
        self.ui.btnExcluiEmpresa.clicked.connect(self.excluir_empresas)
        #############################################################

        #############################################################
        #Cadastro de Empresas
        self.ui.btnCadEmpresas.clicked.connect(self.cadstar_empresa)
        self.ui.btnLimpEmpresa.clicked.connect(self.limpar_empresa)
        #Enter para buscar o cep
        self.ui.cep.returnPressed.connect(self.pega_cep)
        #############################################################

        #############################################################
        #Tela Gerar Tooken
        self.ui.btnPesqColabEmp.clicked.connect(self.lista_colaboradores_token)
        self.ui.btnGerarTooken.clicked.connect(self.gerar_token)
        #############################################################

    ########################################################################################
    #Menu da Esquerda
    def menu_esquerda(self):
        #Animação de abrir e fechar o menu da esquerda
        width = self.ui.frame.width()

        if width == 41:
            widthExtended = 161
            self.animation = QPropertyAnimation(self.ui.frame, b"minimumWidth")
            self.animation.setDuration(250)
            self.animation.setStartValue(width)
            self.animation.setEndValue(widthExtended)
            self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animation.start()

            x = self.ui.pushButton_2.x()
            self.ui.pushButton_2.move(140, 10)
            self.animationbtn = QPropertyAnimation(self.ui.pushButton_2, b"move")
            self.animationbtn.setDuration(400)
            self.animationbtn.setStartValue(x)
            self.animationbtn.setEndValue(10)
            self.animationbtn.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animationbtn.start()
        else:
            widthExtended = 41
            self.animation = QPropertyAnimation(self.ui.frame, b"maximumWidth")
            self.animation.setDuration(250)
            self.animation.setStartValue(width)
            self.animation.setEndValue(widthExtended)
            self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animation.start()
            self.ui.frame.setFixedWidth(41)
            self.ui.pushButton_2.move(10, 10)
    ########################################################################################

    ########################################################################################
    #Interações com a Empresa
    def pega_cep(self):
        try:
            self.limpar_requisicao_cep()
            cep = self.ui.cep.text()
            cep = cep.replace("-", "")
            retorno = requests.get(f'https://viacep.com.br/ws/{cep}/json/').json()
            rua = retorno["logradouro"]
            complemento = retorno["complemento"]
            bairro = retorno["bairro"]
            cidade = retorno["localidade"]
            estado = retorno["uf"]

            self.ui.cidade.insert(cidade)
            self.ui.estado.insert(estado)
            if len(rua) != 0:
                self.ui.rua.insert(rua)
            if len(complemento) != 0:
                self.ui.complemento.insert(complemento)
            if len(bairro) != 0:
                self.ui.bairro.insert(bairro)
        except:
            pass
        
    def opcao_Empre(self):
        #Animação da abrir e fecahar o dropdown da Empresa
        height = self.ui.frameEmpresa.height()

        if height == 0:
            heigthExtended = 114
            self.animation = QPropertyAnimation(self.ui.frameEmpresa, b"minimumHeight")
            self.animation.setDuration(600)
            self.animation.setStartValue(height)
            self.animation.setEndValue(heigthExtended)
            self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animation.start()
        else: 
            self.animation = QPropertyAnimation(self.ui.frameEmpresa, b"maximumHeight")
            self.animation.setDuration(250)
            self.animation.setStartValue(height)
            self.animation.setEndValue(114)
            self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animation.start()
            self.ui.frameEmpresa.setFixedHeight(0)
    
    def cadstar_empresa(self):
        try:
            #Dados do endereço
            rua = self.ui.rua.text()
            numero = self.ui.numero.text()
            bairro = self.ui.bairro.text()
            complemento = self.ui.complemento.text()
            cep = self.ui.cep.text()
            cidade = self.ui.cidade.text()
            estado = self.ui.estado.text()

            #Insere o enderço e pega o id para inserir na empresa
            Endereco.insert_endereco(estado, cidade, bairro, rua, numero, complemento, cep)
            id_endereco = Endereco.id_endereco_empresa()

            #Insere Empresa
            nome_empresa = self.ui.nomeEmpresa.text()
            sigla = self.ui.siglaEmpresa.text()
            cnpj = self.ui.cnpj.text()
            Empresa.insert_empresa(sigla, nome_empresa, cnpj, id_endereco)
            
            #Insere Gestor
            nome_gestor = self.ui.nomeGestor.text()
            email_gestor = self.ui.emailGestor.text()
            tel_gestor = self.ui.telGestor.text()
            cpf_gestor = self.ui.cpfGestor.text()
            cargo = "Gestor"
            permisao = 2
            sigla_setor_gestor = ""
            Pessoa.insert_gestor(nome_gestor, email_gestor, tel_gestor, cargo, cpf_gestor, permisao, sigla_setor_gestor, sigla)
            
            #Insere Login Gestor
            id_pessoa = Pessoa.id_login()
            login = self.ui.usuarioGestor.text().upper()
            senha = self.ui.senhaGestor.text().upper()
            Login.insert_login(login, senha, id_pessoa)
            
            self.limpar_empresa()
        except Error as e:
            msg = QMessageBox()
            msg.setText("Algo Deu Errado")
            msg.setWindowTitle("Aviso")
            msg.setIcon(QMessageBox.Critical)
            msg.setDetailedText(f'{e}')
            msg.exec_()
        else:
            msg = QMessageBox.information(QMessageBox(), "AVISO", "Inserido com Sucesso!")
            self.lista_de_empresas()
            self.empresas_cadastradas()
    
    def atualizar_empresa(self):
        sigla = self.empresas_selcionado_id_banco()
        if id != None:
            try:
                self.ui.Paginas.setCurrentWidget(self.ui.EmpresaCad)
                dados = Empresa.campos_atualizar(sigla)
                self.ui.siglaEmpresa.setText(str(dados[0]))
                self.ui.nomeEmpresa.setText(str(dados[1]))
                self.ui.cnpj.setText(str(dados[2]))
                self.ui.estado.setText(str(dados[3]))
                self.ui.cidade.setText(str(dados[4]))
                self.ui.bairro.setText(str(dados[5]))
                self.ui.rua.setText(str(dados[6]))
                self.ui.numero.setText(str(dados[7]))
                self.ui.cep.setText(str(dados[8]))
                self.ui.complemento.setText(str(dados[9]))
            except Error as e:
                msg = QMessageBox()
                msg.setText("Algo Deu Errado")
                msg.setWindowTitle("Aviso")
                msg.setIcon(QMessageBox.Critical)
                msg.setDetailedText(f'{e}')
                msg.exec_()
    
    def excluir_empresas(self):
        sigla_empresa = self.empresas_selcionado_id_banco()
        nome_empresa = Empresa.campos_atualizar(sigla_empresa)
        validacao = None
        if sigla_empresa != None:
            try:
                msg = QMessageBox.question(QMessageBox(), "AVISO!!!", "Desja Excluir a Empresa " + str(nome_empresa[1]) + " ?", QMessageBox.Yes | QMessageBox.No)

                if msg == QMessageBox.Yes:
                    Empresa.excluir_empresas(sigla_empresa)
                else:
                    validacao = 0
                
            except Error as e:
                msg = QMessageBox()
                msg.setText("Algo Deu Errado")
                msg.setWindowTitle("Aviso")
                msg.setIcon(QMessageBox.Critical)
                msg.setDetailedText(f'{e}')
                msg.exec_()
            else:
                if validacao == None:
                    msg = QMessageBox.information(QMessageBox(), "AVISO", "A Empresa foi excluida com sucesso!") 
                    self.lista_de_empresas()
                    self.empresas_cadastradas()

    def limpar_empresa(self):
        self.ui.rua.clear()
        self.ui.numero.clear()
        self.ui.bairro.clear()
        self.ui.complemento.clear()
        self.ui.cep.clear()
        self.ui.cidade.clear()
        self.ui.estado.clear()
        self.ui.nomeEmpresa.clear()
        self.ui.siglaEmpresa.clear()
        self.ui.cnpj.clear()
        self.ui.nomeGestor.clear()
        self.ui.emailGestor.clear()
        self.ui.telGestor.clear()
        self.ui.cpfGestor.clear()
        self.ui.usuarioGestor.clear()
        self.ui.senhaGestor.clear()

    def limpar_requisicao_cep(self):
        self.ui.rua.clear()
        self.ui.numero.clear()
        self.ui.bairro.clear()
        self.ui.complemento.clear()
        self.ui.cidade.clear()
        self.ui.estado.clear()
    
    def empresas_cadastradas(self):
        num_empresas = Empresa.quantidade_de_empresas()
        self.ui.numEmpresas.setText(f"{num_empresas[0]}")
        self.ui.numEmpresas.setStyleSheet("QLabel { color: rgb(34, 90, 229); font-weight: bold; font-size: 16px; }")
    ########################################################################################

    ########################################################################################
    #Gerar Token
    def lista_colaboradores_token(self):
        self.ui.TabelaGerarToken.setRowCount(0)
        sigla_empresa = self.ui.btnSiglaEmpresa.currentText()
        colaboradores = Pessoa.veiw_pessoa_gerar_token(sigla_empresa)

        for linhas, dados in enumerate(colaboradores):
            self.ui.TabelaGerarToken.insertRow(linhas)
            for coluna, dados in enumerate(dados):
                self.ui.TabelaGerarToken.setItem(linhas, coluna, QTableWidgetItem(str(dados)))
                a = 1

    def gerar_token(self):
        sigla_empresa = self.ui.btnSiglaEmpresa.currentText()
        try:
            Token.gera_token_colaborador(sigla_empresa)
        except Error as e:
            msg = QMessageBox()
            msg.setText("Algo Deu Errado")
            msg.setWindowTitle("Aviso")
            msg.setIcon(QMessageBox.Critical)
            msg.setDetailedText(f'{e}')
            msg.exec_()
        else:
            msg = QMessageBox.information(QMessageBox(), "AVISO", "Os Tokens foram gerados com sucesso!")
        
        self.lista_colaboradores_token()
    
    def tela_gerar_token(self):
        self.ui.Paginas.setCurrentWidget(self.ui.GerarToken)
        empresas = Empresa.view_sigla_Empresa()
        for x in empresas:
            self.ui.btnSiglaEmpresa.addItems([f"{x[0]}"])
        
    ########################################################################################

    ########################################################################################
    #Lista de Empresas
    def lista_de_empresas(self):
        self.ui.TabelaEmpresas.setRowCount(0)
        empresas = Empresa.view_empresa()

        for linhas, dados in enumerate(empresas):
            self.ui.TabelaEmpresas.insertRow(linhas)
            for coluna, dados in enumerate(dados):
                self.ui.TabelaEmpresas.setItem(linhas, coluna, QTableWidgetItem(str(dados)))
                a = 1
    
    def lista_de_empresas_pesquisa(self):
        self.ui.TabelaEmpresas.setRowCount(0)
        pesquisa = self.ui.PesqEmpresa.text()
        empresas = Empresa.view_empresa_pesquisa(pesquisa)

        for linhas, dados in enumerate(empresas):
            self.ui.TabelaEmpresas.insertRow(linhas)
            for coluna, dados in enumerate(dados):
                self.ui.TabelaEmpresas.setItem(linhas, coluna, QTableWidgetItem(str(dados)))
                a = 1
    
    def empresas_selcionado(self):
        return self.ui.TabelaEmpresas.currentRow()
    
    def empresas_selcionado_id_banco(self):
        valor = self.ui.TabelaEmpresas.item(self.empresas_selcionado(), 0)
        return valor.text() if not valor is None else valor
    ########################################################################################

    def sair(self):
        #Sair do sistema
        MenuConsultor.close(self)
