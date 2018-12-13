#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File    : redis_consumer.py
@Author  : HaoQiangJian
@Site    : 
@Time    : 18-12-13 下午1:49
@Version : 
"""
import redis
import time

pool = redis.ConnectionPool(host='127.0.0.1', port=6379)

r = redis.Redis(connection_pool=pool)
print('*****订单监听系统********')
print('************************')
print('**开始监听新的订单中*****')
print('************************')

while True:
    name = r.rpop('test_queue')
    if name == None:
        time.sleep(3)
    else:
        # playsound("audio.mp3")
        now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print(name)
        print('speak..' + now)
