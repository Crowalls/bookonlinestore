from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from models import db, User
from werkzeug.security import generate_password_hash

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)

@profile_bp.route('/profile/update', methods=['POST'])
@login_required
def update_profile():
    user = User.query.get(current_user.id)
    user.username = request.form['username']
    user.email = request.form['email']
    if 'password' in request.form and request.form['password']:
        user.password = generate_password_hash(request.form['password'])
    db.session.commit()
    flash('Profile updated successfully', 'success')
    return redirect(url_for('profile.profile'))
