#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File    : redis.py
@Author  : HaoQiangJian
@Site    : 
@Time    : 18-9-20 下午12:03
@Version : 
"""

from redis import StrictRedis
import pickle
from .config import REDIS_DB, REDIS_HOST, REDIS_PORT, REDIS_PWD


class Redis:

    def __init__(self):
        self.rcon = StrictRedis(REDIS_HOST, REDIS_PORT, REDIS_DB, password=REDIS_PWD)

    def set_data(self, key, data, ex=None, px=None):
        """
        将内存数据二进制通过序列号转为文本流，再存入redis
        Set the value at key ``name`` to ``value``

        ``ex`` sets an expire flag on key ``name`` for ``ex`` seconds.

        ``px`` sets an expire flag on key ``name`` for ``px`` milliseconds.
        """
        print('----set_data----------------------')
        self.rcon.set(pickle.dumps(key), pickle.dumps(data), ex=ex, px=px)

    def get_data(self, key):
        """将文本流从redis中读取并反序列化，返回"""
        print('----get_data----------------------')
        data = self.rcon.get(pickle.dumps(key))
        if data is None:
            return None
        return pickle.loads(data)

    def del_data(self, key):
        """删除"""
        print('----del_data----------------------')
        data = self.rcon.delete(pickle.dumps(key))
        if data is None:
            return None
        return data

    def rpush_data(self, name, value):
        """
        Redis操作List 尾部增加
        :param name:
        :param value:
        :return:
        """
        print('----rpush_data----------------------')
        self.rcon.rpush(pickle.dumps(name), pickle.dumps(value))

    def lrange_data(self, name):
        """
        获取List中所有元素
        :param name:
        :return:
        """
        print('----lrange_data----------------------')
        data = []
        for item in self.rcon.lrange(pickle.dumps(name), 0, -1):
            data.append(pickle.loads(item))
        return data

    def lpop_data(self, name):
        """
        移除List中第一个元素
        :param name:
        :return:
        """
        print('----lpop_data----------------------')
        data = self.rcon.lpop(pickle.dumps(name))
        if data is None:
            return None
        return pickle.loads(data)

    def llen(self, name):
        """
        获取列表长度
        :param name:
        :return:
        """
        print('----llen----------------------')
        return self.rcon.llen(pickle.dumps(name))
