from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from DataBase import db_book_rating_emails
from Controllers import auth_controller
from bson.objectid import ObjectId
import config
import smtplib
import requests
db_book_rating_emails = db_book_rating_emails.DataBase()

""" 
API DE PÓS-VENDA/RATING DO LIVRO
ENVIO DE EMAIL PARA O USER
O EMAIL REDIRECIONA AO FRONT, ONDE ELE FAZ A AVALIAÇÃO
"""


class MailControl:

    def build_email(self, receiver: str, title: str, message: str) -> bool:
        try:
            msg = MIMEMultipart()
            msg['From'] = config.SENDER
            msg['To'] = receiver
            msg['Subject'] = title
            msg.attach(MIMEText(message, 'plain'))
            server = smtplib.SMTP('SMTP.office365.com: 587')
            server.starttls()
            server.login(msg['From'], config.PASSWORD)
            server.sendmail(msg['From'], msg['To'], msg.as_string())
            server.quit()
        except:
            return False
        return True

    def send_email_to_user(self):
        """
        Carrega as orders que não receberam email de pos-venda em data_many_sales,
        Cria uma lista dos users de cada order em list_users_ids
        Coleta os dados desses users pela API externa por post de list_users_ids
        Para cada venda:
            carrega o email do user,
            nome (que é descriptografado)
        Constrói o email e envia para o user de cada order.
        :return: Transforma o coluna "was_sent" de book_rating_emails de False para True
        """
        list_users_ids = []
        data_many_sales, status = db_book_rating_emails.get_sales_without_rating_email()
        data_many_sales = list(data_many_sales)
        if status == 200 and len(data_many_sales)>0:
            for dict_sales in data_many_sales:
                list_users_ids.append(ObjectId(dict_sales["user_id"]))

        data_many_users = requests.post(f"http://192.268.0.74:5030/users/list", dict(_id=list_users_ids))

        for data_one_sale in data_many_sales:
            print("data_one_sale", data_one_sale)
            for data_one_user in data_many_users["users"]:
                if data_one_sale['user_id'] == data_one_user["id"]:
                    email = data_one_user["email"]
                    print("email", email)
                    name = auth_controller.decrypt(data_one_user["first_name"], config.CRYPT_KEY)
                    if MailControl().build_email(receiver=email, title="Avaliação de Produto - Livro para Todxs",
                                             message=self.create_message(name, data_one_sale['_id'])):

                        return db_book_rating_emails.update_email_status_to_true(data_one_sale['_id'])

    def create_message(self, name, id_collection_emails):
        """
        Construção da mensagem a ser enviada no email
        :param name: primeiro nome do cliente
        :param id_collection_emails: _id do log de envio de emails na collection "book_rating_emails"
        :return: corpo do email
        """
        message = f"Olá {name}! De 1 a 5, que nota você daria para o(s) livro(s) que comprou?" \
                  f"Saiba que a sua opinião é muito importante para nós e para nossa comunidade de leitores. " \
                  f"Que tal fazer uma avaliação e mostrar sua opinião?" \
                  f"Clique no link abaixo para avaliar os produtos comprados:" \
                  f"\n\nhttp://localhost:5030/after_sales/load_books/{id_collection_emails}" \
                  f"\nConte sempre conosco!" \
                  f"Equipe LIVRO PARA TODXS"
        return message


MailControl().send_email_to_user()














###list_users_ids = [ObjectId("60a69cd9d8aa0cbd0545d24c"), ObjectId("60a69fcb63feb1663027970a")]

# data_many_users = {
#     "users": [
#         {
#             "email": "yuripiffer@hotmail.com",
#             "first_name": "gAAAAABgppgE6uwh38jLP2rrl7pjEZ5PTmj-zUHmFfNjSPMqS7vB6bdSL6e2lejfb5ptWPwVLt5hJdUClvRo5K7io3VxQPIT_w==",
#             "id": "60a3fb759f5cf6c89b8f22fa"
#         },
#         {
#             "email": "nadiavhansen@gmail.com",
#             "first_name": "gAAAAABgppgE6uwh38jLP2rrl7pjEZ5PTmj-zUHmFfNjSPMqS7vB6bdSL6e2lejfb5ptWPwVLt5hJdUClvRo5K7io3VxQPIT_w==",
#             "id": "90a34b759f5cf6c89b8f22fb"
#         }
#     ]
# }