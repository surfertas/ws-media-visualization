#! /usr/bin/env python
# date: 5/5/2017
# author: Tasuku Miura

import os
from flask import Flask
from flask import Blueprint
from flask import g
from flask import request
from flask import flash
from flask import render_template
from flask import url_for
from flask import Response
from flask import redirect
import controllers.media_controller as mc

view = Blueprint('view', __name__, template_folder='templates')


@view.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'GET':
        return render_template('index.html')

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == password:
            return redirect('/main')
        else:
            return render_template('index.html')


@view.route('/main')
def main():
    return render_template('main.html')


@view.route('/videos/process/flow', methods=['POST'])
def generate_flow():
    if request.method == 'POST':
        if 'file' not in request.files:
            print('No file')

        if mc.add_video(request.files['file']):
            mc.process_media("gen_flow")
            mc.reformat_vid()
            return render_template('display.html')

    return render_template('main.html')


@view.route('/video_stream')
def video_stream():
    return Response(mc.frame_generator(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
