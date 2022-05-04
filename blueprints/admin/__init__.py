from flask import Blueprint, render_template
from flask_login import login_user
from flask_login import logout_user, current_user
from passlib.hash import argon2
import uuid

bp_admin = Blueprint('bp_admin', __name__)


@bp_admin.get('/admin')
def admin_get():
    return render_template('admin.html')
