#!/usr/bin/env python3

# Curses ABX tester.
#
# Copyright (C) 2017  Quentin Young
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

import curses as cs
import random
from functools import partial
from pyglet.media import *
from sys import argv

version = '0.0.1'
title = 'goodear %s - An ABX Tester' % version

usage = """Usage:
    ./goodear.py -h
    ./goodear.py <clip1> <clip2>"""


class Clip:
    def __init__(self, clipfile):
        self.file = clipfile;
        self.player = Player()
        self.source = load(self.file.name, streaming=False)
        self.player.queue(self.source)
        self.channels = self.source.audio_format.channels
        self.samplerate = self.source.audio_format.sample_rate
        self.length = self.source.duration

    def play(self):
        self.player.play()

    def pause(self):
        self.player.pause()

    def time(self):
        return self.player.time

    def seek(self, time):
        self.player.seek(time)

global playing


def pause():
    global playing
    playing.pause()

def play(clip):
    global playing
    time = None
    if playing is not None:
        playing.pause()
        time = playing.time()
        clip.seek(time)
    playing = clip
    playing.play()


# key handlers
actions = {
    'a': None, # partial(play, clipA)
    'b': None, # partial(play, clipB)
    'x': None, # partial(play, clipX)
    'p': pause,
    '[': '<rewind>',
    ']': '<forward>',
    's': '<show stats>',
}

def layout(stdscr):
    stdscr.clear()

    def layout_clip(cw, clip, abx):
        cw.addstr(1, 2, abx + '  ' + clip.file.name)
        cw.vline(1, 3, cs.ACS_VLINE, 1)
        cw.vline(1, cw.getmaxyx()[1] - 4, cs.ACS_VLINE, 1)
        cw.hline(2, 1, cs.ACS_HLINE, cv1.getmaxyx()[1])
        cw.addstr(3, 2, 'Length:      %d' % clip.length)
        cw.addstr(4, 2, 'Sample rate: %d' % clip.samplerate)
        cw.addstr(5, 2, 'Channels:    %d' % clip.channels)
        cw.box()


    # maximize available space via floor
    cvw = int((cs.COLS - 2) / 3)
    cvh = 15
    cvord = (2, 1)

    cv1 = cs.newwin(cvh, cvw, cvord[0], cvord[1] + cvw * 0)
    cvx = cs.newwin(cvh, cvw, cvord[0], cvord[1] + cvw * 1)
    cv2 = cs.newwin(cvh, cvw, cvord[0], cvord[1] + cvw * 2)

    layout_clip(cv1, clipA, 'A')
    layout_clip(cv2, clipB, 'B')

    cvx.addstr(1, 2, "X (Unknown)")
    cvx.box()

    tpad = cs.COLS - len(title)
    stdscr.addstr(1, 1, ' ' + title + tpad * ' ', cs.A_REVERSE)

    stdscr.box()
    stdscr.refresh()
    cv1.refresh()
    cvx.refresh()
    cv2.refresh()

if __name__ == "__main__":

    if len(argv) != 3:
        print(usage)
        exit()

    # Load audio files
    cf1 = open(argv[1], 'r')
    cf2 = open(argv[2], 'r')

    print("Loading %s..." % cf1.name)
    clipA = Clip(cf1)
    print("Loading %s..." % cf2.name)
    clipB = Clip(cf2)

    clips = [clipA, clipB]
    clipX = random.choice(clips)
    playing = None

    # bind action handlers
    actions['a'] = partial(play, clipA)
    actions['b'] = partial(play, clipB)
    actions['x'] = partial(play, clipX)

    # setup screen
    stdscr = cs.initscr()
    cs.noecho()
    cs.cbreak()
    layout(stdscr)

    # main loop

    while True:
        key = stdscr.getch()
        if key == cs.KEY_RESIZE:
            layout(stdscr, objects)
        key = chr(key)
        if key not in actions:
            continue
        f = actions[key]
        f()


    cs.endwin()

    cf1.close()
    cf2.close()
