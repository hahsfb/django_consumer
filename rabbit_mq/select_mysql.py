# !/usr/bin/python3

import pymysql

# 打开数据库连接
db = pymysql.connect("127.0.0.1", "root", "root", "test")

# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()
try:
    # 使用 execute()  方法执行 SQL 查询
    cursor.execute(
        "select mid, door_state, lock_state, token, restart_time,tag from cli_machine where mid in ('100-000002', '10017');")

    # # 提交到数据库执行
    # db.commit()
    print(cursor.rownumber)
    # 使用 fetchone() 方法获取单条数据.
    data = cursor.fetchone()
    while data != None:
        print(data, cursor.rownumber)
        data = cursor.fetchone()

    # print("Database version : %s " % data)
    data = cursor.fetchone()
    print(data)

    # 关闭数据库连接
    db.close()
except:
   # 发生错误时回滚
   db.rollback()

