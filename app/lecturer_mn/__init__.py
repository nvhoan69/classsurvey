from flask import Blueprint

blueprint = Blueprint(
    'lecturer_mn_blueprint',
    __name__,
    url_prefix='/lecturer_mn',
    template_folder='templates',
    static_folder='static'
)