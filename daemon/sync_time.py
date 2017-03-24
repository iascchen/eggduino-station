#!/usr/bin/python
# -*- coding: utf-8 -*-

from time import time, sleep
import datetime
import ntplib
import os
import serial

cmds_send_interval = 1
msg_wait_interval = 0.1
wait_timeout_times = 10

# For Edison
# uart = mraa.Uart(0)
# print uart.getDevicePath()
# ser = serial.Serial(uart.getDevicePath(), 9600)

# For Raspberry Pi Zero
# ser = serial.Serial('/dev/ttyAMA0', 9600)

# For Raspberry Pi 3
ser = serial.Serial('/dev/serial0', 9600)

##################
# Utils
##################


current_milli_time = lambda: int(round(time() * 1000))


def int_to_hexstr(value):
    return '{:02x}'.format(value)


def utc_string_for_ab05(ts):
    year = int_to_hexstr(ts.year - 2000)
    month = int_to_hexstr(ts.month)
    day = int_to_hexstr(ts.day)
    hour = int_to_hexstr(ts.hour)
    minute = int_to_hexstr(ts.minute)
    second = int_to_hexstr(ts.second)
    weekday = int_to_hexstr(ts.weekday())

    return year + month + weekday + day + hour + minute + second


##################
# Get Time
##################

def utp_time():
    c = ntplib.NTPClient()
    response = c.request('europe.pool.ntp.org', version=3)
    return datetime.datetime.utcfromtimestamp(response.tx_time)


def set_sys_datetime(dt):
    cmd = "date -s '{0}'".format(dt)
    print "\tSYSTEM CMD : ", cmd
    os.system(cmd)


def fetch_rtc():
    ser.write("AB05\n")

    wait = wait_timeout_times  # wait 5 * msg_wait_interval
    while wait > 0:
        msg = ser.readline().strip()  # Read the newest output from the Eggduino

        if msg.startswith("Ti"):
            # print "RTC MSG : ", msg
            rtc_now = datetime.datetime.strptime(msg, 'Ti;%Y;%m;%d;%H;%M;%S')
            # print "RTC NOW : ", rtc_now
            return rtc_now

        wait -= 1
        sleep(msg_wait_interval)  # Delay for one tenth of a second
        if wait == 0:
            print "!!! RTC query time Out"


def set_rtc(dt):
    cmd = "AB05{0}".format(utc_string_for_ab05(dt))
    print "\tRTC SET : ", cmd
    ser.write(cmd + "\n")


###########################################
###########################################

print "Before TimeSync : ", datetime.datetime.now()
print "\tRTC : ", fetch_rtc()

try:
    now = utp_time()
    print "Use UTP : ", now
    # print "UTP", utc_string_for_ab05(now)
    set_rtc(now)
    set_sys_datetime(now)

    print "After TimeSync : "
    print "\tSYS : ", datetime.datetime.now()
    # print "\tUTP : ", utp_time()
    print "\tRTC : ", fetch_rtc()

except:
    now = fetch_rtc()
    print "Use RTC : ", now
    set_sys_datetime(now)

    print "After TimeSync : "
    print "\tSYS : ", datetime.datetime.now()
    print "\tRTC : ", fetch_rtc()

