import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'agrismart-secret-key-2025'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024

    uri = os.environ.get('DATABASE_URL') or 'sqlite:///agrismart.db'
    if uri.startswith('postgres://'):
        uri = uri.replace('postgres://', 'postgresql://', 1)
    SQLALCHEMY_DATABASE_URI = uri