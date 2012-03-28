# -*- coding: utf-8 -*-
#
# debugger
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/python-debugger
#

import debugger



logStream = open('mylog', 'a')

def logMethod(msg):
    logStream.write('%s\n' % msg)

debugger.DebugMetaClass.setLogMethod(logMethod)



# Python3:
# class C(object, metaclass=debugger.DebugMetaClass):
class C(object):
    __metaclass__ = debugger.DebugMetaClass

    def f(self):
        return 'f'



c = C()
c.f()



logStream.close()



'''
#DEBUG#> call of C.f(<__main__.C object at 0x8302dac>)
#> called from examples/ownLogger.py:32: c.f()
#> time: 0.000 s
#> with result: 'f'
'''
