from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(message="O e-mail é obrigatório."),  # Mensagem de erro se o campo estiver vazio
        Email(message="Digite um e-mail válido.")  # Mensagem de erro se o formato for inválido
    ])
    password = PasswordField('Senha', validators=[DataRequired(message="A senha é obrigatória.")])
    submit = SubmitField('Entrar')

class RegistrationForm(FlaskForm):
    username = StringField('Nome de usuário', validators=[
        DataRequired(message="O nome de usuário é obrigatório."), 
        Length(min=2, max=20, message="O nome de usuário deve ter entre 2 e 20 caracteres.")
    ])
    email = StringField('Email', validators=[
        DataRequired(message="O e-mail é obrigatório."), 
        Email(message="Digite um e-mail válido.")
    ])
    password = PasswordField('Senha', validators=[DataRequired(message="A senha é obrigatória.")])
    submit = SubmitField('Cadastrar')

class TaskForm(FlaskForm):
    title = StringField('Título', validators=[DataRequired(message="O título é obrigatório.")])
    description = TextAreaField('Descrição')
    submit = SubmitField('Criar Tarefa')

class QuickThoughtForm(FlaskForm):
    content = TextAreaField('Pensamento Rápido', validators=[DataRequired(message="O conteúdo não pode estar vazio.")])
    submit = SubmitField('Adicionar Pensamento')
