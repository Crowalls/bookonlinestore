from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from models import db, CartItem, Book

cart_bp = Blueprint('cart', __name__, template_folder='../templates')

@cart_bp.route('/')
@login_required
def view_cart():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    cart_list = [{
        'id': item.id,
        'book_id': item.book_id,
        'title': item.book.title,
        'quantity': item.quantity
    } for item in cart_items]
    return jsonify(cart_list)

@cart_bp.route('/add', methods=['POST'])
@login_required
def add_to_cart():
    data = request.json
    book = Book.query.get(data['book_id'])
    if book:
        cart_item = CartItem.query.filter_by(user_id=current_user.id, book_id=book.id).first()
        if cart_item:
            cart_item.quantity += 1
        else:
            cart_item = CartItem(user_id=current_user.id, book_id=book.id, quantity=1)
            db.session.add(cart_item)
        db.session.commit()
        return '', 201
    return '', 404

@cart_bp.route('/remove/<int:cart_item_id>', methods=['DELETE'])
@login_required
def remove_from_cart(cart_item_id):
    cart_item = CartItem.query.get(cart_item_id)
    if cart_item:
        db.session.delete(cart_item)
        db.session.commit()
        return '', 204
    return '', 404
