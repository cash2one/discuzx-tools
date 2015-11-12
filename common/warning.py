#!usr/bin/env python
# coding: utf-8

import pyglet


class WarnMedia(object):
    def __init__(self, file_path):
        self.music = pyglet.resource.media(file_path)

    def play(self):
        self.music.play()
        pyglet.app.run()
