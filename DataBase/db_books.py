import json
from json.encoder import JSONEncoder
from pymongo import MongoClient
from bson.objectid import ObjectId
from pymongo.errors import ConnectionFailure


class Database:

    def __init__(self):
        self.conn = MongoClient(
            "mongodb+srv://system:t7TRSmoJnO1DeZUa@cluster0.bawny.mongodb.net/myFirstDatabase?retryWrites=true&w=majority",
            ssl=True, ssl_cert_reqs='CERT_NONE')
        self.db = self.conn["database_teste"]
        self.search_history = self.db["search_history"]
        self.new_books = self.db["new_books"]

    def get_rating_and_total_comments(self, id_book):
        #TALVEZ ADAPTAR ESSAS INFOS COM O CARLOS
        try:
            book_info = list(self.new_books.find({"_id": ObjectId(id_book)}))
            actual_rating = book_info[0]["rating"]
            comments = book_info[0]["comments"]
            n_comments = len(comments)
            return dict(actual_rating=actual_rating, n_comments=n_comments, comments=comments), 200
        except ConnectionFailure as ex:
            return ex.args[0], 500

    def insert_book_rating_and_comments(self, id_book, new_rating, general_comments):
        try:
            response = self.new_books.updateOne({"_id": ObjectId(id_book)}, {
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
