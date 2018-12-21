import json

from app.admin import blueprint
from flask import render_template, request, jsonify, redirect, url_for
from flask_login import login_required

from app.base.helpers import requires_access_level

@blueprint.route('/')
@login_required
@requires_access_level('admin')
def index():
    return render_template('index.html')
