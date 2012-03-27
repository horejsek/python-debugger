# -*- coding: utf-8 -*-
#
# debugger
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/python-debugger
#

import debugger



# Python3:
# class C(object, metaclass=debugger.DebugMetaClass):
class C(object):
    __metaclass__ = debugger.DebugMetaClass



c = C()

C.f = lambda self: 42

c.f = lambda: 24

c.f()



'''
It's working only for adding of methods to the instances.

#DEBUG# set attribute C.f to <function <lambda> at 0xb73f8764>
	setting of function, decorated
	called from examples/dynamiclyAddedMethod.py:20: c.f = lambda: 24
#DEBUG# call of C.<lambda>()
	time: 0 ms
	with result: 24
	called from examples/dynamiclyAddedMethod.py:22: c.f()
'''
