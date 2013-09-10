# debugger

Python library for debugging.

## Requirements

Python 2.6 or later.

## Installation

    $ sudo pip install debugger

## Examples

    import debugger
    import logging
    logging.basicConfig(level=logging.DEBUG)

    class C(object):
        __metaclass__ = debugger.DebugMetaclass

        def f(self, **kwds):
            return 3

    c = C()
    c.f()
    c.f(a=1, b=2)
    c.x = 1

This code will print:

    DEBUG:root:Call of method C.f(<__main__.C object at 0x8daa22c>)
    Traceback:
	    x.py:12:
		    c.f()
    Time: 0.000 s
    Result: 3
    DEBUG:root:Call of method C.f(<__main__.C object at 0x8daa22c>, a=1, b=2)
    Traceback:
	    x.py:13:
		    c.f(a=1, b=2)
    Time: 0.000 s
    Result: 3
    DEBUG:root:Setting attribute C.x to 1
    Traceback:
	    x.py:14:
		    c.x = 1

For more examples check out directory examples.


Enjoy!
