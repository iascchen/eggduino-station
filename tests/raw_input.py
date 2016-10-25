#!/usr/bin/python

from time import sleep

import mraa
import serial
import time, readline, thread, sys

uart = mraa.Uart(0)
ser = serial.Serial(uart.getDevicePath(), 9600)


def noisy_thread():
    while True:
        print ser.readline()  # Read the newest output from the Arduino
        # sleep(.1)  # Delay for one tenth of a second


thread.start_new_thread(noisy_thread, ())
while True:
    s = raw_input('> ')
    ser.write(s + '\n')
    # print s
