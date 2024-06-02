import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or '669b6c44271cf431eadd07615af6fd15'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql+psycopg2://onlinebookstore_db_user:yqmtgnenCJKAXtzLD1RHptyWz6xZ1MAH@dpg-cpe2945ds78s73epafbg-a/onlinebookstore_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
