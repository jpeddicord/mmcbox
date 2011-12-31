from flask import g, request, session
from flask import render_template, redirect, flash
from flask.ext.login import login_required, login_user, logout_user, current_user

from mmc import app
from mmc.util import templated


@app.route('/')
@login_required
def index():
    pass


@app.route('/login')
@templated()
def login():
    return None


@app.route('/logout')
def logout():
    pass


@app.route('/account/password', methods=['GET', 'POST'])
@templated()
def change_password():
    pass


@app.route('/account/activate')
@templated()
def activate():
    # read activation code
    # wipe activation (on POST)
    # flash warning
    # redirect to password change page
    pass


@app.route('/site/<domain>/')
def browse_files(domain):
    pass


@app.route('/site/<domain>/upload', methods=['POST'])
def upload_file(domain):
    pass


@app.route('/site/<domain>/delete', methods=['POST'])
def delete_file(domain):
    pass


@app.route('/site/<domain>/rename', methods=['POST'])
def rename_file(domain):
    pass
