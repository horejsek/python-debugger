# -*- coding: utf-8 -*-

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


def merge_debug_metaclass_with(UserMetaclass):
    """
    If your class already have some metaclass and you want to use this
    debugger, you need create new one by inherit from both metaclasses - your
    metaclass and metaclass of this debugger. For this purpose there is this
    helper function which create new metaclass automaticaly. You just need to
    pass on reference to your metaclass.
    """
    class NewMetaclass(UserMetaclass, DebugMetaclass):
        def __new__(mcs, classname, bases, classdict):
            cls = UserMetaclass.__new__(mcs, classname, bases, classdict)
            DebugMetaclass.decorate_it(cls, classname, bases, classdict)
            return cls
    return NewMetaclass


class DebugMetaclass(type):
    """Metaclass which do some logging of using your classes."""

    # Misc logging options.
    _debug_traceback_deep = 3
    _debug_log_by_regexp = ''

    # Logging options of ATTRIBUTES.
    _debug_log_setting_attributes = True
    _debug_log_getting_attributes = True
    _debug_log_getting_undefined_attributes = True
    _debug_log_getting_private_attributes = False

    # Logging options of METHODS.
    _debug_log_calling_method = True
    _debug_log_magic_method = False
    _debug_log_result_of_method = True
    _debug_log_times = True

    def __new__(mcs, classname, bases, classdict):
        # Create new instance of classname.
        cls = type.__new__(mcs, classname, bases, classdict)
        mcs.decorate_it(cls, classname, bases, classdict)
        return cls

    @classmethod
    def decorate_it(mcs, cls, classname, bases, classdict):
        # Decorate all methods.
        for attribute_name, attribute in classdict.items():
            if not hasattr(attribute, '__call__'):
                continue
            if attribute_name.startswith('__') and not mcs._debug_log_magic_method:
                continue
            decorator = mcs.__create_method_decorator(cls)
            setattr(cls, attribute_name, decorator(attribute))

        # Add logging methods for set & get.
        if '__setattr__' not in classdict:
            cls.__setattr__ = mcs.__create_setattr_method(cls)
        else:
            decorator = mcs.__create_setattr_decorator(cls)
            cls.__setattr__ = decorator(cls.__setattr__)

        if '__getattribute__' not in classdict:
            cls.__getattribute__ = mcs.__create_getattr_method(cls)
        else:
            decorator = mcs.__create_getattr_decorator(cls)
            cls.__getattribute__ = decorator(cls.__getattribute__)

    @classmethod
    def __create_setattr_method(mcs, cls):
        def func(self, key, value):
            value = mcs.__log_setting_attribute(cls, key, value)
            return super(cls, self).__setattr__(key, value)
        return func

    @classmethod
    def __create_setattr_decorator(mcs, cls):
        def decorator(func):
            def wrapper(self, key, value):
                value = mcs.__log_setting_attribute(cls, key, value)
                return func(self, key, value)
            return wrapper
        return decorator

    @classmethod
    def __log_setting_attribute(mcs, cls, key, value):
        if not mcs._debug_log_setting_attributes or not mcs.__if_log_by_filter(cls.__name__, key, value):
            return value

        msg = 'Setting attribute %s.%s to %s\n%s' % (
            cls.__name__,
            key,
            repr(value),
            mcs.__get_msg_called_from(),
        )

        # Decorate new method.
        if hasattr(value, '__call__'):
            dbg_decorator = mcs.__create_method_decorator(cls)
            value = dbg_decorator(value)

        mcs.__log(msg)
        return value

    @classmethod
    def __create_getattr_method(mcs, cls):
        def func(self, key):
            mcs.__log_getting_attribute(cls, self, key)
            return super(cls, self).__getattribute__(key)
        return func

    @classmethod
    def __create_getattr_decorator(mcs, cls):
        def decorator(func):
            def wrapper(self, key):
                mcs.__log_getting_attribute(cls, self, key)
                return func(self, key)
            return wrapper
        return decorator

    @classmethod
    def __log_getting_attribute(mcs, cls, ins, key):
        if not mcs._debug_log_getting_attributes or not mcs.__if_log_by_filter(cls.__name__, key):
            return

        if (
            not key.startswith('__') and
            key not in ins.__dict__ and
            key not in ins.__class__.__dict__
        ):
            if not mcs._debug_logOfGettingUndefinedAttributes:
                return
            attribute_type = 'undefined attribute'
        elif not key.startswith('__'):
            if not mcs._debug_log_getting_attributes:
                return
            # Methods are logged by decorators.
            value = super(cls, ins).__getattribute__(key)
            if hasattr(value, '__call__'):
                return
            attribute_type = 'attribute'
        # Some internal private variable starting with `__`.
        else:
            if not mcs._debug_log_getting_private_attributes:
                return
            attribute_type = 'private attribute'

        mcs.__log('Getting of %s %s.%s\n%s' % (
            attribute_type,
            cls.__name__,
            key,
            mcs.__get_msg_called_from(),
        ))

    @classmethod
    def __create_method_decorator(mcs, cls):
        def decorator(func):
            def wrapper(*args, **kwds):
                res = mcs.__log_method(cls, func, args, kwds)
                return res
            return wrapper
        return decorator

    @classmethod
    def __log_method(mcs, cls, func, args, kwds):
        if not mcs._debug_log_calling_method or not mcs.__if_log_by_filter(cls.__name__, func.__name__, args, kwds):
            res = func(*args, **kwds)
            return res

        msg = 'Call of method %s.%s(%s%s%s)\n%s' % (
            cls.__name__,
            func.__name__,
            ', '.join(repr(arg) for arg in args),
            ', ' if kwds else '',
            ', '.join('%s=%s' % (k, v) for k, v in kwds.items()),
            mcs.__get_msg_called_from(),
        )

        try:
            start = time.time()
            res = func(*args, **kwds)
            end = time.time()

            if mcs._debug_log_times:
                msg += '\nTime: %.3f s' % (end - start)
            if mcs._debug_log_result_of_method:
                msg += '\nResult: %s' % repr(res)
        except Exception as exc:
            msg += '\nFailed: %s' % repr(exc)
            raise
        else:
            return res
        finally:
            mcs.__log(msg)

    @classmethod
    def __if_log_by_filter(mcs, *args):
        if re.search(mcs._debug_log_by_regexp, _to_string(args)):
            return True
        return False

    @classmethod
    def __get_msg_called_from(mcs):
        if not mcs._debug_traceback_deep:
            return ''
        start_deep = 3
        msg = 'Traceback:\n'
        for item in traceback.extract_stack()[-(start_deep + mcs._debug_traceback_deep):-start_deep][::-1]:
            msg += '\t%s:%d:\n\t\t%s\n' % (
                item[0],
                item[1],
                item[3],
            )
        return msg.rstrip('\n')

    @classmethod
    def __log(mcs, msg):
        logging.debug(msg)

    @staticmethod
    def set_log_method(log_method):
        def func(mcs, msg):
            log_method(msg)
        DebugMetaclass.__log = classmethod(func)


def _to_string(val):
    if isinstance(val, (list, tuple)):
        return ' '.join(_to_string(v) for v in val)
    elif isinstance(val, dict):
        return ' '.join('%s=%s' % (k, _to_string(v)) for k, v in val.items())
    else:
        return unicode(val)
