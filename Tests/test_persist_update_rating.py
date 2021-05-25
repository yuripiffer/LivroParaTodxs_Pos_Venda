from unittest import mock, TestCase
from Controllers import persist_update_rating as pur



class TestPersistUpdate(TestCase):

    @mock.patch("Controllers.persist_update_rating")
    @mock.patch("Controllers.persist_update_rating.Database")
    def test_post_rating_controller(self, mock_database, mock_persist_update):
        # self.assertEqual(pur.post_rating_controller(dict(comment=dict(user_rating=6))), ('Book rating error', 400))
        # self.assertEqual(pur.post_rating_controller(dict(comment=dict(user_rating=3), book_id="tests")), ("invalid book_id length", 400))

        mock_database.get_rating_and_total_comments.return_value = 1
        # mock_persist_update.calculate.new.rating.return_value = 1
        # mock_persist_update.add_user_comment_to_general_comments.return_value = [""]
        # mock_database.insert_book_rating_and_comments.return_value = ""

        self.assertEqual(pur.post_rating_controller("60a69cd9d8aa0cbd0545d24c"), "")


