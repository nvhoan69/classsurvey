from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, email

class studentDTO(FlaskForm):
    student_id = IntegerField('Id', validators=[])
    student_code = StringField('MSV/Tài khoản', validators=[DataRequired()])
    full_name = StringField('Họ và tên', validators=[DataRequired()])
    vnu_email = StringField('VNU email', validators=[DataRequired(), email])
    user_id = StringField('user_id', validators=[])

