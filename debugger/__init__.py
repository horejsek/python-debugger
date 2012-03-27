# -*- coding: utf-8 -*-
#
# debugger
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/python-debugger
#

import traceback
import time



class DebugMetaClass(type):
    # Misc logging options.
    tracebackDeep = 3

    # Logging options of ATTRIBUTES.
    logOfSettingAttributes = True
    logOfGettingAttributes = True
    logOfGettingUndefinedAttributes = True
    logOfGettingPrivateAttributes = False

    # Logging options of METHODS.
    logOfCallingMethod = True
    logOfResultOfMethod = True
    logTimes = True

    # Logging prefixes.
    logStartString1 = '#DEBUG#> '
    logStartString2 = '#> '


    def __new__(metacls, classname, bases, classDict):
        # Create new instance of classname.
        cls = type.__new__(metacls, classname, bases, classDict)

        # Decorate all methods.
        for attributeName, attribute in classDict.items():
            if hasattr(attribute, '__call__'):
                dbgDecorator = metacls.debugDecorator(cls)
                setattr(cls, attributeName, dbgDecorator(attribute))

        # Add logging methods for set & get.
        cls.__setattr__ = metacls.createSetAttrMethod(cls)
        cls.__getattribute__ = metacls.createGetAttrMethod(cls)

        return cls



    @classmethod
    def createSetAttrMethod(metacls, cls):
        def f(self, key, value):
            metacls.logOfSettingAttribute(cls, key, value)
            return super(cls, self).__setattr__(key, value)
        return f

    @classmethod
    def logOfSettingAttribute(metacls, cls, key, value):
        if not metacls.logOfSettingAttributes:
            return

        metacls.log('%sset attribute %s.%s to %s' % (
            metacls.logStartString1,
            cls.__name__,
            key,
            repr(value),
        ))
        # Decorate new method.
        if hasattr(value, '__call__'):
            dbgDecorator = DebugMetaClass.debugDecorator(cls)
            value = dbgDecorator(value)
            metacls.log('%ssetting of function, decorated' % metacls.logStartString2)
        metacls.calledFrom()



    @classmethod
    def createGetAttrMethod(metacls, cls):
        def f(self, key):
            metacls.logOfGettingAttribute(cls, self, key)
            return super(cls, self).__getattribute__(key)
        return f

    @classmethod
    def logOfGettingAttribute(metacls, cls, ins, key):
        if (
            not key.startswith('__') and
            key not in ins.__dict__ and
            key not in ins.__class__.__dict__
        ):
            if not metacls.logOfGettingUndefinedAttributes:
                return
            of = 'undefined attribute'
        elif not key.startswith('__'):
            if not metacls.logOfGettingAttributes:
                return
            # Methods are logged by decorators.
            value = super(cls, ins).__getattribute__(key)
            if hasattr(value, '__call__'):
                return
            of = 'attribute'
        # Some internal private variable starting with `__`.
        else:
            if not metacls.logOfGettingPrivateAttributes:
                return
            of = 'internal attribute'

        metacls.log('%sget of %s %s.%s' % (
            metacls.logStartString1,
            of,
            cls.__name__,
            key,
        ))
        metacls.calledFrom()



    @classmethod
    def debugDecorator(metacls, cls):
        def f(func):
            def wrapper(*args, **kwds):
                metacls.logOfMethodCalls(cls, func, args, kwds)
                res = metacls.logOfMethods(func, args, kwds)
                return res
            return wrapper
        return f

    @classmethod
    def logOfMethodCalls(metacls, cls, func, args, kwds):
        if not metacls.logOfCallingMethod:
            return

        metacls.log('%scall of %s.%s(%s%s%s)' % (
            metacls.logStartString1,
            cls.__name__,
            func.__name__,
            ', '.join(str(arg) for arg in args),
            ', ' if kwds else '',
            ', '.join('%s=%s' % (k, v) for k, v in kwds.items()),
        ))
        metacls.calledFrom()

    @classmethod
    def logOfMethods(metacls, func, args, kwds):
        if not metacls.logOfCallingMethod:
            res = func(*args, **kwds)
            return res

        try:
            startTime = time.time()
            res = func(*args, **kwds)
            endTime = time.time()

            if metacls.logTimes:
                metacls.log('%stime: %.3f s' % (metacls.logStartString2, (endTime - startTime)))
            if metacls.logOfResultOfMethod:
                metacls.log('%swith result: %s' % (metacls.logStartString2, repr(res)))
        except Exception as e:
            metacls.log('%swith fail: %s' % (metacls.logStartString2, repr(e)))
            raise
        else:
            return res



    @classmethod
    def calledFrom(metacls):
        startDeep = 3
        for calledFrom in traceback.extract_stack()[-(startDeep + metacls.tracebackDeep):-startDeep][::-1]:
            metacls.log('%scalled from %s:%d: %s' % (
                metacls.logStartString2,
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
