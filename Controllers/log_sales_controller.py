from DataBase import db_book_rating_emails
import requests
from datetime import datetime, timedelta
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
    print(date)

    data_many_sales = requests.post("http://192.168.0.61:8000/orders/reports/2", json=date).json() # headers={"access-key": "eadc34b8d3d1463097e6df66dfabd462"},
    print(data_many_sales)
    data_many_sales = json.loads(data_many_sales["orders"])
    persist_orders_in_book_rating_email(data_many_sales)

def persist_orders_in_book_rating_email(data_many_sales):
    """ Constrói a query para persistir os dados dos pedidos do dia anterior.
    :param data_many_sales: dicionário com key 'orders' e values sendo uma lista com vários dics de pedidos
    :return: SEM RETORNO. Persiste os pedidos do dia anterior na collection book_rating_emails
    """
    query=str()
    # O PESSOAL DE VENDAS TÁ TENDO PROBLEMA... ESPERAR DELES
    for one_sale in data_many_sales:
        id_order = one_sale["_id"]
        user_id = one_sale["user"]["user_id"]
        book_id = []
        for dict_product in one_sale["order"]["products"]:
            book_id.append(dict_product["item_id"])
        query = "{" + f"'id_order': '{id_order}', 'user_id': '{user_id}', " \
                       f"'book_id': {book_id}, 'was_sent': false" + "}, "
    query = list(query)
    db_book_rating_emails.insert_orders_in_book_rating_emails(query)

automatic_get_orders_from_yesterday()








# retorno_funcao = {
#   "orders": "[\n  {\n    \"_id\": {\n      \"$oid\": \"60a3f9ef9f5cf6c89b8f22f1\"\n    },\n    \"order\": {\n      \"products\": [\n        {\n          \"item_id\": \"60a3f\",\n          \"item_name\": \"Harry Potter e a Camara Secreta Volume I\",\n          \"item_price\": 10,\n          \"item_quantity\": 1\n        },\n        {\n          \"item_id\": \"60a3g\",\n          \"item_name\": \"Percy Jackson e os Olimpianos\",\n          \"item_price\": 5,\n          \"item_quantity\": 2\n        },\n        {\n          \"item_id\": \"60a3h\",\n          \"item_name\": \"Biblia\",\n          \"item_price\": 5,\n          \"item_quantity\": 500\n        }\n      ],\n      \"user\": {\n        \"user_id\": {\n          \"$oid\": \"60a3f9ef9f5cf6c89b8f22f1\"\n        },\n        \"address\": {\n          \"address_state\": \"RJ\"\n        }\n      },\n      \"method\": \"bill\",\n      \"shipping_price\": 30.0,\n      \"total\": 50.0,\n      \"status\": \"waiting bill\",\n      \"bill\": {\n        \"due_date\": \"2021-05-21\",\n        \"documment_date\": \"2021-05-18\",\n        \"value\": 50.0,\n        \"barcode\": \"23700.99999 05182021.143127 36699909765630712916200499955716015823\"\n      },\n      \"message\": \"ok\"\n    },\n    \"created_at\": {\n      \"$date\": 1621342004524\n    },\n    \"updated_at\": \"2021-05-18 12:46:44.524690\"\n  },\n  {\n    \"_id\": {\n      \"$oid\": \"60a3fad49f5cf6c89b8f22f4\"\n    },\n    \"order\": {\n      \"products\": [\n        {\n          \"item_id\": \"60a3f\",\n          \"item_name\": \"Harry Potter e a Camara Secreta Volume I\",\n          \"item_price\": 10,\n          \"item_quantity\": 1\n        },\n        {\n          \"item_id\": \"60a3g\",\n          \"item_name\": \"Percy Jackson e os Olimpianos\",\n          \"item_price\": 5,\n          \"item_quantity\": 2\n        },\n        {\n          \"item_id\": \"60a3h\",\n          \"item_name\": \"Biblia\",\n          \"item_price\": 5,\n          \"item_quantity\": 500\n        }\n      ],\n      \"user\": {\n        \"user_id\": {\n          \"$oid\": \"60a3fad49f5cf6c89b8f22f4\"\n        },\n        \"address\": {\n          \"address_state\": \"RJ\"\n        }\n      },\n      \"shipping_price\": 30.0,\n      \"method\": \"credit\",\n      \"card\": {\n        \"number\": \"344604579207048\",\n        \"month\": \"05\",\n        \"year\": \"2021\",\n        \"cvc\": 336,\n        \"brand\": \"American Express\"\n      },\n      \"total\": 50.0,\n      \"status\": \"paid\",\n      \"message\": \"ok\"\n    },\n    \"created_at\": {\n      \"$date\": 1621342004524\n    },\n    \"updated_at\": \"2021-05-18 12:46:44.524690\"\n  },\n  {\n    \"_id\": {\n      \"$oid\": \"60a3fb079f5cf6c89b8f22f7\"\n    },\n    \"order\": {\n      \"products\": [\n        {\n          \"item_id\": \"60a3f\",\n          \"item_name\": \"Harry Potter e a Camara Secreta Volume I\",\n          \"item_price\": 10,\n          \"item_quantity\": 1\n        },\n        {\n          \"item_id\": \"60a3g\",\n          \"item_name\": \"Percy Jackson e os Olimpianos\",\n          \"item_price\": 5,\n          \"item_quantity\": 2\n        }\n      ],\n      \"user\": {\n        \"user_id\": {\n          \"$oid\": \"60a3fb079f5cf6c89b8f22f7\"\n        },\n        \"address\": {\n          \"address_state\": \"AC\"\n        }\n      },\n      \"shipping_price\": 5000.0,\n      \"method\": \"credit\",\n      \"card\": {\n        \"number\": \"344604579207048\",\n        \"month\": \"05\",\n        \"year\": \"2021\",\n        \"cvc\": 336,\n        \"brand\": \"American Express\"\n      },\n      \"total\": 5020.0,\n      \"status\": \"not paid\",\n      \"message\": \"insufficient credit balance\"\n    },\n    \"created_at\": {\n      \"$date\": 1621342004524\n    },\n    \"updated_at\": \"2021-05-18 12:46:44.524690\"\n  }\n]",
#   "log_message": "ok"
# }

    #data_many_sales = retorno_funcao


# for one_sale in data_many_sales:
#     id_order = one_sale["_id"]["$oid"]
#     user_id = one_sale["order"]["user"]["user_id"]["$oid"]
#     book_id = []
#     for dict_product in one_sale["order"]["products"]:
#         book_id.append(dict_product["item_id"])
#     query = "{" + f"'id_order': '{id_order}', 'user_id': '{user_id}', " \
#                   f"'book_id': {book_id}, 'was_sent': false" + "}, "
# query = list(query)