from wagonapp import app
from flask import render_template, make_response, request, Response, jsonify, json, session, redirect, url_for, send_file
import functools
from werkzeug.utils import secure_filename
from scrypt import solution

import json



@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/api/file', methods=['POST'])
def get_file():
    # sub_example_audio.csv
    print('Work')

    print(type(request.form.get('file')))
    print(type(request.form.get('test')))

    file = request.files["file"]
    filename = secure_filename(file.filename)
    file.save(filename)

    solution(file.filename)
    #rfile = open('sub_example_audio.csv')

    #print(type(rfile))

    return send_file('DEMO.csv', mimetype = 'text/csv', )



def json_response(data, code=200):
    return Response(status=code, mimetype="application/json", response=json.dumps(data))