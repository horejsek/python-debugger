# -*- coding: utf-8 -*-

import debugger


log_stream = open('mylog', 'a')

def log_method(msg):
    log_stream.write('%s\n' % msg)

debugger.DebugMetaclass.set_log_method(log_method)


# Python3:
# class C(object, metaclass=debugger.DebugMetaclass):
class C(object):
    __metaclass__ = debugger.DebugMetaclass

    def f(self):
        return 'f'


c = C()
c.f()


log_stream.close()


"""
Call of method C.f(<__main__.C object at 0x8b60aec>)
Traceback:
	ownLogger.py:24:
		c.f()
Time: 0.000 s
Result: 'f'
"""

