# -*- coding: utf-8 -*-
from flask import Flask,render_template,request,abort
import yaml

app = Flask(__name__)
config = {}
path = ''

@app.route(f'/<path>')
def form(path):
    assert path==config['path']
    if path==config['path']:
        return render_template('form.html')
    else:
        return abort(404)

@app.route('/refresh', methods=['POST'])
def refresh():
    token = request.form['token']
    if token==config['token']:
        open(config['refresh'],'w')
        return render_template('done.html',
                                message=config['message'],
                                url=config['link'])
    else:
        return abort(404)

if __name__ == '__main__':
    refresh_path = get_env('REFRESH_PATH')
    with open(f'{refresh_path}/refresh.yaml', 'r') as f:
        config = yaml.load(f, Loader=yaml.SafeLoader)['vocab']
        print(config)
        path = config['path']
    app.run(host='0.0.0.0', port=80)

