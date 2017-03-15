# How to make Eggduino mAcron Environment —— Raspberry Pi Zero

This file just record some steps of make the eggduino mAcron environment.
It is **NOT** a complete documents.

## Raspberry Pi Zero

### On PC

    ls /dev/tty.usbserial*
    screen /dev/tty.usbserial-A900gdlA 115200

first login

    User: pi
    Password : raspberry

### System Config

`sudo raspi-config`

1 Change User Password => eggduino
2 Change Hostname => eggduino
5 Interfacing Options => enable ssh
5 Interfacing Options => Disable serial login / Enable serial

### Enable Root SSH Login

`sudo passwd root`
Set password as `eggduino`

`sudo vi /etc/ssh/sshd_config`
Search for `PermitRootLogin` and change it to `yes`.

### ZeroConf

    sudo apt-get install avahi-daemon avahi-utils
    sudo insserv avahi-daemon

### Wifi Network

[Refernce Link](https://www.raspberrypi.org/documentation/configuration/wireless/wireless-cli.md)

Before: 

	pi@eggduino_pi:~$ ifconfig wlan0
	wlan0     Link encap:Ethernet  HWaddr e8:4e:06:2b:87:55
	          inet6 addr: fe80::2ee1:a471:e456:5975/64 Scope:Link
	          UP BROADCAST MULTICAST  MTU:1500  Metric:1
	          RX packets:0 errors:0 dropped:50 overruns:0 frame:0
	          TX packets:0 errors:0 dropped:0 overruns:0 carrier:0
	          collisions:0 txqueuelen:1000
	          RX bytes:0 (0.0 B)  TX bytes:0 (0.0 B)


	pi@eggduino_pi:~$sudo iwlist wlan0 scan

	pi@eggduino_pi:~$ sudo su
	root@eggduino_pi:/home/pi# wpa_passphrase %wifissidname %wifipassword >> /etc/wpa_supplicant/wpa_supplicant.conf
	
	wpa_passphrase Microduino MakerModule2015 >> /etc/wpa_supplicant/wpa_supplicant.conf

Make sure

	pi@eggduino_pi:~$ wpa_passphrase %wifissidname %wifipassword
	pi@eggduino_pi:~$ sudo vi /etc/wpa_supplicant/wpa_supplicant.conf

Enable 

	pi@eggduino_pi:~$ sudo wpa_cli reconfigure
	Selected interface 'wlan0'
	OK

	pi@eggduino_pi:~$ ifconfig wlan0
	wlan0     Link encap:Ethernet  HWaddr e8:4e:06:2b:87:55
	          inet addr:192.168.9.213  Bcast:192.168.9.255  Mask:255.255.255.0
	          inet6 addr: fe80::dc1a:e088:5aec:bea1/64 Scope:Link
	          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
	          RX packets:181 errors:0 dropped:100 overruns:0 frame:0
	          TX packets:145 errors:0 dropped:1 overruns:0 carrier:0
	          collisions:0 txqueuelen:1000
	          RX bytes:34561 (33.7 KiB)  TX bytes:22900 (22.3 KiB)

	pi@eggduino_pi:~$

### Work as Wifi AP

https://cdn-learn.adafruit.com/downloads/pdf/setting-up-a-raspberry-pi-as-a-wifi-access-point.pdf 

### Serials Setting

    pi@eggduino:~/workshops/eggduino-station/tests $ ls /dev/ttyAMA0 -ls
    0 crw-rw-rw- 1 root tty 204, 64 Mar 13 15:51 /dev/ttyAMA0
    sudo chmod 666 /dev/ttyAMA0
    
    sudo adduser pi tty

### Software Install

    sudo apt-get update
    sudo apt-get upgrade
    
    sudo apt-get install python-simplejson python-pip sqlite3
    pip install pyserial ntplib
    
[SQLite3 Reference](https://iotbytes.wordpress.com/sqlite-db-on-raspberry-pi/)

=====================


## Wifi Configuration

http://rwx.io/blog/2015/08/16/edison-wifi-config/

configure_edison --wifi

wpa_cli status

cd /etc/wpa_supplicant
vi wpa_supplicant.conf
systemctl stop wpa_supplicant
systemctl start wpa_supplicant

--------------
AP mode
--------------

systemctl stop wpa_supplicant
systemctl start hostapd




