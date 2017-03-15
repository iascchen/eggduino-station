import datetime
import ntplib


def int_to_hexstr(value):
    return '{:02x}'.format(value)


def utc_string(ts):
    year = int_to_hexstr(ts.year - 2000)
    month = int_to_hexstr(ts.month)
    day = int_to_hexstr(ts.day)
    hour = int_to_hexstr(ts.hour)
    minute = int_to_hexstr(ts.minute)
    second = int_to_hexstr(ts.second)
    weekday = int_to_hexstr(ts.weekday())

    return year + month + weekday + day + hour + minute + second


def utp_time():
    c = ntplib.NTPClient()
    response = c.request('europe.pool.ntp.org', version=3)
    return datetime.datetime.utcfromtimestamp(response.tx_time)


try:
    now = utp_time()
    print "UTP", utc_string(now)
except:
    now = datetime.datetime.now()
    print "UTC", utc_string(now)

# import os

# os.system('date -s %s' % date_str)
