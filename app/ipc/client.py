# -*- coding:utf-8 -*-
"""
@datetime:2018/12/25 2:45
@author: gjh
"""
import threading
from websocket import create_connection
import json
import time, datetime
ws_server = "ws://bizkf.bigmeddata.com:30008/websocket/"
# ws_server = "ws://127.0.0.1:30008/websocket/"
ws = create_connection(ws_server)

machine_id = "658-125412"


def keepalive():
    for i in range(10):
        time.sleep(1)
        ws.send(123)
        print(ws)


def create_connect(wb_url, mid):
    dict1 = {
        "command": "start-up",
        "machine_id": mid
    }
    ws.send(json.dumps(dict1))
    return ws


wb_obj = create_connect(ws_server, machine_id)
# dict1 = {
#     "command": "start-up",
#     "machine_id": "100-100002"
# }
# ws.send(json.dumps(dict1))
# ws.send("kjhkh")
# ws.send("1231231")
#
# ws.send("1231231")
# ws.send("=======")
# ws.send("1231231")
# print(ws.headers)


def check_if_door_open():
    global b_allow_unlock, tag, wb_obj, token
    while 1:
        try:
            rt = wb_obj.recv()
            print("阻塞")
        except Exception as error:
            print(error)
            print("尝试重连长连接...")
            wb_obj = None
            wb_obj = create_connect(ws_server, machine_id)
            if wb_obj:
                try:
                    # comm_server.continue_upload_videos(machine_id)
                    rt = wb_obj.recv()    #阻塞
                except Exception as e:
                    print(e)
                    time.sleep(1)
                    continue
            else:
                time.sleep(1)
                continue
        print("-------------收到命令----------------")
        try:
            result = json.loads(rt)
            print(result, 'command', result['command'])
            print("-------------命令----------------")
            if 'command' in result.keys():
                if result['command'] == 'unlock':
                    mid = result['machine_id']
                    if machine_id == mid:
                        print('打开门。。。。')
                        # door_control.unlock()
            if result['lock_state'] == '0':
                token = result['token']
                tag = result['tag']
                n_time = int(time.mktime(datetime.datetime.now().timetuple()))
                if token != '':
                    lst = int(token[:10])
                else:
                    lst = n_time
                if n_time - lst < 60:
                    b_allow_unlock = True
                else:
                    b_allow_unlock = False
                    # comm_server.close_door(dor_id)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    res_dict = {"sensor_status": "NORMAL", "hard_number": machine_id, "humidity": str(30), "temperature": str(20),
                "camera_status": "NORMAL", "network_status": "ONLINE", "command": "heart-beat"}
    ws.send(json.dumps(res_dict))
    check_if_door_open()
    # dict1 = {"command": "heart-beat"}
    # while True:
    #     print("----")
    #     msg = ws.recv()
    #     res_dict = {"sensor_status": "NORMAL", "hard_number": "100-100002", "humidity": str(30), "temperature": str(20),
    #                 "camera_status": "NORMAL", "network_status": "ONLINE", "command": "heart-beat"}
    #     ws.send(json.dumps(res_dict))
    #     print(msg)
    #     time.sleep(10)