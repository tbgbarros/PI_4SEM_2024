
from flask import Blueprint, render_template, redirect, url_for, flash,session
from app.forms import SignupForm, LoginForm

bp = Blueprint('main', __name__,template_folder='templates/main')

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/principal')
def principal():
    if 'username' in session:
        return render_template('main/principal.html')
    else:
        flash('Você precisa fazer login para acessar esta página.', 'warning')
        return redirect(url_for('auth.login'))
