# -*- coding: utf-8 -*-
#
# debugger
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/python-debugger
#

import traceback
import time
import re
import logging
logging.basicConfig(level=logging.DEBUG)

# Python 2 vs. Python 3.
try:
    unicode
except NameError:
    unicode = str



def mergeDebugMetaclassWith(UserMetaclass):
    """If your class already have some metaclass and you want to use this
    debugger, you need create new one by inherit from both metaclasses - your
    metaclass and metaclass of this debugger. For this purpose there is this
    helper function which create new metaclass automaticaly. You just need to
    pass on reference to your metaclass.
    """
    class NewMetaclass(UserMetaclass, DebugMetaclass):
        def __new__(metacls, className, bases, classDict):
            cls = UserMetaclass.__new__(metacls, className, bases, classDict)
            DebugMetaclass.decorateIt(cls, className, bases, classDict)
            return cls
    return NewMetaclass



class DebugMetaclass(type):
    """Metaclass which do some logging of using your classes."""

    # Misc logging options.
    _debug_tracebackDeep = 3
    _debug_logByRegexp = ''

    # Logging options of ATTRIBUTES.
    _debug_logOfSettingAttributes = True
    _debug_logOfGettingAttributes = True
    _debug_logOfGettingUndefinedAttributes = True
    _debug_logOfGettingPrivateAttributes = False

    # Logging options of METHODS.
    _debug_logOfCallingMethod = True
    _debug_logOfResultOfMethod = True
    _debug_logTimes = True

    # Logging prefixes.
    _debug_logStartString1 = '#DEBUG#> '
    _debug_logStartString2 = '#> '


    def __new__(metacls, className, bases, classDict):
        # Create new instance of classname.
        cls = type.__new__(metacls, className, bases, classDict)
        metacls.decorateIt(cls, className, bases, classDict)
        return cls

    @classmethod
    def decorateIt(metacls, cls, className, bases, classDict):
        # Decorate all methods.
        for attributeName, attribute in classDict.items():
            if hasattr(attribute, '__call__') and not attributeName.startswith('__'):
                dbgDecorator = metacls.__debugDecorator(cls)
                setattr(cls, attributeName, dbgDecorator(attribute))

        # Add logging methods for set & get.
        if '__setattr__' not in classDict:
            cls.__setattr__ = metacls.__createSetAttrMethod(cls)
        else:
            decorator = metacls.__decorateSetAttrMethod(cls)
            cls.__setattr__ = decorator(cls.__setattr__)

        if '__getattribute__' not in classDict:
            cls.__getattribute__ = metacls.__createGetAttrMethod(cls)
        else:
            decorator = metacls.__decorateGetAttrMethod(cls)
            cls.__getattribute__ = decorator(cls.__getattribute__)



    @classmethod
    def __createSetAttrMethod(metacls, cls):
        def f(self, key, value):
            value = metacls.__logOfSettingAttribute(cls, key, value)
            return super(cls, self).__setattr__(key, value)
        return f

    @classmethod
    def __decorateSetAttrMethod(metacls, cls):
        def f(fc):
            def wrapper(self, key, value):
                value = metacls.__logOfSettingAttribute(cls, key, value)
                return fc(self, key, value)
            return wrapper
        return f

    @classmethod
    def __logOfSettingAttribute(metacls, cls, key, value):
        if not metacls._debug_logOfSettingAttributes or not metacls.__logfilter(cls.__name__, key, value):
            return value

        metacls.__log('%sset attribute %s.%s to %s' % (
            metacls._debug_logStartString1,
            cls.__name__,
            key,
            repr(value),
        ))
        # Decorate new method.
        if hasattr(value, '__call__'):
            dbgDecorator = metacls.__debugDecorator(cls)
            value = dbgDecorator(value)
            metacls.__log('%ssetting of function, decorated' % metacls._debug_logStartString2)
        metacls.__calledFrom()

        return value



    @classmethod
    def __createGetAttrMethod(metacls, cls):
        def f(self, key):
            metacls.__logOfGettingAttribute(cls, self, key)
            return super(cls, self).__getattribute__(key)
        return f

    @classmethod
    def __decorateGetAttrMethod(metacls, cls):
        def f(fc):
            def wrapper(self, key):
                metacls.__logOfGettingAttribute(cls, self, key)
                return fc(self, key)
            return wrapper
        return f

    @classmethod
    def __logOfGettingAttribute(metacls, cls, ins, key):
        if not metacls.__logfilter(cls.__name__, key):
            return

        if (
            not key.startswith('__') and
            key not in ins.__dict__ and
            key not in ins.__class__.__dict__
        ):
            if not metacls._debug_logOfGettingUndefinedAttributes:
                return
            of = 'undefined attribute'
        elif not key.startswith('__'):
            if not metacls._debug_logOfGettingAttributes:
                return
            # Methods are logged by decorators.
            value = super(cls, ins).__getattribute__(key)
            if hasattr(value, '__call__'):
                return
            of = 'attribute'
        # Some internal private variable starting with `__`.
        else:
            if not metacls._debug_logOfGettingPrivateAttributes:
                return
            of = 'internal attribute'

        metacls.__log('%sget of %s %s.%s' % (
            metacls._debug_logStartString1,
            of,
            cls.__name__,
            key,
        ))
        metacls.__calledFrom()



    @classmethod
    def __debugDecorator(metacls, cls):
        def f(func):
            def wrapper(*args, **kwds):
                metacls.__logOfMethodCalls(cls, func, args, kwds)
                res = metacls.__logOfMethods(cls, func, args, kwds)
                return res
            return wrapper
        return f

    @classmethod
    def __logOfMethodCalls(metacls, cls, func, args, kwds):
        if metacls.__ifLogMethods(cls, func, args, kwds):
            return

        metacls.__log('%scall of %s.%s(%s%s%s)' % (
            metacls._debug_logStartString1,
            cls.__name__,
            func.__name__,
            ', '.join(str(arg) for arg in args),
            ', ' if kwds else '',
            ', '.join('%s=%s' % (k, v) for k, v in kwds.items()),
        ))
        metacls.__calledFrom()

    @classmethod
    def __logOfMethods(metacls, cls, func, args, kwds):
        if metacls.__ifLogMethods(cls, func, args, kwds):
            res = func(*args, **kwds)
            return res

        try:
            startTime = time.time()
            res = func(*args, **kwds)
            endTime = time.time()

            if metacls._debug_logTimes:
                metacls.__log('%stime: %.3f s' % (metacls._debug_logStartString2, (endTime - startTime)))
            if metacls._debug_logOfResultOfMethod:
                metacls.__log('%swith result: %s' % (metacls._debug_logStartString2, repr(res)))
        except Exception as e:
            metacls.__log('%swith fail: %s' % (metacls._debug_logStartString2, repr(e)))
            raise
        else:
            return res

    @classmethod
    def __ifLogMethods(metacls, cls, func, args, kwds):
        return not metacls._debug_logOfCallingMethod or not metacls.__logfilter(cls.__name__, func.__name__, args, kwds)



    @classmethod
    def __logfilter(metacls, *args):
        def toStr(val):
            if isinstance(val, (list, tuple)):
                return ' '.join(toStr(v) for v in val)
            elif isinstance(val, dict):
                return ' '.join('%s=%s' % (k, toStr(v)) for k, v in val.items())
            else:
                return unicode(val)

        if re.search(metacls._debug_logByRegexp, toStr(args)):
            return True
        return False



    @classmethod
    def __calledFrom(metacls):
        startDeep = 3
        for calledFrom in traceback.extract_stack()[-(startDeep + metacls._debug_tracebackDeep):-startDeep][::-1]:
            metacls.__log('%scalled from %s:%d: %s' % (
                metacls._debug_logStartString2,
                calledFrom[0],
                calledFrom[1],
                calledFrom[3],
            ))



    @classmethod
    def __log(metacls, msg):
        logging.debug(msg)

    @staticmethod
    def setLogMethod(logMethod):
        def f(metacls, msg):
            logMethod(msg)
        DebugMetaclass.__log = classmethod(f)
