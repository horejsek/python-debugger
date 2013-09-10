#!/usr/bin/env python
#
# debugger
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/python-debugger
#

from distutils.core import setup

setup(
    name = 'debugger',
    packages = [
        'debugger/',
    ],
    version = '1.3',
    url = 'https://github.com/horejsek/python-debugger',
    description = 'Debugging.',
    author = 'Michal Horejsek',
    author_email = 'horejsekmichal@gmail.com',
    license='PSF',
    classifiers = [
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Python Software Foundation License',
        'Operating System :: OS Independent',
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)

