# -*- coding: UTF-8 -*-
from flask import Flask
from flask_bootstrap import Bootstrap

bootstrap = Bootstrap()

app = Flask(__name__)
bootstrap.init_app(app)

from app import views
