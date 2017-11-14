#!/usr/bin/python
# -*- coding: ascii -*-

from os.path import abspath, dirname, join
from glob import glob
from distutils.core import setup, Extension

args = {
    'name'          : 'FellesLab',
    'description'   : 'Laboratory Setups at NTNU',
    'version'       : '0.1.0',
    'packages'      : ['felleslab',
                       'felleslab.communication',
                       'felleslab.core',
                       'felleslab.equipment',
                       'felleslab.icons',
                       'felleslab.qt_plugins',
                       'felleslab.qt_widgets',
                       'felleslab.qt_widgets.thermocouple',
                       'felleslab.qt_widgets.solenoidvalve',
                       'felleslab.qt_widgets.controller',
                       'felleslab.qt_widgets.buttons'
                      ],
    'package_dir'  : {'felleslab': 'src'},
    'package_data' : {
                       'felleslab.icons': ['src','icons','*/*.svg'],
                     },
                     
    'classifiers': [
        "License :: GNU - General Public License (GPL)",
        "Programing Language :: Python",
        "Development Status :: 0 - Beta",
        "Intended Audience :: Science and Engineering",
        "Topic :: Communications and IoT",
    ],
    'keywords': 'RS485',
} # end ARGS


setup(**args)

