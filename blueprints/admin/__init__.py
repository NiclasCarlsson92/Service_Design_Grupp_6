from flask import Blueprint, render_template

bp_admin = Blueprint('bp_admin', __name__)


@bp_admin.get('/admin')
def admin_get():
    return render_template('admin.html')
