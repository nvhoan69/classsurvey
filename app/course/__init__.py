from flask import Blueprint

blueprint = Blueprint(
    'course_blueprint',
    __name__,
    url_prefix='/course',
    template_folder='templates',
    static_folder='static'
)