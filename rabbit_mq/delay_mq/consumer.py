#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File    : consumer.py
@Author  : HaoQiangJian
@Site    : 
@Time    : 18-11-13 下午5:27
@Version : 
"""

import time
import json
import pymysql
from config.messageMQ import MessageMQ, QUEUE
from config.config import DB_HOST, DB_NAME, DB_PORT, DB_PWD, DB_USER

message = MessageMQ()  # 创建socket连接

message.conn_master()


def conn_db():
    # 打开数据库连接
    db = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PWD, database=DB_NAME, port=DB_PORT)

    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    return cursor


def check_shopping(phone, hard_number, token):
    cursor = conn_db()
    cursor.execute("select token from cli_machine where mid=%s" % hard_number)
    data = cursor.fetchone()
    if data and data == token:
        # TODO 发送短信提醒
        print('%s 短信提醒' % phone)
        pass


# 回调函数
def methods(ch, method, properties, body):
    print('----------------------------')
    print(ch)
    print(method)
    data = json.loads(body.decode())
    print(data)
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    print(properties)
    routing_key = None
    if len(properties.headers.get('x-death')) > 0 and len(properties.headers.get('x-death')[0].get('routing-keys')[0]) > 0:
        routing_key = properties.headers.get('x-death')[0].get('routing-keys')[0]


    if routing_key and 'timing.queue' in routing_key:
        # 定时任务执行消费
        pass
    elif routing_key and 'delay.shopping.queue' in routing_key:
        # 购物五分钟是否关门提醒
        check_shopping(data.get('phone'), data.get('hard_number'), data.get('token'))
    else:
        print('----------------------------')
        ch.basic_ack(delivery_tag=method.delivery_tag)


if __name__=='__main__':
    message.channel.basic_consume(consumer_callback=methods, queue=QUEUE)
    message.channel.start_consuming()


