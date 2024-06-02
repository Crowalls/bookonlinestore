from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from models import db, User

# 创建一个蓝图对象
profile_bp = Blueprint('profile', __name__)

# 个人资料页面路由，GET 请求
@profile_bp.route('/profile', methods=['GET'])
@login_required
def profile():
    return render_template('profile.html', user=current_user)

# 更新个人资料路由，POST 请求
@profile_bp.route('/profile/update_profile', methods=['POST'])
@login_required  # 确保用户已登录
def update_profile():
    # 获取表单中的数据
    username = request.form.get('username')
    email = request.form.get('email')
    phone = request.form.get('phone')

    # 更新当前用户信息
    user = User.query.get(current_user.id)
    user.username = username
    user.email = email
    user.phone = phone

    # 提交到数据库
    db.session.commit()
    flash('Profile updated successfully', 'success')
    return redirect(url_for('profile.profile'))
