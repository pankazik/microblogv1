import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret123'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://demo:demo@localhost/demo'
    SQLALCHEMY_TRACK_MODIFICATIONS = False