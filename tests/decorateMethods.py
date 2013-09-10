# -*- coding: utf-8 -*-

import unittest

import debugger
debugger.DebugMetaclass.set_log_method(lambda msg: None)


class C(object):
    __metaclass__ = debugger.DebugMetaclass

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
