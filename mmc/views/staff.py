from smtplib import SMTPResponseException

from flask import redirect, url_for, flash

from mmc import app
from mmc.forms import StaffCreateAccountForm
from mmc.models import User
from mmc.util import templated, staff_only


@app.route('/staff/users/')
@staff_only
@templated()
def staff_users():
    return dict(users=User.query.order_by(User.email))


@app.route('/staff/users/new/', methods=['GET', 'POST'])
@staff_only
@templated()
def staff_create_account():
    form = StaffCreateAccountForm()

    if form.validate_on_submit():
        user = User.create_user(form.email.data)
        if form.notify.data:
            try:
                user.mail_activation()
            except SMTPResponseException as e:
                flash("Failed to send activation email: {0}".format(e.smtp_error), 'error')
            except Exception as e:
                flash("Failed to send activation email for an unknown reason.", 'error')
            else:
                flash("Activation email sent.")
        flash("User created.", 'success')
        return redirect(url_for('staff_users'))

    return dict(form=form)
