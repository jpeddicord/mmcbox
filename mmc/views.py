import os
import os.path

from flask import g, request, session
from flask import render_template, redirect, flash
from flask import url_for
from flask.ext.login import login_required, login_user, logout_user, current_user

from mmc import app, db
from mmc.forms import SiteForm
from mmc.models import User, Website
from mmc.util import templated, check_domain


@app.route('/')
@login_required
def index():
    w = Website.query.filter_by(user=current_user).first()
    if w:
        return redirect(w.url())
    else:
        return redirect(url_for('new_site'))


@app.route('/login', methods=['GET', 'POST'])
@templated()
def login():
    if request.method == 'POST':
        user = User.query.filter_by(email=request.form['email']).first()
        if user and user.authenticate(request.form['password']):
            login_user(user)
            return redirect(request.args.get('next') or url_for('index'))
    return None


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


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


@app.route('/site/new')
@templated()
def new_site():
    # check for an existing site and deny
    if Website.query.filter_by(user=current_user).first():
        flash("Sorry, at the moment you may only have one website. Stay tuned.")
        return redirect(url_for('index'))

    # create and check a form
    form = SiteForm()
    if form.validate_on_submit():
        # add a website
        w = Website()
        w.user = current_user
        w.domain = form.domain.data
        db.session.add(w)
        db.session.commit()
        return redirect(w.url())

    return dict(form=form)


@app.route('/site/<domain>/')
@templated()
def browse_files(domain):
    w = Website.query.filter_by(domain=domain).first()
    for root, dirs, files in os.walk(w.get_dir()):
        return dict(dirs=dirs, files=files)


@app.route('/site/<domain>/upload', methods=['POST'])
def upload_file(domain):
    pass


@app.route('/site/<domain>/delete', methods=['POST'])
def delete_file(domain):
    pass


@app.route('/site/<domain>/rename', methods=['POST'])
def rename_file(domain):
    pass
