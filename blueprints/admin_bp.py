from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from models import db, User, Book, Order, OrderItem
from werkzeug.security import check_password_hash
from ai_chat import chat_with_openai
import logging
from decimal import Decimal

admin_bp = Blueprint('admin', __name__, template_folder='../templates')

logging.basicConfig(level=logging.DEBUG)

@admin_bp.route('/admin_login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        admin = User.query.filter_by(username=username).first()
        if admin and check_password_hash(admin.password, password):
            login_user(admin)
            return redirect(url_for('admin.home'))
        else:
            flash('登录失败，请检查用户名和密码', 'danger')
    return render_template('admin_login.html')

@admin_bp.route('/admin_logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('admin.login'))

@admin_bp.route('/admin_home')
@login_required
def home():
    return render_template('admin_home.html')

@admin_bp.route('/admin/book_management')
@login_required
def book_management():
    return render_template('book_management.html')

@admin_bp.route('/admin/book_management/list')
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

@admin_bp.route('/admin/book_management/add', methods=['POST'])
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

@admin_bp.route('/admin/book_management/edit/<int:book_id>', methods=['POST'])
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

@admin_bp.route('/admin/book_management/delete/<int:book_id>', methods=['DELETE'])
@login_required
def delete_book(book_id):
    book = Book.query.get(book_id)
    if book:
        db.session.delete(book)
        db.session.commit()
        return '', 204
    return '', 404

@admin_bp.route('/chat_with_ai', methods=['POST'])
@login_required
def chat():
    data = request.json
    text = data.get('text')
    response = chat_with_openai(text)
    return jsonify({'response': response})

@admin_bp.route('/admin/order_management')
@login_required
def order_management():
    orders = Order.query.all()
    return render_template('order_management.html', orders=orders)

@admin_bp.route('/admin/order_management/list')
@login_required
def list_orders():
    orders = Order.query.all()
    orders_list = []
    for order in orders:
        user = User.query.get(order.user_id)
        order_items = OrderItem.query.filter_by(order_id=order.id).all()
        items = [{
            'title': item.book.title,
            'quantity': item.quantity,
            'price': float(item.price)
        } for item in order_items]
        orders_list.append({
            'id': order.id,
            'user': user.username if user else 'Unknown',
            'items': items,
            'total': float(order.total),
            'status': order.status,
            'created_at': order.created_at.strftime('%Y-%m-%d %H:%M:%S')
        })
    return jsonify(orders_list)

@admin_bp.route('/admin/user_management')
@login_required
def user_management():
    users = User.query.all()
    return render_template('user_management.html', users=users)

@admin_bp.route('/admin/edit_user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    user = User.query.get(user_id)
    if request.method == 'POST':
        user.username = request.form['username']
        user.email = request.form['email']
        user.phone = request.form['phone']
        db.session.commit()
        flash('用户信息更新成功', 'success')
        return redirect(url_for('admin.user_management'))
    return render_template('edit_user.html', user=user)

@admin_bp.route('/admin/delete_user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        flash('用户已删除', 'success')
    return redirect(url_for('admin.user_management'))
