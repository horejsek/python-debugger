# -*- coding: utf-8 -*-
#
# debugger
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/python-debugger
#

import debugger
import time



# Python3:
# class C(object, metaclass=debugger.DebugMetaClass):
class C(object):
    __metaclass__ = debugger.DebugMetaClass

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
#DEBUG#> call of C.__init__(<__main__.C object at 0x845be2c>)
#> called from examples/example.py:29: c = C()
#> time: 0.000 s
#> with result: None
#DEBUG#> get of undefined attribute C.x
#> called from examples/example.py:31: try: c.x
#DEBUG#> set attribute C.x to 1
#> called from examples/example.py:34: c.x = 1
#DEBUG#> get of attribute C.x
#> called from examples/example.py:35: c.x
#DEBUG#> call of C.pow(<__main__.C object at 0x845be2c>, 3)
#> called from examples/example.py:37: c.pow(3)
#> time: 0.000 s
#> with result: 9
#DEBUG#> call of C.pow(<__main__.C object at 0x845be2c>, num=3, exponent=3)
#> called from examples/example.py:38: c.pow(num=3, exponent=3)
#> time: 0.000 s
#> with result: 27
#DEBUG#> call of C.sum(<__main__.C object at 0x845be2c>, 1, 2, 3, 4, 5)
#> called from examples/example.py:40: c.sum(1, 2, 3, 4, 5)
#> time: 0.235 s
#> with result: 15
'''
