from time import sleep

import mraa
import serial

uart = mraa.Uart(0)
ser = serial.Serial(uart.getDevicePath(), 9600)

# > stty -F /dev/ttyMFD1
# speed 9600 baud; line = 0;
# min = 0; time = 0;
# -brkint -icrnl -imaxbel
# -opost
# -isig -icanon -iexten -echo -echoe -echok -echoctl -echoke


while True:
     print ser.readline() # Read the newest output from the Arduino
     sleep(.1) # Delay for one tenth of a second
