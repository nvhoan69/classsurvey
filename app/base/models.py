from bcrypt import gensalt, hashpw
from flask_login import UserMixin

from app import db, login_manager



ACCESS = {
    'admin': 0,
    'lecturer':1,
    'student':2
}


class User(db.Model, UserMixin):

    __tablename__ = 'user'

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(16, 'utf8mb4_unicode_ci'), nullable=False, unique=True)
    password = db.Column(db.String(255, 'utf8mb4_unicode_ci'), nullable=False)
    role = db.Column(db.Integer, nullable=False)

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]
            if property == 'password':
                value = hashpw(value.encode('utf8'), gensalt())
            setattr(self, property, value)

    def __repr__(self):
        return str(self.username)

    def get_id(self):
        return self.user_id

    def allowed(self, access_level):
        return self.role == ACCESS[access_level]

@login_manager.user_loader
def user_loader(id):
    return User.query.filter_by(user_id=id).first()


@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    user = User.query.filter_by(username=username).first()
    return user if user else None

