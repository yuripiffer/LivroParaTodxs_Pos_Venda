from DataBase.db_books import Database
db_books = Database()

""" 
API DE PÓS-VENDA/RATING DO LIVRO
SCRIPT QUE TRATA OS DADOS DE AVALIAÇÃO DO USUÁRIO RECEBIDOS DO FRONT
E CALCULA O NOVO RATING DO LIVRO 
"""

def post_rating_controller(user_vote):
    try:
        user_rating = user_vote["comment"]["user_rating"]
        if user_rating not in [1,2,3,4,5]:
            return "Book rating error", 400
        book_id = user_vote["book_id"]
        if len(book_id) != 24:
            return "invalid book_id length", 400
        
        actual_rating, n_comments, comments = db_books.get_rating_and_total_comments(book_id)       

        new_rating = calculate_new_rating(user_rating, actual_rating, n_comments)
        general_comments = add_user_comment_to_general_comments(user_vote["comment"], comments)

        response = db_books.insert_book_rating_and_comments(book_id, new_rating, general_comments)
        return response
    except Exception as error:
        return str(error), 500


def calculate_new_rating(user_rating, actual_rating, n_comments):
    new_rating = (actual_rating * n_comments + user_rating)/(n_comments+1)
    return new_rating


def add_user_comment_to_general_comments(user_vote_comment, general_comments):
    general_comments.append(user_vote_comment)
    return general_comments
