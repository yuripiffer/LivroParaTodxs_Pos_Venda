from bson.objectid import ObjectId
from DataBase import db_books
import pymongo
import pandas as pd
import json

db_books  = db_books.Database()


class DataBase:

    def __init__(self):
        """
        Esta função init faz a conexão com banco de dados e gera a collection
        """
        try:
            self.conn = pymongo.MongoClient("mongodb+srv://system:t7TRSmoJnO1DeZUa@cluster0.bawny."
                                            "mongodb.net/myFirstDatabase?retryWrites=true&w=majority",
                                            ssl=True, ssl_cert_reqs='CERT_NONE')
            self.db = self.conn["database_teste"]
            self.bre = self.db["book_rating_emails"]
        except:
            raise Exception("Failed to connect with the TestDataBase, check your string connection!!")

    def get_sales_without_rating_email(self):
        try:
            response = self.bre.find({"was_sent": False})
            return response, 200
        except:
            return "Error: Could not connect", 500

    def insert_orders_in_book_rating_emails(self, query):
        self.bre.insert_many(query)

    def get_book_rating_emails_by_id(self, id_book_rating_emails):
        try:
            item_book_rating_emails = self.bre.find({"_id": ObjectId(id_book_rating_emails)})
            list_id_books = list(item_book_rating_emails)[0]['book_id']
            dict_books_and_status = db_books.get_many_books(list_id_books)
            return dict_books_and_status
        except Exception as error:
            return str(error.args[0]), 500

    def update_email_status_to_true(self, id_books_rating_emails):
        self.bre.update_one({"_id": id_books_rating_emails}, {"$set": {"was_sent": True}})


resultado = DataBase().bre.find({"was_sent": False})
print(pd.DataFrame(resultado))

DataBase().insert_orders_in_book_rating_emails([{'order_id':'60a3fb079f5cf6c89b8f22f7'}, {'order_id':'60a3fb079f5cf6c89b8f22f7'}])