from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, HiddenField

## login and registration


class LoginForm(FlaskForm):
    username = TextField('Tài khoản', id='username_login')
    password = PasswordField('Mật khẩu', id='pwd_login')

class AddStudent(FlaskForm):
    student_id = HiddenField()
    student_code = TextField('MSV/Tài khoản')
    full_name = TextField('Họ và tên')
    vnu_email = TextField('VNU email')
    khoa = TextField('Khóa đào tạo')

class AddLecturer(FlaskForm):
    lecturer_id = HiddenField()
    account = TextField('Tài khoản')
    full_name = TextField('Họ và tên')
    vnu_email = TextField('VNU email')