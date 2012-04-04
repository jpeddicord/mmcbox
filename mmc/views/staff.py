from flask import request

from mmc import app, db
from mmc.util import templated, staff_only


@app.route('/staff/users/')
@staff_only
def staff_users():
    pass
