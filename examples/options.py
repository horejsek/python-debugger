# -*- coding: utf-8 -*-
#
# debugger
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/python-debugger
#

import debugger

'''
With following options debuger will print nothing.
By default is everything turn on and tracebackDeep is set to 2.
'''

debugger.DebugMetaClass.tracebackDeep = 0

debugger.DebugMetaClass.logOfSettingAttributes = False
debugger.DebugMetaClass.logOfGettingAttributes = False
debugger.DebugMetaClass.logOfGettingUndefinedAttributes = False

debugger.DebugMetaClass.logOfCallingMethod = False
debugger.DebugMetaClass.logOfResultOfMethod = False

debugger.DebugMetaClass.logTimes = False



class C(object):
    __metaclass__ = debugger.DebugMetaClass

    def __init__(self):
        pass

    def pow(self, num, exponent=2):
        return num**exponent

    def sum(self, *args):
        return sum(args)


c = C()

try: c.x
except: pass

c.x = 1
c.x

c.pow(3)
c.pow(num=3, exponent=3)

c.sum(1, 2, 3, 4, 5)
