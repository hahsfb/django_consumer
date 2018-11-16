#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File    : consumer.py
@Author  : HaoQiangJian
@Site    : 
@Time    : 18-11-13 下午5:27
@Version : 
"""

import pika, time
import uuid

from .config import MQ_HOST, MQ_PORT, MQ_USR, MQ_PWD


# consumer = pika.BlockingConnection(
#             pika.ConnectionParameters(host=MQ_HOST, port=MQ_PORT, virtual_host='/',
#                                       credentials=pika.PlainCredentials(MQ_PWD, MQ_PWD))
#         )  # 创建socket连接
# channel = consumer.channel()  # 创建管道
# # channel.exchange_declare(exchange='order-exchange', exchange_type='topic')
# channel.exchange_declare(exchange='order-exchange', durable=True, exchange_type='topic')
# channel.queue_declare(queue='order-queue', durable=True)


class FibonacciRpcClient(object):
    def __init__(self):
        self.response = None
        self.corr_id = None
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=MQ_HOST, port=MQ_PORT,
                                      credentials=pika.PlainCredentials(MQ_USR, MQ_PWD)))

        self.channel = self.connection.channel()
        # self.channel.exchange_declare(exchange='rpc_exchange')
        # result = self.channel.queue_declare(queue='rpc_queue', durable=True, exclusive=True)
        result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(self.on_response, no_ack=True,
                                   queue=self.callback_queue)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, n):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(exchange='',
                                   routing_key='rpc_queue',
                                   properties=pika.BasicProperties(
                                         reply_to=self.callback_queue,
                                         correlation_id=self.corr_id,
                                         ),
                                   body=str(n))
        while self.response is None:
            self.connection.process_data_events()
        return int(self.response)


fibonacci_rpc = FibonacciRpcClient()

print(" [x] Requesting fib(30)")
response = fibonacci_rpc.call(30)
print(" [.] Got %r" % response)
