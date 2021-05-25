from unittest import mock, TestCase
from DataBase.db_book_rating_emails import DataBase


class TestDataBase(TestCase):

    @mock.patch("DataBase.db_book_rating_emails.DataBase.bre", create=True)
    def test_get_sales_without_rating_email(self, mock_bre):
        with mock.patch.object(DataBase, "__init__", lambda x: None):
            mock_bre.find.side_effect = ["retorno_mockado", Exception]
            self.assertEqual(DataBase().get_sales_without_rating_email(), ('retorno_mockado', 200))

            self.assertEqual(DataBase().get_sales_without_rating_email(), ("Error: Could not connect", 500))

    @mock.patch("DataBase.db_book_rating_emails.db_books")
    @mock.patch("DataBase.db_book_rating_emails.DataBase.bre", create=True)
    def test_get_book_rating_emails_by_id(self, mock_bre, mock_books):
        with mock.patch.object(DataBase, "__init__", lambda x: None):
            mock_bre.find.return_value = [dict(book_id="list_id_books_mockado")]
            mock_books.get_many_books.return_value = "valor_mockado"
            self.assertEqual(DataBase().get_book_rating_emails_by_id("60a69cd9d8aa0cbd0545d24c"), "valor_mockado")
            self.assertEqual(DataBase().get_book_rating_emails_by_id(""), ("'' is not a valid ObjectId, it must be a 12-byte input or a 24-character hex " 'string', 500))




