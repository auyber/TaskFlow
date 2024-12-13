# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Inicializar a instância do banco de dados e do login
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    # Criar a instância do Flask
    app = Flask(__name__)
    
    # Configurações do aplicativo
    app.config['SECRET_KEY'] = 'your_secret_key'  # Alterar para uma chave secreta segura
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # Alterar para o URI do seu banco de dados

    # Inicializar o banco de dados e o login
    db.init_app(app)
    login_manager.init_app(app)

    # Definir o user_loader
    from app.models import User  # Importação da classe User dentro da função create_app
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))  # Retorna o usuário com base no ID da sessão

    # Importar as rotas dentro da função para evitar importação circular
    from app.routes import init_routes
    init_routes(app)

    app.config['DEBUG'] = True

    return app
