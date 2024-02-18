from __future__ import with_statement
from mako.template import Template
import time
import os

import config as cfg

tmpl_path = os.path.abspath(__file__) + r"\templates"

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

def turn_on(section_id, ip):
    section, device = get_section_and_device(section_id, ip)

    if ip == "all":
        devices = section.get("devices", [])
        order = section.get("order_turn_on", "desc")
        if order == "asc":
            devices = reversed(devices)

        for device_info in devices:
            device_info.turn_on()
    else:
        device.turn_on()

    return False
def turn_off(section_id, ip_address):
    section, device = get_section_and_device(section_id, ip_address)

    if ip_address == "all":
        devices = section.get("devices", [])
        order = section.get("order_turn_off", "desc")
        if order == "asc":
            devices = reversed(devices)

        for device_info in devices:
            device_info.turn_off()
    else:
        device.turn_off()

    return False

def get_input_html_str(section_id, ip):
    with open(tmpl_path + r"\input_form.html", 'r') as fp:
        return Template(fp.read()).render(section_id=section_id,ip=ip)
    
def get_table_row_html_str(row_class, ip_label, r_label, status_label, input_html):
    with open(tmpl_path + r"\row.html", 'r') as fp:
        return Template(fp.read()).render(row_class=row_class,ip_label=ip_label,r_label=r_label,status_label=status_label,input_html=input_html)

def get_section_rows_html_arr(section):
    sec_id = section.get("id", "none")
    sec_name = section.get("name")
    sec_prefix_devices = section.get("prefix_devices", [])
    sec_devices = section.get("devices", [])
    sec_order_turn_on = section.get("order_turn_on", "desc")
    sec_order_turn_off = section.get("order_turn_off", "desc")

    rows_html = []
    alt_row = False
    for row in sec_prefix_devices:
        r_label = row.label
        r_show_status = row.show_status
        r_predelay = row.predelay

        ip_label = row.ip if row.ip != "all" else "***.***.***.***"

        status_label = ""
        if row.show_status:
            status_label = row.status()

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
        r_show_status = row.show_status
        r_predelay = row.predelay

        ip_label = row.ip if row.ip != "all" else "***.***.***.***"

        status_label = ""
        if row.show_status:
            status_label = row.status()

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

def generate_section_table_html_str(section):
    section_name = section.get("name") or None

    rows_arr = get_section_rows_html_arr(section)
    rows_html = "".join(rows_arr)
    with open(tmpl_path + r"\table.html", 'r') as fp:
        return Template(fp.read()).render(section_name=section_name,rows_html=rows_html)

def generate_includes_html_str():
    with open(tmpl_path + r"\includes.html", 'r') as fp:
        return Template(fp.read()).render()

def generate_section_index_html_str(body):
    title = cfg.title
    includes = generate_includes_html_str()

    with open(tmpl_path + r"\base.html", 'r') as fp:
        return Template(fp.read()).render(title=title,includes=includes,body=body)

def get_section_index_html():
    section_html_list = [generate_section_table_html_str(sec) for sec in cfg.sections]
    sections_html = " ".join(section_html_list)
    return generate_section_index_html_str(sections_html)
