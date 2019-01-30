# -*- coding: UTF-8 -*-
def get_config():
    try:
        import ConfigParser
        return ConfigParser.ConfigParser()
    except:
        import configparser
        return configparser.ConfigParser()

def get_input(string):
    try:
        return raw_input(string)
    except:
        return input(string)