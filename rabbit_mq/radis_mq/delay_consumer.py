# coding: utf8
import time, datetime
from rabbit_mq.radis_mq.delay_queue import DelayQueue


if __name__ == '__main__':

    redis_conf = {'host': '127.0.0.1', 'port': 6379, 'db': 0, 'password': '123456'}
    # 构造延迟队列对象
    queue = DelayQueue(redis_conf)
    # push 20条数据
    for i in range(20):
        item = {'user': 'user-{}'.format(i), 'time': str(datetime.datetime.now())}
        queue.push(item)
        time.sleep(1)

    # # 从延迟队列中马上获取10条数据
    # data = queue.pop(num=10)
    # # 刚添加的马上获取是获取不到的
    # assert len(data) == 10
    # # 休眠10秒
    # time.sleep(10)
    # # 从延迟队列中获取10条数据
    # data = queue.pop(num=10)
    # assert len(data) == 10
    # # 从延迟队列中获取截止到5秒之前添加的10条数据
    # data = queue.pop(num=10, previous=5)
    # assert len(data) == 10
    while True:
        data = queue.pop(num=1)
        if not data:
            time.sleep(1)
        else:
            print(datetime.datetime.now())
            print(data)
