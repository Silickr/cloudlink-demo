# -*- coding: UTF-8 -*-
import os

APP_ENV = 'development' or os.environ.get('FLASK_APP_ENV')


class Config:
    # 配置你的appid和secret，最好存在环境变量中
    CLIENT_ID = ""
    CLIENT_SECRET = ""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess it'

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    CLOUDLINK_API_URL = 'https://cloudlinkworkplace-open.myhuaweicloud.com/api'


configs = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}