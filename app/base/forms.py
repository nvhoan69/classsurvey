from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, HiddenField

## login and registration


class LoginForm(FlaskForm):
    username = TextField('Tài khoản', id='username_login')
    password = PasswordField('Mật khẩu', id='pwd_login')

class AddStudent(FlaskForm):
    id = HiddenField()
    student_code = TextField('MSV/Tài khoản')
    full_name = TextField('Họ và tên')
    vnu_email = TextField('VNU email')
    class_course = TextField('Khóa đào tạo')

class AddLecturer(FlaskForm):
    id = HiddenField()
    username = TextField('Tài khoản')
    full_name = TextField('Họ và tên')
    vnu_email = TextField('VNU email')