#!/usr/bin/env python

import os

from flask import *

from mmc import *
from mmc.models import *


try:
    from IPython import embed
    embed()

except ImportError:
    print "IPython is recommended for shell usage, but you don't have it installed."
    print "Falling back to built-in Python."

    import readline
    from pprint import pprint
    os.environ['PYTHONINSPECT'] = 'True'
