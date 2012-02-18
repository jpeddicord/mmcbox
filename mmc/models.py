from hashlib import sha256
from os import mkdir
from os.path import join, exists
from random import randint

from flask import url_for
from flask.ext.login import UserMixin
from flask.ext.mail import Message
from werkzeug import secure_filename

from mmc import app, db, login_manager, mail


ACTIVATION_EMAIL = """
Welcome to mmcbox!

Your account has been activated. Please sign in using this
one-time link and set your password:

    {0}

Once you're signed in, you can begin to create your website.
If you are having trouble with your account, feel free to
reply to this message and we'll try to sort things out.

Enjoy.
"""

FORGOT_PASSWORD_EMAIL = """
Forgot your password? Reset it here:

    {0}

If you need help, feel free to reply to this email and we'll
try to sort things out.
"""

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.Unicode(128), unique=True)
    password = db.Column(db.String(128))
    activation = db.Column(db.String(16))
    staff = db.Column(db.Boolean, default=False)
    storage_limit = db.Column(db.Integer)

    @staticmethod
    def generate_random_string(length):
        return ''.join([chr(ord('a') + randint(0, 25)) for c in range(length)])

    @classmethod
    def create_user(cls, email):
        user = cls()
        user.email = email
        user.activation = User.generate_random_string(16)
        db.session.add(user)
        db.session.commit()
        return user

    def __str__(self):
        return self.email

    def __repr__(self):
        return "<User '{0}'>".format(self.email)

    def authenticate(self, password):
        if not self.password:
            return False
        # first 8 characters are the salt
        salt = self.password[:8]
        # verify the password and salt
        check = sha256(salt + password)
        return check.hexdigest() == self.password[8:]

    def set_password(self, password):
        # generate a salt
        salt = User.generate_random_string(8)
        # store the digest
        digest = sha256(salt + password)
        self.password = salt + digest.hexdigest()

    def mail_activation(self):
        """Send an activation email."""

        msg = Message("mmcbox account activation",
                      sender=app.config['DEFAULT_MAIL_SENDER'])
        msg.add_recipient(self.email)
        msg.body = ACTIVATION_EMAIL.format(url_for('activate',
                                           code=self.activation,
                                           _external=True))
        mail.send(msg)

    def mail_forgot_password(self):
        """Send a password reset email."""

        msg = Message("mmcbox password reset",
                      sender=app.config['DEFAULT_MAIL_SENDER'])
        msg.add_recipient(self.email)
        msg.body = FORGOT_PASSWORD_EMAIL.format(url_for('activate',
                                                code=self.activation,
                                                _external=True))
        mail.send(msg)


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
        if not exists(path):
            mkdir(path)
        return path

