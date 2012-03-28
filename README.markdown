# debugger

Python library for debugging.

## Requirements

- Python 2.6 or later.

## Installation

Installation of Python module `debugger` is very simple - just extract archive
and then from created directory debugger run this command:

    $ sudo make install

That's all! After this step you can start your favorite Python interpret (perhaps
bpython) and try import module `debugger`. See for examples below.


## Examples:

    class C(object):
        __metaclass__ = debugger.DebugMetaClass

        def f(self, **kwds):
            return 3

    c = C()
    c.f()
    c.f(a=1, b=2)
    c.x = 1

This code will print:

    #DEBUG#> call of C.f(<__main__.C object at 0xa463a6c>)
    #> called from <input>:2: None
    #> time: 0.000 s
    #> with result: 3
    #DEBUG#> call of C.f(<__main__.C object at 0xa463a6c>, a=1, b=2)
    #> called from <input>:2: None
    #> time: 0.000 s
    #> with result: 3
    #DEBUG#> set attribute C.x to 1
    #> called from <input>:2: None

For examples check out directory examples.


Enjoy!
