# -*- coding: utf-8 -*-
#
# debugger
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/python-debugger
#

import debugger
import time



class C(object, metaclass=debugger.DebugMetaClass):
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



'''
#DEBUG# call of C.__init__(<__main__.C object at 0xb752cbcc>)
	time: 0.000 s
	with result: None
	called from examples/example.py:25: c = C()
#DEBUG# get of undefined attribute C.x
	called from examples/example.py:27: try: c.x
#DEBUG# set attribute C.x to 1
	called from examples/example.py:30: c.x = 1
#DEBUG# get of attribute C.x
	called from examples/example.py:31: c.x
#DEBUG# call of C.pow(<__main__.C object at 0xb752cbcc>, 3)
	time: 0.000 s
	with result: 9
	called from examples/example.py:33: c.pow(3)
#DEBUG# call of C.pow(<__main__.C object at 0xb752cbcc>, num=3, exponent=3)
	time: 0.000 s
	with result: 27
	called from examples/example.py:34: c.pow(num=3, exponent=3)
#DEBUG# call of C.sum(<__main__.C object at 0xb752cbcc>, 1, 2, 3, 4, 5)
	time: 0.235 s
	with result: 15
	called from examples/example.py:36: c.sum(1, 2, 3, 4, 5)
'''
