#!/usr/bin/env python

import os
import readline
from pprint import pprint

from flask import *

from mmc import *
from mmc.models import *


os.environ['PYTHONINSPECT'] = 'True'
