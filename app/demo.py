# -*- coding: UTF-8 -*-
from auth import authenticate


def demo_get_user_id(_client):
    return _client.get_user_id()


def demo_get_users(_client, userid):
    return _client.get_users(userId=userid)


if __name__ == "__main__":
    client = authenticate()
    userid = demo_get_user_id(client)
    users = demo_get_users(client, userid)
    print 'Users detail:'
    print 'English name is :%s' % users.usernameEn
    print 'Mobile number is: %s' % users.mobileNumber