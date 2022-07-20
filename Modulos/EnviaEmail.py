import win32com.client as win32
from BD.classes import Token

class EnviaEmail:
    def enviar_email(email_colab, nome_colab, nome_empresa):
        outlook = win32.Dispatch("outlook.application")

        #Token do Colaborador
        token = Token.token_email()

        #Cria o Email
        email = outlook.CreateItem(0)

        #Informçaões do email
        email.To = email_colab
        email.Subject = "Scanawe"
        email.HTMLBody = f"""<p>Olá {nome_colab},</p> 
            <p>A Empresa {nome_empresa} juntamente com nós da Scanawe desenvolvemos um</p>
            <p>questionário para detectarmos possíveis problemas de assédio no local de</p>
            <p>trabalho.</p>
            <br>
            <p>Estamos te enviando um Token de acesso que garantirá seu anonimato ao</p>
            <p>responder o questionário.</p>
            <br>
            <b>Token: {token}</b>
            <br>
            <br>
            <p>A Empresa {nome_empresa} entrará em contato para os próximos passos.</p>
            <br>
            <br>
            <br>
            <p>Atenciosamente,</p>
            <p>Scanawe.</p>"""
        #Envia o Email
        email.Send()