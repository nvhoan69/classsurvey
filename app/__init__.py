from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from importlib import import_module
from flask_marshmallow import  Marshmallow

db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()

def register_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)
    ma.init_app(app)

def register_blueprints(app):
    for module_name in ('base', 'admin', 'student_mn', 'survey', 'version',
                        'lecturer_mn', 'test_gv', 'test_sv', 'course'):
        module = import_module('app.{}.routes'.format(module_name))
        app.register_blueprint(module.blueprint)

def configure_database(app):

    @app.before_first_request
    def initialize_database():
        db.create_all()

    @app.teardown_request
    def shutdown_session(exception=None):
        db.session.remove()

def create_app():
    app = Flask(__name__, static_folder='base/static', template_folder='base/templates')
    app.config['SECRET_KEY'] = 'key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://classsurvey:123@localhost:3306/ourdb'

    register_extensions(app)
    register_blueprints(app)
    configure_database(app)

    return app