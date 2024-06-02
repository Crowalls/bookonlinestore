import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://onlinebookstore_db_user:yqmtgnenCJKAXtzLD1RHptyWz6xZ1MAH@dpg-cpe2945ds78s73epafbg-a:5432/onlinebookstore_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
