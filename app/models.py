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

SELECT_ALL_ITEMS_HISTORY = '''select
    ts, temp_01, temp_02, temp_03, temp_04, temp_05, temp_06, temp_07, temp_08,
    temp_09, temp_10, temp_11, temp_12, temp_13, temp_14, temp_15, temp_16,
    quat_w, quat_x, quat_y, quat_z, hum, temp_s, hum_s, light_s
    from messages
    where (ts > ?) and (ts < ?)
    order by ts'''

SELECT_TEMPERATURE_MIN = '''select min(
	min(temp_01), min(temp_02), min(temp_03), min(temp_04),
	min(temp_05), min(temp_06), min(temp_07), min(temp_08),
    min(temp_09), min(temp_10), min(temp_11), min(temp_12),
    min(temp_13), min(temp_14), min(temp_15), min(temp_16)) as temp_min
    from messages
    where (ts > ?) and (ts < ?)'''

SELECT_TEMPERATURE_MAX = '''select max(
	max(temp_01), max(temp_02), max(temp_03), max(temp_04),
	max(temp_05), max(temp_06), max(temp_07), max(temp_08),
    max(temp_09), max(temp_10), max(temp_11), max(temp_12),
    max(temp_13), max(temp_14), max(temp_15), max(temp_16)) as temp_max
    from messages
    where (ts > ?) and (ts < ?)'''

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


def get_temperature_range_min(from_ts, to_ts):
    return query_db(SELECT_TEMPERATURE_MIN, args=(from_ts, to_ts))


def get_temperature_range_max(from_ts, to_ts):
    return query_db(SELECT_TEMPERATURE_MAX, args=(from_ts, to_ts))

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
