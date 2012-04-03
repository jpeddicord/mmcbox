from flask.ext.wtf import Form, Required, EqualTo, Length, Regexp, TextField, PasswordField, ValidationError

from mmc.models import Website


class SiteForm(Form):
    domain = TextField("Domain", [Required(), Regexp("^[a-zA-Z0-9\-]+\.mmcbox\.com$", message="Not a valid domain name. Make sure it ends in .mmcbox.com.")])

    def validate_domain(self, field):
        if Website.query.filter_by(domain=field.data).first():
            raise ValidationError("Domain name already in use by someone else.")


class ChangePasswordForm(Form):
    password = PasswordField("New Password", [Required(), Length(min=6), EqualTo('confirm')])
    confirm = PasswordField("Confirm")

