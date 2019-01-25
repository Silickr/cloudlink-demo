# -*- coding: UTF-8 -*-
from config import configs
from config import APP_ENV
import json
from urllib2 import Request, urlopen, HTTPError, URLError


class CloudLink(object):
    def __init__(self, params):
        self.code = params['code']
        self.access_token = self.__get_access_token()
        self.user_id = self.__get_userid()

    def __get_access_token(self):
        response = self.__call_auth_v1_tickets(self.code)
        if response.get("code") == "0":
            return response.get("access_token")
        else:
            return None

    def __get_userid(self):
        if self.access_token is not None:
            response = self.__call_auth_v1_userid(self.access_token)
            return response
        else:
            return None

    @staticmethod
    def __call_auth_v1_tickets(code):
        headers = {"Content-Type": "application/json"}
        tickets_url = configs[APP_ENV].CLOUDLINK_API_URL + "/auth/v1/tickets"
        body = {"state": 1,
                "type": "u",
                "client_id": configs[APP_ENV].CLIENT_ID,
                "client_secret": configs[APP_ENV].CLIENT_SECRET,
                "code": code}
        postdata = json.dumps(body)
        token_req = Request(url=tickets_url, data=postdata, headers=headers)

        try:
            response = urlopen(token_req)
        except HTTPError as e:
            print("The server couldn\'t fulfill the request.")
            print('reason:', e.reason)
        except URLError as e:
            print('Failed to reach a server.')
            print('reason:', e.reason)
        else:
            print(u'执行获取token正常!')
        content = response.read()
        return json.loads(content)

    @staticmethod
    def __call_auth_v1_userid(access_token):
        headers = {"x-wlk-Authorization": access_token}
        user_id_url = configs[APP_ENV].CLOUDLINK_API_URL + "/auth/v1/userid"
        user_id_req = Request(url=user_id_url, headers=headers)

        try:
            response = urlopen(user_id_req)
        except HTTPError as e:
            print("The server conldn\'t fulfill the request.")
            print('reason:', e.reason)
        except URLError as e:
            print('Failed to reach a server.')
            print('reason:', e.reason)
        else:
            print(u'执行获取userId正常!')
        content = response.read()
        return json.loads(content)

    def get_user_id(self):
        if self.user_id is not None:
            result = self.user_id['userId']
        else:
            result = 'code has been used! or code is invalid'
        return result
