from flask import Blueprint

blueprint = Blueprint(
    'ad_lecturer_blueprint',
    __name__,
    url_prefix='/admin',
    template_folder='templates',
    static_folder='static'
)