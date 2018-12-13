# -*- coding:utf-8 -*-
"""
@datetime:2018/11/29 9:41
@author: gjh
"""
import time
from socketserver import BaseRequestHandler, ThreadingTCPServer
import pymysql

BUF_SIZE = 1024
min_port = 6000
max_port = 6010


class Handler(BaseRequestHandler):
    def handle(self):
        address, pid = self.client_address
        print('%s connected!' % address, type(address))
        data = self.request.recv(BUF_SIZE).decode()
        print("----------------------------------")
        while True:
            rts = find_data(data)
            if rts:
                s = rts[0][4]
                print(rts)
            else:
                continue
            if s:
                self.request.sendto("{}".format("开门").encode("utf-8"), (address, PORT))
                return_msg = self.request.recv(BUF_SIZE).decode()
                update_status(_ip=address, status=int(return_msg))
            else:
                time.sleep(1.5)


def connect_db():
    d = pymysql.connect("192.168.3.104", "root", "123456", "cross")
    return d, d.cursor()


def add_data(_ip, _port, _ipc_name):
    sql = "insert into open_port(ip, port, ipc_name) values(%s, %s, %s);"
    cursor.execute(sql, (_ip, _port,  _ipc_name))
    try:
        db.commit()
        return True
    except Exception as e:
        print(e)
        db.rollback()
        return False


def find_data(ipc_name):
    try:
        sql = "SELECT * FROM open_port Where ipc_name=%s"
        cursor.execute(sql, (ipc_name,))
    except Exception as e:
        return None
    return cursor.fetchall()


def fina_all_data():
    sql = "SELECT * FROM open_port"
    cursor.execute(sql)
    return cursor.fetchall()


def deal_data(*kwargs):
    res = [x[2] for x in kwargs]
    return res


def update_status(_ip, status):
    sql = "UPDATE open_port SET `status` = %s WHERE ip = %s"
    s = cursor.execute(sql, (status, _ip))
    return s


if __name__ == '__main__':
    HOST = "192.168.3.104"
    PORT = 6009
    ADDR = (HOST, PORT)
    db, cursor = connect_db()
    # ddd = fina_all_data()
    ports = set([x for x in range(min_port, max_port+1)])
    work_port = set([])
    server = ThreadingTCPServer(ADDR, Handler)
    server.serve_forever()
    print(server)
    db.close()
