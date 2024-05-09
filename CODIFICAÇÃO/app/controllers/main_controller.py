
from flask import Blueprint, render_template, redirect, url_for, flash
from app.forms import SignupForm, LoginForm

bp = Blueprint('main', __name__,template_folder='templates/main')

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/principal')
def principal():
    return render_template('main/principal.html')
