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



class C(object):
    __metaclass__ = debugger.DebugMetaClass

    def f(self):
        return 'f'



c = C()
c.f()



logStream.close()



'''
#DEBUG# call of C.f(<__main__.C object at 0xb74c250c>)
	with result: 'f'
	called from examples/ownLogger.py:26: c.f()
'''
