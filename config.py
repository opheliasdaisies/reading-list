import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://localhost/reading_list'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CSRF_ENABLED = True
