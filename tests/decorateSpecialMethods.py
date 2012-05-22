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

    callsOfSetattr = 0
    callsOfGetattr = 0
    foo = None

    def __setattr__(self, key, value):
        if key == 'foo':
            C.callsOfSetattr += 1
            return
        super(C, self).__setattr__(key, value)

    def __getattribute__(self, key):
        if key == 'foo':
            C.callsOfGetattr += 1
            return
        return super(C, self).__getattribute__(key)



class DecorateSpecialMethodsTest(unittest.TestCase):
    def testHasSetAttrMethod(self):
        self.assertTrue('__setattr__' in vars(C))

    def testHasGetAttrMethod(self):
        self.assertTrue('__getattribute__' in vars(C))

    def testNotOverwriteSetAttrMethod(self):
        c = C()
        self.assertEqual(C.callsOfSetattr, 0)
        c.foo = 42
        self.assertEqual(C.callsOfSetattr, 1)

    def testNotOverwriteGetAttrMethod(self):
        c = C()
        self.assertEqual(C.callsOfGetattr, 0)
        c.foo
        self.assertEqual(C.callsOfGetattr, 1)

