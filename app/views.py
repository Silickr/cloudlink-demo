# -*- coding: UTF-8 -*-
from app import app
from flask import request, make_response, render_template, jsonify, session, g
from knowledge_entity import KNOWLEDGE_ENTITY
from datetime import datetime
from time import mktime
from wsgiref.handlers import format_date_time
from auth import authenticate
from demo import demo_get_user_id


@app.route('/')
@app.route('/knowledge/')
def knowledge():
    user_id = request.cookies.get('userId')
    if user_id is None:
        print('No User Info Found')
        response = make_response(
            render_template('knowledge.html',
                            userId='anonymous',
                            text=KNOWLEDGE_ENTITY.get('default')))
        response.set_cookie('userId',
                            'anonymous',
                            max_age=60 * 60 * 2)
        return response
    else:
        print(user_id)
        return render_template(
            'knowledge.html', userId=user_id,
            text=KNOWLEDGE_ENTITY.get(userid, KNOWLEDGE_ENTITY.get('default')))


@app.route('/userid/<code>')
def userid(code):
    if code is not None:
        client = authenticate(code)
        userId = demo_get_user_id(client)
        return jsonify({'code': '0', 'userId': userId})
    return jsonify({'code': '101', 'message': 'code is missing!'})


@app.after_request
def add_header(response):
    now = datetime.now()
    stamp = mktime(now.timetuple())
    response.headers['Last-Modified'] = format_date_time(stamp)
    response.headers['Cache-Control'] = 'max-age=300'
    return response


