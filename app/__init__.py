# -*- coding: UTF-8 -*-
from flask import Flask
from flask_bootstrap import Bootstrap
from config import configs
from config import APP_ENV

bootstrap = Bootstrap()

app = Flask(__name__)
app.config.from_object(configs[APP_ENV])
configs[APP_ENV].init_app(app)
bootstrap.init_app(app)


from app import views
