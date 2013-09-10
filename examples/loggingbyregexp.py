# -*- coding: utf-8 -*-

import debugger
import time
import logging
logging.basicConfig(level=logging.DEBUG)


debugger.DebugMetaclass._debug_log_by_regexp = 'sum'


# Python3:
# class C(object, metaclass=debugger.DebugMetaclass):
class C(object):
    __metaclass__ = debugger.DebugMetaclass

    def __init__(self):
        pass

    def pow(self, num, exponent=2):
        return num**exponent

    def sum(self, *args):
        time.sleep(0.235)
        return sum(args)


c = C()

try: c.x
except: pass

c.x = 1
c.x

c.pow(3)
c.pow(num=3, exponent=3)

c.sum(1, 2, 3, 4, 5)


"""
DEBUG:root:Call of method C.sum(<__main__.C object at 0x9605c0c>, 1, 2, 3, 4, 5)
Traceback:
	loggingByRegexp.py:39:
		c.sum(1, 2, 3, 4, 5)
Time: 0.235 s
Result: 15
"""

