from DataBase.db_books import Database
db_books = Database()


def post_rating_controller(user_vote):
    try:
        user_rating = user_vote["user_rating"]
        id_book = user_vote["id_book"]
        actual_rating, n_comments, comments = db_books.get_rating_and_total_comments(id_book)
        new_rating = calculate_new_rating(user_rating, actual_rating, n_comments)
        general_comments = add_user_comment_to_general_comments(user_vote["comment"], comments)
        response = db_books.insert_book_rating_and_comments(id_book, new_rating, general_comments)
        return response
    except:
        return Exception, 400


def calculate_new_rating(user_rating, actual_rating, n_comments):
    new_rating = (actual_rating * n_comments + user_rating)/(n_comments+1)
    return new_rating


def add_user_comment_to_general_comments(user_vote_comment, general_comments):
    general_comments.append(user_vote_comment)
    return general_comments
