#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File    : producer.py
@Author  : HaoQiangJian
@Site    : 
@Time    : 18-11-13 下午5:03
@Version : 
"""

# import pika, json
import time
from rabbit_mq.messageMQ import MessageMQ
#
# # 延迟交换机
# delay_exchange = 'delay.shopping.exchange'
# # 延迟队列
# delay_queue = 'delay.shopping.queue'
#
# # 是否延迟队列
# # is_delay = True
# is_delay = False
#
# # 消费交换机
# exchange = 'cabinet.exchange'
# # 消费队列
# queue = 'cabinet.queue'
#
# message = MessageMQ()
#
# # 延迟队列参数设置
# arguments = None
#
# if is_delay is True:
#     # 声明收容交换机
#     message.channel.exchange_declare(exchange=exchange, durable=True, exchange_type='topic')
#     # 声明收容队列
#     message.channel.queue_declare(queue=queue, durable=True)
#     # 收容队列和收容交换机绑定
#     message.channel.queue_bind(exchange=exchange, queue=queue)
#     # 设置延迟队列参数
#     arguments = {
#         'x-message-ttl': 1000 * 60,  # 延迟时间 （毫秒）
#         'x-dead-letter-exchange': exchange,  # 延迟结束后指向交换机（死信收容交换机）
#         'x-dead-letter-routing-key': queue,  # 延迟结束后指向队列（死信收容队列）
#     }
# # 声明队列
# message.channel.exchange_declare(exchange=delay_exchange, exchange_type='topic', durable=True)
# # 声明交换机
# message.channel.queue_declare(queue=delay_queue, durable=True, arguments=arguments)
# # 队列和交换机绑定
# message.channel.queue_bind(exchange=delay_exchange, queue=delay_queue)
# # 队列参数
# data = {
#     'date': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
# }
# # 加入队列
# message.channel.basic_publish(
#     routing_key=queue, body=json.dumps(data),
#     properties=pika.BasicProperties(delivery_mode=2),
#     exchange=exchange
# )
# message.close()



message = MessageMQ()
#
# order = {
#     'id': 'order',
#     'date': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
# }
# message.order_charge(body=order, expiration='60000')



# order1 = {
#     'id': 'order1',
#     'date': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
# }
# message.order_charge(body=order1)



data = {
    'date': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
    'phone': '13771073133',
    'hard_number': '100-000002',
    'token': '123456789kkkkkkkkkk'
}
message.shopping_tips(body=data)



# order2 = {
#     'id': 'SC21312312321321',
#     'date': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
# }
# message.timely_message(body=order2)



# order3 = {
#     'id': 'order3',
#     'date': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
#     'phone': '13771073133',
#     'hard_number': '100-000002',
#     'token': '123456789kkkkkkkkkk'
# }
# message.timing_task(body=order3, expires=1000*10)

