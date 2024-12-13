# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate  # Importar Flask-Migrate

# Inicializar a instância do banco de dados, do login e do Migrate
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()  # Inicializar o Migrate

def create_app():
    # Criar a instância do Flask
    app = Flask(__name__)
    
    # Configurações do aplicativo
    app.config['SECRET_KEY'] = 'your_secret_key'  # Alterar para uma chave secreta segura
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # Alterar para o URI do seu banco de dados

    # Inicializar o banco de dados, o login e o Flask-Migrate
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)  # Inicializando o Migrate com a app e o db

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
