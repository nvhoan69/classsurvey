from flask import Blueprint

blueprint = Blueprint(
    'student_mn_blueprint',
    __name__,
    url_prefix='/student_mn',
    template_folder='templates',
    static_folder='static'
)