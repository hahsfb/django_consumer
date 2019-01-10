#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File    : messageMQ.py
@Author  : HaoQiangJian
@Site    : 
@Time    : 18-12-11 上午11:22
@Version : 
"""

import json
import pika
import time

from .config import MQ_HOST, MQ_PORT, MQ_USR, MQ_PWD, DELAY_EXCHANGE_5MIN, DELAY_QUEUE_5MIN, EXCHANGE, QUEUE, \
    ORDER_EXCHANGE, ORDER_QUEUE, TIMING_QUEUE, TIMING_EXCHANGE


def get_tem_name():
    tem = str(int(time.time()))
    return TIMING_QUEUE + '_' + tem


class MessageMQ:
    # def __init__(self, queue, exchange, exchange_type='fanout', virtual_host='/'):
    def __init__(self, virtual_host='/'):
        self.conn = pika.BlockingConnection(
            pika.ConnectionParameters(host=MQ_HOST, port=MQ_PORT, virtual_host=virtual_host,
                                      credentials=pika.PlainCredentials(MQ_USR, MQ_PWD))
        )
        if self.conn.is_open is False:
            print('connection fail')

        self.channel = self.conn.channel()

    def basic_publish(self, routing_key, body, exchange='order-exchange', expiration=None, timestamp=None):
        self.channel.basic_publish(
            exchange=exchange,
            routing_key=routing_key,
            body=json.dumps(body),
            properties=pika.BasicProperties(
                delivery_mode=2,
                expiration=str(expiration) if expiration else None,
                timestamp=timestamp
            )
        )
        return self

    def close(self):
        return self.conn.close()

    def conn_master(self):
        # 声明收容交换机
        self.channel.exchange_declare(exchange=EXCHANGE, durable=True, exchange_type='direct')
        # 声明收容队列
        self.channel.queue_declare(queue=QUEUE, durable=True)
        # 收容队列和收容交换机绑定
        self.channel.queue_bind(exchange=EXCHANGE, queue=QUEUE)
        return self

    def conn_shopping_tips(self):
        # 设置延迟队列参数
        arguments = {
            'x-message-ttl': 1000 * 60 * 5,  # 延迟时间 （毫秒）
            'x-dead-letter-exchange': EXCHANGE,  # 延迟结束后指向交换机（死信收容交换机）
            'x-dead-letter-routing-key': QUEUE,  # 延迟结束后指向队列（死信收容队列）
        }
        # 声明队列
        self.channel.exchange_declare(exchange=DELAY_EXCHANGE_5MIN, exchange_type='direct', durable=True,
                                      arguments=arguments)
        # 声明交换机
        self.channel.queue_declare(queue=DELAY_QUEUE_5MIN, durable=True, arguments=arguments)
        # 队列和交换机绑定
        self.channel.queue_bind(exchange=DELAY_EXCHANGE_5MIN, queue=DELAY_QUEUE_5MIN)
        return self

    def conn_order(self):
        # 设置延迟队列参数
        arguments = {  # 延迟时间 （毫秒）
            'x-expires': 1000 * 60,
            'x-dead-letter-exchange': EXCHANGE,  # 延迟结束后指向交换机（死信收容交换机）
            'x-dead-letter-routing-key': QUEUE,  # 延迟结束后指向队列（死信收容队列）
        }
        # 声明队列
        self.channel.exchange_declare(exchange=ORDER_EXCHANGE, exchange_type='direct', durable=True)
        # 声明交换机
        self.channel.queue_declare(queue=ORDER_QUEUE, durable=True, arguments=arguments)
        # 队列和交换机绑定
        self.channel.queue_bind(exchange=ORDER_EXCHANGE, queue=ORDER_QUEUE)
        return self

    def __create_task(self, tem_queue, expires):
        # 设置延迟队列参数
        arguments = {  # 延迟时间 （毫秒）
            'x-expires': expires + 100,
            'x-dead-letter-exchange': EXCHANGE,  # 延迟结束后指向交换机（死信收容交换机）
            'x-dead-letter-routing-key': QUEUE,  # 延迟结束后指向队列（死信收容队列）
        }
        # 声明队列
        self.channel.exchange_declare(exchange=TIMING_EXCHANGE, exchange_type='direct', durable=True)
        # 声明交换机
        self.channel.queue_declare(queue=tem_queue, durable=True, arguments=arguments)
        # 队列和交换机绑定
        self.channel.queue_bind(exchange=TIMING_EXCHANGE, queue=tem_queue)
        return self

    def shopping_tips(self, body):
        self.conn_master().conn_shopping_tips().basic_publish(DELAY_QUEUE_5MIN, body,
                                                              exchange=DELAY_EXCHANGE_5MIN).close()

    def order_charge(self, body):
        self.conn_master().conn_order().basic_publish(routing_key=ORDER_QUEUE, body=body,
                                                      exchange=ORDER_EXCHANGE).close()

    def timely_message(self, body):
        self.conn_master().basic_publish(routing_key=QUEUE, body=body, exchange=EXCHANGE, timestamp=1544605200).close()

    def timing_task(self, body, expires):
        tem_queue = get_tem_name()
        self.conn_master().__create_task(tem_queue, expires) \
            .basic_publish(routing_key=tem_queue, body=body, exchange=TIMING_EXCHANGE, expiration=expires).close()
