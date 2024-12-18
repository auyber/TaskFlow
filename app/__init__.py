from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
import os  # To generate a random secret key

# Initialize the database instance, login, and Migrate
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

def create_app():
    # Create the Flask instance
    app = Flask(__name__)

    # App configurations
    app.config['SECRET_KEY'] = os.urandom(24)  # Generating a random secret key
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # Database path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable SQLAlchemy modification tracking

    # Initialize the database, login, and Flask-Migrate
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)  # Initializing Migrate with the app and db

    # Define the user_loader
    from app.models import User  # Importing the User class inside the create_app function
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))  # Returns the user based on the session ID

    # Import routes inside the function to avoid circular import
    from app.routes import init_routes
    init_routes(app)

    app.config['DEBUG'] = False  # Debug configuration

    return app
