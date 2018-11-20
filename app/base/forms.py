from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField

## login and registration


class LoginForm(FlaskForm):
    username = TextField('Tài khoản', id='username_login')
    password = PasswordField('Mật khẩu', id='pwd_login')

