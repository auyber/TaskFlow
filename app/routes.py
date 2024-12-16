from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, current_user, logout_user
from app import db
from app.models import User, Task, QuickThought
from werkzeug.security import check_password_hash, generate_password_hash
from .forms import LoginForm, RegistrationForm, QuickThoughtForm, TaskForm

def init_routes(app):
    # Filtro customizado para 'yesno'
    @app.template_filter('yesno')
    def yesno_filter(value):
        return "Concluída" if value else "Não concluída"

    # Página inicial
    @app.route('/index')
    @login_required
    def index():
        return render_template('index.html')

    # Login
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

    # Registro de usuários
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

    # Tarefas
    @app.route('/tasks', methods=['GET', 'POST'])
    @login_required
    def tasks():
        user_tasks = Task.query.filter_by(user_id=current_user.id).all()
        form = TaskForm()

        # Se o formulário for enviado, tratamos a edição
        if form.validate_on_submit():
            task_id = request.form.get('task_id')
            task = Task.query.get_or_404(task_id)
            task.title = form.title.data
            task.description = form.description.data
            db.session.commit()

            flash("Tarefa editada com sucesso!", "edit_task_success")
            return redirect(url_for('tasks'))  # Volta para a página de tarefas

        return render_template('tasks.html', tasks=user_tasks, form=form)

    @app.route('/task/create', methods=['GET', 'POST'])
    @login_required
    def create_task():
        form = TaskForm()

        if form.validate_on_submit():
            title = form.title.data
            description = form.description.data

            new_task = Task(title=title, description=description, user_id=current_user.id)
            db.session.add(new_task)
            db.session.commit()

            flash("Tarefa criada com sucesso!", "create_task_success")
            return redirect(url_for('create_task'))  # Mantém o usuário na página atual

        return render_template('create_task.html', form=form)

    @app.route('/task/edit/<int:task_id>', methods=['GET', 'POST'])
    @login_required
    def edit_task(task_id):
        task = Task.query.get_or_404(task_id)
        if task.user_id != current_user.id:
            abort(403)  # Usuário não autorizado a editar esta tarefa

        form = TaskForm()

        if form.validate_on_submit():
            task.title = form.title.data
            task.description = form.description.data
            db.session.commit()

            flash("Tarefa editada com sucesso!", "edit_task_success")
            return redirect(url_for('tasks'))  # Redireciona para a página de tarefas após edição

        # Preenche o formulário com os dados da tarefa para edição
        form.title.data = task.title
        form.description.data = task.description
        return render_template('tasks.html', form=form, task=task)

    # Deletar tarefas
    @app.route('/task/delete/<int:task_id>', methods=['POST'])
    @login_required
    def delete_task(task_id):
        task = Task.query.get_or_404(task_id)

        if task.user_id != current_user.id:
            flash("Você não tem permissão para excluir essa tarefa.", "danger")
            return redirect(url_for('tasks'))

        db.session.delete(task)
        db.session.commit()

        flash("Tarefa excluída com sucesso!", "delete_task_success")
        return redirect(url_for('tasks'))  # Redireciona para a página de tarefas após exclusão

    # Pensamentos Rápidos
    @app.route('/quick-thought', methods=['GET', 'POST'])
    @login_required
    def quick_thought():
        form = QuickThoughtForm()
        editing_thought_id = request.args.get('edit', type=int)

        if form.validate_on_submit() and not editing_thought_id:
            content = form.content.data
            new_thought = QuickThought(content=content, user_id=current_user.id)
            db.session.add(new_thought)
            db.session.commit()
            flash("Pensamento adicionado com sucesso!", "success")
            return redirect(url_for('quick_thought'))

        thoughts = QuickThought.query.filter_by(user_id=current_user.id).all()
        return render_template('quick_thought.html', form=form, thoughts=thoughts, editing_thought_id=editing_thought_id)


    @app.route('/quick-thought/edit/<int:thought_id>', methods=['POST'])
    @login_required
    def edit_thought(thought_id):
        thought = QuickThought.query.get_or_404(thought_id)
        if thought.user_id != current_user.id:
            flash("Você não tem permissão para editar este pensamento.", "error")
            return redirect(url_for('quick_thought'))

        content = request.form.get('content')
        if content:
            thought.content = content
            db.session.commit()
            flash("Pensamento atualizado com sucesso!", "success")
        return redirect(url_for('quick_thought'))


    @app.route('/quick-thought/delete/<int:thought_id>', methods=['POST'])
    @login_required
    def delete_thought(thought_id):
        thought = QuickThought.query.get_or_404(thought_id)
        if thought.user_id != current_user.id:
            flash("Você não tem permissão para excluir este pensamento.", "error")
            return redirect(url_for('quick_thought'))

        db.session.delete(thought)
        db.session.commit()
        flash("Pensamento excluído com sucesso!", "success")
        return redirect(url_for('quick_thought'))


    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('login'))
