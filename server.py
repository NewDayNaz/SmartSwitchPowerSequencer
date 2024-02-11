from flask import Flask, escape, request, redirect, url_for
from pyHS100 import Discover, SmartPlug
import requests
import time

app = Flask(__name__)

device_list = ["10.10.10.247","10.10.10.249","10.10.10.248","10.10.10.246","10.10.10.226"]
# Soundboard, Stagebox, Speaker L, Speaker R, TV
sound_device_list = ["10.10.10.254","10.10.10.251","10.10.10.252","10.10.10.253"]
# sound_device_list = []

@app.route('/')
def home():
    device_rows = []
    altRow = False
    for ip in device_list:
        plug = SmartPlug(ip)
        try:
            input_html = """
                <form action="/turn_on?ip=%s" method="POST">
                    <button class="btn btn-primary spinner-button" type="submit">Turn on</button>
                </form>
                <form action="/turn_off?ip=%s" method="POST">
                    <button class="btn btn-warning spinner-button" type="submit">Turn off</button>
                </form>
            """ % (ip, ip)

            if not altRow:
                row = "<tr class='table-primary'><td>%s</td><td>%s</td><td>%s</td></tr>" % (ip, plug.alias + " (" + plug.state + ")", input_html)
            else:
                row = "<tr class='table-secondary'><td>%s</td><td>%s</td><td>%s</td></tr>" % (ip, plug.alias + " (" + plug.state + ")", input_html)

            altRow = not altRow
            device_rows.append(row)
        except:
            input_html = """
                            <form action="/" method="GET">
                                <button class="btn btn-primary spinner-button" type="submit">OFFLINE</button>
                            </form>
                            <form action="/" method="GET">
                                <button class="btn btn-warning spinner-button" type="submit">OFFLINE</button>
                            </form>
                        """

            if not altRow:
                row = "<tr class='table-primary'><td>%s</td><td>%s</td><td>%s</td></tr>" % (ip, "UNAVAILABLE (OFFLINE)", input_html)
            else:
                row = "<tr class='table-secondary'><td>%s</td><td>%s</td><td>%s</td></tr>" % (ip, "UNAVAILABLE (OFFLINE)", input_html)

            altRow = not altRow
            device_rows.append(row)


    device_rows_string = ""
    for row in device_rows:
        device_rows_string += row

    soundboard = SmartPlug(sound_device_list[0])
    sound_system_status = "(OFFLINE)"
    try:
        sound_system_status = "(" + plug.state + ")"
    except:
        sound_system_status = "(OFFLINE)"

    return """
        <html>
        <head>
            <title>Power Dashboard</title>
            <meta charset="UTF-8" />
            <meta name="viewport" content="width=device-width, initial-scale=1.0" />
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-eOJMYsd53ii+scO/bJGFsiCZc+5NDVN2yr8+0RDqr0Ql0h+rP48ckxlpbzKgwra6" crossorigin="anonymous">
            <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta3/dist/js/bootstrap.bundle.min.js" integrity="sha384-JEW9xMcG8R+pH31jmWH6WWP0WintQrMb4s7ZOdauHnUtxwoG2vI5DkLtS3qm9Ekf" crossorigin="anonymous"></script>
            <script src="https://code.jquery.com/jquery-2.2.4.min.js" integrity="sha256-BbhdlvQf/xTY9gja0Dq3HiwQF8LaCRTXxZKRutelT44=" crossorigin="anonymous"></script>
            <script type="text/javascript">
                    $(document).ready(function() {
                        $(".spinner-button").click(function() {
                          // disable button
                          $(this).submit();
                          // add spinner to button
                          $(this).html('<span class="spinner-grow spinner-grow-sm" role="status"></span> loading...');
                        });
                    });
            </script>
        </head>
        <body>
        <div class="row mb-3">
            <div class="col-md-3"></div>
            <div class="col-md-6">
                <h1>Sound System Dashboard</h1>
                
                <table class="table">
                <thead>
                    <tr>
                        <th>IP</th>
                        <th>Name</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    <tr class='table-success'>
                        <td>**.**.**.***</td>
                        <td>Sound system %s</td>
                        <td>
                            <form action="/turn_on_sound" method="POST">
                                <button class="btn btn-primary spinner-button" type="submit">Turn on</button>
                            </form>
                            <form action="/turn_off_sound" method="POST">
                                <button class="btn btn-warning spinner-button" type="submit">Turn off</button>
                            </form>
                        </td>
                    </tr>
                </tbody>
                </table>
            </div>
            <div class="col-md-3"></div>
        </div>
        <div class="row mb-3">
            <div class="col-md-3"></div>
            <div class="col-md-6">
                <h1>Lighting Dashboard</h1>
                
                <table class="table">
                <thead>
                    <tr>
                        <th>IP</th>
                        <th>Name</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    <tr class='table-success'>
                        <td>**.**.**.***</td>
                        <td>All lighting devices</td>
                        <td>
                            <form action="/turn_on" method="POST">
                                <button class="btn btn-primary spinner-button" type="submit">Turn on</button>
                            </form>
                            <form action="/turn_off" method="POST">
                                <button class="btn btn-warning spinner-button" type="submit">Turn off</button>
                            </form>
                        </td>
                    </tr>
                    %s
                </tbody>
                </table>
            </div>
            <div class="col-md-3"></div>
        </div>
        </body>
        </html>
        """ % (sound_system_status, device_rows_string)

@app.route('/turn_off', methods=['POST'])
def turn_off():
    ip = request.args.get("ip", "all")
    if ip in device_list:
        plug = SmartPlug(ip)
        plug.turn_off()
    else:
        for dev in reversed(device_list):
            try:
                plug = SmartPlug(dev)
                plug.turn_off()
                time.sleep(1)
            except:
                print("error")

    print("Turning off", ip)
    return redirect('/')

@app.route('/turn_on', methods=['POST'])
def turn_on():
    ip = request.args.get("ip", "all")
    if ip in device_list:
        plug = SmartPlug(ip)
        plug.turn_on()
    else:
        for dev in device_list:
            try:
                plug = SmartPlug(dev)
                plug.turn_on()
                time.sleep(1.5)
            except:
                print("done")

    print("Turning on", ip)
    return redirect('/')


@app.route('/turn_off_sound', methods=['POST'])
def turn_off_sound():
    ip = request.args.get("ip", "all")
    if ip in sound_device_list:
        plug = SmartPlug(ip)
        plug.turn_off()
    else:
        firstEntry = True
        # r = requests.post("http://homeassistant:8123/api/webhook/turn_off_sound_system")
        for dev in reversed(sound_device_list):
            try:
                plug = SmartPlug(dev)
                plug.turn_off()
                if firstEntry:
                    firstEntry = False
                    time.sleep(0.2)
                else:
                    time.sleep(5)
            except:
                print("error")

    print("Turning off", ip)
    return redirect('/')

@app.route('/turn_on_sound', methods=['POST'])
def turn_on_sound():
    ip = request.args.get("ip", "all")
    if ip in sound_device_list:
        plug = SmartPlug(ip)
        plug.turn_on()
    else:
        # r = requests.post("http://homeassistant:8123/api/webhook/turn_on_sound_system")
        firstEntry = True
        for dev in sound_device_list:
            try:
                plug = SmartPlug(dev)
                plug.turn_on()
                if firstEntry:
                    firstEntry = False
                    time.sleep(15)
                else:
                    time.sleep(5)
            except:
                print("done")

    print("Turning on", ip)
    return redirect('/')


if __name__ == "__main__":
    app.run()