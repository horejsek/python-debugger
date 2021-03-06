# -*- coding: utf-8 -*-

import debugger
import time
import logging
logging.basicConfig(level=logging.DEBUG)


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
DEBUG:root:Setting attribute C.x to 1
Traceback:
	example.py:30:
		c.x = 1
DEBUG:root:Getting of attribute C.x
Traceback:
	example.py:31:
		c.x
DEBUG:root:Call of method C.pow(<__main__.C object at 0x9392d0c>, 3)
Traceback:
	example.py:33:
		c.pow(3)
Time: 0.000 s
Result: 9
DEBUG:root:Call of method C.pow(<__main__.C object at 0x9392d0c>, num=3, exponent=3)
Traceback:
	example.py:34:
		c.pow(num=3, exponent=3)
Time: 0.000 s
Result: 27
DEBUG:root:Call of method C.sum(<__main__.C object at 0x9392d0c>, 1, 2, 3, 4, 5)
Traceback:
	example.py:36:
		c.sum(1, 2, 3, 4, 5)
Time: 0.235 s
Result: 15
"""

