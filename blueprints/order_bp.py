from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from models import db, Order, OrderItem, Book

order_bp = Blueprint('order', __name__, template_folder='../templates')

@order_bp.route('/orders')
@login_required
def list_orders():
    orders = Order.query.filter_by(user_id=current_user.id).all()
    orders_list = []
    for order in orders:
        order_items = OrderItem.query.filter_by(order_id=order.id).all()
        items = [{
            'title': item.book.title,
            'quantity': item.quantity,
            'price': float(item.price)
        } for item in order_items]
        orders_list.append({
            'id': order.id,
            'items': items,
            'total': float(order.total),
            'status': order.status,
            'created_at': order.created_at.strftime('%Y-%m-%d %H:%M:%S')
        })
    return jsonify(orders_list)

@order_bp.route('/orders/create', methods=['POST'])
@login_required
def create_order():
    data = request.json
    order = Order(user_id=current_user.id, total=Decimal(data['total']), status='Pending')
    db.session.add(order)
    db.session.commit()

    for item in data['items']:
        book = Book.query.get(item['book_id'])
        order_item = OrderItem(order_id=order.id, book_id=book.id, quantity=item['quantity'], price=book.price)
        db.session.add(order_item)

    db.session.commit()
    return '', 201

@order_bp.route('/orders/cancel/<int:order_id>', methods=['POST'])
@login_required
def cancel_order(order_id):
    order = Order.query.get(order_id)
    if order and order.user_id == current_user.id:
        order.status = 'Cancelled'
        db.session.commit()
        return '', 204
    return '', 404
