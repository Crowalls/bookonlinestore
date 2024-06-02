from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from models import db, CartItem, Book

cart_bp = Blueprint('cart_bp', __name__, template_folder='../templates')

@cart_bp.route('/cart')
@login_required
def view_cart():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    return render_template('cart.html', cart_items=cart_items)

@cart_bp.route('/cart/add/<int:book_id>')
@login_required
def add_to_cart(book_id):
    existing_item = CartItem.query.filter_by(user_id=current_user.id, book_id=book_id).first()
    if existing_item:
        existing_item.quantity += 1
    else:
        new_item = CartItem(user_id=current_user.id, book_id=book_id, quantity=1)
        db.session.add(new_item)
    db.session.commit()
    return redirect(url_for('cart_bp.view_cart'))

@cart_bp.route('/cart/remove/<int:book_id>', methods=['DELETE'])
@login_required
def remove_from_cart(book_id):
    cart_item = CartItem.query.filter_by(user_id=current_user.id, book_id=book_id).first()
    if cart_item:
        db.session.delete(cart_item)
        db.session.commit()
    return '', 204

@cart_bp.route('/cart/checkout', methods=['POST'])
@login_required
def checkout():
    # 结账逻辑
    return redirect(url_for('order_confirmation'))
