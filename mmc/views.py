import os
import os.path

from flask import g, request, session
from flask import render_template, redirect, flash
from flask import url_for
from flask.ext.login import login_required, login_user, logout_user, current_user

from mmc import app, db
from mmc.forms import SiteForm, ChangePasswordForm
from mmc.models import User, Website
from mmc.util import templated, check_domain, filesystem_path


@app.route('/')
@login_required
def index():
    w = Website.query.filter_by(user=current_user).first()
    if w:
        return redirect(w.url())
    else:
        return redirect(url_for('new_site'))


@app.route('/account/login', methods=['GET', 'POST'])
@templated()
def login():
    if request.method == 'POST':
        user = User.query.filter_by(email=request.form['email']).first()
        if user and user.authenticate(request.form['password']):
            login_user(user)
            return redirect(request.args.get('next') or url_for('index'))
        else:
            flash("Invalid username or password.")
    return None


@app.route('/account/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/account/password', methods=['GET', 'POST'])
@login_required
@templated()
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        current_user.set_password(form.password.data)
        db.session.add(current_user)
        db.session.commit()
        flash("Password changed.")
        return redirect(url_for('index'))

    print form.errors
    return dict(form=form)



@app.route('/account/activate')
@templated()
def activate():
    # read activation code
    # wipe activation (on POST)
    # flash warning
    # redirect to password change page
    pass


@app.route('/site/new')
@login_required
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


@app.route('/site/<domain>/files/')
@app.route('/site/<domain>/files/<path:path>')
@login_required
@check_domain
@templated()
def browse_files(domain, path=''):
    w = Website.query.filter_by(domain=domain).first()
    d = filesystem_path(domain, path)
    for root, dirs, files in os.walk(d):
        return dict(domain=domain, path=path, dirs=dirs, files=files,
                    join=os.path.join)


@app.route('/site/<domain>/edit/<path:path>')
@login_required
@check_domain
@templated()
def edit_file(domain, path):
    w = Website.query.filter_by(domain=domain).first()
    fname = filesystem_path(domain, path)
    #TODO: check file size, text editable, etc
    with open(fname) as f:
        return dict(file_content=f.read())


@app.route('/site/<domain>/upload', methods=['POST'])
@login_required
@check_domain
def upload_file(domain):
    pass


@app.route('/site/<domain>/delete', methods=['POST'])
@login_required
@check_domain
def delete_file(domain):
    pass


@app.route('/site/<domain>/rename', methods=['POST'])
@login_required
@check_domain
def rename_file(domain):
    pass

