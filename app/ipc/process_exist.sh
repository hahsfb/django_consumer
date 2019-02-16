#!/usr/bin/env bash
while true
do
        process=`ps -aux | grep mysqld | grep -v grep`;

        if ["$process" == ""]; then
                sleep 1;
                echo "process 不存在,开始执行";
                mysql;
        else
                echo "process exsits";
                break;
        fi
done
