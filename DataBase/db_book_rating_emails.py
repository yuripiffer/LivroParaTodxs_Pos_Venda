import pymongo
from bson.objectid import ObjectId
from datetime import datetime
from DataBase import db_books
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
        """ CHECAR COM CARINHO AMANHÃ!
        """
        item_book_rating_emails = self.bre.find({"_id": ObjectId(id_book_rating_emails)})
        list_id_books = item_book_rating_emails["id_products"]
        dict_books_and_status = db_books.get_many_books(list_id_books)
        return dict_books_and_status

    def update_email_status_to_true(self, id_books_rating_emails):
        """
        CHECAR COM CARINHO AMANHÃ!
        :param id_books_rating_emails:
        :return:
        """
        self.bre.updateOne({"_id": ObjectId(id_books_rating_emails)}, {"$set": {"was_sent": True}})