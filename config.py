import os

class Config:
    SECRET_KEY = 'your_secret_key'  # Substitua por uma chave secreta segura
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
