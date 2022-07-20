from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.Qt import Qt
from PyQt5.QtCore import pyqtSlot
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtPrintSupport import *
import os, sys

from Templates.Login_User import Ui_Dialog
from Modulos.Dashboard_Gestor import MenuGestor
from Modulos.Dashboard_Consultor import MenuConsultor
from BD.classes import *
from BD.schema import Conexao


class LoginUser(QDialog):
    def __init__(self, *args, **argvs):
        super(LoginUser,self).__init__(*args, **argvs)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        #############################################################
        #Botão entrar
        self.ui.btnEntrar.clicked.connect(self.login)
        #############################################################

    def login(self):
        #Valida Login, e exibe a tela de cordo com as permições do usúario
        login = self.ui.inputUsuario.text().upper()
        pssd = self.ui.inputSenha.text().upper()
        resp = Login.valida_login(login, pssd)
        if resp[0] == True:
            permissao = Login.valida_permissao(resp[1])
            if permissao[0] == 1:
                self.window = MenuConsultor(resp[3])
                self.window.show()
                LoginUser.hide(self)
            else:
                self.window = MenuGestor(resp[2], resp[3])
                self.window.show()
                LoginUser.hide(self)
        else:
            msg = QMessageBox.information(QMessageBox(), "AVISO!!!", "Login\\Senha Incorreto!")
            self.ui.inputSenha.clear()
            self.ui.inputUsuario.clear()
    

