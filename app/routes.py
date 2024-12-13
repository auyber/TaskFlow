from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, current_user, logout_user
from app import db
from app.models import User
from werkzeug.security import check_password_hash, generate_password_hash
from .forms import LoginForm, RegistrationForm

def init_routes(app):

    # Rota da página inicial (index) - Protegida, só acessível se autenticado
    @app.route('/index')
    @login_required
    def index():
        return render_template('index.html')

    # Rota de login
    @app.route('/', methods=['GET', 'POST'])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('index'))

        form = LoginForm()
        
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('index'))
            else:
                flash("Credenciais incorretas, tente novamente.", "error")
        return render_template('login.html', form=form)

    # Rota de registro de usuário
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if current_user.is_authenticated:
            return redirect(url_for('index'))

        form = RegistrationForm()
        
        if form.validate_on_submit():
            username = form.username.data
            email = form.email.data
            password = form.password.data

            # Verificar se o nome de usuário ou email já estão cadastrados
            existing_user = User.query.filter_by(username=username).first()
            existing_email = User.query.filter_by(email=email).first()

            if existing_user:
                flash("Nome de usuário já cadastrado!", "error")
                return redirect(url_for('register'))
            elif existing_email:
                flash("Email já cadastrado!", "error")
                return redirect(url_for('register'))

            # Criação do novo usuário
            hashed_password = generate_password_hash(password, method='sha256')
            new_user = User(username=username, email=email, password=hashed_password)

            db.session.add(new_user)
            db.session.commit()

            login_user(new_user)
            return redirect(url_for('index'))

        return render_template('register.html', form=form)

    # Rota de logout
    @app.route('/logout')
    @login_required
    def logout():
        logout_user()  # Realiza o logout do usuário
        return redirect(url_for('login'))  # Redireciona para a página de login após o logout
