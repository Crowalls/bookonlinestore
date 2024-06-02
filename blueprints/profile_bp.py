from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, User

profile_bp = Blueprint('profile', __name__, template_folder='../templates')


@profile_bp.route('/profile', methods=['GET'])
@login_required
def profile():
    return render_template('profile.html', user=current_user)


@profile_bp.route('/profile', methods=['POST'])
@login_required
def update_profile():
    username = request.form['username']
    email = request.form['email']
    phone = request.form['phone']

    current_user.username = username
    current_user.email = email
    current_user.phone = phone

    try:
        db.session.commit()
        flash('个人资料更新成功', 'success')
    except:
        db.session.rollback()
        flash('个人资料更新失败，请重试', 'danger')

    return redirect(url_for('profile.profile'))
