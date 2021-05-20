import requests
from DataBase import db_book_rating_emails
db_book_rating_emails = db_book_rating_emails.DataBase()
from datetime import datetime

""" Camada que vai ser rodada 1x por dia
Chama a api externa de vendas e carrega as vendas do dia anterior numa collection "book_rating_emails"
"""

def automatic_get_sales_from_yesterday():

    #>>>> > > > > > VER ESSAS 3 LINHAS ABAIXO COM O ORLANDO
    today = datetime.today()
    yesterday = today - 1
    dados_vendas = requests.get(f"http://localhost:5001/?????????????-PASSAR-DATA").json()

    query = "["
    for venda in dados_vendas:
        id_order = venda["id"]
        id_user = venda["id_user"]
        id_products = venda["id_products"] # é uma lista

        query += "{" + f"'id_order': '{id_order}', 'id_user': '{id_user}', 'id_products': '{id_products}', 'was_sent': false" + "}, "
    query += " ]"

    db_book_rating_emails.insert_orders_in_book_rating_emails(query)





