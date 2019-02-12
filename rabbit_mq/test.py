#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File    : test.py
@Author  : HaoQiangJian
@Site    : 
@Time    : 18-12-12 下午4:56
@Version : 
"""
import time



if __name__ == '__main__':
    dtime = "2018-12-12 17:00:00"  # 转换成时间数组
    timeArray = time.strptime(dtime, "%Y-%m-%d %H:%M:%S")  # 转换成时间戳
    timestamp = time.mktime(timeArray)
    print(timestamp)