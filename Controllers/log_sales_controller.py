from DataBase import db_book_rating_emails
from datetime import datetime, timedelta
import requests
import json


db_book_rating_emails = db_book_rating_emails.DataBase()

""" 
API DE PÓS-VENDA/RATING DO LIVRO
SCRIPT QUE COLETA O LOG DE VENDAS DO DIA ANTERIOR E PERSISTE NA COLLECTION 
DE EMAILS PARA ENVIAR AO USER
"""


def automatic_get_orders_from_yesterday():
    """
    Identifica a data de ontem,
    Carrega por uma API os pedidos de ontem
    Chama uma função para persistir esses dados na collection book_rating_emails
    :return: sem retorno, pois trata-se de uma função automática.
    """    
    
    yesterday = datetime.now() - timedelta(1)
    yesterday = datetime.strftime(yesterday, '%Y-%m-%d')    
    date = {"initial_date": yesterday, "final_date": yesterday}
    headers = {'content-type': 'application/json', 'Key': "eadc34b8d3d1463097e6df66dfabd462"}
    data_many_sales = requests.post("http://192.168.0.80:8000/orders/reports/2", json=date, headers=headers).json()     
    data_many_sales = json.loads(data_many_sales["orders"])    
    persist_orders_in_book_rating_email(data_many_sales)

def persist_orders_in_book_rating_email(data_many_sales):
    """ Constrói a query para persistir os dados dos pedidos do dia anterior.
    :param data_many_sales: dicionário com key 'orders' e values sendo uma lista com vários dics de pedidos
    :return: SEM RETORNO. Persiste os pedidos do dia anterior na collection book_rating_emails
    """
    query=str()
    list_query = []

    for one_sale in data_many_sales:
        id_order = one_sale["_id"]["$oid"]
        user_id = one_sale['order']["user"]["user_id"]
        book_id = []
        for dict_product in one_sale["order"]["products"]:
            book_id.append(dict_product["item_id"])
        query = {'id_order': id_order, 'user_id': user_id, 'book_id': book_id, 'was_sent': False} 
        list_query.append(query)               
    db_book_rating_emails.insert_orders_in_book_rating_emails(list_query)
    
