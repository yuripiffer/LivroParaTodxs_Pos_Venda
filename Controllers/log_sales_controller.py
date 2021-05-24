from DataBase import db_book_rating_emails
import requests
import datetime
import json

db_book_rating_emails = db_book_rating_emails.DataBase()

"""ARQUIVO QUE VAI SER RODADO 1X AO DIA
Chama a api externa de vendas e carrega 
as vendas do dia anterior numa collection "book_rating_emails"
"""

def automatic_get_orders_from_yesterday():
    """
    Identifica a data de ontem,
    Carrega por uma API os pedidos de ontem
    Chama uma função para persistir esses dados na collection book_rating_emails
    :return: sem retorno, pois trata-se de uma função automática.
    """
    today = datetime.date.today()
    yesterday = datetime.datetime.strptime(str(today - datetime.timedelta(days=1)), '%Y-%m-%d')
    date = {"initial_date": yesterday, "final_date": yesterday}
    #data_many_sales = retorno_funcao
    data_many_sales = requests.post(f"http://127.0.0.1:8000/orders/reports/2", json=date)
    data_many_sales = data_many_sales.json()
    data_many_sales = json.loads(data_many_sales["orders"])
    persist_orders_in_book_rating_email(data_many_sales)

def persist_orders_in_book_rating_email(data_many_sales):
    """ Constrói a query para persistir os dados dos pedidos do dia anterior.
    :param data_many_sales: dicionário com key 'orders' e values sendo uma lista com vários dics de pedidos
    :return: SEM RETORNO. Persiste os pedidos do dia anterior na collection book_rating_emails
    """
    query=str()
    #REFATORAR CONFORME OS NOMES GERADOS NO RELATÓRIO
    for one_sale in data_many_sales:
        id_order = one_sale["_id"]["$oid"]
        user_id = one_sale["order"]["user"]["user_id"]["$oid"]
        book_id = []
        for dict_product in one_sale["order"]["products"]:
            book_id.append(dict_product["item_id"])
        query = "{" + f"'id_order': '{id_order}', 'user_id': '{user_id}', " \
                       f"'book_id': {book_id}, 'was_sent': false" + "}, "
    query = list(query)
    db_book_rating_emails.insert_orders_in_book_rating_emails(query)


retorno_funcao = {
  "orders": "[\n  {\n    \"_id\": {\n      \"$oid\": \"60a3f9ef9f5cf6c89b8f22f1\"\n    },\n    \"order\": {\n      \"products\": [\n        {\n          \"item_id\": \"60a3f\",\n          \"item_name\": \"Harry Potter e a Camara Secreta Volume I\",\n          \"item_price\": 10,\n          \"item_quantity\": 1\n        },\n        {\n          \"item_id\": \"60a3g\",\n          \"item_name\": \"Percy Jackson e os Olimpianos\",\n          \"item_price\": 5,\n          \"item_quantity\": 2\n        },\n        {\n          \"item_id\": \"60a3h\",\n          \"item_name\": \"Biblia\",\n          \"item_price\": 5,\n          \"item_quantity\": 500\n        }\n      ],\n      \"user\": {\n        \"user_id\": {\n          \"$oid\": \"60a3f9ef9f5cf6c89b8f22f1\"\n        },\n        \"address\": {\n          \"address_state\": \"RJ\"\n        }\n      },\n      \"method\": \"bill\",\n      \"shipping_price\": 30.0,\n      \"total\": 50.0,\n      \"status\": \"waiting bill\",\n      \"bill\": {\n        \"due_date\": \"2021-05-21\",\n        \"documment_date\": \"2021-05-18\",\n        \"value\": 50.0,\n        \"barcode\": \"23700.99999 05182021.143127 36699909765630712916200499955716015823\"\n      },\n      \"message\": \"ok\"\n    },\n    \"created_at\": {\n      \"$date\": 1621342004524\n    },\n    \"updated_at\": \"2021-05-18 12:46:44.524690\"\n  },\n  {\n    \"_id\": {\n      \"$oid\": \"60a3fad49f5cf6c89b8f22f4\"\n    },\n    \"order\": {\n      \"products\": [\n        {\n          \"item_id\": \"60a3f\",\n          \"item_name\": \"Harry Potter e a Camara Secreta Volume I\",\n          \"item_price\": 10,\n          \"item_quantity\": 1\n        },\n        {\n          \"item_id\": \"60a3g\",\n          \"item_name\": \"Percy Jackson e os Olimpianos\",\n          \"item_price\": 5,\n          \"item_quantity\": 2\n        },\n        {\n          \"item_id\": \"60a3h\",\n          \"item_name\": \"Biblia\",\n          \"item_price\": 5,\n          \"item_quantity\": 500\n        }\n      ],\n      \"user\": {\n        \"user_id\": {\n          \"$oid\": \"60a3fad49f5cf6c89b8f22f4\"\n        },\n        \"address\": {\n          \"address_state\": \"RJ\"\n        }\n      },\n      \"shipping_price\": 30.0,\n      \"method\": \"credit\",\n      \"card\": {\n        \"number\": \"344604579207048\",\n        \"month\": \"05\",\n        \"year\": \"2021\",\n        \"cvc\": 336,\n        \"brand\": \"American Express\"\n      },\n      \"total\": 50.0,\n      \"status\": \"paid\",\n      \"message\": \"ok\"\n    },\n    \"created_at\": {\n      \"$date\": 1621342004524\n    },\n    \"updated_at\": \"2021-05-18 12:46:44.524690\"\n  },\n  {\n    \"_id\": {\n      \"$oid\": \"60a3fb079f5cf6c89b8f22f7\"\n    },\n    \"order\": {\n      \"products\": [\n        {\n          \"item_id\": \"60a3f\",\n          \"item_name\": \"Harry Potter e a Camara Secreta Volume I\",\n          \"item_price\": 10,\n          \"item_quantity\": 1\n        },\n        {\n          \"item_id\": \"60a3g\",\n          \"item_name\": \"Percy Jackson e os Olimpianos\",\n          \"item_price\": 5,\n          \"item_quantity\": 2\n        }\n      ],\n      \"user\": {\n        \"user_id\": {\n          \"$oid\": \"60a3fb079f5cf6c89b8f22f7\"\n        },\n        \"address\": {\n          \"address_state\": \"AC\"\n        }\n      },\n      \"shipping_price\": 5000.0,\n      \"method\": \"credit\",\n      \"card\": {\n        \"number\": \"344604579207048\",\n        \"month\": \"05\",\n        \"year\": \"2021\",\n        \"cvc\": 336,\n        \"brand\": \"American Express\"\n      },\n      \"total\": 5020.0,\n      \"status\": \"not paid\",\n      \"message\": \"insufficient credit balance\"\n    },\n    \"created_at\": {\n      \"$date\": 1621342004524\n    },\n    \"updated_at\": \"2021-05-18 12:46:44.524690\"\n  }\n]",
  "log_message": "ok"
}

automatic_get_orders_from_yesterday()



