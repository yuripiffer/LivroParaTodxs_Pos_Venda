from unittest import mock, TestCase
from DataBase.db_books import Database
from bson.objectid import ObjectId
import json


class TestDatabase(TestCase):

    @mock.patch("DataBase.db_books.Database.books", create=True)
    def test_get_rating_and_total_comments(self, mock_books):
        with mock.patch.object(Database, "__init__", lambda x: None):
            mock_books.find.return_value = [dict(rating=1, comments=["valor_mockado"])]
            self.assertEqual(Database().get_rating_and_total_comments("60a69cd9d8aa0cbd0545d24c"), (1, 1, ['valor_mockado']))
            self.assertEqual(Database().get_rating_and_total_comments(""), ("'' is not a valid ObjectId, it must be a 12-byte input or a 24-character hex "'string', 500))

    @mock.patch("DataBase.db_books.Database.books", create=True)
    def test_insert_book_rating_and_comments(self, mock_books):
        with mock.patch.object(Database, "__init__", lambda x: None):
            mock_books.update_one.return_value.modified_count = 0
            self.assertEqual(Database().insert_book_rating_and_comments("60a69cd9d8aa0fbd0541d24c", 5, ["Olá", "Olá"]), ("Could´t update rating", 400))
            mock_books.update_one.return_value.modified_count = 1
            self.assertEqual(Database().insert_book_rating_and_comments("60a69cd9d8aa0fbd0541d24c", 5, ["Olá", "Olá"]), ("Ok", 200))
            self.assertEqual(Database().insert_book_rating_and_comments("errado", 5, ["Olá", "Olá"]), ("'errado' is not a valid ObjectId, it must be a 12-byte input or a 24-character " 'hex string', 500))

    @mock.patch("DataBase.db_books.Database.books", create=True)
    def test_get_many_books(self, mock_books):
        mock_books.find.return_value = []
        self.assertEqual(Database().get_many_books(["60a69cd9d8aa0fbd0541d24c", "12b69cd9d8aa0fbd0541d24c"]), ('[]', 200))
        self.assertEqual(Database().get_many_books(["errado"]), ("'errado' is not a valid ObjectId, it must be a 12-byte input or a 24-character " 'hex string', 500))

    def test_convert_to_object_id(self):
        self.assertEqual(Database().convert_to_object_id(["60a69cd9d8aa0fbd0541d24c"]), [ObjectId("60a69cd9d8aa0fbd0541d24c")])
