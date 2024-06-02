from flask import Blueprint, render_template, jsonify, request, redirect, url_for
from flask_login import login_required, current_user
from models import db, CartItem, Book

cart_bp = Blueprint('cart', __name__, template_folder='../templates')

@cart_bp.route('/')
@login_required
def cart_page():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    cart_books = []
    for item in cart_items:
        book = Book.query.get(item.book_id)
        cart_books.append({
            'book': book,
            'quantity': item.quantity
        })
    return render_template('cart.html', cart_items=cart_books)

@cart_bp.route('/items')
@login_required
def cart_items():
    items = CartItem.query.filter_by(user_id=current_user.id).all()
    items_list = [{
        'book_id': item.book_id,
        'title': item.book.title,
        'author': item.book.author,
        'price': float(item.book.price),
        'quantity': item.quantity
    } for item in items]
    return jsonify(items_list)

@cart_bp.route('/remove/<int:book_id>', methods=['DELETE'])
@login_required
def remove_cart_item(book_id):
    item = CartItem.query.filter_by(user_id=current_user.id, book_id=book_id).first()
    if item:
        db.session.delete(item)
        db.session.commit()
        return '', 204
    return '', 404

@cart_bp.route('/checkout', methods=['POST'])
@login_required
def checkout():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    if not cart_items:
        return redirect(url_for('cart.cart_page'))

    return render_template('order_confirmation.html', cart_items=cart_items)
