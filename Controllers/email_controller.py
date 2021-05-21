from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import requests
from DataBase import db_book_rating_emails

db_book_rating_emails = db_book_rating_emails.DataBase()
import auth_controller
from flask import jsonify
from bson.objectid import ObjectId

SENDER = "livroparatodxs@outlook.com"
PASSWORD = "zFD9L2Y@bRt5"

""" Camada que faz a conexão com o sistema de envio de emails
e onde se tem a função de enviar o email
"""


class MailControl:

    def build_email(self, receiver: str, title: str, message: str) -> bool:
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
        lista_id_users = []
        dados_vendas, status = db_book_rating_emails.get_sales_without_rating_email()
        dados_vendas = list(dados_vendas)
        # if status == 200 and len(dados_vendas)>0:
        #     for dict_vendas in dados_vendas:
        #         lista_id_users.append(ObjectId(dict_vendas["id_user"]))

        # lista_id_users = [ObjectId("60a69cd9d8aa0cbd0545d24c"), ObjectId("60a69fcb63feb1663027970a")]
        # dados_pessoais = requests.post(f"http://192.268.0.74:5030/users/list", dict(_id=lista_id_users))
        print(dados_vendas)
        dados_pessoais = {
            "users": [
                {
                    "email": "yuripiffer@hotmail.com",
                    "first_name": "gAAAAABgppgE6uwh38jLP2rrl7pjEZ5PTmj-zUHmFfNjSPMqS7vB6bdSL6e2lejfb5ptWPwVLt5hJdUClvRo5K7io3VxQPIT_w==",
                    "id": "60a3fb759f5cf6c89b8f22fa"
                },
                {
                    "email": "nadiavhansen@gmail.com",
                    "first_name": "gAAAAABgppgE6uwh38jLP2rrl7pjEZ5PTmj-zUHmFfNjSPMqS7vB6bdSL6e2lejfb5ptWPwVLt5hJdUClvRo5K7io3VxQPIT_w==",
                    "id": "90a34b759f5cf6c89b8f22fb"
                }
            ]
        }

        for venda in dados_vendas:
            for dados_uma_pessoa in dados_pessoais["users"]:
                if venda['id_user'] == dados_uma_pessoa["id"]:
                    email = dados_uma_pessoa["email"]
                    print(email)
                    name = auth_controller.decrypt(dados_uma_pessoa["first_name"], "K22eIoXBwOnMuJL6nRo0GOIZLGNgGa_diB_FJvUa3AY=")
                    if MailControl().build_email(receiver=email,
                                             title= "Avaliação de Produto - Livro para Todxs",
                                             message = self.create_message(name, venda['_id'])):

                        return db_book_rating_emails.update_email_status_to_true(venda['_id'])
                    #TEM QUE PENSAR NO TRY PARA NÃO PARAR A LISTA
    #
    #
    def create_message(self, nome, id_collection_emails):
        message = f"Olá {nome}, clique no link abaixo para avaliar os produtos comprados!." \
                  f"\n\nhttp://localhost:5030/after_sales/load_books/{id_collection_emails}"
        return message


MailControl().send_email_to_user()
