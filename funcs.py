import time

import config as cfg

def get_section_and_device(section_id, ip):
    # Find the section with the given section_id
    section = next((x for x in cfg.sections if x.get("id") == section_id), None)

    # Find the device with the given IP address
    device = None
    if ip == "all":
        # Look for devices in the prefix_devices
        device = next((x for x in section.get("prefix_devices", []) if x.ip == ip), None)
    else:
        # Look for devices in the devices list
        device = next((x for x in section.get("devices", []) if x.ip == ip), None)

    return (section, device)

async def turn_on(section_id, ip):
    section, device = get_section_and_device(section_id, ip)

    if ip == "all":
        devices = section.get("devices", [])
        order = section.get("order_turn_on", "desc")
        if order == "asc":
            devices = reversed(devices)

        for device_info in devices:
            await device_info.turn_on()
    else:
        await device.turn_on()

    return False
async def turn_off(section_id, ip_address):
    section, device = get_section_and_device(section_id, ip_address)

    if ip_address == "all":
        devices = section.get("devices", [])
        order = section.get("order_turn_off", "desc")
        if order == "asc":
            devices = reversed(devices)

        for device_info in devices:
            await device_info.turn_off()
    else:
        await device.turn_off()

    return False

def get_input_html_str(section_id, ip):
    return """
        <form action="/turn_on?section=%s&ip=%s" method="POST">
            <button class="btn btn-primary spinner-button" type="submit">Turn on</button>
        </form>
        <form action="/turn_off?section=%s&ip=%s" method="POST">
            <button class="btn btn-warning spinner-button" type="submit">Turn off</button>
        </form>
    """ % (section_id, ip, section_id, ip)
    
def get_table_row_html_str(row_class, ip_label, r_label, status_label, input_html):
    return f"""
        <tr class='{row_class}'>
            <td>{ip_label}</td>
            <td>{r_label} {status_label}</td>
            <td>
                {input_html}
            </td>
        </tr>
    """

async def get_section_rows_html_arr(section):
    sec_id = section.get("id", "none")
    sec_name = section.get("name")
    sec_prefix_devices = section.get("prefix_devices", [])
    sec_devices = section.get("devices", [])
    sec_order_turn_on = section.get("order_turn_on", "desc")
    sec_order_turn_off = section.get("order_turn_off", "desc")

    rows_html = []
    alt_row = False
    for row in sec_prefix_devices:
        await row.update()
        r_label = row.label
        r_show_status = row.show_status
        r_predelay = row.predelay

        ip_label = row.ip if row.ip != "all" else "***.***.***.***"

        status_label = ""
        if row.show_status:
            status_label = await row.status()

        input_html = get_input_html_str(sec_id, row.ip)
        row_html = get_table_row_html_str(
            "table-success", 
            ip_label, 
            row.label, 
            status_label, 
            input_html
        )
        rows_html.append(row_html)

    for row in sec_devices:
        await row.update()
        r_show_status = row.show_status
        r_predelay = row.predelay

        ip_label = row.ip if row.ip != "all" else "***.***.***.***"

        status_label = ""
        if row.show_status:
            status_label = await row.status()

        input_html = get_input_html_str(sec_id, row.ip)
        
        row_html = get_table_row_html_str(
            "table-primary" if not alt_row else "table-secondary", 
            ip_label, 
            row.label, 
            status_label, 
            input_html
        )
        rows_html.append(row_html)
        alt_row = not alt_row
    
    return rows_html

async def generate_section_table_html_str(section):
    section_name = section.get("name") or None

    rows_html = await get_section_rows_html_arr(section)
    return f"""
        <div class="row mb-3">
        <div class="col-md-3"></div>
        <div class="col-md-6">
            <h1>{section_name}</h1>
            
            <table class="table">
            <thead>
                <tr>
                    <th>IP</th>
                    <th>Name</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                {rows_html}
            </tbody>
            </table>
        </div>
        <div class="col-md-3"></div>
    </div>
    """

def generate_includes_html_str():
    return """
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
    """

def generate_section_index_html_str(body):
    title = cfg.title
    includes = generate_includes_html_str()
    
    return f"""
        <html>
        <head>
            <title>{title}</title>
            <meta charset="UTF-8" />
            <meta name="viewport" content="width=device-width, initial-scale=1.0" />
            {includes}
        </head>
        <body>
            {body}
        </body>
        </html>
    """

async def get_section_index_html():
    section_html_list = [await generate_section_table_html_str(sec) for sec in cfg.sections]
    sections_html = " ".join(section_html_list)
    return generate_section_index_html_str(sections_html)
