from flask import Flask, redirect, url_for, render_template
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config
from models import db, User
from werkzeug.security import generate_password_hash

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate = Migrate(app, db)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login.login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.before_first_request
    def create_tables():
        db.create_all()
        create_admin_account()

    def create_admin_account():
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(username='admin', password=generate_password_hash('admin123'), email='admin@example.com')
            db.session.add(admin)
            db.session.commit()

    from blueprints import register_bp, login_bp, book_bp, cart_bp, profile_bp, order_bp, admin_bp

    app.register_blueprint(register_bp, url_prefix='/')
    app.register_blueprint(login_bp, url_prefix='/')
    app.register_blueprint(book_bp, url_prefix='/')
    app.register_blueprint(cart_bp, url_prefix='/cart')
    app.register_blueprint(profile_bp, url_prefix='/')
    app.register_blueprint(order_bp, url_prefix='/')
    app.register_blueprint(admin_bp, url_prefix='/admin')

    @app.route('/')
    def main():
        return redirect(url_for('index'))

    @app.route('/index')
    def index():
        return render_template('index.html')

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
