#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import upcloud

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()   

setup(
    name='upcloud',
    version=upcloud.__version__,
    license='License :: OSI Approved :: MIT License',
    description='manage your bucket of UpYun',
    author=upcloud.__author__,
    author_email=upcloud.__mail__,
    platforms='Platform Independent',
    url='https://github.com/kehr/upcloud',
    packages=['upcloud'],
    keywords=['upyun', 'upcloud','python', 'client'],
    install_requires=[
        "upyun >= 2.2.0",
        "progressbar >= 2.2"
    ],
    entry_points={
        'console_scripts': [
            'upcloud=upcloud.main:main',
        ],
    },
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Topic :: Software Development',
        'Topic :: Utilities',
    ],
)
