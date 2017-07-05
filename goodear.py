#!/usr/bin/env python3

import curses as cs
from sys import argv

version = '0.0.1'
title = 'goodear %s - An ABX Tester' % version

usage = """Usage:
    ./goodear.py -h
    ./goodear.py <clip1> <clip2>"""

decoders = {
    'flac': 'flac',
    'mp3': 'lame',
    'vorbis': 'oggenc',
    'opus': 'opusenc',
# --------------------
    'other': 'sox'
}

actions = {
    'a': '<play a>',
    'b': '<play b>',
    'x': '<play c>',
    's': '<show stats>',
}

# left <-> right arrows select "a == x" or "b == x"

class Clip:
    def __init__(self, clipfile):
        self.file = clipfile;
        self.format = 'Vorbis'
        self.length = '00:42'
        self.bitrate = 320;

def layout(stdscr, objects):
    clip1 = objects['clip1']
    clip2 = objects['clip2']

    def layout_clip(cw, clip, abx):
        cw.addstr(1, 2, abx + '  ' + clip.file.name)
        cw.vline(1, 3, cs.ACS_VLINE, 1)
        cw.hline(2, 1, cs.ACS_HLINE, cv1.getmaxyx()[1])
        cw.addstr(3, 2, 'Length: %s' % clip.length + '\n')
        cw.addstr(4, 2, 'Format: %s' % clip.format + '\n')
        cw.addstr(5, 2, '  Kbps: %s' % clip.bitrate + '\n')
        cw.box()


    cvw = int(cs.COLS / 3) - 2
    cvh = 15
    cvord = (2, 1)

    cv1 = cs.newwin(cvh, cvw, cvord[0], cvord[1])
    cv2 = cs.newwin(cvh, cvw, cvord[0], cvord[1] + cvw + 1)

    layout_clip(cv1, clip1, 'A')
    layout_clip(cv2, clip2, 'B')

    tpad = cs.COLS - len(title)
    stdscr.addstr(0, 0, title + tpad * ' ', cs.A_REVERSE)

    stdscr.refresh()
    cv1.refresh()
    cv2.refresh()

if __name__ == "__main__":

    if len(argv) != 3:
        print(usage)
        exit()

    stdscr = cs.initscr()
    cs.noecho()
    cs.cbreak()

    cf1 = open(argv[1], 'r')
    cf2 = open(argv[2], 'r')

    clip1 = Clip(cf1)
    clip2 = Clip(cf2)

    objects = {
        'clip1': clip1,
        'clip2': clip2
    }

    layout(stdscr, objects)

    # run()
    input('a')

    cs.endwin()

    cf1.close()
    cf2.close()
