from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, HiddenField

from wtforms import StringField, IntegerField, DateTimeField, PasswordField, DateField
from wtforms.validators import DataRequired, Email

from wtforms.fields.html5 import EmailField

## login and registration


class LoginForm(FlaskForm):
    username = TextField('Tài khoản', id='username_login')
    password = PasswordField('Mật khẩu', id='pwd_login')

class AddStudent(FlaskForm):
    id = HiddenField()
    student_code = StringField('MSV/Tài khoản', validators=[DataRequired()])
    full_name = StringField('Họ và tên', validators=[DataRequired()])
    vnu_email = EmailField('VNU email', [DataRequired(), Email()])
    class_course = StringField('Khóa đào tạo', validators=[DataRequired()])

class AddLecturer(FlaskForm):
    id = HiddenField()
    username = TextField('Tài khoản', validators=[DataRequired()])
    full_name = TextField('Họ và tên', validators=[DataRequired()])
    vnu_email = EmailField('VNU email', [DataRequired(), Email()])

class EditCourse(FlaskForm):
    id = HiddenField()
    course_code = TextField('Mã môn học', validators=[DataRequired()])
    name = TextField('Tên môn học', validators=[DataRequired()])

class EditSurvey(FlaskForm):
    id = HiddenField()
    survey_title = TextField('Tiêu đề', validators=[DataRequired()])

class EditVersion(FlaskForm):
    id = HiddenField()
    name = TextField('Tên mẫu', validators=[DataRequired()])