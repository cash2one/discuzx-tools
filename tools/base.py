#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys


def init():
    sys.path.append(
        os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
    return True


config_setup = init()
