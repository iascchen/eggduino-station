# -*- coding: utf-8 -*-


from app import app, get_db, models, current_milli_time, forms
from flask import render_template, request, redirect
import json
import subprocess
import datetime
import re

history_period = 1 * 3600 * 1000  # 1 hour

CMD_T_STOP = 'AB0100'
CMD_H_STOP = 'AB0200'
CMD_Q_STOP = 'AB0300'
CMD_S_STOP = 'AB0400'

CMD_T = 'AB0101'
CMD_H = 'AB0201'
CMD_Q = 'AB0301'
CMD_S = 'AB0401'
CMD_RTC = 'AB05'

TIME_SYNC_SHELL = './daemon/sync_time.py'
# TIME_SYNC_SHELL = './daemon/test_python.py'
MACRON_SHELL = './daemon/macron_daemon.py'
# MACRON_SHELL = './daemon/test_python.py'

macron_pid = None


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


def int_to_hexstr2(value):
    return '{:02x}'.format(value)


def int_to_hexstr4(value):
    return '{:04x}'.format(value)


def compose_eggduino_cmd(tem, hum, mov, env):
    tem_interval = CMD_T + int_to_hexstr2(tem)
    hum_interval = CMD_H + int_to_hexstr2(hum)
    mov_interval = CMD_Q + int_to_hexstr4(mov)
    env_interval = CMD_S + int_to_hexstr2(env)

    init_cmds = [CMD_T_STOP, CMD_H_STOP, CMD_Q_STOP, CMD_S_STOP, tem_interval, hum_interval, mov_interval, env_interval]

    # nohup ./deamon/macron.py -c ab0100, ab0200, ad0300, ad0400, ab010128, ab020114, ab0301000a, ab040128 &

    # return ['nohup', MACRON_SHELL, '-c', ",".join(init_cmds), '&']
    return [MACRON_SHELL, '-c', ",".join(init_cmds)]


def process_exist(process_name):
    cmd_ps = ['ps', 'aux']
    cmd_grep = ['grep', process_name]
    cmd_grep_v = ['grep', '-v', 'grep']

    p1 = subprocess.Popen(cmd_ps, stdout=subprocess.PIPE)
    p2 = subprocess.Popen(cmd_grep, stdout=subprocess.PIPE, stdin=p1.stdout)
    p3 = subprocess.Popen(cmd_grep_v, stdout=subprocess.PIPE, stdin=p2.stdout)

    out, err = p3.communicate()
    result = [x for x in re.split(',| ', out) if x != '']

    if len(result) > 1:
        return result[1]
    else:
        return None


def process_kill(pid):
    cmd = ['kill', '-9', str(pid)]
    print cmd
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p.wait()


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


###################################
# Admin Setting
###################################

@app.route('/time')
def server_time():
    now = datetime.datetime.now()
    return render_template("time.html", server_time=now)


@app.route('/sync_time')
def sync_time():
    cmd = [TIME_SYNC_SHELL]

    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    # print "pid : ", p.pid
    now = datetime.datetime.now()
    return render_template("time.html", server_time=now, output=out)


@app.route('/interval')
def interval():
    form_stop = forms.PidForm(request.form)
    form = forms.IntervalForm(request.form)

    macron_pid = process_exist(MACRON_SHELL)
    form_stop.hidden_pid.data = macron_pid
    form.hidden_pid.data = macron_pid

    return render_template("interval.html", form=form, form_stop=form_stop, pid=macron_pid)


@app.route('/apply_interval', methods=['POST'])
def apply_interval():
    form = forms.IntervalForm(request.form)
    # print 'IntervalForm requested for tem_interval=%s, hum_interval=%s, mov_interval=%s, env_interval=%s' % (form.tem_interval.data, form.hum_interval.data, form.mov_interval.data, form.env_interval.data)

    if request.method == 'POST' and form.validate():
        if form.hidden_pid.data:
            process_kill(form.hidden_pid.data)

        cmd = compose_eggduino_cmd(form.tem_interval.data, form.hum_interval.data,
                                   form.mov_interval.data, form.env_interval.data)
        print cmd

        p = subprocess.Popen(cmd, stdout=open('nohup.out', 'w'), stderr=open('logfile.log', 'a'))
        print "pid : ", p.pid
        # out, err = p.communicate()

        return redirect("/interval", code=302)
    else:
        return render_template('interval.html', form=form)


@app.route('/stop_daemon', methods=['POST'])
def stop_daemon():
    form_stop = forms.PidForm(request.form)

    if request.method == 'POST' and form_stop.validate():
        process_kill(form_stop.pid.data)

    return redirect("/interval", code=302)


@app.route('/download_data', methods=['GET', 'POST'])
def download_data():
    names = ["downloadData", ]
    return render_template("index.html", text=names)
