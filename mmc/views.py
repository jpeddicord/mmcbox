import os
import os.path

from flask import request
from flask import redirect, flash, abort
from flask import url_for
from flask.ext.login import login_required, login_user, logout_user, current_user
from werkzeug import secure_filename

from mmc import app, db, magic
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
            # login
            login_user(user)
            # clear their activation
            user.activation = None
            db.session.add(user)
            db.session.commit()
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
        current_user.activation = None
        db.session.add(current_user)
        db.session.commit()
        flash("Password changed.")
        return redirect(url_for('index'))

    return dict(form=form)

@app.route('/account/forgotpass', methods=['GET', 'POST'])
@templated()
def forgot_password():
    if request.method == 'POST':
        user = User.query.filter_by(email=request.form['email']).first()
        # not found
        if not user:
            flash("Account not found. Contact accounts@mmcbox.com for help.")
            return redirect(url_for('forgot_password'))
        # generate a new activation
        user.activation = User.generate_random_string(16)
        user.password = None
        # save and email
        db.session.add(user)
        db.session.commit()
        user.mail_forgot_password()
        # notify and redirect
        flash("Please check your email for further instructions.")
        return redirect(url_for('login'))
    return None


@app.route('/account/activate/<code>')
@templated()
def activate(code):
    # find the user to activate
    user = User.query.filter_by(activation=code).first()
    if not user:
        abort(404)

    # sign them in
    login_user(user)

    # tell them to change their password
    flash("Please set your new password.")
    return redirect(url_for('change_password'))


@app.route('/site/new', methods=['GET', 'POST'])
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
        w.domain = form.domain.data.lower()
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
    # ensure the directory on the filesystem is created
    Website.query.filter_by(domain=domain).first().get_dir()

    # get the physical path
    d = filesystem_path(domain, path)
    for root, dirs, files in os.walk(d):
        return dict(domain=domain, path=path, dirs=dirs, files=files,
                    join=os.path.join)


@app.route('/site/<domain>/edit/<path:path>')
@login_required
@check_domain
@templated()
def edit_file(domain, path):
    fname = filesystem_path(domain, path)

    # calculate the folder this file is in
    if '/' in path:
        browse = url_for('browse_files', domain=domain, path=path.rsplit('/', 1)[0])
    else:
        browse = ''

    # check file size
    size = os.path.getsize(fname)

    # check magic
    mime = magic.from_file(fname)
    if 'text' not in mime and size > 16:
        flash("This doesn't appear to be a text file, so we can't edit it here. If you want to replace it, just upload it again.")
        return redirect(browse)

    # warn about size issues after magic check
    if size > 200 * 1024:
        flash("Sorry, that file is a little too large to edit on the web.")
        return redirect(browse)

    with open(fname) as f:
        return dict(file_content=f.read().decode('utf-8'), domain=domain, path=path)


@app.route('/site/<domain>/save/<path:path>', methods=['POST'])
@login_required
@check_domain
def save_file(domain, path):
    fname = filesystem_path(domain, path)

    # first, write to a secondary file
    secondary = fname + '~'
    data = request.form['content']
    with open(secondary, 'w') as f:
        f.write(data.encode('utf-8'))

    # then, remove the original and rename the new file
    if os.path.exists(fname):
        os.remove(fname)
    os.rename(secondary, fname)
    return ''


@app.route('/site/<domain>/upload', methods=['POST'])
@login_required
@check_domain
def upload_file(domain):
    f = request.files['files[]']
    if f and f.filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']:
        filename = secure_filename(f.filename)
        path = filesystem_path(domain, request.form['path'])
        fullpath = os.path.join(path, filename)
        f.save(fullpath)
        return '{}'
    else:
        return abort(400)


@app.route('/site/<domain>/new-file', methods=['POST'])
@login_required
@check_domain
def new_file(domain):
    filename = secure_filename(request.form['filename'])
    path = filesystem_path(domain, request.form['path'])
    fullpath = os.path.join(path, filename)
    if not os.path.exists(fullpath):
        with open(fullpath, 'w') as f:
            f.write('\n')
    return ''


@app.route('/site/<domain>/new-folder', methods=['POST'])
@login_required
@check_domain
def new_folder(domain):
    filename = secure_filename(request.form['filename'])
    path = filesystem_path(domain, request.form['path'])
    fullpath = os.path.join(path, filename)
    if not os.path.exists(fullpath):
        os.mkdir(fullpath)
    return ''


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

