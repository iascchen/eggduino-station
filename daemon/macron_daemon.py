#!/usr/bin/python -u
# -*- coding: utf-8 -*-

import argparse
import datetime
import sched
import sqlite3
import struct
import thread
from time import time, sleep

import serial

# import mraa

##########################
# Parse input params
##########################

parser = argparse.ArgumentParser(
    description='Example : AB0100,AB0200,AB0300,AB0400,AB01010f,AB020105,AB03010384,AB040105')
parser.add_argument('-c', '--cmds', help='delimited list input', type=str)
parser.add_argument('-s', '--schedules', help='schedules', type=str)
args = parser.parse_args()

# print(args)

if args.cmds is None:
    args.cmds = ''

params_cmds_list = args.cmds.upper().split(',')

if args.schedules is None:
    args.schedules = ''

params_schedules = args.schedules.upper().strip()

##########################
# Important Variables
##########################

CMD_T = 'AB0101'
CMD_H = 'AB0201'
CMD_Q = 'AB0301'
CMD_S = 'AB0401'
CMD_RTC = 'AB05'

# CMD_T_MIN = 'AB010101'       # interval 1s and get data 16s, it will be about 20s return 1 record
# CMD_H_MIN = 'AB020105'
# CMD_Q_MIN = 'AB030102'
# CMD_S_MIN = 'AB040105'

CMD_T_STOP = 'AB0100'
CMD_H_STOP = 'AB0200'
CMD_Q_STOP = 'AB0300'
CMD_S_STOP = 'AB0400'

# For Edison
# uart = mraa.Uart(0)
# print uart.getDevicePath()
# ser = serial.Serial(uart.getDevicePath(), 9600)

# For Raspberry Pi Zero
# ser = serial.Serial('/dev/ttyAMA0', 9600)

# For Raspberry Pi 3
ser = serial.Serial('/dev/serial0', 9600)

cmds_send_interval = 1
msg_wait_interval = 0.1

stop_cmds = [CMD_T_STOP, CMD_H_STOP, CMD_Q_STOP, CMD_S_STOP]
init_cmds = stop_cmds + [CMD_T, CMD_H, CMD_Q, CMD_S]

##########################
# Const
##########################

MSG_START = "AABB"
MSG_END = "0D0A"

DATA_LEN = 4
DATA_START_INDEX = 6
STA_START_INDEX = 3

MSG_CMD_MPU = 'AA'
MPU_NUM = 4
MPU_LEN = 38

MSG_CMD_TEM = 'BB'
TEM_NUM = 16

MSG_CMD_HUM = 'CC'
HUM_NUM = 1
HUM_LEN = 14

MSG_CMD_STA = 'Ma;'
STA_NUM = 3

INSERT_EGG_TEMPERATURES = '''INSERT INTO messages
    (ts, temp_01, temp_02, temp_03, temp_04, temp_05, temp_06, temp_07, temp_08,
    temp_09, temp_10, temp_11, temp_12, temp_13, temp_14, temp_15, temp_16)
    VALUES
    (?,   ?,?,?,?,?,?,?,?,   ?,?,?,?,?,?,?,?) '''

INSERT_EGG_QUATERNIONS = '''INSERT INTO messages (ts, quat_w, quat_x, quat_y, quat_z) VALUES (?,   ?,?,?,?) '''

INSERT_EGG_HUMINITY = '''INSERT INTO messages (ts, hum) VALUES (?,   ?) '''

INSERT_STATION = '''INSERT INTO messages (ts, hum_s, light_s, temp_s) VALUES (?,   ?,?,?) '''

##########################
# Functions
##########################

current_milli_time = lambda: int(round(time() * 1000))


def int_to_hexstr(value):
    return '{:02x}'.format(value)


def utc_string():
    now = datetime.datetime.utcnow()

    year = int_to_hexstr(now.year - 2000)
    month = int_to_hexstr(now.month)
    day = int_to_hexstr(now.day)
    hour = int_to_hexstr(now.hour)
    minute = int_to_hexstr(now.minute)
    second = int_to_hexstr(now.second)
    weekday = int_to_hexstr(now.weekday())

    return year + month + weekday + day + hour + minute + second


def hex_to_quat(hex_str):
    value = struct.unpack('h', hex_str.decode("hex"))
    ret = value[0] / 16384.0
    return float("{0:.3f}".format(ret))


def hex_to_hum(hex_str):
    value = struct.unpack('H', hex_str.decode("hex"))
    ret = -6.0 + 125.0 * (value[0] / 65535.0)
    return float("{0:.3f}".format(ret))


