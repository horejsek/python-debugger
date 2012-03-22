# -*- coding: utf-8 -*-
#
# debugger
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/python-debugger
#

import traceback
import time



class DebugMetaClass(type):
    tracebackDeep = 2

    logOfSettingAttributes = True
    logOfGettingAttributes = True
    logOfGettingUndefinedAttributes = True

    logOfCallingMethod = True
    logOfResultOfMethod = True

    logTimes = True

    def __new__(metacls, classname, bases, classDict):
        cls = type.__new__(metacls, classname, bases, classDict)

        for attributeName, attribute in classDict.items():
            if hasattr(attribute, '__call__'):
                dbgDecorator = DebugMetaClass.debugDecorator(cls)
                setattr(cls, attributeName, dbgDecorator(attribute))

        cls.__setattr__ = DebugMetaClass.createSetAttrMethod(cls)
        cls.__getattribute__ = DebugMetaClass.createGetAttrMethod(cls)

        return cls

    @classmethod
    def createSetAttrMethod(metacls, cls):
        def f(self, key, value):
            if metacls.logOfSettingAttributes:
                metacls.log('#DEBUG# set attribute %s.%s to %s' % (
                    cls.__name__,
                    key,
                    repr(value),
                ))
                if hasattr(value, '__call__'):
                    dbgDecorator = DebugMetaClass.debugDecorator(cls)
                    value = dbgDecorator(value)
                    metacls.log('\tsetting of function, decorated')
                metacls.calledFrom()
            return super(cls, self).__setattr__(key, value)
        return f

    @classmethod
    def createGetAttrMethod(metacls, cls):
        def f(self, key):
            if not key.startswith('__') and (key not in self.__dict__ and key not in self.__class__.__dict__):
                if metacls.logOfGettingUndefinedAttributes:
                    metacls.log('#DEBUG# get of undefined attribute %s.%s' % (cls.__name__, key))
                    metacls.calledFrom()
            elif not key.startswith('__'):
                value = super(cls, self).__getattribute__(key)
                if metacls.logOfGettingAttributes and not hasattr(value, '__call__'):
                    metacls.log('#DEBUG# get of attribute %s.%s' % (cls.__name__, key))
                    metacls.calledFrom()
            return super(cls, self).__getattribute__(key)
        return f

    @classmethod
    def debugDecorator(metacls, cls):
        def f(func):
            def wrapper(*args, **kwds):
                if not metacls.logOfCallingMethod:
                    return func(*args, **kwds)

                metacls.log('#DEBUG# call of %s.%s(%s%s%s)' % (
                    cls.__name__,
                    func.__name__,
                    ', '.join(str(arg) for arg in args),
                    ', ' if kwds else '',
                    ', '.join('%s=%s' % (k, v) for k, v in kwds.items()),
                ))
                try:
                    startTime = time.time()
                    res = func(*args, **kwds)
                    endTime = time.time()
                    if metacls.logTimes:
                        metacls.log('\ttime: %.3f s' % ((endTime - startTime)))
                    if metacls.logOfResultOfMethod:
                        metacls.log('\twith result: %s' % repr(res))
                    metacls.calledFrom()
                except Exception as e:
                    metacls.log('\twith fail: %s' % repr(e))
                    metacls.calledFrom()
                    raise e
                else:
                    return res
            return wrapper
        return f

    @classmethod
    def calledFrom(metacls):
        startDeep = 2
        for calledFrom in traceback.extract_stack()[-(startDeep + metacls.tracebackDeep):-startDeep][::-1]:
            metacls.log('\tcalled from %s:%d: %s' % (
                calledFrom[0],
                calledFrom[1],
                calledFrom[3],
            ))

    @classmethod
    def log(metacls, msg):
        print(msg)

    @staticmethod
    def setLogMethod(logMethod):
        def f(metacls, msg):
            logMethod(msg)
        DebugMetaClass.log = classmethod(f)

