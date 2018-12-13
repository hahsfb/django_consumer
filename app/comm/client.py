# -*- coding:utf-8 -*-
"""
@datetime:2018/11/29 9:23
@author: gjh
"""

import socket
import os
import time

name = socket.gethostname()
# host = "39.105.118.178"
host = "192.168.3.104"
port = 6009

OPEN = False
# config = "./ip.txt"
ip = ""

while True:
    mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    mySocket.connect((host, port))
    print("连接到服务器", name)
    mySocket.send(name.encode())
    msg = mySocket.recv(1024)
    Receive = msg.decode("utf-8")
    _in = input("输入数字 0： ")
    mySocket.send(_in.encode())
    mySocket.close()
    time.sleep(1)
