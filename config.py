import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')  # Fetch the secret key from the .env file
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///site.db')  # Fetch database URI from the .env file or use default SQLite
    SQLALCHEMY_TRACK_MODIFICATIONS = False
