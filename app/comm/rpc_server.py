#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File    : rpc_server.py
@Author  : HaoQiangJian
@Site    : 
@Time    : 18-11-15 下午5:30
@Version : 
"""

import pika, time
from .config import MQ_HOST, MQ_PORT, MQ_USR, MQ_PWD


consumer = pika.BlockingConnection(
            pika.ConnectionParameters(host=MQ_HOST, port=MQ_PORT,
                                      credentials=pika.PlainCredentials(MQ_USR, MQ_PWD))
        )  # 创建socket连接
channel = consumer.channel()  # 创建管道
# channel.exchange_declare(exchange='order-exchange', exchange_type='topic')
# channel.exchange_declare(exchange='rpc_exchange')
channel.queue_declare(queue='rpc_queue')


def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n-1) + fib(n-2)


def on_request(ch, method, props, body):
    n = int(body)

    print(" [.] fib(%s)" % n)
    response = fib(n)

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id=props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(on_request, queue='rpc_queue')

print(" [x] Awaiting RPC requests")
channel.start_consuming()


