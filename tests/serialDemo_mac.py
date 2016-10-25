#!/usr/bin/python
# -*- coding: utf-8 -*-

from time import time, sleep
import sqlite3
import serial
import struct
import argparse

##########################
# Parse input params
##########################

parser = argparse.ArgumentParser(description='Example : AB0100,AB0200,AB0200,AB010105,AB020105,AB030101')
parser.add_argument('-c', '--cmds', help='delimited list input', type=str)
args = parser.parse_args()

if args.cmds is None:
    args.cmds = ''
print(args)

params_cmds_list = args.cmds.upper().split(',')

##########################
# Important Variables
##########################

CMD_T = 'AB010105'
CMD_H = 'AB020105'
CMD_Q = 'AB030101'

CMD_T_STOP = 'AB0100'
CMD_H_STOP = 'AB0200'
CMD_Q_STOP = 'AB0300'

ser = serial.Serial("/dev/tty.usbserial-A900gdaE", 9600)
# ser = serial.Serial('/dev/ttyMFD1', 9600)
conn = sqlite3.connect('../db/database.db')

cmds_send_interval = 0.5
msg_wait_interval = 0.1

init_cmds = [CMD_T_STOP, CMD_H_STOP, CMD_Q_STOP, CMD_T, CMD_H, CMD_Q]
# init_cmds = [CMD_T_STOP, CMD_T]
# init_cmds = [CMD_Q_STOP, CMD_Q]
# init_cmds = [CMD_H_STOP, CMD_H]

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

MSG_CMD_TEM = 'BB'
TEM_NUM = 16

MSG_CMD_HUM = 'CC'
HUM_NUM = 1

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

def hex_to_quat(hex_str):
    value = struct.unpack('h', hex_str.decode("hex"))
    ret = value[0] / 16384.0
    return float("{0:.3f}".format(ret))


def hex_to_hum(hex_str):
    value = struct.unpack('H', hex_str.decode("hex"))
    ret = -6.0 + 125.0 * (value[0] / 65535.0)
    return float("{0:.3f}".format(ret))


def hex_to_tem(hex_str):
    print hex_str
    value = struct.unpack('h', hex_str.decode("hex"))
    print value
    ret = 0.125 * value[0] >> 5

    return float("{0:.3f}".format(ret))


def dispatch_messages(msg):
    print '%s , %d' % (msg, len(msg))

    if msg.startswith(MSG_START + MSG_CMD_HUM) and len(msg) >= DATA_START_INDEX + HUM_NUM * DATA_LEN:
        e_hum = hex_to_hum(msg[DATA_START_INDEX: DATA_START_INDEX + DATA_LEN * HUM_NUM])
        print (e_hum)

        ts = int(time() * 10)
        conn.execute(INSERT_EGG_HUMINITY, (ts, e_hum))
        conn.commit()

    elif msg.startswith(MSG_START + MSG_CMD_TEM) and len(msg) >= DATA_START_INDEX + TEM_NUM * DATA_LEN:
        t = []
        for i in range(0, TEM_NUM):
            start_index = DATA_START_INDEX + i * DATA_LEN
            end_index = start_index + DATA_LEN
            t.append(hex_to_tem(msg[start_index:end_index]))

        print t

        # ts = int(time() * 10)
        # conn.execute(INSERT_EGG_TEMPERATURES, (ts, t[0], t[1], t[2], t[3], t[4], t[5], t[6], t[7],
        #                                        t[8], t[9], t[10], t[11], t[12], t[13], t[14], t[15]))
        # conn.commit()

    elif msg.startswith(MSG_START + MSG_CMD_MPU) and len(msg) >= DATA_START_INDEX + MPU_NUM * DATA_LEN:

        q = []
        for i in range(0, MPU_NUM):
            start_index = DATA_START_INDEX + i * DATA_LEN
            end_index = start_index + DATA_LEN
            q.append(hex_to_quat(msg[start_index:end_index]))

        print q

        ts = int(time() * 10)
        conn.execute(INSERT_EGG_QUATERNIONS, (ts, q[0], q[1], q[2], q[3]))
        conn.commit()

    elif msg.startswith(MSG_CMD_STA):
        ret_array = msg[STA_START_INDEX:].split(';')

        if len(ret_array) >= STA_NUM:
            s_tem = float(ret_array[0])
            s_hum = float(ret_array[1])
            s_lex = float(ret_array[2])
            print (s_tem, s_hum, s_lex)

            ts = int(time() * 10)
            conn.execute(INSERT_STATION, (ts, s_hum, s_lex, s_tem))
            conn.commit()
    return


def start_egg_notify(cmds):
    print "Start Egg Notification ..."

    for cmd in cmds:
        print 'command send :', cmd
        ser.write(cmd + '\n')
        sleep(cmds_send_interval)


##########################
# Main Process
##########################

if params_cmds_list != ['']:
    init_cmds = params_cmds_list

start_egg_notify(init_cmds)

while True:
    msg = ser.readline().strip()  # Read the newest output from the Arduino
    dispatch_messages(msg)

    if msg == '436F6E6E6563746564':
        start_egg_notify(init_cmds)

    sleep(msg_wait_interval)  # Delay for one tenth of a second
