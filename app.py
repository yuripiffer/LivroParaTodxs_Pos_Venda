from flask import Flask, request
from DataBase import db_book_rating_emails
from Controllers import persist_update_rating
from ast import literal_eval

db_emails = db_book_rating_emails.DataBase()

"""
API DE PÓS-VENDA/RATING DO LIVRO
"""

app = Flask(__name__)

@app.route("/after_sales/load_books/<id_book_rating_emails>", methods=['GET'])
def load_books(id_book_rating_emails):
    response = db_emails.get_book_rating_emails_by_id(id_book_rating_emails)
    return response

@app.route("/after_sales/post_rating/", methods=['POST'])
def post_rating():
    user_vote = request.data.decode("utf-8")
    user_vote = literal_eval(user_vote)
    response = persist_update_rating.post_rating_controller(user_vote)
    return response

app.run(debug=True)
