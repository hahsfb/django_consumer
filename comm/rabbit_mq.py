#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File    : rabbit_mq.py
@Author  : HaoQiangJian
@Site    : 
@Time    : 18-11-13 下午5:03
@Version : 
"""

import pika, json
# from app.biz.setting import MQ_HOST, MQ_PORT, MQ_USR, MQ_PWD

MQ_HOST     = '127.0.0.1'
MQ_PORT     = 5672
MQ_USR      = 'guest'
MQ_PWD      = 'guest'
MQ_ORDER_TOPIC = 'admin_order'


class MessageMQ:
    def __init__(self, queue='hello'):
        self.conn = pika.BlockingConnection(
            pika.ConnectionParameters(host=MQ_HOST, port=MQ_PORT, virtual_host='/',
                                      credentials=pika.PlainCredentials(MQ_USR, MQ_PWD))
        )
        self.channel = self.conn.channel()
        self.channel.exchange_declare(exchange='order-exchange', durable=True, exchange_type='topic')
        self.channel.queue_declare(queue=queue, durable=True)

    def basic_publish(self, routing_key, body, exchange='order-exchange'):
        return self.channel.basic_publish(
            exchange=exchange,
            routing_key=routing_key,
            body=body,
            properties=pika.BasicProperties(
                delivery_mode=2,
            )
        )

    def close(self):
        return self.conn.close()


if __name__ == '__main__':
    mq = MessageMQ(queue='order-queue')
    aa = mq.basic_publish('order.def', json.dumps({'x': 2, 'y': 6}))
    mq.conn.close()
    print(aa)
    print()



"""
credentials = pika.PlainCredentials('', '123456')
connection = pika.BlockingConnection(pika.ConnectionParameters(
    '192.168.56.19', 5672, '/', credentials))
channel = connection.channel()

# 声明queue
channel.queue_declare(queue='balance')

# n RabbitMQ a message can never be sent directly to the queue, it always needs to go through an exchange.
channel.basic_publish(exchange='',
                      routing_key='balance',
                      body='Hello World!')
print(" [x] Sent 'Hello World!'")
connection.close()
"""