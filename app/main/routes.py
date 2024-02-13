from flask import current_app, render_template
from app.main import bp

import funcs as funcs

 @bp.route('/')
def home():
    sections = [generate_section_table_html_str(sec) for sec in current_app.config.sections]
    return render_template('index.html', sections=sections)
    return funcs.get_section_index_html()

@bp.route('/turn_off', methods=['POST'])
def turn_off():
    section = request.args.get("section", "none")
    ip = request.args.get("ip", "all")
    funcs.turn_off(section, ip)
    return redirect('/')

@bp.route('/turn_on', methods=['POST'])
def turn_on():
    section = request.args.get("section", "none")
    ip = request.args.get("ip", "all")
    funcs.turn_on(section, ip)
    return redirect('/')