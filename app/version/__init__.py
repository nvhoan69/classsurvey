from flask import Blueprint

blueprint = Blueprint(
    'version_blueprint',
    __name__,
    url_prefix='/version',
    template_folder='templates',
    static_folder='static'
)