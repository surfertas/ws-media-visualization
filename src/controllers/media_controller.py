#!/usr/bin/env python
# date: 5/5/2017
# author: Tasuku Miura

import os
import glob
import cv2
from subprocess import call
from flask import Flask, g, request, flash
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = set(['mov'])
configpath = os.getcwd()
MEDIA_DIR = "{}/media".format(configpath)
OUT_DIR = "{}/out".format(configpath)


def allowed_file(filename):
    """ Filters for allowed extensions. """
    return ('.' in filename and
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS)


def add_video(stream):
    """ Adds video to the directory specified in MEDIA_DIR. """
    # Flush out the output directory for any remaining video content.
    print("configpath is: {}".format(configpath))

    try:
        ret = call(["rm", "-r", "{}/final.mov".format(OUT_DIR)])
    except IOError:
        print("Call process failed.")

    file = request.files['file']
    if allowed_file(file.filename):
        secure = secure_filename(file.filename)
        stream.save(os.path.join(MEDIA_DIR, secure))
        return True
    else:
        return False


def process_media(func):
    """ Main function that calls function to process media. """
    subfolders = os.walk(MEDIA_DIR)
    for dirpath, dirnames, fnames in subfolders:
        media = os.path.join(MEDIA_DIR, fnames[0])
        try:
            ret = call(["python", "{}/{}.py".format(
                os.path.join(configpath, "scripts"), func), media, OUT_DIR])
        except IOError:
            print("Call process failed.")

        return ret


def reformat_vid():
    """ Calls shell script to reformat video from avi to mov. """
    subfolders = os.walk(OUT_DIR)
    for _, _, fnames in subfolders:
        media = os.path.join(OUT_DIR, fnames[0])
        try:
            ret = call(["{}/vid2vid.sh".format(
                os.path.join(configpath, "scripts")), "-i", media, "-o",
                os.path.join(configpath, "out/final")])
        except IOError:
            print("Call process failed.")

        return ret


def frame_generator():
    """ Generates frames from stream. """
    _, _, fnames = os.walk(OUT_DIR).next()
    media = os.path.join(OUT_DIR, fnames[0])
    stream = cv2.VideoCapture(media)
    while stream.isOpened():
        ret, frame = stream.read()
        if not ret:
            break

        ret, jpeg = cv2.imencode('.jpg', frame)

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')
