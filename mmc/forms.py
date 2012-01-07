from flask.ext.wtf import Form, Required, EqualTo, Length, Regexp, TextField, PasswordField


class SiteForm(Form):
    domain = TextField("Domain", [Required(), Regexp("^[a-zA-Z0-9\-\.]+$", message="Not a valid domain name.")])

class ChangePasswordForm(Form):
    password = PasswordField("New Password", [Required(), Length(min=6), EqualTo('confirm')])
    confirm = PasswordField("Confirm")

