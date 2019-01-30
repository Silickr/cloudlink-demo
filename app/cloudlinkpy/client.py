# -*- coding: UTF-8 -*-
import requests
import json
from .helpers.error import CloudLinkClientError
from .cloudlink.models.users import Users

API_URL = 'https://cloudlinkworkplace-open.myhuaweicloud.com/api'
API_URL_TEMPLATE = '{api_url}/{route}'
# 测试地址
TEST_DOMAIN = 'https://grapejuice.azurewebsites.net'


class AuthWrapper(object):
    def __init__(self, access_token, code, client_id, client_secret, ticket_type='u'):
        self.current_access_token = access_token

        if code is None:
            raise TypeError('A code must be provided!')
        self.code = code
        self.client_id = client_id
        self.client_secret = client_secret
        self.type = ticket_type

    def get_current_code(self):
        return self.code

    def get_current_access_token(self):
        return self.current_access_token

    def refresh(self):
        data = {
            'code': self.code,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'type': self.type
        }

        url = API_URL_TEMPLATE.format(API_URL, 'auth/v1/tickets')

        response = requests.post(url, data=data)

        if response.status_code != 200:
            raise CloudLinkClientError('Error refreshing access token!', response.status_code)

        response_data = response.json()
        self.current_access_token = response_data['access_token']


class CloudLink(object):
    def __init__(self, client_id, client_secret, access_token=None, code=None):
        self.client_id = client_id
        self.client_secret = client_secret
        self.auth = None

        if code is not None:
            self.auth = AuthWrapper(access_token, code, client_id, client_secret)

    def set_user_auth(self, access_token, code):
        self.auth = AuthWrapper(access_token, code, self.client_id, self.client_secret)

    def get_client_id(self):
        return self.client_id

    def get_auth_url(self):
        return '%s/auth/authorize' % TEST_DOMAIN

    def authorize(self, response):
        return self.make_request('POST', 'auth/v1/tickets', {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'code': response,
            'type': 'u'
        }, True)

    @staticmethod
    def build_url(route=None):
        url = API_URL_TEMPLATE.format(api_url=API_URL, route=route)
        return url

    def prepare_headers(self, data=None, force_anon=False):
        """
        1、非认证场景获取token用json,设定force_anon=True
        2、认证场景
            2-1、如果是get请求用x-wlk
            2-2、r如果是post请求用x-wlk 及 json
        :param force_anon:
        :return:
        """
        headers = {}
        if force_anon or self.auth is None:
            headers['Content-Type'] = 'application/json'
        else:
            if self.client_id is None:
                raise CloudLinkClientError('Client credentials not found!')
            else:
                if data and isinstance(data, dict):
                    headers['x-wlk-Authorization'] = self.auth.get_current_access_token()
                    headers['Content-Type'] = 'application/json'
                else:
                    headers['x-wlk-Authorization'] = self.auth.get_current_access_token()

        return headers

    def make_request(self, method, route, data=None, force_anon=False):
        method = method.lower()
        method_to_call = getattr(requests, method)

        header = self.prepare_headers(force_anon)
        url = self.build_url(route)

        if method in ('delete', 'get'):
            response = method_to_call(url, headers=header, params=data, data=data)
        else:
            # 将data转为json对象
            data = json.dumps(data)
            response = method_to_call(url, headers=header, data=data)

        try:
            response_data = response.json()
        except:
            raise CloudLinkClientError('JSON decoding of response failed')

        # 待修改,token失效重新获取逻辑
        if 'errorCode' in response_data:
            raise CloudLinkClientError(response_data['errorCode'], response_data['errorMessage'])

        # code 不合法或者过期
        if response_data['code'] != '0':
            raise CloudLinkClientError(response_data['code'], response_data['message'])

        return response_data

    def get_user_id(self):
        userid = self.make_request('GET', 'auth/v1/userid')
        return userid['userId']

    def get_users(self, **kwargs):
        if 'userId' in kwargs:
            params = '%s=%s' % ('userId', kwargs['userId'])
        if 'mobileNumber' in kwargs:
            params = '%s=%s' % ('mobileNumber', kwargs['mobileNumber'])
        if 'corpUserId' in kwargs:
            params = '%s=%s' % ('corpUserId', kwargs['corpUserId'])
        route = 'contact/v1/users?%s' % params
        users_data = self.make_request('GET', route)
        return Users(users_data['userStatus'],
                     users_data['userId'],
                     users_data['deptCode'],
                     users_data['mobileNumber'],
                     users_data['userNameCn'],
                     users_data['userNameEn'],
                     users_data['sex'],
                     users_data['corpUserId'],
                     users_data['userEmail'],
                     users_data['secretary'],
                     users_data['phoneNumber'],
                     users_data['address'],
                     users_data['remark'])



