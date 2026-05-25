# -*- coding: utf-8 -*-
from flask import Flask,render_template,request,abort
import yaml
from os import getenv

app = Flask(__name__)
config = {}

@app.route(f'/<path>')
def form(path):
    if path in config:
        return render_template('form.html')
    else:
        return abort(404)

@app.route('/refresh', methods=['POST'])
def refresh():
    token = request.form['token']
    path = request.headers['Referer'].split('/')[-1]
    if path in config and token==config[path]['token']:
        open(config[path]['refresh'],'w')
        return render_template('done.html',
                                message=config[path]['message'],
                                url=config[path]['link'])
    else:
        return abort(404)

if __name__ == '__main__':
    refresh_path = getenv('REFRESH_PATH')
    with open(f'{refresh_path}/refresh.yaml', 'r') as f:
        config = yaml.load(f, Loader=yaml.SafeLoader)
        print(config)
    app.run(host='0.0.0.0', port=80)

