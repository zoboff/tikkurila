# encoding=utf8
'''
Created on 12.10.2018.

@author: zobov
'''
import tikkurila_colors, utils
from flask import Flask, render_template, request
import copy
import colorsys
import re

HOST = '127.0.0.1'
PORT = 5000
TITLE = 'Search Tikkurila by RGB'

app = Flask(__name__)


@app.route('/') 
def index() -> 'html':
    return render_template('color.html',
                           the_title=TITLE, 
                           the_note='Enter any color. For example: F490, FDE02A',)


@app.route('/', methods=['POST'])
def find() -> 'html':
    if 'color' in request.form:
        color_name = request.form['color']
    if color_name:
        # remove "#"
        color_name = color_name.lstrip('#') 
        # by name? -> "F490"
        re_name = re.compile('^[a-zA-Z]{1}[0-9]{3}$')
        if re_name.match(color_name):
            return by_name(color_name)
        else:
            # by hex? -> "FEA0BC"
            re_hex = re.compile('^[A-Fa-f0-9]{6}$')
            if re_hex.match(color_name):
                return by_hex(color_name)
    # color not found        
    return render_template('color.html',
                           the_title=TITLE,
                           the_note='Color "{}" not found'.format(color_name),)


def by_name(color_name) -> 'html':
    color = tikkurila_colors.color_by_name(color_name)
    if color:
        msg = 'Name "{}"; HEX: {}; RGB({}, {}, {})'.format(color[3], utils.rgb_to_hex(color[0], color[1], color[2]), color[0], color[1], color[2])
        return render_template('color_by_name.html',
                           the_title=TITLE,
                           the_note='',
                           the_result='',                           
                           the_name_color0=msg,
                           the_color0=utils.rgb_to_hex(color[0], color[1], color[2]),)
    else:
        msg = 'Color "{}" not found.'.format(color_name.upper())
        return render_template('color.html',
                           the_title=TITLE,
                           the_note=color,
                           the_result=msg,)


def by_hex(color_name) -> 'html':
    # extract RGB
    r, g, b = utils.hex_to_rgb(color_name)
    # 
    msg = 'Color: #{}; RGB({}, {}, {}); '.format(color_name, r, g, b)
    # make a sorted array
    cp_colors = copy.copy(tikkurila_colors.COLORS)
    for clr in cp_colors:
        clr[4] = abs(clr[0] - r) + abs(clr[1] - g) + abs(clr[2] - b)    
    # sort
    from operator import itemgetter
    cp_colors.sort(key=itemgetter(4))
    # hsl
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    msg += 'HLS: {0:.3f}, {1:.3f}, {2:.3f}.'.format(h, l, s)
    # result
    return render_template('color_by_hex.html',
                           the_title=TITLE,
                           the_note='',
                           the_result='',
                           the_name_color0=msg,
                           the_color0=utils.rgb_to_hex(r, g, b),
                           the_color1=utils.rgb_to_hex(cp_colors[0][0], cp_colors[0][1], cp_colors[0][2]),
                           the_color2=utils.rgb_to_hex(cp_colors[1][0], cp_colors[1][1], cp_colors[1][2]),
                           the_color3=utils.rgb_to_hex(cp_colors[2][0], cp_colors[2][1], cp_colors[2][2]),
                           the_name_color1=cp_colors[0][3],
                           the_name_color2=cp_colors[1][3],
                           the_name_color3=cp_colors[2][3],)
    
        
if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=True)
