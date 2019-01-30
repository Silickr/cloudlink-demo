# -*- coding: UTF-8 -*-
from cloudlinkpy.client import CloudLink
from helpers import get_input, get_config


def authenticate():
    config = get_config()
    config.read('auth.ini')
    client_id = config.get('credentials', 'client_id')
    client_secret = config.get('credentials', 'client_secret')
    client = CloudLink(client_id, client_secret)

    name = config.get('credentials', 'loginName')
    pw = config.get('credentials', 'password')
    # redirect_url = config.get('credentials', 'redirect_url')

    authorization_url = client.get_auth_url()
    print("Go to the following URL: "
          "{0}?name={1}&pw={2}".format(authorization_url, name, pw))

    code = get_input("Please enter auth code: ")

    credentials = client.authorize(code)
    client.set_user_auth(credentials['access_token'], code)

    print("Authentication successful! Here are the details:")
    print("   Access token:  {0}".format(credentials['access_token']))

    return client


if __name__ == "__main__":
    authenticate()

