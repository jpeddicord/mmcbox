from flask.ext.wtf import Form, Required, Regexp, TextField


class SiteForm(Form):
    domain = TextField("Domain", [Required(), Regexp("^[a-zA-Z0-9\-\.]+$")])

