from flask import Blueprint

blueprint = Blueprint(
    'survey_blueprint',
    __name__,
    url_prefix='/survey',
    template_folder='templates',
    static_folder='static'
)