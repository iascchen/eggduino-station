# mAcron for Eggduino
 
(Version 4)
 
This software is a part of Eggduino, a project of [ICBP (International Centre for Birds of Prey)](http://www.icbp.org/index/), supported by microduino and their friends.

Support eggduino hardware firmware version : **VultureEgg_0.2.C14.00.hex**. Related project is [https://github.com/lixianyu/VultureEgg141](https://github.com/lixianyu/VultureEgg141)

## License 

Author : Hao CHEN
Email : iascchen (at) gmail.com

You can modify and distribute these code freely for education and scientific research, under the license of [Apache License 2.0](LICENSE) 

## Software Architecture

                       |
                      BLE
         Smart Egg ----|--->  mAcron Daemon --------> SQLite --------> mAcron Web App
                       |     (Recieve datas)                           (Visualization)
                       |
    Eggduino Hardware  |                 Eggduino Station 
                       |

## Connect to mAcron

running on Raspberry Pi 3

OS : 2017-03-02-raspbian-jessie

### Connect with USB

You can use Putty(Win) or Term2(Mac) 

#### Ethernet

The network structure show as follow:

                        BLE                       Ethernet            Wifi／Ethernet
    Eggduino Hardware  ----->  Eggduino Station  --------->  Router  <--------------  Your computer
    
Connect the raspberry pi 3 to the same router with your computer. Use name `eggduino.local` to access it. 

### Connect with SSH

Username is `root`, and password is `eggduino`

	#### Connect with SSH from your Computer

	$ ssh root@eggduino.local
	root@eggduino.local's password: eggduino
	
	The programs included with the Debian GNU/Linux system are free software;
	the exact distribution terms for each program are described in the
	individual files in /usr/share/doc/*/copyright.
	
	Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
	permitted by applicable law.
	Last login: Mon Mar 20 10:17:50 2017 from fe80::1cf7:ee6:4c83:8254%wlan0
	root@eggduino:~#

#### Setting Wireless Connection

The network structure show as follow:

                        BLE                       Wifi           Wifi
    Eggduino Hardware  ----->  Eggduino Station  -----> Router  <-----  Your computer

Here recorded the steps of wifi configuration, you can change the setting according to your wireless network. [Reference Link](https://www.raspberrypi.org/documentation/configuration/wireless/wireless-cli.md)

Before: 

	root@eggduino:~# ifconfig wlan0
	wlan0     Link encap:Ethernet  HWaddr e8:4e:06:2b:87:55
	          inet6 addr: fe80::2ee1:a471:e456:5975/64 Scope:Link
	          UP BROADCAST MULTICAST  MTU:1500  Metric:1
	          RX packets:0 errors:0 dropped:50 overruns:0 frame:0
	          TX packets:0 errors:0 dropped:0 overruns:0 carrier:0
	          collisions:0 txqueuelen:1000
	          RX bytes:0 (0.0 B)  TX bytes:0 (0.0 B)


	root@eggduino:~# iwlist wlan0 scan
	root@eggduino:~# wpa_passphrase %wifissidname% %wifipassword% >> /etc/wpa_supplicant/wpa_supplicant.conf
	
for example：
	
	wpa_passphrase Microduino MakerModule2015 >> /etc/wpa_supplicant/wpa_supplicant.conf

Make sure the wireless setting is saved：

	root@eggduino:~# vi /etc/wpa_supplicant/wpa_supplicant.conf

Enable 

	root@eggduino:~# wpa_cli reconfigure
	Selected interface 'wlan0'
	OK

	root@eggduino:~# ifconfig wlan0
	wlan0     Link encap:Ethernet  HWaddr e8:4e:06:2b:87:55
	          inet addr:192.168.9.213  Bcast:192.168.9.255  Mask:255.255.255.0
	          inet6 addr: fe80::dc1a:e088:5aec:bea1/64 Scope:Link
	          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
	          RX packets:181 errors:0 dropped:100 overruns:0 frame:0
	          TX packets:145 errors:0 dropped:1 overruns:0 carrier:0
	          collisions:0 txqueuelen:1000
	          RX bytes:34561 (33.7 KiB)  TX bytes:22900 (22.3 KiB)

	root@eggduino:~# 

You can use `wpa_cli status` the check the wireless setting, and got the ip address of eggduino station.

    root@eggduino:~# wpa_cli status
    
## Run mAcron for Eggduino

The source code and data are stored on SD Card. 

    root@eggduino:~# cd workspaces/eggduino-station
    root@eggduino:~/workspaces/eggduino-station# ls
    README.md  config.py   db      manage.py          tests
    app        daemon  requirenments.txt  start_server.sh
    
	root@eggduino:~/workspaces/eggduino-station# python manage.py runserver
    
### Directory Structure

    |- app          ----->   Source code of web server
    |- db           ----->   database.db stored the all data, it is a SQLite file  
    |- daemon       ----->   The daemon to recieve data from eggduino and store them to SQLite
    |- docs         ----->   Markdown file and imgs used on README
    |- tests        ----->   Some test code
    config.py       ----->   config the SQLite Database stored on 'db/database.db'
    start_server.sh ----->   Script to run web server on BACKEND
    README.md       ----->   Please read this file firstly

If you want to get the whole data, you should copy the file under folder 'db', and process it as SQLite DB file.
There are some tools can open SQLite DB file, such as 'DB browser of SQLite' of MAC.
    
### Web Server

#### Run Server

You can start the server by `python manage.py runserver`, you can access the server with http://ip_address:5000

    root@eggduino:~/workspaces/eggduino-station# python manage.py runserver
    /usr/lib/python2.7/site-packages/flask/exthook.py:71: ExtDeprecationWarning: Importing flask.ext.script is deprecated, use flask_script instead.
      .format(x=modname), ExtDeprecationWarning
     * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
     * Restarting with stat
    /usr/lib/python2.7/site-packages/flask/exthook.py:71: ExtDeprecationWarning: Importing flask.ext.script is deprecated, use flask_script instead.
      .format(x=modname), ExtDeprecationWarning
     * Debugger is active!
     * Debugger pin code: 277-916-687

Disable Debug mode, change the `use_debugger=True` to `use_debugger=False`

    root@eggduino:/media/sdcard/mAcron-egg# vi manage.py
    
    ...
    manager.add_command("runserver", Server(host='0.0.0.0', port=5000, use_debugger=False))
    ...

Run Web Server as backend. You can use the shell `./start_server.sh`

    root@eggduino:/media/sdcard/mAcron-egg# nohup python manage.py runserver &
    
    root@eggduino:/media/sdcard/mAcron-egg# tail -f nohup.out
    
Stop backend running Server

    root@eggduino:/media/sdcard/mAcron-egg# ps -ef | grep python
      501 67739     1   0  2:40PM ttys002    0:00.22 python manage.py runserver
      501 67780 63076   0  2:42PM ttys002    0:00.00 grep python
    root@eggduino:/media/sdcard/mAcron-egg# kill -9 67739

    
#### Screen Snapshots

`/Status` show the latest data send from egg and station.

![docs/status_1.png](docs/status_1.png)
![docs/status_2.png](docs/status_2.png)

`/History/Temperatures` show the temperatures of egg in latest one hour.

![docs/temps.png](docs/temps.png)

`/History/Quaternions` show the quaternions of egg in latest one hour.

![docs/quats.png](docs/quats.png)

`/History/Humidity` show the humidity of egg in latest one hour.

![docs/hums.png](docs/hums.png)

`/History/Environment` show the data of station in latest one hour.

![docs/station.png](docs/station.png)

### Run Daemon 

#### As frontend process

When you just want to test the system, you can start daemon in console, and receive data form eggduino. 
In this mode you can interact with it by input interval command. More detail of please read the part of "Change interval when mAcron running as frontend process". 

**But if you close the windows of terminal console, the daemon will be exited too**.

    root@eggduino:/media/sdcard/mAcron-egg# cd daemon/
    root@eggduino:/media/sdcard/mAcron-egg/daemon# ./macron.py -c ab0100,ab0200,ad0300,ab010114,ab020105,ab030102
    
#### As backend process

When you need to let the station collect data continuously, even after you close the terminal console. More detail of command, please read the part of "-c/--cmds The Commands"

You should:

1. Start the daemon as backend. The example show : stop all data push with `ab0100,ab0200,ad0300,ad0400,`, and start data intervals as : temperature 20s(Hex 14), humidity 5s(Hex 05), quaternions 2s(Hex 02), station 20s(Hex 14)
    
        root@eggduino:/media/sdcard/mAcron-egg/daemon# nohup ./macron.py -c ab0100,ab0200,ad0300,ad0400,ab010114,ab020105,ab030102,ab040114 &

2. Check the output information is correct, can use `tail` command as follow, and use `Ctrl+C` exit tail display

        root@eggduino:/media/sdcard/mAcron-egg/daemon# tail -f nohup.out 
    
3. Disconnect the console terminal and leave. 

In this mode, if you want change data interval, you **MUST** kill old process and restart new backend daemon with new interval value.

You should:
    
1. Check the process id of mAcron daemon

        root@eggduino:/media/sdcard/mAcron-egg/daemon# ps -ef | grep macron
    
2. `kill` old process as follow. The XXXX is process id of the daemon. (If you don't understand what i am talking ,you can ask somebody known linux, or goolge ps and kill command of linux)

        root@eggduino:/media/sdcard/mAcron-egg/daemon# kill -9 XXXX
        
3. Restart daemon. The example start intervals as : temperature 40s(Hex 28), humidity 20s(Hex 14), quaternions 10ms(Hex 0a), station 40s(Hex 28)
    
        root@eggduino:/media/sdcard/mAcron-egg/daemon# nohup ./macron.py -c ab0100,ab0200,ad0300,ad0400,ab010128,ab020114,ab0301000a,ab040128 &

#### -c/--cmds The Commands 

**IMPORTANT** If you want to change the data interval, you should send stop before start. for example: 

    ab0100 (press enter) 
    ab010101 (press enter) 

Stop notification

* ab0100 / AB0100 : Stop temperature notification of eggduino
* ab0200 / AB0200 : Stop humidity notification of eggduino
* ab0300 / AB0300 : Stop mpu6050 measurement of eggduino
* ab0400 / AB0400 : Stop station notification

Start notification with default interval

* ab0101 / AB0101 : Start temperature notification with default interval, 20s. its minimal value is 20s
* ab0201 / AB0201 : Start humidity notification with default interval, 70s. its minimal value is 5s
* ab0301 / AB0301 : Start mpu6050 and measurement period is the default interval, 2s. 
* ab0401 / AB0401 : Start station notification with default interval, 5s. its minimal value is 2s

Start notification with setting interval

* ab0101nn / AB0101nn : Start temperature notification with setting interval, for example : set interval as 20s should send ab010114. According the LM75 sensor is slow, only return 1 temperature per second, so if you send `ab010101`, the temperature return interval will be about 16s
* ab0201nn / AB0201nn : Start humidity notification with setting interval, for example : set interval as 5s should send ab020105
* ab0301nnnn / AB0301nnnn : Start quaternions notification with setting interval, the unit is **millis seconds**, for example : set interval as 2ms should send ab03010002. 
* ab0401nn / AB0401nn : Start station notification with setting interval, for example : set interval as 15s should send ab04010f

**nn** is the hex value of seconds. for example : if you want to set interval as `10` seconds, set **nn** as `0a`

**nnnn** is the hex value of **millis seconds**. for example : if you want to set interval as `10` millis seconds, set **nnnn** as `000a`

    // AB03010001 -- start, interval is 1ms;
    // AB03010064 -- start, interval is 100ms;
    // AB0301012C -- start, interval is 300ms;
    // AB03010384 -- start, interval is 900ms;
    // AB03010BB8 -- start, interval is 3000ms;
    // AB03011388 -- start, interval is 5000ms;
    // AB03012710 -- start, interval is 10000ms;

#### Change interval when mAcron running as frontend process

When mAcron is running, you can input interval command

    ...
    AABBAA1E04924032004E2BDF2BB40A750D0D0A
     -> 1477279723265 [0.677, 0.685, 0.167, 0.21]
    > ab0100AABBAAFA03524092004C2B212C060A270D0D0A
     -> 1477279725968 [0.677, 0.69, 0.157, 0.206]
    
    ab0100

	    ==> command sending : AB0100
     
    > Ma;20.9;41.6;165.0
     -> 1477279728155 (20.9, 41.6, 165.0)
    AABBAAEA037A404800352B2C2CF7095A0D0D0A
     -> 1477279728283 [0.675, 0.69, 0.156, 0.209]


## Adjust Temperature Visualization

The rainbow color palette will map temperatures to 512 colors, you can change `lut = getLut(19.0, 21.0)` to gain better effect:

    function init() {
        // !!!!!!!!!!!!
        // You can change this range for color lut
        lut = getLut(19.0, 21.0);   // getLut( min_temperature, max_temperature);
        ...

You can find these code in: 
* /app/templates/egg_tems.html(**line 79**) 
* /app/templates/curr_status.html(**line 131**) 