# -*- coding: utf-8 -*-
from collections import ChainMap
from flask import Flask,render_template,request,abort
from os import getenv
import yaml

app = Flask(__name__)
config = {}
paths = {}

@app.route(f'/<path>')
def form(path):
    if path in paths:
        return render_template('form.html')
    else:
        return abort(404)

@app.route('/refresh', methods=['POST'])
def refresh():
    token = request.form['token']
    path = request.headers['Referer'].split('/')[-1]
    if token == config[paths[path]]['token']:
        open(config[paths[path]]['refresh'],'w')
        return render_template('done.html',
                                message=config[paths[path]]['message'],
                                url=config[paths[path]]['link'])
    else:
        return abort(404)

if __name__ == '__main__':
    refresh_path = getenv('REFRESH_PATH')
    with open(f'{refresh_path}/refresh.yaml', 'r') as f:
        ext_config = yaml.load(f, Loader=yaml.SafeLoader) #['vocab']
        for key in ext_config.keys():
            config[key] = dict(ChainMap(*ext_config[key]))
            paths[config[key]['path']] = key
    app.run(host='0.0.0.0', port=80)

