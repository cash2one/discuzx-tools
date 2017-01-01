#!usr/bin/env python
# coding: utf-8

import pyglet


class WarnMedia(object):
    """声音警报.

        https://github.com/AVbin/AVbin/downloads
        http://stackoverflow.com/questions/10302873/python-pyglet-avbin-how-to-install-avbin
    """

    def __init__(self, file_path):
        """先尝试相对路径, 再尝试绝对路径载入.
        """

        try:
            self.music = pyglet.resource.media(file_path)
        except pyglet.resource.ResourceNotFoundException:
            self.music = pyglet.media.load(file_path)
        else:
            self.music = None

    def play(self):
        """如有效可播放.
        """

        if self.music:
            self.music.play()
            pyglet.app.run()
