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

class D(object):
    pass



class CreateSpecialMethodsTest(unittest.TestCase):
    def testSetAttrNotInEmptyClasss(self):
        self.assertTrue('__setattr__' not in vars(D))

    def testGetAttrNotInEmptyClasss(self):
        self.assertTrue('__getattribute__' not in vars(D))

    def testCreateOfSetAttrMethod(self):
        self.assertTrue('__setattr__' in vars(C))

    def testCreateOfGetAttrMethod(self):
        self.assertTrue('__getattribute__' in vars(C))

