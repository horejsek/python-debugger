# -*- coding: utf-8 -*-

import debugger
import logging
logging.basicConfig(level=logging.DEBUG)

"""
With following options debuger will print nothing.
"""

debugger.DebugMetaclass._debug_traceback_deep = 0
debugger.DebugMetaclass._debug_log_by_regexp = ''

debugger.DebugMetaclass._debug_log_setting_attributes = False
debugger.DebugMetaclass._debug_log_getting_attributes = False
debugger.DebugMetaclass._debug_log_getting_undefined_attributes = False
debugger.DebugMetaclass._debug_log_getting_private_attributes = False

debugger.DebugMetaclass._debug_log_calling_method = False
debugger.DebugMetaclass._debug_log_magic_method = False
debugger.DebugMetaclass._debug_log_result_of_method = False
debugger.DebugMetaclass._debug_log_times = False


# Python3:
# class C(object, metaclass=debugger.DebugMetaclass):
class C(object):
    __metaclass__ = debugger.DebugMetaclass

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

