# -*- coding: utf-8 -*-
#
# debugger
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/python-debugger
#

import unittest

import debugger
debugger.DebugMetaClass.setLogMethod(lambda msg: None)



class C(object):
    __metaclass__ = debugger.DebugMetaClass

    calls = 0

    def f(self):
        C.calls += 1

class D(object):
    def f(self):
        pass



class DecorateMethodsTest(unittest.TestCase):
    def testDecorate(self):
        self.assertNotEqual(C.f.__name__, D.f.__name__)

    def testNotOverwrite(self):
        c = C()
        self.assertEqual(C.calls, 0)
        c.f()
        self.assertEqual(C.calls, 1)

    def testNotDecorateVariables(self):
        self.assertFalse(hasattr(C.calls, '__call__'))
