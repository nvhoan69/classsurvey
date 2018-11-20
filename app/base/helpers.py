from functools import wraps
from flask import url_for, redirect, session, render_template

from app.base.models import User, ACCESS

def requires_access_level(access_level):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not session.get('level_access'):
                return redirect(url_for('base_blueprint.login'))

            if not access_level == session.get('level_access'):
                return render_template('errors/page_403.html')
            return f(*args, **kwargs)
        return decorated_function
    return decorator


