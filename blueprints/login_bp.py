from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from models import db, User
from werkzeug.security import check_password_hash

login_bp = Blueprint('login', __name__, template_folder='../templates')

@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('profile.profile'))
        else:
            flash('登录失败，请检查用户名和密码', 'danger')
    return render_template('login.html')

@login_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('你已经成功退出', 'success')
    return redirect(url_for('login.login'))
