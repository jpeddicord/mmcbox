from flask.ext.wtf import Form, Required, EqualTo, Length, Regexp, TextField, PasswordField


class SiteForm(Form):
    # TODO: validate to ensure it doesn't exist.
    domain = TextField("Domain", [Required(), Regexp("^[a-zA-Z0-9\-\.]+$", message="Not a valid domain name.")])

class ChangePasswordForm(Form):
    password = PasswordField("New Password", [Required(), Length(min=6), EqualTo('confirm')])
    confirm = PasswordField("Confirm")

