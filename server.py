from flask import Flask, request, redirect, url_for

import funcs as funcs
import config as cfg

app = Flask(__name__)

@app.route('/')
def home():
    return funcs.get_section_index_html()

@app.route('/turn_off', methods=['POST'])
def turn_off():
    section = request.args.get("section", "none")
    ip = request.args.get("ip", "all")
    funcs.turn_off(section, ip)
    return redirect('/')

@app.route('/turn_on', methods=['POST'])
def turn_on():
    section = request.args.get("section", "none")
    ip = request.args.get("ip", "all")
    funcs.turn_on(section, ip)
    return redirect('/')

@app.route('/toggle', methods=['POST'])
def toggle():
    section = request.args.get("section", "none")
    ip = request.args.get("ip", "all")
    funcs.toggle(section, ip)
    return redirect('/')

if __name__ == "__main__":
    app.run()