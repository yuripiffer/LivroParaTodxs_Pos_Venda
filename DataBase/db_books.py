import json
from json.encoder import JSONEncoder
from pymongo import MongoClient
from bson.objectid import ObjectId
from pymongo.errors import ConnectionFailure
import config

"""
API DE PÓS-VENDA/RATING DO LIVRO
CAMADA DE CONEXÃO COM A COLLECTION DE LIVROS (PRODUTOS)
"""


class Database:

    def __init__(self):
        self.conn = MongoClient(config.URL_CLUSTER, ssl=True, ssl_cert_reqs='CERT_NONE')
        self.db = self.conn[config.database_mongo]
        self.search_history = self.db[config.collection_search_history]
        self.new_books = self.db[config.collection_books]

    def get_rating_and_total_comments(self, id_book):
        try:
            book_info = list(self.new_books.find({"_id": ObjectId(id_book)}))
            actual_rating = book_info[0]["rating"]
            comments = book_info[0]["comments"]
            n_comments = len(comments)
            return actual_rating, n_comments, comments
        except ConnectionFailure as ex:
            return ex.args[0], 500

    def insert_book_rating_and_comments(self, id_book, new_rating, general_comments):
        try:
            response = self.new_books.update_one({"_id": ObjectId(id_book)}, {
                "$set": {"rating": new_rating, "comments": general_comments}}).modified_count
            if response:
                return "Ok", 200
            return "Could´t update rating", 400
        except ConnectionFailure as ex:
            return ex.args[0], 500

    def get_many_books(self, list_id_books):
        try:
            book_info = list(self.new_books.find({'_id':{'$in': self.convert_to_object_id(list_id_books)}}))
            for i in range(len(book_info)):
                book_info[i]['_id'] = str(book_info[i]['_id'])
            return json.dumps(book_info), 200
        except Exception as error:
            return str(error.args[0]), 500

    def convert_to_object_id(self, list_id_books):
        list_objectid_books = []
        for id in list_id_books:
            list_objectid_books.append(ObjectId(id))
        return list_objectid_books

