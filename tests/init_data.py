#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import sqlite3
import random

INSERT_EGG_TEMPERATURES = '''INSERT INTO messages
    (ts, temp_01, temp_02, temp_03, temp_04, temp_05, temp_06, temp_07, temp_08,
    temp_09, temp_10, temp_11, temp_12, temp_13, temp_14, temp_15, temp_16)
    VALUES
    (?,   ?,?,?,?,?,?,?,?,   ?,?,?,?,?,?,?,?) '''

INSERT_EGG_QUATERNIONS = '''INSERT INTO messages (ts, quat_w, quat_x, quat_y, quat_z) VALUES (?,   ?,?,?,?) '''

INSERT_EGG_HUMINITY = '''INSERT INTO messages (ts, hum) VALUES (?,   ?) '''

INSERT_STATION = '''INSERT INTO messages (ts, hum_s, light_s, temp_s) VALUES (?,   ?,?,?) '''

current_milli_time = lambda: int(round(time.time() * 1000))

###################
# DB Init
###################

conn = sqlite3.connect('../db/database.db')

print "Opened database successfully"


def random_tem():
    return random.uniform(40.0, 43.0)


def random_hum():
    return random.uniform(0.0, 100.0)


def random_quat():
    return random.uniform(0.0, 1.0)


def random_light():
    return random.uniform(100.0, 1000.0)


for num in range(0, 100):
    ts = current_milli_time()
    # print ts
    conn.execute(INSERT_EGG_TEMPERATURES, (ts,
                                           random_tem(), random_tem(), random_tem(), random_tem(),
                                           random_tem(), random_tem(), random_tem(), random_tem(),
                                           random_tem(), random_tem(), random_tem(), random_tem(),
                                           random_tem(), random_tem(), random_tem(), random_tem()))

    conn.execute(INSERT_EGG_QUATERNIONS, (ts + 1, random_quat(), random_quat(), random_quat(), random_quat()))

    conn.execute(INSERT_EGG_HUMINITY, (ts + 2, random_hum()))

    conn.execute(INSERT_STATION, (ts + 3, random_hum(), random_light(), random_tem()))

    time.sleep(0.1)  # Delay for one 1 ms

# for num in range(0, 10):
#     ts = current_milli_time()
#     # print ts
#     conn.execute(INSERT_EGG_QUATERNIONS, (ts, random_quat(), random_quat(), random_quat(), random_quat()))
#     time.sleep(0.001)  # Delay for one 1 ms
#
# for num in range(0, 10):
#     ts = current_milli_time()
#     # print ts
#     conn.execute(INSERT_EGG_HUMINITY, (ts, random_hum()))
#     time.sleep(0.001)  # Delay for one 1 ms
#
# for num in range(0, 10):
#     ts = current_milli_time()
#     # print ts
#     conn.execute(INSERT_STATION, (ts, random_hum(), random_light(), random_tem()))
#     time.sleep(0.001)  # Delay for one 1 ms

conn.commit()

print "Records created successfully"

conn.close()
