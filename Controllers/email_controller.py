from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import requests
from DataBase import db_book_rating_emails
db_book_rating_emails = db_book_rating_emails.DataBase()

SENDER = "livroparatodxs@outlook.com"
PASSWORD = "zFD9L2Y@bRt5"


""" Camada que faz a conexão com o sistema de envio de emails
e onde se tem a função de enviar o email
"""

class MailControl:

    def build_email(self, receiver:str, title:str, message:str) -> bool:
        try:
            msg = MIMEMultipart()
            msg['From'] = SENDER
            msg['To'] = receiver
            msg['Subject'] = title
            msg.attach(MIMEText(message, 'plain'))
            server = smtplib.SMTP('SMTP.office365.com: 587')
            server.starttls()
            server.login(msg['From'], PASSWORD)
            server.sendmail(msg['From'], msg['To'], msg.as_string())
            server.quit()
        except:
            return False
        return True

    def send_email_to_user(self):
        dados_vendas = db_book_rating_emails.get_sales_without_rating_email()
        if dados_vendas[1] == 200:
            if len(dados_vendas[0])>0:
                lista_id_users = []
                for vendas in dados_vendas[0]:
                    lista_id_users.append(vendas["id_user"])

                dados_pessoais = requests.post(f"http://localhost:5030/users/list", data = lista_id_users)

                for venda in dados_vendas[0]:
                    if venda['id_user'] == dados_pessoais['id_user']:
                        email = dados_pessoais['email']
                        nome = dados_pessoais['nome'] #DESCRIPTOGRAFAR O NOME
                        if MailControl().build_email(receiver = email,
                                                       title = "Avaliação de Produto - Livro para Todxs",
                                                       message = f"Olá {nome}, clique no link abaixo "
                                                       f"para avaliar os produtos comprados!."
                                                       f"\n\nhttp://localhost:5030/CRIAR_ROTA/{venda['id']}"):
                            return db_book_rating_emails.update_email_status_to_true(venda['id'])