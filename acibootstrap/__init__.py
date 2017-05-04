#!/usr/bin/env python
from flask import Flask
#from flask.ext.bootstrap import Bootstrap
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('acibootstrap/logs/acibootstrap.log')
fh.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
formatter = logging.Formatter('%(asctime)s - %(name)s - '
                              '%(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(ch)

logger.critical('*' * 25)
logger.critical('acibootstrap is starting')
logger.critical('*' * 25)

app = Flask(__name__, static_url_path='/static')

#bootstrap = Bootstrap(app)

import views
