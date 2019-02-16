#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File    : server.py
@Author  : HaoQiangJian
@Site    : 
@Time    : 19-2-14 上午9:33
@Version : 
"""
# -*- coding:utf-8 -*-
"""
@datetime:2018/12/25 2:41
@author: gjh
"""

from bottle import request, Bottle, abort
from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler
import json
import threading
import requests

app = Bottle()
users = {}

xt_url = "http://127.0.0.1:5001/v2/terminal/status/update"


def deal_msg(message):
    data = json.loads(message)
    try:
        print(data)
        if data.get("command") == "heart-beat":
            print("心跳")
            data.pop("command")
            response = requests.post(xt_url, json=data, timeout=3)
            print(response.text)
        else:
            print("其他操作")
    except Exception as error:
        print(error)


@app.get('/websocket/')
def handle_websocket():
    wsock = request.environ.get('wsgi.websocket')
    if not wsock:
        abort(400, 'Expected WebSocket request.')
    message = wsock.receive()
    data = json.loads(message)
    cmd = data.get("command")
    machine_id = data.get("machine_id")
    if cmd == "start-up":
        if machine_id in users.keys():
            return
        users[machine_id] = wsock
    print("现有连接用户：%s" % (len(users)))
    print(data.get("machine_id"))
    while True:
        try:
            message = wsock.receive()
            threading.Thread(target=deal_msg(message=message)).start()
        except Exception as e:
            print(e)
            break
    print("users: ", users)
    users.pop(machine_id)
    print(len(users))
    print("users: ", users)


@app.route("/send_msg", method=["POST"])
def send_msg():
    data = request.json
    machine_id = data.get("machine_id")
    print(data)
    if machine_id:
        conn = users[machine_id]
        print(conn)
        if conn:
            conn.send(json.dumps(data))
            return true_return()
    return false_return(code=-1)


def true_return(code=200, data="", msg="请求成功"):
    rt = {
        "code": code,
        "data": data,
        "msg": msg
    }
    return rt


def false_return(code=-1, data="", msg="请求失败"):
    rt = {
        "code": code,
        "data": data,
        "msg": msg
    }
    return rt


if __name__ == '__main__':
    server = WSGIServer(("0.0.0.0", 30008), app, handler_class=WebSocketHandler)
    server.serve_forever()
