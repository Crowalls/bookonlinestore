from app import app, db
from models import User, Book

with app.app_context():
    db.create_all()

    if not User.query.filter_by(username='testuser').first():
        user = User(username='testuser', password='testpassword', email='test@example.com')
        db.session.add(user)
        db.session.commit()

    if not Book.query.filter_by(title='Test Book').first():
        book = Book(title='Test Book', author='Test Author', price=19.99, description='This is a test book.', stock=10,
                    cover_image='/static/image/main.jpg')
        db.session.add(book)
        db.session.commit()
