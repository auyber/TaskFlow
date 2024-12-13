from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, current_user, logout_user
from app import db
from app.models import User, Task, QuickThought
from werkzeug.security import check_password_hash, generate_password_hash
from .forms import LoginForm, RegistrationForm

def init_routes(app):
    # Filtro customizado para 'yesno' para tratar valores booleanos
    @app.template_filter('yesno')
    def yesno_filter(value):
        return "Concluída" if value else "Não concluída"
    
    # Rota da página inicial (index)
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
                flash("Usuário ou senha incorretos. Tente novamente.", "error")
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

            existing_user = User.query.filter_by(username=username).first()
            existing_email = User.query.filter_by(email=email).first()

            if existing_user:
                flash("Nome de usuário já cadastrado!", "error")
                return redirect(url_for('register'))
            elif existing_email:
                flash("Email já cadastrado!", "error")
                return redirect(url_for('register'))

            hashed_password = generate_password_hash(password, method='sha256')
            new_user = User(username=username, email=email, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()

            login_user(new_user)
            flash("Cadastro realizado com sucesso!", "success")
            return redirect(url_for('index'))

        return render_template('register.html', form=form)

    # Rota para exibir tarefas do usuário
    @app.route('/tasks', methods=['GET'])
    @login_required
    def tasks():
        user_tasks = Task.query.filter_by(user_id=current_user.id).all()
        return render_template('tasks.html', tasks=user_tasks)

    # Rota para criar uma tarefa
    @app.route('/task/create', methods=['GET', 'POST'])
    @login_required
    def create_task():
        if request.method == 'POST':
            title = request.form['title']
            description = request.form['description']
            if not title:
                flash("O título é obrigatório.", "error")
                return redirect(url_for('create_task'))

            new_task = Task(title=title, description=description, user_id=current_user.id)
            db.session.add(new_task)
            db.session.commit()
            flash("Tarefa criada com sucesso!", "success")
            return redirect(url_for('tasks'))  # Redireciona para a página de tarefas

        return render_template('create_task.html')

    # Rota para editar uma tarefa
    @app.route('/task/edit/<int:task_id>', methods=['GET', 'POST'])
    @login_required
    def edit_task(task_id):
        task = Task.query.get_or_404(task_id)
        if task.user_id != current_user.id:
            flash("Você não tem permissão para editar esta tarefa.", "error")
            return redirect(url_for('tasks'))

        if request.method == 'POST':
            task.title = request.form['title']
            task.description = request.form['description']
            task.completed = 'completed' in request.form
            db.session.commit()
            flash("Tarefa atualizada com sucesso!", "success")
            return redirect(url_for('tasks'))

        return render_template('edit_task.html', task=task)

    # Rota para excluir uma tarefa
    @app.route('/task/delete/<int:task_id>', methods=['POST'])
    @login_required
    def delete_task(task_id):
        task = Task.query.get_or_404(task_id)
        if task.user_id != current_user.id:
            flash("Você não tem permissão para excluir esta tarefa.", "error")
            return redirect(url_for('tasks'))

        db.session.delete(task)
        db.session.commit()
        flash("Tarefa excluída com sucesso!", "success")  # Mensagem flash após exclusão
        return redirect(url_for('tasks'))  # Redireciona para a página de tarefas

    # Rota para adicionar um pensamento rápido
    @app.route('/quick-thought', methods=['GET', 'POST'])
    @login_required
    def quick_thought():
        if request.method == 'POST':
            content = request.form['content']
            if not content:
                flash("O conteúdo não pode estar vazio.", "error")
                return redirect(url_for('quick_thought'))

            new_thought = QuickThought(content=content, user_id=current_user.id)
            db.session.add(new_thought)
            db.session.commit()
            flash("Pensamento adicionado com sucesso!", "success")
            return redirect(url_for('quick_thought'))

        thoughts = QuickThought.query.filter_by(user_id=current_user.id).all()
        return render_template('quick_thought.html', thoughts=thoughts)

    # Rota para fazer logout
    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('login'))
