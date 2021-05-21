import requests
from DataBase import db_book_rating_emails
db_book_rating_emails = db_book_rating_emails.DataBase()
import datetime
import json

# retorno_funcao = {
#   "orders": "[\n  {\n    \"_id\": {\n      \"$oid\": \"60a3f9ef9f5cf6c89b8f22f1\"\n    },\n    \"order\": {\n      \"products\": [\n        {\n          \"item_id\": \"60a3f\",\n          \"item_name\": \"Harry Potter e a Camara Secreta Volume I\",\n          \"item_price\": 10,\n          \"item_quantity\": 1\n        },\n        {\n          \"item_id\": \"60a3g\",\n          \"item_name\": \"Percy Jackson e os Olimpianos\",\n          \"item_price\": 5,\n          \"item_quantity\": 2\n        },\n        {\n          \"item_id\": \"60a3h\",\n          \"item_name\": \"Biblia\",\n          \"item_price\": 5,\n          \"item_quantity\": 500\n        }\n      ],\n      \"user\": {\n        \"user_id\": {\n          \"$oid\": \"60a3f9ef9f5cf6c89b8f22f1\"\n        },\n        \"address\": {\n          \"address_state\": \"RJ\"\n        }\n      },\n      \"method\": \"bill\",\n      \"shipping_price\": 30.0,\n      \"total\": 50.0,\n      \"status\": \"waiting bill\",\n      \"bill\": {\n        \"due_date\": \"2021-05-21\",\n        \"documment_date\": \"2021-05-18\",\n        \"value\": 50.0,\n        \"barcode\": \"23700.99999 05182021.143127 36699909765630712916200499955716015823\"\n      },\n      \"message\": \"ok\"\n    },\n    \"created_at\": {\n      \"$date\": 1621342004524\n    },\n    \"updated_at\": \"2021-05-18 12:46:44.524690\"\n  },\n  {\n    \"_id\": {\n      \"$oid\": \"60a3fad49f5cf6c89b8f22f4\"\n    },\n    \"order\": {\n      \"products\": [\n        {\n          \"item_id\": \"60a3f\",\n          \"item_name\": \"Harry Potter e a Camara Secreta Volume I\",\n          \"item_price\": 10,\n          \"item_quantity\": 1\n        },\n        {\n          \"item_id\": \"60a3g\",\n          \"item_name\": \"Percy Jackson e os Olimpianos\",\n          \"item_price\": 5,\n          \"item_quantity\": 2\n        },\n        {\n          \"item_id\": \"60a3h\",\n          \"item_name\": \"Biblia\",\n          \"item_price\": 5,\n          \"item_quantity\": 500\n        }\n      ],\n      \"user\": {\n        \"user_id\": {\n          \"$oid\": \"60a3fad49f5cf6c89b8f22f4\"\n        },\n        \"address\": {\n          \"address_state\": \"RJ\"\n        }\n      },\n      \"shipping_price\": 30.0,\n      \"method\": \"credit\",\n      \"card\": {\n        \"number\": \"344604579207048\",\n        \"month\": \"05\",\n        \"year\": \"2021\",\n        \"cvc\": 336,\n        \"brand\": \"American Express\"\n      },\n      \"total\": 50.0,\n      \"status\": \"paid\",\n      \"message\": \"ok\"\n    },\n    \"created_at\": {\n      \"$date\": 1621342004524\n    },\n    \"updated_at\": \"2021-05-18 12:46:44.524690\"\n  },\n  {\n    \"_id\": {\n      \"$oid\": \"60a3fb079f5cf6c89b8f22f7\"\n    },\n    \"order\": {\n      \"products\": [\n        {\n          \"item_id\": \"60a3f\",\n          \"item_name\": \"Harry Potter e a Camara Secreta Volume I\",\n          \"item_price\": 10,\n          \"item_quantity\": 1\n        },\n        {\n          \"item_id\": \"60a3g\",\n          \"item_name\": \"Percy Jackson e os Olimpianos\",\n          \"item_price\": 5,\n          \"item_quantity\": 2\n        }\n      ],\n      \"user\": {\n        \"user_id\": {\n          \"$oid\": \"60a3fb079f5cf6c89b8f22f7\"\n        },\n        \"address\": {\n          \"address_state\": \"AC\"\n        }\n      },\n      \"shipping_price\": 5000.0,\n      \"method\": \"credit\",\n      \"card\": {\n        \"number\": \"344604579207048\",\n        \"month\": \"05\",\n        \"year\": \"2021\",\n        \"cvc\": 336,\n        \"brand\": \"American Express\"\n      },\n      \"total\": 5020.0,\n      \"status\": \"not paid\",\n      \"message\": \"insufficient credit balance\"\n    },\n    \"created_at\": {\n      \"$date\": 1621342004524\n    },\n    \"updated_at\": \"2021-05-18 12:46:44.524690\"\n  }\n]",
#   "log_message": "ok"
# }

""" Camada que vai ser rodada 1x por dia
Chama a api externa de vendas e carrega as vendas do dia anterior numa collection "book_rating_emails"
"""

def automatic_get_sales_from_yesterday():
    today = datetime.date.today()
    yesterday = datetime.datetime.strptime(str(today - datetime.timedelta(days=1)), '%Y-%m-%d')
    date = {"initial_date": yesterday, "final_date": yesterday}
    #dados_vendas = retorno_funcao
    dados_vendas = requests.post(f"http://127.0.0.1:8000/orders/reports/2", json=date)
    dados_vendas = dados_vendas.json()
    dados_vendas = json.loads(dados_vendas["orders"])

    query=str()
    for venda in dados_vendas:
        id_order = venda["_id"]["$oid"]
        id_user = venda["order"]["user"]["user_id"]["$oid"]
        id_products = []
        for dict_product in venda["order"]["products"]:
            id_products.append(dict_product["item_id"])
        query = "{" + f"'id_order': '{id_order}', 'id_user': '{id_user}', " \
                       f"'id_products': {id_products}, 'was_sent': false" + "}, "
    query = list(query)
    print(query)

    db_book_rating_emails.insert_orders_in_book_rating_emails(query)



#automatic_get_sales_from_yesterday()



