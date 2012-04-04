from flask.ext.wtf import Form
from flask.ext.wtf import Required, EqualTo, Length, Regexp, ValidationError
from flask.ext.wtf import TextField, PasswordField, BooleanField

from mmc.models import User, Website


class SiteForm(Form):
    domain = TextField("Domain", [Required(), Regexp("^[a-zA-Z0-9\-]+\.mmcbox\.com$", message="Not a valid domain name. Make sure it ends in .mmcbox.com.")])

    def validate_domain(self, field):
        if Website.query.filter_by(domain=field.data).first():
            raise ValidationError("Domain name already in use by someone else.")


class ChangePasswordForm(Form):
    password = PasswordField("New Password", [Required(), Length(min=6)])
    confirm = PasswordField("Confirm", [EqualTo('password')])


class StaffCreateAccountForm(Form):
    email = TextField("Email", [Required()])
    notify = BooleanField("Send activation email")

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("Account already exists.")
