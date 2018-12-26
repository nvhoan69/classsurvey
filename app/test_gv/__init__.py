from flask import Blueprint

blueprint = Blueprint(
    'lecturer_blueprint',
    __name__,
    url_prefix='/lecturer',
    template_folder='templates',
    static_folder='static'
)