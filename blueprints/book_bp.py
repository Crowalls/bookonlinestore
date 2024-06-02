from flask import Blueprint, render_template
from flask_login import login_required
from models import Book

book_bp = Blueprint('book', __name__, template_folder='../templates')

@book_bp.route('/books', methods=['GET'])
@login_required
def books():
    all_books = Book.query.all()
    return render_template('book_detail.html', books=all_books)

@book_bp.route('/book/<int:book_id>', methods=['GET'])
@login_required
def book_detail(book_id):
    book = Book.query.get_or_404(book_id)
    return render_template('book_detail.html', book=book)
