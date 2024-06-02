from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash
from models import db, User

register_bp = Blueprint('register', __name__, template_folder='../templates')

@register_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        phone = request.form['phone']

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('用户名已存在', 'danger')
            return redirect(url_for('register.register'))

        new_user = User(
            username=username,
            password=generate_password_hash(password),
            email=email,
            phone=phone
        )
        db.session.add(new_user)
        db.session.commit()
        flash('注册成功，请登录', 'success')
        return redirect(url_for('login.login'))

    return render_template('register.html')
