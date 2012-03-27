# -*- coding: utf-8 -*-
#
# debugger
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/python-debugger
#

import debugger
import time



debugger.DebugMetaClass.logByRegexp = 'sum'



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
#DEBUG#> call of C.sum(<__main__.C object at 0xb70f4e0c>, 1, 2, 3, 4, 5)
#> called from examples/loggingByRegexp.py:44: c.sum(1, 2, 3, 4, 5)
#> time: 0.235 s
#> with result: 15
'''
