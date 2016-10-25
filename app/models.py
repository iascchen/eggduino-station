# -*- coding: utf-8 -*-

from app import query_db

SELECT_EGG_TEMPERATURES = '''select
    ts, temp_01, temp_02, temp_03, temp_04, temp_05, temp_06, temp_07, temp_08,
    temp_09, temp_10, temp_11, temp_12, temp_13, temp_14, temp_15, temp_16,
    (temp_01 + temp_02 + temp_03 + temp_04 + temp_05 + temp_06 + temp_07 + temp_08
    + temp_09 + temp_10 + temp_11 + temp_12 + temp_13 + temp_14 + temp_15 + temp_16) / 16
    from messages
    where (temp_01 is not null)
    order by ts desc limit 1'''

SELECT_EGG_HUMIDITY = '''select
    ts, hum
    from messages
    where (hum is not null)
    order by ts desc limit 1'''

SELECT_EGG_QUATERNIONS = '''select ts, quat_w, quat_x, quat_y, quat_z
    from messages
    where quat_w is not null
    order by ts desc limit 1'''

SELECT_STATION = '''select ts, hum_s, light_s, temp_s
    from messages
    where hum_s is not null
    order by ts desc limit 1'''

SELECT_TEMPERATURES_HISTORY = '''select
    ts, temp_01, temp_02, temp_03, temp_04, temp_05, temp_06, temp_07, temp_08,
    temp_09, temp_10, temp_11, temp_12, temp_13, temp_14, temp_15, temp_16,
    (temp_01 + temp_02 + temp_03 + temp_04 + temp_05 + temp_06 + temp_07 + temp_08
    + temp_09 + temp_10 + temp_11 + temp_12 + temp_13 + temp_14 + temp_15 + temp_16) / 16,
    temp_s
    from messages
    where (ts > ?) and (ts < ?) and ((temp_01 is not null) or (temp_s is not null))
    order by ts limit ?'''

SELECT_HUMIDITIES_HISTORY = '''select
    ts, hum, hum_s
    from messages
    where (ts > ?) and (ts < ?) and ((hum is not null) or (hum_s is not null))
    order by ts limit ?'''

SELECT_QUATERNIONS_HISTORY = '''select ts, quat_w, quat_x, quat_y, quat_z
    from messages
    where (ts > ?) and (ts < ?) and (quat_w is not null)
    order by ts limit ?'''

SELECT_STATION_HISTORY = '''select ts, hum_s, light_s, temp_s
    from messages
    where (ts > ?) and (ts < ?) and (hum_s is not null)
    order by ts limit ?'''

DEFAULT_LIMIT = 10000


def get_last_egg_temperatures():
    return query_db(SELECT_EGG_TEMPERATURES, one=True)


def get_last_egg_humidity():
    return query_db(SELECT_EGG_HUMIDITY, one=True)


def get_last_egg_quaternions():
    return query_db(SELECT_EGG_QUATERNIONS, one=True)


def get_last_station():
    return query_db(SELECT_STATION, one=True)


def get_history_temperatures(from_ts, to_ts, limit=DEFAULT_LIMIT):
    return query_db(SELECT_TEMPERATURES_HISTORY, args=(from_ts, to_ts, limit))


def get_history_humidities(from_ts, to_ts, limit=DEFAULT_LIMIT):
    return query_db(SELECT_HUMIDITIES_HISTORY, args=(from_ts, to_ts, limit))


def get_history_quaternions(from_ts, to_ts, limit=DEFAULT_LIMIT):
    return query_db(SELECT_QUATERNIONS_HISTORY, args=(from_ts, to_ts, limit))


def get_history_station(from_ts, to_ts, limit=DEFAULT_LIMIT):
    return query_db(SELECT_STATION_HISTORY, args=(from_ts, to_ts, limit))

# SELECT_AGGREGATE_TEMPERATURES = '''select ts, hum_s, light_s, temp_s
#     from messages
#     where hum_s is not null
#     order by ts desc
#     limit 1'''
#
# SELECT expression1, expression2, ... expression_n,
#        max(aggregate_expression)
# FROM tables
# [WHERE conditions]
# GROUP BY expression1, expression2, ... expression_n;
