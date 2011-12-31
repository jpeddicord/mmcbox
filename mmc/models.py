from hashlib import sha256
from os import mkdir
from os.path import join, exists
from random import randint

from flask import url_for
from flask.ext.login import UserMixin
from werkzeug import secure_filename

from mmc import app, db, login_manager


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.Unicode(128), unique=True)
    password = db.Column(db.String(128))
    activation = db.Column(db.String(16))
    staff = db.Column(db.Boolean, default=False)
    storage_limit = db.Column(db.Integer)

    def authenticate(self, password):
        # first 8 characters are the salt
        salt = self.password[:8]
        # verify the password and salt
        check = sha256(salt + password)
        return check.hexdigest() == self.password[8:]

    def set_password(self, password):
        # generate a salt
        salt = ''.join([chr(ord('a') + randint(0, 25)) for c in range(8)])
        # store the digest
        digest = sha256(salt + password)
        self.password = salt + digest.hexdigest()


@login_manager.user_loader
def load_user(userid):
    return User.query.get(userid)


class Website(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref='websites')
    domain = db.Column(db.String(64), unique=True)
    storage_limit = db.Column(db.Integer)
    file_limit = db.Column(db.Integer)

    def calculate_size(self):
        return 0

    def url(self):
        return url_for('browse_files', domain=self.domain)

    def get_dir(self):
        path = join(app.config['SITES_DIR'], secure_filename(self.domain))
        if not exists:
            os.mkdir(path)
        return path

