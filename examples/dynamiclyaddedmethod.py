# -*- coding: utf-8 -*-

import debugger
import logging
logging.basicConfig(level=logging.DEBUG)


# Python3:
# class C(object, metaclass=debugger.DebugMetaclass):
class C(object):
    __metaclass__ = debugger.DebugMetaclass


c = C()

C.f = lambda self: 42

c.f = lambda: 24

c.f()


"""
It's working only for adding of methods to the instances.

DEBUG:root:Setting attribute C.f to <function <lambda> at 0x94ae64c>
Traceback:
	dynamiclyAddedMethod.py:18:
		c.f = lambda: 24
DEBUG:root:Call of method C.<lambda>()
Traceback:
	dynamiclyAddedMethod.py:20:
		c.f()
Time: 0.000 s
Result: 24
"""