def hex_to_tem(hex_str):
    value = struct.unpack('h', hex_str.decode("hex"))
    ret = 0.125 * (value[0] >> 5)
    return float("{0:.3f}".format(ret))


def dispatch_messages(msg):
    conn = sqlite3.connect('./db/database.db')

    print msg

    # Humidity
    if msg.startswith(MSG_START + MSG_CMD_HUM) and len(msg) == HUM_LEN:
        e_hum = hex_to_hum(msg[DATA_START_INDEX: DATA_START_INDEX + DATA_LEN * HUM_NUM])

        ts = current_milli_time()
        print ' -> ', ts, e_hum
        conn.execute(INSERT_EGG_HUMINITY, (ts, e_hum))
        conn.commit()

    # Temperatures
    elif msg.startswith(MSG_START + MSG_CMD_TEM) and len(msg) >= DATA_START_INDEX + TEM_NUM * DATA_LEN:
        t = []
        for i in range(0, TEM_NUM):
            start_index = DATA_START_INDEX + i * DATA_LEN
            end_index = start_index + DATA_LEN
            t.append(hex_to_tem(msg[start_index:end_index]))

        ts = current_milli_time()
        print ' -> ', ts, t
        conn.execute(INSERT_EGG_TEMPERATURES, (ts, t[0], t[1], t[2], t[3], t[4], t[5], t[6], t[7],
                                               t[8], t[9], t[10], t[11], t[12], t[13], t[14], t[15]))
        conn.commit()

    # Quaternions
    elif msg.startswith(MSG_START + MSG_CMD_MPU) and len(msg) == MPU_LEN:
        # MPU will return 7 data : ax,ay,az,qw,qx,qy,qz, we only need qw,qx,qy,qz
        q = []
        for i in range(3, 3 + MPU_NUM):
            start_index = DATA_START_INDEX + i * DATA_LEN
            end_index = start_index + DATA_LEN
            q.append(hex_to_quat(msg[start_index:end_index]))

        ts = current_milli_time()
        print ' -> ', ts, q

        conn.execute(INSERT_EGG_QUATERNIONS, (ts, q[0], q[1], q[2], q[3]))
        conn.commit()

    elif msg.startswith(MSG_CMD_STA):
        ret_array = msg[STA_START_INDEX:].split(';')

        if len(ret_array) >= STA_NUM:
            s_tem = float(ret_array[0])
            s_hum = float(ret_array[1])
            s_lex = float(ret_array[2])

            ts = current_milli_time()
            print ' -> ', ts, (s_tem, s_hum, s_lex)

            conn.execute(INSERT_STATION, (ts, s_hum, s_lex, s_tem))
            conn.commit()

    conn.close()
    return


def start_egg_notify(cmds):
    print "==> Start Egg Notification ..."

    for cmd in cmds:
        print '\t==> command sending :', cmd.strip()
        ser.write(cmd.strip() + '\n')
        sleep(cmds_send_interval)


def load_schedules(schedules_str):
    schedule = sched.scheduler(time, sleep)

    time_offset = 0
    for task in schedules_str.split("\n"):
        print "==> ", task
        task_parts = task.split(":")

        try:
            cmds = task_parts[0]
            if not cmds.startswith("#"):
                time_sleep = int(task_parts[1])
                schedule.enter(time_offset, 0, start_egg_notify, [stop_cmds + cmds.split(",")])
                time_offset += time_sleep
        except:
            pass

    schedule.run()


##########################
# Main Process
##########################

if params_cmds_list != ['']:
    init_cmds = params_cmds_list
    start_egg_notify(init_cmds)

# params_schedules = '''
# # ab0101,ab0201,ab0301,ab0401:20
# # ab0201,ab0201,ab0301,ab0401:20
# # ab0301,ab0201,ab0301,ab0401:20
# ab0401,ab0201,ab0301,ab0401:20
# ab0501,ab0201,ab0301,ab0401:20
# ab0601,ab0201,ab0301,ab0401:20
# '''

if params_schedules != '':
    thread.start_new_thread(load_schedules, (params_schedules,))


def show_data():
    while True:
        msg = ser.readline().strip()  # Read the newest output from the Eggduino
        dispatch_messages(msg)

        if msg == '436F6E6E65637465640D0A':  # Connected
            # start_egg_notify(init_cmds)

            if params_cmds_list != ['']:
                start_egg_notify(init_cmds)

            if params_schedules != '':
                # TODO ： Need Test. If uncomment these sentense, maybe have two thread of run schedules
                # thread.start_new_thread(load_schedules, (params_schedules,))
                pass

        sleep(msg_wait_interval)  # Delay for one tenth of a second


thread.start_new_thread(show_data, ())

while True:
    print ".\n"
    sleep(cmds_send_interval)
