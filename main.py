from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import *
from PyQt5.QtPrintSupport import *
import sys
from Modulos.Login_Token import LoginToken
from BD.schema import Conexao

#Inicia a Aplicação
app = QApplication(sys.argv)
if (QDialog.Accepted == True):
    db = Conexao()
    #Conexao.creatDb(db)
    Conexao.connect(db)
    #Conexao.table(db)
    window = LoginToken()
    window.show()
sys.exit(app.exec_())