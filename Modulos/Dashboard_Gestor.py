from ast import Try
from turtle import color
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.Qt import Qt
from PyQt5.QtCore import pyqtSlot, QPropertyAnimation
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtPrintSupport import *
import os, sys
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from numpy import random


from Templates.Dashboard_Gestor import Ui_Dialog
from BD.classes import *
from Modulos.EnviaEmail import EnviaEmail


class MenuGestor(QDialog):
    def __init__(self, sigla_empresa, usuario, *args, **argvs):
        super(MenuGestor,self).__init__(*args, **argvs)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.sigla_empresa = sigla_empresa
        self.usuario = usuario
        #############################################################
        #Quantidade de Colaboradores e Setores Cadastrados
        self.colaborador_cadastrado()
        self.setor_cadastrado()
        #############################################################

        #############################################################
        #Frame Superior
        self.ui.btnHome.clicked.connect(lambda: self.ui.Paginas.setCurrentWidget(self.ui.pageHome))
        self.ui.NomeUsuario.setText(self.usuario)
        #############################################################

        #############################################################
        #Botão que abre menu da esquerda
        self.ui.Menu.clicked.connect(self.menu_esquerda)
        #############################################################

        #############################################################
        #Botões do Menu a esquerda
        self.ui.btnColab.clicked.connect(self.opcao_Colab)
        self.ui.btnEmpresas.clicked.connect(self.opcao_Setor)
        self.ui.bntSair.clicked.connect(self.sair)
        self.ui.btnRelat.clicked.connect(lambda: self.ui.Paginas.setCurrentWidget(self.ui.Relatorio))
        #############################################################

        #############################################################
        #Tamanho das Colunas da tabela de Colaboradores
        self.ui.ListaPessoas.setColumnWidth(0, 0)
        self.ui.ListaPessoas.setColumnWidth(1, 360)
        self.ui.ListaPessoas.setColumnWidth(2, 400)
        self.ui.ListaPessoas.setColumnWidth(3, 250)
        self.ui.ListaPessoas.setColumnWidth(4, 198)
        #############################################################

        #############################################################
        #Tamanho das Colunas da tabela de Setores
        self.ui.TabelaSetor.setColumnWidth(0, 50)
        self.ui.TabelaSetor.setColumnWidth(1, 250)
        self.ui.TabelaSetor.setColumnWidth(2, 360)
        self.ui.TabelaSetor.setColumnWidth(3, 55)
        self.ui.TabelaSetor.setColumnWidth(4, 400)
        #############################################################

        #############################################################
        #Botões dropdown do Colaborador
        self.ui.btnListColab.clicked.connect(lambda: self.ui.Paginas.setCurrentWidget(self.ui.ListaPessoa))
        self.ui.btnCadColab.clicked.connect(self.tela_cadatro_colab)
        #############################################################

        #############################################################
        #Botões dropdown do Setor
        self.ui.btnCadSetor.clicked.connect(lambda: self.ui.Paginas.setCurrentWidget(self.ui.SetorCad))
        self.ui.btnListSetor.clicked.connect(lambda: self.ui.Paginas.setCurrentWidget(self.ui.ListaSetor))
        #############################################################

        #############################################################
        #Botões da Tela Cadastro Colaborador
        self.ui.bntLimparPS.clicked.connect(self.limpar_colaborador)
        self.ui.bntCadastarPS.clicked.connect(self.cadastar_colaborador)
        #############################################################

        #############################################################
        #Lista de Colaboradores
        self.lista_colaborador()
        self.ui.btnPesqPessoa.clicked.connect(self.lista_colaborador_pesquisa)
        self.ui.btnAlteraPessoa.clicked.connect(self.atualizar_colaborador)
        self.ui.btnExcluiPessoa.clicked.connect(self.excluir_colaborador)
        #Seleciona Colaborador
        self.ui.ListaPessoas.itemSelectionChanged.connect(self.colaborador_selcionado)
        #############################################################

        #############################################################
        #Lista de Setores
        self.lista_setor()
        self.ui.btnPesqSetor.clicked.connect(self.lista_setor_pesquisa)
        self.ui.btnAlteraSetor.clicked.connect(self.atualizar_setor)
        self.ui.btnExcluiSetor.clicked.connect(self.excluir_setor)
        #############################################################

        #############################################################
        #Botões do Cadastro de Setor
        self.ui.bntCadSetor.clicked.connect(self.cadastrar_setor)
        #############################################################

        #############################################################
        #Botões Tela relatório
        self.ui.btnPesqQuestao.clicked.connect(self.grafico_questoes)
        #############################################################


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

            x = self.ui.Menu.x()
            self.ui.Menu.move(140, 10)
            self.animationbtn = QPropertyAnimation(self.ui.Menu, b"move")
            self.animationbtn.setDuration(400)
            self.animationbtn.setStartValue(x)
            self.animationbtn.setEndValue(10)
            self.animationbtn.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animationbtn.start()
        else:
            self.animation = QPropertyAnimation(self.ui.frame, b"maximumWidth")
            self.animation.setDuration(250)
            self.animation.setStartValue(width)
            self.animation.setEndValue(41)
            self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animation.start()
            self.ui.frame.setFixedWidth(41)
            self.ui.Menu.move(10, 10)
    
    ########################################################################################
    #Interações com Colaborador
    def opcao_Colab(self):
        #Animação da abrir e fecahar o dropdown do Colaborador
        height = self.ui.frameColab.height()

        if height == 0:
            heigthExtended = 114
            self.animation = QPropertyAnimation(self.ui.frameColab, b"minimumHeight")
            self.animation.setDuration(600)
            self.animation.setStartValue(height)
            self.animation.setEndValue(heigthExtended)
            self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animation.start()
        else: 
            self.animation = QPropertyAnimation(self.ui.frameColab, b"maximumHeight")
            self.animation.setDuration(250)
            self.animation.setStartValue(height)
            self.animation.setEndValue(114)
            self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animation.start()
            self.ui.frameColab.setFixedHeight(0)

    def cadastar_colaborador(self):
        try:
            verifaca = None
            nome_colab = self.ui.NomeCadPS.text()
            cpf_colab = self.ui.CPFCadPS.text()
            email_colab = self.ui.EmailCadPS.text()
            cargo_colab = self.ui.CargoCadPS.text()
            setor_colab = self.ui.SetorCadPS.currentText()
            tel_colab = self.ui.TelCadPS.text()

            if setor_colab != "":
                pass
            else:
                verifaca = 0 
                msg = QMessageBox.information(QMessageBox(), "AVISO", "Selecione um Setor")
            
            if nome_colab != "":
                pass
            else:
                verifaca = 0 
                msg = QMessageBox.information(QMessageBox(), "AVISO", "Insira um Nome")
            
            if email_colab != "":
                pass
            else:
                verifaca = 0 
                msg = QMessageBox.information(QMessageBox(), "AVISO", "Insira um E-mail")
            
            if cargo_colab != "":
                pass
            else:
                verifaca = 0 
                msg = QMessageBox.information(QMessageBox(), "AVISO", "Insira um Cargo")

            if len(cpf_colab) < 14:
                verifaca = 0 
                msg = QMessageBox.information(QMessageBox(), "AVISO", "Insira um CPF")
            else:
                pass
            
            if len(tel_colab) < 16:
                verifaca = 0 
                msg = QMessageBox.information(QMessageBox(), "AVISO", "Insira um Telefone")
            else:
                pass

            if verifaca == None:
                Pessoa.insert_pessoa(nome_colab, email_colab, tel_colab, cargo_colab, cpf_colab, 3, setor_colab, self.sigla_empresa)
                self.colaborador_cadastrado()
            else:
                pass

        except Error as e:
            msg = QMessageBox()
            msg.setText("Algo Deu Errado")
            msg.setWindowTitle("Aviso")
            msg.setIcon(QMessageBox.Critical)
            msg.setDetailedText(f'{e}')
            msg.exec_()
        else:
            if verifaca == None:
                msg = QMessageBox.information(QMessageBox(), "AVISO", "Inserido com Sucesso!")
                self.limpar_colaborador()
                self.lista_colaborador()
                nome_empresa = Empresa.campos_atualizar(self.sigla_empresa)
                EnviaEmail.enviar_email(email_colab, nome_colab, nome_empresa[1])
            else:
                pass     
        

    def lista_colaborador(self):
        self.ui.ListaPessoas.setRowCount(0)
        colaboradores = Pessoa.view_pessoa(self.sigla_empresa)
        
        for linhas, dados in enumerate(colaboradores):
            self.ui.ListaPessoas.insertRow(linhas)
            for coluna, dados in enumerate(dados):
                self.ui.ListaPessoas.setItem(linhas, coluna, QTableWidgetItem(str(dados)))
                a = 1

    def lista_colaborador_pesquisa(self):
        self.ui.ListaPessoas.setRowCount(0)
        pesquisa = self.ui.PesqPessoa.text()
        colaboradores = Pessoa.view_pessoa_pesquisa(pesquisa, self.sigla_empresa)

        for linhas, dados in enumerate(colaboradores):
            self.ui.ListaPessoas.insertRow(linhas)
            for coluna, dados in enumerate(dados):
                self.ui.ListaPessoas.setItem(linhas, coluna, QTableWidgetItem(str(dados)))
                a = 1

    def colaborador_selcionado(self):
        return self.ui.ListaPessoas.currentRow()
    
    def colaborador_selcionado_id_banco(self):
        valor = self.ui.ListaPessoas.item(self.colaborador_selcionado(), 0)
        return valor.text() if not valor is None else valor

    def atualizar_colaborador(self):
        id = self.colaborador_selcionado_id_banco()
        if id != None:
            try:
                self.ui.Paginas.setCurrentWidget(self.ui.PessoaCad)
                dados = Pessoa.campos_atulizar(id)
                self.ui.NomeCadPS.setText(str(dados[0]))
                self.ui.CPFCadPS.setText(str(dados[1]))
                self.ui.EmailCadPS.setText(str(dados[2]))
                self.ui.TelCadPS.setText(str(dados[3]))
                self.ui.CargoCadPS.setText(str(dados[4]))
                self.ui.SetorCadPS.setCurrentText(str(dados[5]))
            except Error as e:
                msg = QMessageBox()
                msg.setText("Algo Deu Errado")
                msg.setWindowTitle("Aviso")
                msg.setIcon(QMessageBox.Critical)
                msg.setDetailedText(f'{e}')
                msg.exec_()
            else:
                msg = QMessageBox.information(QMessageBox(), "AVISO", "Os Dados foram atualizados com sucesso!")
                self.limpar_colaborador()
                self.lista_colaborador()
                self.colaborador_cadastrado()
            
    def excluir_colaborador(self):
        id = self.colaborador_selcionado_id_banco()
        nome_colab = Pessoa.campos_atulizar(id)
        validacao = None
        if id != None:
            try:
                msg = QMessageBox.question(QMessageBox(), "AVISO!!!", "Desja Excluir o Colaborador " + str(nome_colab[0]) + " ?", QMessageBox.Yes | QMessageBox.No)
                if msg == QMessageBox.Yes:
                    Pessoa.excluir_pessoa(id)
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
                    msg = QMessageBox.information(QMessageBox(), "AVISO", "O Colaborador foi excluido com sucesso!")
                    self.lista_colaborador()
                    self.colaborador_cadastrado()

    def tela_cadatro_colab(self):
        self.ui.Paginas.setCurrentWidget(self.ui.PessoaCad)
        #Carrega os setores para cadastro
        setores = Setor.view_sigla_setor(self.sigla_empresa)
        for x in setores:
            self.ui.SetorCadPS.addItems([f"{x[0]}"]) 

    def limpar_colaborador(self):
        self.ui.CPFCadPS.clear()
        self.ui.CargoCadPS.clear()
        self.ui.EmailCadPS.clear()
        self.ui.NomeCadPS.clear()
        self.ui.SetorCadPS.clear()
        self.ui.CargoCadPS.clear()
        self.ui.TelCadPS.clear()
    
    ########################################################################################
    
    ########################################################################################
    #Interações com o Setor
    def opcao_Setor(self):
        #Animação da abrir e fecahar o dropdown do Setor
        height = self.ui.frameSetor.height()

        if height == 0:
            heigthExtended = 114
            self.animation = QPropertyAnimation(self.ui.frameSetor, b"minimumHeight")
            self.animation.setDuration(600)
            self.animation.setStartValue(height)
            self.animation.setEndValue(heigthExtended)
            self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animation.start()
        else: 
            self.animation = QPropertyAnimation(self.ui.frameSetor, b"maximumHeight")
            self.animation.setDuration(250)
            self.animation.setStartValue(height)
            self.animation.setEndValue(114)
            self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animation.start()
            self.ui.frameSetor.setFixedHeight(0)
    
    def cadastrar_setor(self):
        try:
            nome_setor = self.ui.nomeSetorCad.text()
            sigla_setor = self.ui.nomeSetorCad_2.text()
            loc_setor = self.ui.locSetorCad.text()
            setor_pai = self.ui.SetorPaiCad.text()
            ramal_setor = self.ui.RamalSetorCad.text()
            desc_setor = self.ui.textEdit.toPlainText()

            Setor.insert_setor(sigla_setor, nome_setor, loc_setor, ramal_setor, setor_pai, desc_setor, self.sigla_empresa)
        except Error as e:
            msg = QMessageBox()
            msg.setText("Algo Deu Errado")
            msg.setWindowTitle("Aviso")
            msg.setIcon(QMessageBox.Critical)
            msg.setDetailedText(f'{e}')
            msg.exec_()
        else:
            msg = QMessageBox.information(QMessageBox(), "AVISO", "Inserido com Sucesso!")
            self.limapar_setor()
            self.lista_setor()
            self.setor_cadastrado()

    def lista_setor(self):
        self.ui.TabelaSetor.setRowCount(0)
        setores = Setor.view_setor(self.sigla_empresa)
        
        for linhas, dados in enumerate(setores):
            self.ui.TabelaSetor.insertRow(linhas)
            for coluna, dados in enumerate(dados):
                self.ui.TabelaSetor.setItem(linhas, coluna, QTableWidgetItem(str(dados)))
                a = 1

    def lista_setor_pesquisa(self):
        self.ui.TabelaSetor.setRowCount(0)
        pesquisa = self.ui.PesqSetor.text()
        setores = Setor.view_setor_pesquisa(pesquisa, self.sigla_empresa)

        for linhas, dados in enumerate(setores):
            self.ui.TabelaSetor.insertRow(linhas)
            for coluna, dados in enumerate(dados):
                self.ui.TabelaSetor.setItem(linhas, coluna, QTableWidgetItem(str(dados)))
                a = 1

    def setor_selcionado(self):
        return self.ui.TabelaSetor.currentRow()
    
    def setor_selcionado_id_banco(self):
        valor = self.ui.TabelaSetor.item(self.setor_selcionado(), 0)
        return valor.text() if not valor is None else valor
    
    def atualizar_setor(self):
        id = self.setor_selcionado_id_banco()
        if id != None:
            try:
                self.ui.Paginas.setCurrentWidget(self.ui.SetorCad)
                dados = Setor.campos_atualizar(id, self.sigla_empresa)
                self.ui.nomeSetorCad.setText(str(dados[0]))
                self.ui.nomeSetorCad_2.setText(str(dados[1]))
                self.ui.locSetorCad.setText(str(dados[2]))
                self.ui.SetorPaiCad.setText(str(dados[3]))
                self.ui.RamalSetorCad.setText(str(dados[4]))
                self.ui.textEdit.setText(str(dados[5]))
            except Error as e:
                msg = QMessageBox()
                msg.setText("Algo Deu Errado")
                msg.setWindowTitle("Aviso")
                msg.setIcon(QMessageBox.Critical)
                msg.setDetailedText(f'{e}')
                msg.exec_()
            else: 
                msg = QMessageBox.information(QMessageBox(), "AVISO", "Os Dados foram atualizados com sucesso!")
                self.limapar_setor()
                self.lista_setor()
                self.setor_cadastrado()

    def excluir_setor(self):
        id = self.setor_selcionado_id_banco()
        setor = Setor.campos_atualizar(id, self.sigla_empresa)
        validacao = None
        if id != None:
            try:
                msg = QMessageBox.question(QMessageBox(), "AVISO!!!", "Desja Excluir o Setor " + str(setor[0]) + " ?", QMessageBox.Yes | QMessageBox.No)
                if msg == QMessageBox.Yes:
                    Setor.excluir_setor(id)
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
                    msg = QMessageBox.information(QMessageBox(), "AVISO", "Setor excluido com sucesso!")
                    self.lista_setor()
                    self.setor_cadastrado()

    def limapar_setor(self):
        self.ui.nomeSetorCad.clear()
        self.ui.nomeSetorCad_2.clear()
        self.ui.locSetorCad.clear()
        self.ui.SetorPaiCad.clear()
        self.ui.RamalSetorCad.clear()
        self.ui.textEdit.clear()

    ######################################################################################## 

    ########################################################################################
    #Dashboard Principal
    def colaborador_cadastrado(self):
        num_colab = Pessoa.quantidade_pessoas_cadastradas(self.sigla_empresa)
        self.ui.NumColab.setText(f"{num_colab[0]}")
        self.ui.NumColab.setStyleSheet("QLabel { color: rgb(34, 90, 229); font-weight: bold; font-size: 16px; }")

    def setor_cadastrado(self):
        num_setor = Setor.quantidade_setor_cadastrados(self.sigla_empresa)
        self.ui.NumSetor.setText(f"{num_setor[0]}")
        self.ui.NumSetor.setStyleSheet("QLabel { color: rgb(241, 198, 91); font-weight: bold; font-size: 16px; }")

    ########################################################################################

    ########################################################################################
    #Tela ralatório
    def grafico_questoes(self):
        if self.ui.comboBox.currentIndex() == 0:
            self.ui.PaginasQuestao.setCurrentWidget(self.ui.Questao1)
            self.ui.figure.clear()

            respostas = ["Feminino", "Masculino", "Outro"]

            resp_questA = Resposta.view_grafico_quest1_A_fase1()
            resp_questB = Resposta.view_grafico_quest1_B_fase1()
            resp_questC = Resposta.view_grafico_quest1_C_fase1()
            valores = [resp_questA[0], resp_questB[0], resp_questC[0]]  

            plt.bar(respostas, valores, color = "blue", width = 0.2)

            plt.xlabel("Respostas")
            plt.ylabel("N° Respostas")
            plt.title("Questão 1 - Fase 1")
            self.ui.canvas.draw()
        
        elif self.ui.comboBox.currentIndex() == 1:
            self.ui.PaginasQuestao.setCurrentWidget(self.ui.Questao1)
            self.ui.figure.clear()

            respostas = ["Entre 18 e 24 anos", "Entre 25 e 34 anos", "Entre 35 e 44 anos", "45 anos ou mais"]

            resp_questA = Resposta.view_grafico_quest2_A_fase1()
            resp_questB = Resposta.view_grafico_quest2_B_fase1()
            resp_questC = Resposta.view_grafico_quest2_C_fase1()
            resp_questD = Resposta.view_grafico_quest2_D_fase1()
            valores = [resp_questA[0], resp_questB[0], resp_questC[0], resp_questD[0]]

            plt.bar(respostas, valores, color = "blue", width = 0.4)

            plt.xlabel("Respostas")
            plt.ylabel("N° Respostas")
            plt.title("Questão 2 - Fase 1")
            self.ui.canvas.draw()
        
        elif self.ui.comboBox.currentIndex() == 2:
            self.ui.PaginasQuestao.setCurrentWidget(self.ui.Questao1)
            self.ui.figure.clear()

            respostas = ["Solteiro(a)", "Casado(a)", "Viúvo(a)", "Outro"]

            resp_questA = Resposta.view_grafico_quest3_A_fase1()
            resp_questB = Resposta.view_grafico_quest3_B_fase1()
            resp_questC = Resposta.view_grafico_quest3_C_fase1()
            resp_questD = Resposta.view_grafico_quest3_D_fase1()
            valores = [resp_questA[0], resp_questB[0], resp_questC[0], resp_questD[0]]

            plt.bar(respostas, valores, color = "blue", width = 0.4)

            plt.xlabel("Respostas")
            plt.ylabel("N° Respostas")
            plt.title("Questão 3 - Fase 1")
            self.ui.canvas.draw()
        
        elif self.ui.comboBox.currentIndex() == 3:
            self.ui.PaginasQuestao.setCurrentWidget(self.ui.Questao1)
            self.ui.figure.clear()

            respostas = ["Setor A", "Setor B", "Setor C", "Outro setor"]

            resp_questA = Resposta.view_grafico_quest4_A_fase1()
            resp_questB = Resposta.view_grafico_quest4_B_fase1()
            resp_questC = Resposta.view_grafico_quest4_C_fase1()
            resp_questD = Resposta.view_grafico_quest4_D_fase1()
            valores = [resp_questA[0], resp_questB[0], resp_questC[0], resp_questD[0]]

            plt.bar(respostas, valores, color = "blue", width = 0.4)

            plt.xlabel("Respostas")
            plt.ylabel("N° Respostas")
            plt.title("Questão 4 - Fase 1")
            self.ui.canvas.draw()
        
        elif self.ui.comboBox.currentIndex() == 4:
            self.ui.PaginasQuestao.setCurrentWidget(self.ui.Questao1)
            self.ui.figure.clear()

            respostas = ["Nunca", "Às vezes", "Diariamente", "Semanalmente"]

            resp_questA = Resposta.view_grafico_quest1_A()
            resp_questB = Resposta.view_grafico_quest1_B()
            resp_questC = Resposta.view_grafico_quest1_C()
            resp_questD = Resposta.view_grafico_quest1_D()
            valores = [resp_questA[0], resp_questB[0], resp_questC[0], resp_questD[0]]  

            plt.bar(respostas, valores, color = "blue", width = 0.4)

            plt.xlabel("Respostas")
            plt.ylabel("N° Respostas")
            plt.title("Questão 1 - Fase 2")
            self.ui.canvas.draw()

        elif self.ui.comboBox.currentIndex() == 5:
            self.ui.PaginasQuestao.setCurrentWidget(self.ui.Questao1)
            self.ui.figure.clear()

            respostas = ["Nunca", "Às vezes", "Diariamente", "Semanalmente"]

            resp_questA = Resposta.view_grafico_quest2_A()
            resp_questB = Resposta.view_grafico_quest2_B()
            resp_questC = Resposta.view_grafico_quest2_C()
            resp_questD = Resposta.view_grafico_quest2_D()
            valores = [resp_questA[0], resp_questB[0], resp_questC[0], resp_questD[0]]  

            plt.bar(respostas, valores, color = "blue", width = 0.4)

            plt.xlabel("Respostas")
            plt.ylabel("N° Respostas")
            plt.title("Questão 2 - Fase 2")
            self.ui.canvas.draw()
        
        elif self.ui.comboBox.currentIndex() == 6:
            self.ui.PaginasQuestao.setCurrentWidget(self.ui.Questao1)
            self.ui.figure.clear()

            respostas = ["Nunca", "Às vezes", "Diariamente", "Semanalmente"]

            resp_questA = Resposta.view_grafico_quest3_A()
            resp_questB = Resposta.view_grafico_quest3_B()
            resp_questC = Resposta.view_grafico_quest3_C()
            resp_questD = Resposta.view_grafico_quest3_D()
            valores = [resp_questA[0], resp_questB[0], resp_questC[0], resp_questD[0]]  

            plt.bar(respostas, valores, color = "blue", width = 0.4)

            plt.xlabel("Respostas")
            plt.ylabel("N° Respostas")
            plt.title("Questão 3 - Fase 2")
            self.ui.canvas.draw()
        
        elif self.ui.comboBox.currentIndex() == 7:
            self.ui.PaginasQuestao.setCurrentWidget(self.ui.Questao1)
            self.ui.figure.clear()

            respostas = ["Nunca", "Às vezes", "Diariamente", "Semanalmente"]

            resp_questA = Resposta.view_grafico_quest4_A()
            resp_questB = Resposta.view_grafico_quest4_B()
            resp_questC = Resposta.view_grafico_quest4_C()
            resp_questD = Resposta.view_grafico_quest4_D()
            valores = [resp_questA[0], resp_questB[0], resp_questC[0], resp_questD[0]]  

            plt.bar(respostas, valores, color = "blue", width = 0.4)

            plt.xlabel("Respostas")
            plt.ylabel("N° Respostas")
            plt.title("Questão 4 - Fase 2")
            self.ui.canvas.draw()
        
        elif self.ui.comboBox.currentIndex() == 8:
            self.ui.PaginasQuestao.setCurrentWidget(self.ui.Questao1)
            self.ui.figure.clear()

            respostas = ["Nunca", "Às vezes", "Diariamente", "Semanalmente"]

            resp_questA = Resposta.view_grafico_quest5_A()
            resp_questB = Resposta.view_grafico_quest5_B()
            resp_questC = Resposta.view_grafico_quest5_C()
            resp_questD = Resposta.view_grafico_quest5_D()
            valores = [resp_questA[0], resp_questB[0], resp_questC[0], resp_questD[0]]  

            plt.bar(respostas, valores, color = "blue", width = 0.4)

            plt.xlabel("Respostas")
            plt.ylabel("N° Respostas")
            plt.title("Questão 5 - Fase 2")
            self.ui.canvas.draw()
        
        elif self.ui.comboBox.currentIndex() == 9:
            self.ui.PaginasQuestao.setCurrentWidget(self.ui.Questao1)
            self.ui.figure.clear()

            respostas = ["Alguns dias", "Algumas semanas", "Alguns meses", "Um ano"]

            resp_questA = Resposta.view_grafico_quest6_A()
            resp_questB = Resposta.view_grafico_quest6_B()
            resp_questC = Resposta.view_grafico_quest6_C()
            resp_questD = Resposta.view_grafico_quest6_D()
            valores = [resp_questA[0], resp_questB[0], resp_questC[0], resp_questD[0]]  

            plt.bar(respostas, valores, color = "blue", width = 0.4)

            plt.xlabel("Respostas")
            plt.ylabel("N° Respostas")
            plt.title("Questão 6 - Fase 2")
            self.ui.canvas.draw()

        elif self.ui.comboBox.currentIndex() == 10:
            self.ui.PaginasQuestao.setCurrentWidget(self.ui.Questao1)
            self.ui.figure.clear()

            respostas = ["Colegas", "Algumas semanas", "Alguns meses", "Um ano"]

            resp_questA = Resposta.view_grafico_quest6_A()
            resp_questB = Resposta.view_grafico_quest6_B()
            resp_questC = Resposta.view_grafico_quest6_C()
            resp_questD = Resposta.view_grafico_quest6_D()
            valores = [resp_questA[0], resp_questB[0], resp_questC[0], resp_questD[0]]  

            plt.bar(respostas, valores, color = "blue", width = 0.4)

            plt.xlabel("Respostas")
            plt.ylabel("N° Respostas")
            plt.title("Questão 7 - Fase 2")
            self.ui.canvas.draw()
        
        elif self.ui.comboBox.currentIndex() == 11:
            self.ui.PaginasQuestao.setCurrentWidget(self.ui.Questao1)
            self.ui.figure.clear()

            respostas = ["Ignoraram o fato", "Procuraram medir a situação", "Puniram o(s) agressor(es)", "Puniram você"]

            resp_questA = Resposta.view_grafico_quest8_A()
            resp_questB = Resposta.view_grafico_quest8_B()
            resp_questC = Resposta.view_grafico_quest8_C()
            resp_questD = Resposta.view_grafico_quest8_D()
            valores = [resp_questA[0], resp_questB[0], resp_questC[0], resp_questD[0]]  

            plt.bar(respostas, valores, color = "blue", width = 0.4)

            plt.xlabel("Respostas")
            plt.ylabel("N° Respostas")
            plt.title("Questão 8 - Fase 2")
            self.ui.canvas.draw()
        
        elif self.ui.comboBox.currentIndex() == 12:
            self.ui.PaginasQuestao.setCurrentWidget(self.ui.Questao1)
            self.ui.figure.clear()

            respostas = ["Sim", "Não"]

            resp_questA = Resposta.view_grafico_quest9_A()
            resp_questB = Resposta.view_grafico_quest9_B()
            valores = [resp_questA[0], resp_questB[0]]  

            plt.bar(respostas, valores, color = "blue", width = 0.4)

            plt.xlabel("Respostas")
            plt.ylabel("N° Respostas")
            plt.title("Questão 9 - Fase 2")
            self.ui.canvas.draw()
        
        elif self.ui.comboBox.currentIndex() == 13:
            self.ui.PaginasQuestao.setCurrentWidget(self.ui.Questao1)
            self.ui.figure.clear()

            respostas = ["Desejar melhorias de salário", "Receio de serem eles ...", "Estarem do lado do(s) agressor(es)", "Outros"]

            resp_questA = Resposta.view_grafico_quest10_A()
            resp_questB = Resposta.view_grafico_quest10_B()
            resp_questC = Resposta.view_grafico_quest10_C()
            resp_questD = Resposta.view_grafico_quest10_D()
            valores = [resp_questA[0], resp_questB[0], resp_questC[0], resp_questD[0]]  

            plt.bar(respostas, valores, color = "blue", width = 0.4)

            plt.xlabel("Respostas")
            plt.ylabel("N° Respostas")
            plt.title("Questão 10 - Fase 2")
            self.ui.canvas.draw()
        
    ########################################################################################
    
    def sair(self):
        #Sair do Sistema
        MenuGestor.close(self)
