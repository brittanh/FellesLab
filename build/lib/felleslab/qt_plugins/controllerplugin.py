#!/usr/bin/python
# -*- coding: ascii -*-
"""
ooooooooooo        oooo oooo                     ooooo                .o8       
`888'    `8        `888 `888                     `888'               "888       
 888      .ooooo.   888  888   .ooooo.   .oooo.o  888        .oooo.   888oooo.  
 888ooo8 d88' `88b  888  888  d88' `88b d88(  "8  888       `P  )88b  d88' `88b 
 888   " 888ooo888  888  888  888ooo888 `"Y88b.   888        .oP"888  888   888 
 888     888    .o  888  888  888    .o o.  )88b  888     o d8(  888  888   888 
o888o    `Y8bod8P' o888oo888o `Y8bod8P' 8""888P' o888ooood8 `Y888""8o `Y8bod8P' 

@summary       Controller
@author:       Brittany Hall
@organization  Department of Chemical Engineering, NTNU, Norway
@contact       sigve.karolius@ntnu.no
@license       Free (GPL.v3) !!! Distributed as-is !!!
@requires      Python 2.7.x or higher
@since         2017-11-02
@version       0.1

"""

#from PyQt5.QtGui import QIcon, QPixmap
#from PyQt5.QtDesigner import QPyDesignerCustomWidgetPlugin

from PyQt4.QtGui import QIcon, QPixmap
from PyQt4.QtDesigner import QPyDesignerCustomWidgetPlugin


from felleslab.qt_widgets.controller import QFellesController
from felleslab.icons import *

# Name of the Icon used for the widget
my_widget_icon  = ':/icons/thermocouples/16x16_thumbnail.png'
my_widget_name  = "QFellesController"
my_widget_group = "QtFellesLabWidgets"
my_widget_module = 'felleslab.qt_widgets.controller'

class PyControllerPlugin(QPyDesignerCustomWidgetPlugin):

    def __init__(self, parent=None):
        super(PyControllerPlugin, self).__init__(parent)
        self.initialized = False

    def initialize(self, interface=None):
        """ Called after plugin is loaded into QtDesigner """
        if self.initialized:
            return
        self.initialized = True

    def isInitialized(self):
        return self.initialized

    def createWidget(self, parent):
        """ Create a new instance of the widget with the appropriate parent """
        return QFellesController(parent)

    def name(self):
        """ Name of the custom widget class that is provided by this plugin """
        return my_widget_name

    def group(self):
        """ Return the group of the QtDesigner box the widget belongs to """
        return my_widget_group

    def icon(self):
        """ Icon used to represent the widget in the QtDesigner box """
        return QIcon(QPixmap(my_widget_icon))

    def toolTip(self):
        return ""

    def whatsThis(self):
        return ""

    def isContainer(self):
        """ Is the widget a container for other widgets? """
        return False

    def domXml(self):
        """ XML description of the default values of the properties """
        return '<widget class="%s" name="%s">\n' \
               ' <property name="toolTip">\n' \
               '  <string>Tip</string>\n' \
               ' </property>\n' \
               ' <property name="whatsThis">\n' \
               '  <string>What is this</string>\n' \
               ' </property>\n' \
               ' <property name="portname">\n' \
               '  <string>/dev/ttyUSB0</string>\n' \
               ' </property>\n' \
               ' <property name="slaveaddress">\n' \
               '  <number>0</number>\n' \
               ' </property>\n' \
               ' <property name="channel">\n' \
               '  <number>0</number>\n' \
               ' </property>\n' \
               '</widget>\n' %(my_widget_name,"Valve")

    def includeFile(self):
        """ Returns the module containing the custom widget class """
        return "%s" %(my_widget_module)

