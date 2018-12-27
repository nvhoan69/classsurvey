from flask import Blueprint

blueprint = Blueprint(
    'result_blueprint',
    __name__,
    url_prefix='/result',
    template_folder='templates',
    static_folder='static'
)