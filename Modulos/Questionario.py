from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.Qt import Qt
from PyQt5.QtCore import pyqtSlot, QPropertyAnimation
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap, QKeyEvent
from PyQt5.QtPrintSupport import *
import os, sys
from BD.classes import *

from Templates.Questionario import Ui_MainWindow

lista_questao = []
lista_resp = []
lista_resp_quest7 = []

class Questionario(QMainWindow):
    def __init__(self, *args, **argvs):
        super(Questionario,self).__init__(*args, **argvs)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        #############################################################
        #Botão iniciar Questionário 
        self.ui.btnIniciarQuest.clicked.connect(lambda: self.ui.Paginas.setCurrentWidget(self.ui.Questao1Fase1))
        #############################################################

        #############################################################
        #Tela Questão 1 Fase 1
        self.ui.btnNextQuest1Fase1.clicked.connect(self.questao1_fase1)
        #############################################################

        #############################################################
        #Tela Questão 2 Fase 1
        self.ui.btnNextQuest2Fase1.clicked.connect(self.questao2_fase1)
        self.ui.btnBackQuest2Fase1.clicked.connect(self.limpa_questao2_fase1)
        #############################################################

        #############################################################
        #Tela Questão 3 Fase 1
        self.ui.btnNextQuest3Fase1.clicked.connect(self.questao3_fase1)
        self.ui.btnBackQuest3Fase1.clicked.connect(self.limpa_questao3_fase1)
        #############################################################

        #############################################################
        #Tela Questão 4 Fase 1
        self.ui.btnFinishQuest4Fase1.clicked.connect(self.questao4_fase1)
        self.ui.btnBackQuest4Fase1.clicked.connect(self.limpa_questao4_fase1)
        #############################################################

        #############################################################
        #Tela Questão 1 Fase 2
        self.ui.btnNextQuest1Fase2.clicked.connect(self.questao1_fase2)
        #############################################################

        #############################################################
        #Tela Questão 2 Fase 2
        self.ui.btnNextQuest2Fase2.clicked.connect(self.questao2_fase2)
        self.ui.btnBackQuest2Fase2.clicked.connect(self.limpa_questao2_fase2)
        #############################################################

        #############################################################
        #Tela Questão 3 Fase 2
        self.ui.btnNextQuest3Fase2.clicked.connect(self.questao3_fase2)
        self.ui.btnBackQuest3Fase2.clicked.connect(self.limpa_questao3_fase2)
        #############################################################

        #############################################################
        #Tela Questão 4 Fase 2
        self.ui.btnNextQuest4Fase2.clicked.connect(self.questao4_fase2)
        self.ui.btnBackQuest4Fase2.clicked.connect(self.limpa_questao4_fase2)
        #############################################################

        #############################################################
        #Tela Questão 5 Fase 2
        self.ui.btnNextQuest5Fase2.clicked.connect(self.questao5_fase2)
        self.ui.btnBackQuest5Fase2.clicked.connect(self.limpa_questao5_fase2)
        #############################################################

        #############################################################
        #Tela Questão 6 Fase 2
        self.ui.btnNextQuest6Fase2.clicked.connect(self.questao6_fase2)
        self.ui.btnBackQuest6Fase2.clicked.connect(self.limpa_questao6_fase2)
        #############################################################

        #############################################################
        #Tela Questão 7 Fase 2
        self.ui.btnNextQuest7Fase2.clicked.connect(self.questao7_fase2)
        self.ui.btnBackQuest7Fase2.clicked.connect(lambda: self.ui.Paginas.setCurrentWidget(self.ui.Questao6Fase2))
        #############################################################

        #############################################################
        #Tela Questão 8 Fase 2
        self.ui.btnNextQuest8Fase2.clicked.connect(self.questao8_fase2)
        self.ui.btnBackQuest8Fase2.clicked.connect(self.limpa_questao8_fase2)
        #############################################################

        #############################################################
        #Tela Questão 9 Fase 2
        self.ui.btnNextQuest9Fase2.clicked.connect(self.questao9_fase2)
        self.ui.btnBackQuest9Fase2.clicked.connect(self.limpa_questao9_fase2)
        #############################################################

        #############################################################
        #Tela Questão 10 Fase 2
        self.ui.btnFinishQuest10Fase2.clicked.connect(self.questao10_fase2)
        self.ui.btnBackQuest10Fase2.clicked.connect(self.limpa_questao10_fase2)
        #############################################################

    ########################################################################################
    #Questão 1 - Fase 1
    def questao1_fase1(self):
        global lista_questao
        global lista_resp
        resp_fase1_quest1 = None
        self.ui.Paginas.setCurrentWidget(self.ui.Questao2Fase1)
        if self.ui.RespAQuest1Fase1.isChecked():
            resp_fase1_quest1 = self.ui.RespAQuest1Fase1.text()
        elif self.ui.RespBQuest1Fase1.isChecked():
            resp_fase1_quest1 = self.ui.RespBQuest1Fase1.text()
        elif self.ui.RespCQuest1Fase1.isChecked():
            resp_fase1_quest1 = self.ui.RespCQuest1Fase1.text()

        if "Quesão1Fase1" not in lista_questao:
            lista_questao.append("Quesão1Fase1")
            lista_resp.append(resp_fase1_quest1)
    ########################################################################################

    ########################################################################################
    #Limpa questão 2 - Fase 1
    def limpa_questao2_fase1(self):
        global lista_questao
        global lista_resp
        self.ui.Paginas.setCurrentWidget(self.ui.Questao1Fase1)
        lista_questao.pop()
        lista_resp.pop()
    ########################################################################################

    ########################################################################################
    #Questão 2 - Fase 1
    def questao2_fase1(self):
        global lista_questao
        global lista_resp
        resp_fase1_quest2 = None
        self.ui.Paginas.setCurrentWidget(self.ui.Questao3Fase1)
        if self.ui.RespAQuest2Fase1.isChecked():
            resp_fase1_quest2 = self.ui.RespAQuest2Fase1.text()
        elif self.ui.RespBQuest2Fase1.isChecked():
            resp_fase1_quest2 = self.ui.RespBQuest2Fase1.text()
        elif self.ui.RespCQuest2Fase1.isChecked():
            resp_fase1_quest2 = self.ui.RespCQuest2Fase1.text()
        elif self.ui.RespDQuest2Fase1.isChecked():
            resp_fase1_quest2 = self.ui.RespDQuest2Fase1.text()

        if "Quesão2Fase1" not in lista_questao:
            lista_questao.append("Quesão2Fase1")
            lista_resp.append(resp_fase1_quest2)
    ########################################################################################

    ########################################################################################
    #Limpa questão 3 - Fase 1
    def limpa_questao3_fase1(self):
        global lista_questao
        global lista_resp
        self.ui.Paginas.setCurrentWidget(self.ui.Questao2Fase1)
        lista_questao.pop()
        lista_resp.pop()
    ########################################################################################

    ########################################################################################
    #Questão 3 - Fase 1
    def questao3_fase1(self):
        global lista_questao
        global lista_resp
        resp_fase1_quest3 = None
        self.ui.Paginas.setCurrentWidget(self.ui.Questao4Fase1)
        if self.ui.RespAQuest3Fase1.isChecked():
            resp_fase1_quest3 = self.ui.RespAQuest3Fase1.text()
        elif self.ui.RespBQuest3Fase1.isChecked():
            resp_fase1_quest3 = self.ui.RespBQuest3Fase1.text()
        elif self.ui.RespCQuest3Fase1.isChecked():
            resp_fase1_quest3 = self.ui.RespCQuest3Fase1.text()
        elif self.ui.RespDQuest3Fase1.isChecked():
            resp_fase1_quest3 = self.ui.RespDQuest3Fase1.text()

        if "Quesão3Fase1" not in lista_questao:
            lista_questao.append("Quesão3Fase1")
            lista_resp.append(resp_fase1_quest3)
    ########################################################################################
    
    ########################################################################################
    #Limpa questão 4 - Fase 1
    def limpa_questao4_fase1(self):
        global lista_questao
        global lista_resp
        self.ui.Paginas.setCurrentWidget(self.ui.Questao3Fase1)
        lista_questao.pop()
        lista_resp.pop()
    ########################################################################################

    ########################################################################################
    #Questão 4 - Fase 1
    def questao4_fase1(self):
        global lista_questao
        global lista_resp
        resp_fase1_quest4 = None
        self.ui.Paginas.setCurrentWidget(self.ui.Questao1Fase2)
        if self.ui.RespAQuest4Fase1.isChecked():
            resp_fase1_quest4 = self.ui.RespAQuest4Fase1.text()
        elif self.ui.RespBQuest4Fase1.isChecked():
            resp_fase1_quest4 = self.ui.RespBQuest4Fase1.text()
        elif self.ui.RespCQuest4Fase1.isChecked():
            resp_fase1_quest4 = self.ui.RespCQuest4Fase1.text()
        elif self.ui.RespDQuest4Fase1.isChecked():
            resp_fase1_quest4 = self.ui.RespDQuest4Fase1.text()

        if "Quesão4Fase1" not in lista_questao:
            lista_questao.append("Quesão4Fase1")
            lista_resp.append(resp_fase1_quest4)
    ########################################################################################

    ########################################################################################
    #Questão 1 - Fase 2
    def questao1_fase2(self):
        global lista_questao
        global lista_resp
        resp_fase2_quest1 = None
        self.ui.Paginas.setCurrentWidget(self.ui.Questao2Fase2)
        if self.ui.RespAQuest1Fase2.isChecked():
            resp_fase2_quest1 = self.ui.RespAQuest1Fase2.text()
        elif self.ui.RespBQuest1Fase2.isChecked():
            resp_fase2_quest1 = self.ui.RespBQuest1Fase2.text()
        elif self.ui.RespCQuest1Fase2.isChecked():
            resp_fase2_quest1 = self.ui.RespCQuest1Fase2.text()
        elif self.ui.RespDQuest1Fase2.isChecked():
            resp_fase2_quest1 = self.ui.RespDQuest1Fase2.text()

        if "Quesão1Fase2" not in lista_questao:
            lista_questao.append("Quesão1Fase2")
            lista_resp.append(resp_fase2_quest1)
    ########################################################################################

    ########################################################################################
    #Limpa questão 2 - Fase 2
    def limpa_questao2_fase2(self):
        global lista_questao
        global lista_resp
        self.ui.Paginas.setCurrentWidget(self.ui.Questao1Fase1)
        lista_questao.pop()
        lista_resp.pop()
    ########################################################################################

    ########################################################################################
    #Questão 2 - Fase 2
    def questao2_fase2(self):
        global lista_questao
        global lista_resp
        resp_fase2_quest2 = None
        self.ui.Paginas.setCurrentWidget(self.ui.Questao3Fase2)
        if self.ui.RespAQuest2Fase2.isChecked():
            resp_fase2_quest2 = self.ui.RespAQuest2Fase2.text()
        elif self.ui.RespBQuest2Fase2.isChecked():
            resp_fase2_quest2 = self.ui.RespBQuest2Fase2.text()
        elif self.ui.RespCQuest2Fase2.isChecked():
            resp_fase2_quest2 = self.ui.RespCQuest2Fase2.text()
        elif self.ui.RespDQuest2Fase2.isChecked():
            resp_fase2_quest2 = self.ui.RespDQuest2Fase2.text()

        if "Quesão2Fase2" not in lista_questao:
            lista_questao.append("Quesão2Fase2")
            lista_resp.append(resp_fase2_quest2)
    ########################################################################################

    ########################################################################################
    #Limpa questão 3 - Fase 2
    def limpa_questao3_fase2(self):
        global lista_questao
        global lista_resp
        self.ui.Paginas.setCurrentWidget(self.ui.Questao2Fase2)
        lista_questao.pop()
        lista_resp.pop()
    ########################################################################################

    ########################################################################################
    #Questão 3 - Fase 2
    def questao3_fase2(self):
        global lista_questao
        global lista_resp
        resp_fase2_quest3 = None
        self.ui.Paginas.setCurrentWidget(self.ui.Questao4Fase2)
        if self.ui.RespAQuest3Fase2.isChecked():
            resp_fase2_quest3 = self.ui.RespAQuest3Fase2.text()
        elif self.ui.RespBQuest3Fase2.isChecked():
            resp_fase2_quest3 = self.ui.RespBQuest3Fase2.text()
        elif self.ui.RespCQuest3Fase2.isChecked():
            resp_fase2_quest3 = self.ui.RespCQuest3Fase2.text()
        elif self.ui.RespDQuest3Fase2.isChecked():
            resp_fase2_quest3 = self.ui.RespDQuest3Fase2.text()

        if "Quesão3Fase2" not in lista_questao:
            lista_questao.append("Quesão3Fase2")
            lista_resp.append(resp_fase2_quest3)
    ########################################################################################

    ########################################################################################
    #Limpa questão 4 - Fase 2
    def limpa_questao4_fase2(self):
        global lista_questao
        global lista_resp
        self.ui.Paginas.setCurrentWidget(self.ui.Questao3Fase2)
        lista_questao.pop()
        lista_resp.pop()
    ########################################################################################

    ########################################################################################
    #Questão 4 - Fase 2
    def questao4_fase2(self):
        global lista_questao
        global lista_resp
        resp_fase2_quest4 = None
        self.ui.Paginas.setCurrentWidget(self.ui.Questao5Fase2)
        if self.ui.RespAQuest4Fase2.isChecked():
            resp_fase2_quest4 = self.ui.RespAQuest4Fase2.text()
        elif self.ui.RespBQuest4Fase2.isChecked():
            resp_fase2_quest4 = self.ui.RespBQuest4Fase2.text()
        elif self.ui.RespCQuest4Fase2.isChecked():
            resp_fase2_quest4 = self.ui.RespCQuest4Fase2.text()
        elif self.ui.RespDQuest4Fase2.isChecked():
            resp_fase2_quest4 = self.ui.RespDQuest4Fase2.text()

        if "Quesão4Fase2" not in lista_questao:
            lista_questao.append("Quesão4Fase2")
            lista_resp.append(resp_fase2_quest4)
    ########################################################################################

    ########################################################################################
    #Limpa questão 5 - Fase 2
    def limpa_questao5_fase2(self):
        global lista_questao
        global lista_resp
        self.ui.Paginas.setCurrentWidget(self.ui.Questao4Fase2) 
        lista_questao.pop()
        lista_resp.pop()
    ########################################################################################

    ########################################################################################
    #Questão 5 - Fase 2
    def questao5_fase2(self):
        global lista_questao
        global lista_resp
        resp_fase2_quest5 = None
        self.ui.Paginas.setCurrentWidget(self.ui.Questao6Fase2)
        if self.ui.RespAQuest5Fase2.isChecked():
            resp_fase2_quest5 = self.ui.RespAQuest5Fase2.text()
        elif self.ui.RespBQuest5Fase2.isChecked():
            resp_fase2_quest5 = self.ui.RespBQuest5Fase2.text()
        elif self.ui.RespCQuest5Fase2.isChecked():
            resp_fase2_quest5 = self.ui.RespCQuest5Fase2.text()
        elif self.ui.RespDQuest5Fase2.isChecked():
            resp_fase2_quest5 = self.ui.RespDQuest5Fase2.text()

        if "Quesão5Fase2" not in lista_questao:
            lista_questao.append("Quesão5Fase2")
            lista_resp.append(resp_fase2_quest5)
    ########################################################################################

    ########################################################################################
    #Limpa a resposta 6 - Fase 2
    def limpa_questao6_fase2(self):
        global lista_questao
        global lista_resp
        self.ui.Paginas.setCurrentWidget(self.ui.Questao5Fase2)
        lista_questao.pop()
        lista_resp.pop()
    ########################################################################################

    ########################################################################################
    #Questão 6 - Fase 2
    def questao6_fase2(self):
        global lista_questao
        global lista_resp
        resp_fase2_quest6 = None
        self.ui.Paginas.setCurrentWidget(self.ui.Questao7Fase2)
        if self.ui.RespAQuest6Fase2.isChecked():
            resp_fase2_quest6 = self.ui.RespAQuest6Fase2.text()
        elif self.ui.RespBQuest6Fase2.isChecked():
            resp_fase2_quest6 = self.ui.RespBQuest6Fase2.text()
        elif self.ui.RespCQuest6Fase2.isChecked():
            resp_fase2_quest6 = self.ui.RespCQuest6Fase2.text()
        elif self.ui.RespDQuest6Fase2.isChecked():
            resp_fase2_quest6 = self.ui.RespDQuest6Fase2.text()

        if "Quesão6Fase2" not in lista_questao:
            lista_questao.append("Quesão6Fase2")
            lista_resp.append(resp_fase2_quest6)
    ########################################################################################

    def limpa_questao7_fase2(self):
        global lista_questao
        global lista_resp
        self.ui.Paginas.setCurrentWidget(self.ui.Questao2Fase1)
        lista_questao.pop()
        lista_resp.pop()

    ########################################################################################
    #Questão 7 - Fase 2
    def questao7_fase2(self):
        global lista_questao
        global lista_resp
        global lista_resp_quest7
        resp_fase2_quest7_colegas = None
        resp_fase2_quest7_chefes = None
        resp_fase2_quest7_homem = None
        resp_fase2_quest7_mulher = None
        resp_fase2_quest7_subordinado = None
        resp_fase2_quest7_pessoa_esterna = None
        self.ui.Paginas.setCurrentWidget(self.ui.Questao8Fase2)
        if self.ui.RespNAOColQuest7Fase2.isChecked():
            resp_fase2_quest7_colegas = self.ui.RespNAOColQuest7Fase2.text()
        elif self.ui.RespSIMColQuest7Fase2.isChecked():
            resp_fase2_quest7_colegas = self.ui.RespSIMColQuest7Fase2.text()

        if self.ui.RespNAOChefQuest7Fase2.isChecked():
            resp_fase2_quest7_chefes = self.ui.RespNAOChefQuest7Fase2.text()
        elif self.ui.RespSIMChefQuest7Fase2.isChecked():
            resp_fase2_quest7_chefes = self.ui.RespSIMChefQuest7Fase2.text()

        if self.ui.RespNAOHomQuest7Fase2.isChecked():
            resp_fase2_quest7_homem = self.ui.RespNAOHomQuest7Fase2.text()
        elif self.ui.RespSIMHomQuest7Fase2.isChecked():
            resp_fase2_quest7_homem = self.ui.RespSIMHomQuest7Fase2.text()
        
        if self.ui.RespNAOMulQuest7Fase2.isChecked():
            resp_fase2_quest7_mulher = self.ui.RespNAOMulQuest7Fase2.text()
        elif self.ui.RespSIMMulQuest7Fase2.isChecked():
            resp_fase2_quest7_mulher = self.ui.RespSIMMulQuest7Fase2.text()

        if self.ui.RespNAOPessQuest7Fase2.isChecked():
            resp_fase2_quest7_pessoa_esterna = self.ui.RespNAOPessQuest7Fase2.text()
        elif self.ui.RespSIMPessQuest7Fase2.isChecked():
            resp_fase2_quest7_pessoa_esterna = self.ui.RespSIMPessQuest7Fase2.text()

        if self.ui.RespNAOSubQuest7Fase2.isChecked():
            resp_fase2_quest7_subordinado = self.ui.RespNAOSubQuest7Fase2.text()
        elif self.ui.RespSIMSubQuest7Fase2.isChecked():
            resp_fase2_quest7_subordinado = self.ui.RespSIMSubQuest7Fase2.text()


        if "Quesão7Fase2" not in lista_questao:
            #lista_questao.append("Quesão7Fase2")
            lista_resp_quest7.append(resp_fase2_quest7_colegas)
            lista_resp_quest7.append(resp_fase2_quest7_chefes)
            lista_resp_quest7.append(resp_fase2_quest7_homem)
            lista_resp_quest7.append(resp_fase2_quest7_mulher)
            lista_resp_quest7.append(resp_fase2_quest7_subordinado)
            lista_resp_quest7.append(resp_fase2_quest7_pessoa_esterna)
    ########################################################################################

    ########################################################################################
    #Limpa a resposta 8 - Fase 2
    def limpa_questao8_fase2(self):
        global lista_questao
        global lista_resp
        self.ui.Paginas.setCurrentWidget(self.ui.Questao7Fase2)
        lista_questao.pop()
        lista_resp.pop()
    ########################################################################################

    ########################################################################################
    #Questão 8 - Fase 2
    def questao8_fase2(self):
        global lista_questao
        global lista_resp
        resp_fase2_quest8 = None
        self.ui.Paginas.setCurrentWidget(self.ui.Questao9Fase2)
        if self.ui.RespAQuest8Fase2.isChecked():
            resp_fase2_quest8 = self.ui.RespAQuest8Fase2.text()
        elif self.ui.RespBQuest8Fase2.isChecked():
            resp_fase2_quest8 = self.ui.RespBQuest8Fase2.text()
        elif self.ui.RespCQuest8Fase2.isChecked():
            resp_fase2_quest8 = self.ui.RespCQuest8Fase2.text()
        elif self.ui.RespDQuest8Fase2.isChecked():
            resp_fase2_quest8 = self.ui.RespDQuest8Fase2.text()

        if "Quesão8Fase2" not in lista_questao:
            lista_questao.append("Quesão8Fase2")
            lista_resp.append(resp_fase2_quest8)
    ########################################################################################

    ########################################################################################
    #Limpa a resposta 9 - Fase 2
    def limpa_questao9_fase2(self):
        global lista_questao
        global lista_resp
        self.ui.Paginas.setCurrentWidget(self.ui.Questao8Fase2)
        lista_questao.pop()
        lista_resp.pop()
    ########################################################################################    

    ########################################################################################
    #Questão 9 - Fase 2
    def questao9_fase2(self):
        global lista_questao
        global lista_resp
        resp_fase2_quest9 = None
        self.ui.Paginas.setCurrentWidget(self.ui.Questao10Fase2)
        if self.ui.RespAQuest9Fase2.isChecked():
            resp_fase2_quest9 = self.ui.RespAQuest9Fase2.text()
        elif self.ui.RespBQuest9Fase2.isChecked():
            resp_fase2_quest9 = self.ui.RespBQuest9Fase2.text()

        if "Quesão9Fase2" not in lista_questao:
            lista_questao.append("Quesão9Fase2")
            lista_resp.append(resp_fase2_quest9) 
    ########################################################################################

    ########################################################################################
    #Limpa a resposta 10 - Fase 2
    def limpa_questao10_fase2(self):
        global lista_questao
        global lista_resp
        self.ui.Paginas.setCurrentWidget(self.ui.Questao9Fase2) 
        lista_questao.pop()
        lista_resp.pop()
    ########################################################################################

    ########################################################################################
    #Questão 10 - Fase 2
    def questao10_fase2(self):
        global lista_questao
        global lista_resp
        global lista_resp_quest7
        resp_fase2_quest10 = None
        if self.ui.RespAQuest10Fase2.isChecked():
            resp_fase2_quest10 = self.ui.RespAQuest10Fase2.text()
        elif self.ui.RespBQuest10Fase2.isChecked():
            resp_fase2_quest10 = self.ui.RespBQuest10Fase2.text()
        elif self.ui.RespCQuest10Fase2.isChecked():
            resp_fase2_quest10 = self.ui.RespCQuest10Fase2.text()
        elif self.ui.RespDQuest10Fase2.isChecked():
            resp_fase2_quest10 = self.ui.RespDQuest10Fase2.text()

        if "Quesão10Fase2" not in lista_questao:
            lista_questao.append("Quesão10Fase2")
            lista_resp.append(resp_fase2_quest10)
        
        print("Final")
        print(lista_questao)
        print(lista_resp)
        
        msg = QMessageBox.question(QMessageBox(), "AVISO!!!", "Desja Finalizar o Questionário ?", QMessageBox.Yes | QMessageBox.No)

        if msg == QMessageBox.Yes:
            self.ui.Paginas.setCurrentWidget(self.ui.Introducao)
            y = 1
            for x in lista_questao:
                resposta = lista_resp[y-1]
                resposta = resposta[3:]
                Resposta.insert_resposta(resposta, y)
                y = y + 1
    
            for z in lista_resp_quest7:
                resposta = z
                Resposta.insert_resposta(resposta, 14)

            lista_questao.clear()
            lista_resp_quest7.clear()
            lista_resp.clear()
        else:
            pass
    ########################################################################################

