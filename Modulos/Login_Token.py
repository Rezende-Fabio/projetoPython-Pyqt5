from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.Qt import Qt
from PyQt5.QtCore import pyqtSlot
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtPrintSupport import *
import os, sys

from Templates.Login_Token import Ui_Dialog
from Modulos.Login_User import LoginUser
from Modulos.Questionario import Questionario
from BD.classes import Token

class LoginToken(QDialog):
    def __init__(self, *args, **argvs):
        super(LoginToken,self).__init__(*args, **argvs)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        #############################################################
        #Botões da tela
        self.ui.buttonLogin.clicked.connect(self.login_token) 
        self.ui.btnToken.clicked.connect(self.menu)
        #############################################################
    

    def login_token(self):
        #Exibe a tela de login para Gestores e Cosultores
        self.window = LoginUser()
        self.window.show()
        LoginToken.hide(self)

    def menu(self):
        #Valida o Token e exibe a tela do questionário
        token = self.ui.inputUsuario.text()
        respValid = Token.valida_token(token)
        if len(token) == 0:
            msg = QMessageBox.information(QMessageBox(), "AVISO!!!", "Preencha o Campo")
        elif respValid:
            self.window = Questionario()
            self.window.show()
            LoginToken.hide(self)
        else:
            msg = QMessageBox.information(QMessageBox(), "AVISO!!!", "Token inesistete")
            self.ui.inputUsuario.clear()

    