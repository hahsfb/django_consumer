#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File    : consumer.py
@Author  : HaoQiangJian
@Site    : 
@Time    : 18-11-13 下午5:27
@Version : 
"""

import pika, time, json

from ..config import MQ_HOST, MQ_PORT, MQ_USR, MQ_PWD, CRON_TIMES

consumer = pika.BlockingConnection(
    pika.ConnectionParameters(host=MQ_HOST, port=MQ_PORT, virtual_host='/',
                              credentials=pika.PlainCredentials(MQ_USR, MQ_PWD))
)  # 创建socket连接
channel = consumer.channel()  # 创建管道
# channel.exchange_declare(exchange='order-exchange', exchange_type='topic')
channel.exchange_declare(exchange='order-exchange', durable=True, exchange_type='topic')
channel.queue_declare(queue='order-queue', durable=True)
channel.queue_bind(exchange='order-exchange', queue='order-queue', routing_key='order.*')


def add(x, y):
    return x + y


def get_result(x, y):
    # {"status": "success", "result", "xxxxxxxxxxxx"} 正确
    # 不重发了
    # {"status": "fail", "result", "xxxxxxxxxxxx"} 失败
    # 我会重新发
    # {"status": "error", "result", "xxxxxxxxxxxx"} 错误
    # 不重发了
    if x + y > 5:
        return {"status": "error", "code": -1, "msg": "代扣次数达到上限,不需要重发"}
    elif x + y == 5:
        return {"status": "success", "code": 200, "msg": "不需要重发"}
    else:
        return {"status": "fail", "code": -1, "msg": "需要重发"}


def backcall(ch, method, properties, body):  # 参数body是发送过来的消息。
    print(ch)
    print(method)
    print(method.routing_key)
    body = json.loads(body.decode())
    print(body)

    count = 0
    while count < CRON_TIMES:
        count += 1
        if method.routing_key == 'order.abc':
            print(get_result(body.get('x'), body.get('y')))
            continue
        else:
            print(get_result(body.get('x'), body.get('y')))
            break
    print(properties)
    # time.sleep(5)
    channel.basic_ack(delivery_tag=method.delivery_tag)

    # 签收失败,再次发送
    # channel.basic_nack(delivery_tag=method.delivery_tag)


def run():
    channel.basic_consume(backcall,  # 回调函数。执行结束后立即执行另外一个函数返回给发送端是否执行完毕。
                          queue='order-queue'
                          # no_ack=True  # 不会告知服务端我是否收到消息。一般注释。
                          )  # 如果注释掉，对方没有收到消息的话不会将消息丢失，始终在队列里等待下次发送。

    print('waiting for message To exit   press CTRL+C')
    channel.start_consuming()  # 启动后进入死循环。一直等待消息。


if __name__ == '__main__':
    run()