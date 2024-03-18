from flask import render_template, redirect, url_for, flash
from core import app, db  # Importando o objeto app e db
from core.models.model import User
from core.forms import RegistrationForm, LoginForm
import os

# Rota para página inicial
@app.route('/')
def home():
     print("Acessando a página principal")
     return render_template('index.html')

# Rota para cadastro de usuário
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Cadastro realizado com sucesso!', 'success')
        return redirect(url_for('login'))
    return render_template('cadastro.html', form=form)

# Rota para login de usuário
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Usuário ou senha incorretos. Tente novamente.', 'error')
    return render_template('login.html', form=form)
