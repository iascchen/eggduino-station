#!/usr/bin/python

from time import sleep

import time, readline, thread, sys

import serial

# For Edison
# uart = mraa.Uart(0)
# print uart.getDevicePath()
# ser = serial.Serial(uart.getDevicePath(), 9600)

# For Raspberry Pi Zero
# ser = serial.Serial('/dev/ttyAMA0', 9600)

# For Raspberry Pi 3
ser = serial.Serial('/dev/serial0', 9600)

def noisy_thread():
    while True:
        print ser.readline()  # Read the newest output from the Arduino
        # sleep(.1)  # Delay for one tenth of a second


thread.start_new_thread(noisy_thread, ())
while True:
    s = raw_input('> ')
    ser.write(s + '\n')
    # print s
