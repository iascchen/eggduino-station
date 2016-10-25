# -*- coding: utf-8 -*-


from app import app, get_db, models, current_milli_time
from flask import render_template
import json

history_period = 1 * 3600 * 1000  # 1 hour


def cursor_to_nvd3_data(query_result):
    # print query_result

    serials = []

    if not query_result:
        return serials

    cols = len(query_result[0])
    # print cols

    for i in range(1, cols):
        # print i
        row = [[int(o[0]), o[i]] for o in query_result if o[i] is not None]
        # print row
        serials.append(row)

    return serials


@app.route('/')
def index():
    return render_template("curr_status.html")


@app.route('/hum_charts')
def hum_charts():
    to_ts = current_milli_time()
    from_ts = to_ts - history_period

    # print from_ts, to_ts

    datas = models.get_history_humidities(from_ts, to_ts)
    serials = cursor_to_nvd3_data(datas)

    if not serials:
        return render_template("index.html", text="Without records in last one hour, please check your devices")

    ret = [{"key": "Humidity in Egg", "values": serials[0]},
           {"key": "Humidity of Station", "values": serials[1]}]

    return render_template("hum_charts.html", from_ts=from_ts, to_ts=to_ts, serials_data=json.dumps(ret))


@app.route('/station_charts')
def station_charts():
    to_ts = current_milli_time()
    from_ts = to_ts - history_period

    # print from_ts, to_ts

    datas = models.get_history_station(from_ts, to_ts)
    serials = cursor_to_nvd3_data(datas)

    if not serials:
        return render_template("index.html", text="Without records in last one hour, please check your devices")

    ret = [{"key": "Humidity(%)", "values": serials[0]},
           {"key": "Lightness(lux)", "values": serials[1]},
           {"key": "Temperature(ºC)", "values": serials[2]}]

    return render_template("station_charts.html", from_ts=from_ts, to_ts=to_ts, serials_data=json.dumps(ret))


@app.route('/tems')
def egg_tems_charts():
    to_ts = current_milli_time()
    from_ts = to_ts - history_period

    # print from_ts, to_ts

    datas = models.get_history_temperatures(from_ts, to_ts)
    serials = cursor_to_nvd3_data(datas)

    if not serials:
        return render_template("index.html", text="Without records in last one hour, please check your devices")

    ret = []
    for i in range(0, 16):
        _key = "temp_%0.2d" % (i + 1)
        ret.append({"key": _key, "values": serials[i], "classed": "dashed"})

    ret.append({"key": "temp_avg", "values": serials[16]})
    ret.append({"key": "temp_station", "values": serials[17]})
    return render_template("egg_tems.html", from_ts=from_ts, to_ts=to_ts, serials_data=json.dumps(ret))


@app.route('/quats')
def egg_quats_charts():
    to_ts = current_milli_time()
    from_ts = to_ts - history_period

    # print from_ts, to_ts

    datas = models.get_history_quaternions(from_ts, to_ts)
    serials = cursor_to_nvd3_data(datas)

    if not serials:
        return render_template("index.html", text="Without records in last one hour, please check your devices")

    ret = [{"key": "w", "values": serials[0]},
           {"key": "x", "values": serials[1]},
           {"key": "y", "values": serials[2]},
           {"key": "z", "values": serials[3]}]

    return render_template("egg_quats.html", from_ts=from_ts, to_ts=to_ts, serials_data=json.dumps(ret))


@app.route("/curr_data")
def curr_data():
    tems = models.get_last_egg_temperatures()
    quats = models.get_last_egg_quaternions()
    hum = models.get_last_egg_humidity()
    station = models.get_last_station()

    ret = {'tems': tems, 'quats': quats, 'hum': hum, 'station': station}
    return json.dumps(ret)


@app.route('/show_table')
def show_table():
    db = get_db()
    c = db.cursor()

    # Retrieve column information
    # Every column will be represented by a tuple with the following attributes:
    # (id, name, type, notnull, default_value, primary_key)
    c.execute('PRAGMA TABLE_INFO({})'.format('messages'))

    # collect names in a list
    names = [tup[1] for tup in c.fetchall()]
    # print names

    return render_template("index.html", text=names)
