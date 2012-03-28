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

#DEBUG#> set attribute C.f to <function <lambda> at 0xb713964c>
#> setting of function, decorated
#> called from examples/dynamiclyAddedMethod.py:23: c.f = lambda: 24
#DEBUG#> call of C.<lambda>()
#> called from examples/dynamiclyAddedMethod.py:25: c.f()
#> time: 0.000 s
#> with result: 24
'''
