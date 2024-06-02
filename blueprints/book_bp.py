from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required
from models import db, Book
from decimal import Decimal

book_bp = Blueprint('book_detail.html', __name__, template_folder='../templates')

@book_bp.route('/books')
@login_required
def list_books():
    books = Book.query.all()
    books_list = [{
        'id': book.id,
        'title': book.title,
        'author': book.author,
        'price': float(book.price),
        'description': book.description,
        'stock': book.stock,
        'cover_image': book.cover_image
    } for book in books]
    return jsonify(books_list)

@book_bp.route('/books/add', methods=['POST'])
@login_required
def add_book():
    data = request.json
    new_book = Book(
        title=data['title'],
        author=data['author'],
        price=Decimal(data['price']),
        description=data['description'],
        stock=data['stock'],
        cover_image=data.get('cover_image')
    )
    db.session.add(new_book)
    db.session.commit()
    return '', 201

@book_bp.route('/books/edit/<int:book_id>', methods=['POST'])
@login_required
def edit_book(book_id):
    data = request.json
    book = Book.query.get(book_id)
    if book:
        book.title = data['title']
        book.author = data['author']
        book.price = Decimal(data['price'])
        book.description = data['description']
        book.stock = data['stock']
        book.cover_image = data['cover_image']
        db.session.commit()
        return '', 204
    return '', 404

@book_bp.route('/books/delete/<int:book_id>', methods=['DELETE'])
@login_required
def delete_book(book_id):
    book = Book.query.get(book_id)
    if book:
        db.session.delete(book)
        db.session.commit()
        return '', 204
    return '', 404
