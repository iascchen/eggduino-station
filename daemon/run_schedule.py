#!/usr/bin/python
# -*- coding: utf-8 -*-

from time import time, sleep
import sched

schedule = sched.scheduler(time.time, time.sleep)


def perform_command(cmd, inc):
    #    os.system(cmd)
    print(time.time())
    print('zhixing写入数据库', time.time() - tt)
    global tt
    tt = time.time()


def timming_exe(cmd, inc=60):
    # enter用来安排某事件的发生时间，从现在起第n秒开始启动
    schedule.enter(inc, 0, perform_command, (cmd, inc))
    #  # 持续运行，直到计划时间队列变成空为止
    schedule.run()


if __name__ == '__main__':
    tt = time.time()
    print("show time after 5 seconds:", tt)
    timming_exe("echo %time%", 5)
