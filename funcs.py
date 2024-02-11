from pyHS100 import Discover, SmartPlug
import time

import config as cfg

def get_data_from_section_and_ip(section_id, ip):
    sec = None
    for x in cfg.sections:
        x_id = x.get("id") or None
        if x_id == section_id:
            sec = x
            break

    device = None
    if ip == "all":
        for x in sec.get("prefix_rows") or []:
            x_ip = x.get("ip") or None
            if x_ip == ip:
                device = x
                break
    else:
        for x in sec.get("devices") or []:
            x_ip = x.get("ip") or None
            if x_ip == ip:
                device = x
                break

    return (sec, device)

def turn_on(section_id, ip):
    data = get_data_from_section_and_ip(section_id, ip)
    section = data[0] or None
    device = data[1] or None

    if ip == "all":
        device_list = section.get("devices") or []
        order = section.get("order_turn_on") or "desc"
        if order == "asc":
            device_list = reversed(device_list)

        for x in device_list:
            x_predelay = x.get("predelay") or 0
            time.sleep(x_predelay)
            plug = SmartPlug(x.get("ip"))
            plug.turn_on()
    else:
        plug = SmartPlug(device.get("ip"))
        plug.turn_on()

    return False
def turn_off(section_id, ip):
    data = get_data_from_section_and_ip(section_id, ip)
    section = data[0] or None
    device = data[1] or None

    if ip == "all":
        device_list = section.get("devices") or []
        order = section.get("order_turn_off") or "desc"
        if order == "asc":
            device_list = reversed(device_list)

        for x in device_list:
            x_predelay = x.get("predelay") or 0
            time.sleep(x_predelay)
            plug = SmartPlug(x.get("ip"))
            plug.turn_off()
    else:
        plug = SmartPlug(device.get("ip"))
        plug.turn_off()

    return False

def get_section_index_html():
    sections_html = []
    for sec in cfg.sections:
        sec_id = sec.get("id") or "none"
        sec_name = sec.get("name") or None
        sec_prefix_rows = sec.get("prefix_rows") or []
        sec_devices = sec.get("devices") or []
        sec_order_turn_on = sec.get("order_turn_on") or "desc"
        sec_order_turn_off = sec.get("order_turn_off") or "desc"
        
        sec_rows = []

        altRow = False

        for row in sec_prefix_rows:
            r_label = row.get("label") or None
            r_ip = row.get("ip") or None
            r_show_status = row.get("show_status") or None
            r_predelay = row.get("predelay") or 0

            plug = None
            status_label = ""

            ip_label = r_ip

            if ip_label == "all":
                ip_label = "***.***.***.***"
            else:
                plug = SmartPlug(r_ip)
                try:
                    status_label = "(%s)" % plug.state
                except:
                    status_label = "UNAVAILABLE (OFFLINE)"

            input_html = """
                    <form action="/turn_on?section=%s&ip=%s" method="POST">
                        <button class="btn btn-primary spinner-button" type="submit">Turn on</button>
                    </form>
                    <form action="/turn_off?section=%s&ip=%s" method="POST">
                        <button class="btn btn-warning spinner-button" type="submit">Turn off</button>
                    </form>
                """ % (sec_id, r_ip, sec_id, r_ip)

            row_html = """
            <tr class='table-success'>
                <td>%s</td>
                <td>%s %s</td>
                <td>
                    %s
                </td>
            </tr>
            """ % (ip_label, r_label, status_label, input_html)

            sec_rows.append(row_html)

        for row in sec_devices:
            r_label = row.get("label") or None
            r_ip = row.get("ip") or None
            r_show_status = row.get("show_status") or None
            r_predelay = row.get("predelay") or None

            plug = None
            status_label = ""

            ip_label = r_ip

            if ip_label == "all":
                ip_label = "***.***.***.***"
            else:
                plug = SmartPlug(r_ip)
                try:
                    status_label = "(%s)" % plug.state
                except:
                    status_label = "UNAVAILABLE (OFFLINE)"

            input_html = """
                <form action="/turn_on?section=%s&ip=%s" method="POST">
                    <button class="btn btn-primary spinner-button" type="submit">Turn on</button>
                </form>
                <form action="/turn_off?section=%s&ip=%s" method="POST">
                    <button class="btn btn-warning spinner-button" type="submit">Turn off</button>
                </form>
            """ % (sec_id, r_ip, sec_id, r_ip)

            plug = None
            
            row_html = ""
            if not altRow:
                row_html = """
                    <tr class='table-primary'>
                        <td>%s</td>
                        <td>%s %s</td>
                        <td>
                            %s
                        </td>
                    </tr>
                """ % (ip_label, r_label, status_label, input_html)
            else:
                row_html = """
                    <tr class='table-secondary'>
                        <td>%s</td>
                        <td>%s %s</td>
                        <td>
                            %s
                        </td>
                    </tr>
                """ % (ip_label, r_label, status_label, input_html)

            altRow = not altRow

            sec_rows.append(row_html)

        section_table = """
            <div class="row mb-3">
                <div class="col-md-3"></div>
                <div class="col-md-6">
                    <h1>%s</h1>
                    
                    <table class="table">
                    <thead>
                        <tr>
                            <th>IP</th>
                            <th>Name</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        %s
                    </tbody>
                    </table>
                </div>
                <div class="col-md-3"></div>
            </div>
        """ % (sec_name, " ".join(sec_rows))

        sections_html.append(section_table)

    sections_html = " ".join(sections_html)

    return_html = """
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
            %s
        </body>
        </html>
    """ % (sections_html)
    return return_html