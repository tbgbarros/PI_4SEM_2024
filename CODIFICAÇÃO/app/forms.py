from flask_wtf import FlaskForm  # Importa a classe FlaskForm do módulo flask_wtf
from wtforms import (
    StringField,
    PasswordField,
    BooleanField,
    SubmitField,
)  # Importa os tipos de campos do WTForms
from wtforms.validators import (
    DataRequired,
    Length,
    EqualTo,
)  # Importa os validadores do WTForms


class SignupForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired()]
    )  # Campo para o nome de usuário
    password = PasswordField(
        "Password", validators=[DataRequired(), Length(min=8)]
    )  # Campo para a senha
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )  # Campo para confirmar a senha
    submit = SubmitField("Sign Up")  # Botão de envio para cadastrar


class LoginForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired()]
    )  # Campo para o nome de usuário
    password = PasswordField(
        "Password", validators=[DataRequired()]
    )  # Campo para a senha
    remember_me = BooleanField("Remember Me")  # Opção para lembrar o usuário
    submit = SubmitField("Sign In")  # Botão de envio para fazer login
