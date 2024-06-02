from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import check_password_hash
from models import User

login_bp = Blueprint('login', __name__, template_folder='../templates')


@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('book.books'))  # 重定向到书籍列表页面
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')

    return render_template('login.html')


@login_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login.login'))
