from flask import Flask

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

app = Flask(__name__)
app.config.from_object('config')


app.config.update(dict(
    SECRET_KEY='development key'
))

from app import views