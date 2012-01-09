#!/usr/bin/env python

import sys

if len(sys.argv) != 2:
    print "Usage: create_account.py account@email"
    sys.exit(1)

from mmc import app
from mmc import views
from mmc.models import User


email = sys.argv[1]

ctx = app.test_request_context()
ctx.push()

u = User.create_user(email)

print "Activation code is", u.activation

send = raw_input("Send email? [y/N] ")
if send == "y":
    u.mail_activation()

ctx.pop()
