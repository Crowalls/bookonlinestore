import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_default_secret_key')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgres://onlinebookstore_db_user:ymqtgnenCJKAXtzLD1RHptyWz6xZ1MAH@dpg-cpe2945ds78s73epafbg-a/onlinebookstore')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
