from flask import Flask, request, Response, redirect

import funcs as funcs
import config as cfg

app = Flask(__name__)

@app.route('/')
async def home():
    data = await funcs.get_section_index_html()
    return data

@app.route('/turn_off', methods=['POST'])
async def turn_off():
    section = request.args.get("section", "none")
    ip = request.args.get("ip", "all")
    funcs.turn_off(section, ip)
    return redirect('/')

@app.route('/turn_on', methods=['POST'])
async def turn_on():
    section = request.args.get("section", "none")
    ip = request.args.get("ip", "all")
    funcs.turn_on(section, ip)
    return redirect('/')

if __name__ == "__main__":
    app.run()