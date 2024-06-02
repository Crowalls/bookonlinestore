from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import Book, Order, OrderItem, db

order_bp = Blueprint('order', __name__, template_folder='../templates')

@order_bp.route('/order_confirmation', methods=['GET'])
@login_required
def order_confirmation():
    cart_items = []
    books = Book.query.all()
    return render_template('order_confirmation.html', cart_items=cart_items, books=books)

@order_bp.route('/order_confirmation', methods=['POST'])
@login_required
def submit_order():
    address = request.form['address']
    payment_method = request.form['payment']

    # 获取购物车项目及其数量
    cart_items = []
    for key in request.form.keys():
        if key.startswith('quantity-'):
            book_id = int(key.split('-')[1])
            quantity = int(request.form[key])
            if quantity > 0:
                cart_items.append({'book': Book.query.get(book_id), 'quantity': quantity})

    # 创建新订单
    order = Order(user_id=current_user.id, address=address, payment_method=payment_method)
    db.session.add(order)
    db.session.commit()

    # 添加订单项目
    for item in cart_items:
        order_item = OrderItem(order_id=order.id, book_id=item['book'].id, quantity=item['quantity'])
        db.session.add(order_item)

    db.session.commit()
    flash('订单提交成功', 'success')
    return redirect(url_for('order.order_confirmation'))
