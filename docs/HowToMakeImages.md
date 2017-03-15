# This File is Depreciated

Raspberry Pi Zero version should work with latest code version.

# How to make Eggduino mAcron Environment

This file just record some steps of make the eggduino mAcron environment.
It is **NOT** a complete documents.

## Intel Edison 

tty.usbserial-A402EXKV

screen tty.usbserial-A402EXKV 115200

Install yocto image

Device Name : eggduino

User: root
Password : eggduino

=====================

opkg update

http://iotdk.intel.com/repos/3.5/iotdk/edison/core2-32/

opkg install python-pyserial python-simplejson python-sqlite3 python-pip



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




