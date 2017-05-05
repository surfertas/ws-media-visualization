#!/usr/bin/env python
# date: 5/5/2017
# author: Tasuku Miura

import argparse
import cv2
import numpy as np


MHI_DURATION = 0.9
DEFAULT_THRESHOLD = 30
MAX_TIME_DELTA = 0.25
MIN_TIME_DELTA = 0.05

motion_history = None
prev_frame = None


def get_motion_flow(frame, prev_frame):
    """ Returns motion visualization. """
    frame_diff = cv2.absdiff(frame, prev_frame)
    gray_diff = cv2.cvtColor(frame_diff, cv2.COLOR_BGR2GRAY)

    ret, motion_mask = cv2.threshold(
        gray_diff, DEFAULT_THRESHOLD, 1, cv2.THRESH_BINARY)

    timestamp = cv2.getTickCount() / cv2.getTickFrequency()

    cv2.motempl.updateMotionHistory(
        motion_mask, motion_history, timestamp, MHI_DURATION)

    vis = np.uint8(
        np.clip((motion_history - (timestamp - MHI_DURATION)) / MHI_DURATION, 0, 1) * 255)

    return vis


def magnitude(frame):
    """ Returns image with magnitude displayed as image. """
    sobelx = lambda im: cv2.Sobel(im, cv2.CV_64F, 1, 0, ksize=3)
    sobely = lambda im: cv2.Sobel(im, cv2.CV_64F, 0, 1, ksize=3)
    dxabs = cv2.convertScaleAbs(sobelx(frame))
    dyabs = cv2.convertScaleAbs(sobely(frame))

    return cv2.addWeighted(dxabs, 0.5, dyabs, 0.5, 0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Open Lesson: Video processing')
    parser.add_argument('file', type=str,
                        help='Video stream to process')
    parser.add_argument('dir_out', type=str,
                        help='Dir to output processed video')
    args = parser.parse_args()

    stream = cv2.VideoCapture(args.file)

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'XVID')

    out = None
    output_file = '{}/output.avi'.format(args.dir_out)

    def warmup(cap):
        for i in range(10):
            stream.read

    is_start = True
    warmup(stream)
    while stream.isOpened():
        ret, frame = stream.read()

        if not ret:
            break

        if is_start and ret:
            h, w, _ = frame.shape
            motion_history = np.zeros((h, w), np.float32)
            prev_frame = frame.copy()
            out = cv2.VideoWriter(output_file, fourcc, 30, (w, h), False)
            is_start = False

        motion = get_motion_flow(frame, prev_frame)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        vis = magnitude(gray)
        out.write(np.asarray(vis + motion, dtype=np.uint8))
        prev_frame = frame.copy()

    out.release()
    stream.release()
    cv2.destroyAllWindows()
