from bson.objectid import ObjectId
from DataBase import db_books
import config
import pymongo

db_books = db_books.Database()

"""
API DE PÓS-VENDA/RATING DO LIVRO
CAMADA DE CONEXÃO COM A COLLECTION DE CONTROLE DOS EMAILS (A SEREM) ENVIADOS AO USER
PARA AVALIAÇÃO DOS LIVROS
"""


class DataBase:

    def __init__(self):
        try:
            self.conn = pymongo.MongoClient(config.URL_CLUSTER, ssl=True, ssl_cert_reqs='CERT_NONE')
            self.db = self.conn[config.database_mongo]
            self.bre = self.db[config.collection_book_rating_emails]
        except:
            raise Exception("Failed to connect with the TestDataBase, check your string connection!!")

    def get_sales_without_rating_email(self):
        """
        Retorna as vendas do dia anterior para inserir na collection
        de envio de email para os compradores avaliarem o livro
        """
        try:
            response = self.bre.find({"was_sent": False})
            return response, 200
        except:
            return "Error: Could not connect", 500

    def insert_orders_in_book_rating_emails(self, query):
        self.bre.insert_many(query)

    def get_book_rating_emails_by_id(self, id_book_rating_emails):
        """
        :param id_book_rating_emails: id da collection de emails a serem enviados para os users
        :return: json dos livros de uma compra e statuscode
        """
        try:
            item_book_rating_emails = self.bre.find({"_id": ObjectId(id_book_rating_emails)})
            list_id_books = list(item_book_rating_emails)[0]['book_id']
            dict_books_and_status = db_books.get_many_books(list_id_books)
            return dict_books_and_status
        except Exception as error:
            return str(error.args[0]), 500

    def update_email_status_to_true(self, id_books_rating_emails):
        """ Caso o email referente à uma compra tenha sido enviado, transforma
        a coluna "was_sent" de false para true para não ser enviado novamente.
        """
        self.bre.update_one({"_id": id_books_rating_emails}, {"$set": {"was_sent": True}})
