# -*- coding: utf-8 -*-
#
# debugger
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/python-debugger
#

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + '/../'))

import unittest

import createSpecialMethods
import decorateSpecialMethods
import decorateMethods


testModules = (
    createSpecialMethods,
    decorateSpecialMethods,
    decorateMethods,
)


loader = unittest.TestLoader()

suite = loader.loadTestsFromModule(testModules[0])
for testModule in testModules[1:]:
    suite.addTests(loader.loadTestsFromModule(testModule))

runner = unittest.TextTestRunner(verbosity=0)
result = runner.run(suite)

if not result.wasSuccessful():
    sys.exit(1)
