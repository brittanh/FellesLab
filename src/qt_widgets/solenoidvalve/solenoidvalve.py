#!/usr/bin/env/python
# -*- coding: ascii -*-
"""
ooooooooooo        oooo oooo                     ooooo                .o8       
`888'    `8        `888 `888                     `888'               "888       
 888      .ooooo.   888  888   .ooooo.   .oooo.o  888        .oooo.   888oooo.  
 888ooo8 d88' `88b  888  888  d88' `88b d88(  "8  888       `P  )88b  d88' `88b 
 888   " 888ooo888  888  888  888ooo888 `"Y88b.   888        .oP"888  888   888 
 888     888    .o  888  888  888    .o o.  )88b  888     o d8(  888  888   888 
o888o    `Y8bod8P' o888oo888o `Y8bod8P' 8""888P' o888ooood8 `Y888""8o `Y8bod8P' 

@summary
@author:       Sigve Karolius
@organization  Department of Chemical Engineering, NTNU, Norway
@contact       sigve.karolius@ntnu.no
@license       Free (GPL.v3) !!! Distributed as-is !!!
@requires      Python 2.7.x or higher
@since         2017-06-16
@version       0.1

"""

#from PyQt5.QtCore import (pyqtProperty, pyqtSignal, pyqtSlot, QObject, QSize,
#                         QThread, QMetaObject, QEvent)
#from PyQt5.QtWidgets import (QMainWindow, QLabel, QWidget, QPushButton,
#QAbstractButton, QHBoxLayout, QVBoxLayout, QMenuBar, QStatusBar)
#from PyQt5.QtGui import QIcon, QPixmap, QFont

from PyQt4.QtCore import (QTimer, pyqtProperty, pyqtSignal, pyqtSlot, QObject,
QSize, QThread, QMetaObject, QEvent, Qt)
from PyQt4.QtGui import (QIcon, QImage, QPixmap, QFont, QMainWindow, QLabel,
                        QWidget, QPushButton,  QHBoxLayout, QVBoxLayout,
                        QAbstractButton, QDialog)


from felleslab.gui import QFellesWidgetBaseClass
from felleslab.equipment.solenoidvalve import SolenoidValve
from felleslab import icons


valve_closed = ":icons/valves/48x48_solenoid_closed.png"
valve_open   = ":icons/valves/48x48_solenoid_open.png"
valve_void   = ":icons/valves/48x48_solenoid.png"


# Valve Widget -------------------------------------------------------------- #
class QFellesSolenoidValve(QFellesWidgetBaseClass):
    """
    @brief     Widget representing a sol
    """
    valveOpen  = pyqtSignal(name="openValve")
    valveClose = pyqtSignal(name="closeValve")

    ICONS = [ valve_open, valve_closed, valve_void ]

    meta = { "type": "Position",
             "name": "Valve",
             "unit": "[-]",
             "channel" : 0,
             "portname" : "/dev/ttyUSB0",
             "slaveaddress": 1,
             "baudrate" : 19200,
            }

    _state        = -1                                          # <-- set-point
    _initialState =  0                                      # initial set-point
    _finalState   =  0                                     # terminal set-point
    _slave        = SolenoidValve

    def initUi(self, parent=None):
        """ Generates the user interface """
        self.label = QLabel(parent)
        self.label.setObjectName("Solenoid Valve")
        self.label.setPixmap(QPixmap(self.ICONS[self._state]))

        _layout = QHBoxLayout()
        _layout.addWidget(self.label)
        self.setLayout(_layout)

        self.valveClose.connect(self.closeValve)
        self.valveOpen.connect(self.openValve)

    @pyqtProperty(int)
    def initialState(self):
        return self._initialState

    @initialState.setter
    def initialState(self, value):
        self._initialState = value

    @pyqtProperty(int)
    def finalState(self):
        return self._finalState

    @finalState.setter
    def finalState(self, value):
        self._finalState = value

    @property
    def state(self):
        return self.slave.state if self.slave else -1

    @state.setter
    def state(self, value):
        self.slave.state = value
        self.paintEvent()

    def onInit(self):
        if self._initialState == 0:
            self.setOpen()
        else:
            self.setClose()

    def onQuit(self):
        if self._finalState == 0:
            self.setOpen()
        else:
            self.setClose()

    def isOpen(self):
        return self.state == 0

    def isClosed(self):
        return self.state == 1

    def closeValve(self):
        self.slave.setClose()
        self.isClosed()

    def openValve(self):
        self.slave.setOpen()
        self.isOpen()

    @pyqtSlot()
    def setSample(self, event=None):
        """ Called to update widget in GUI
        """
        sample = self.slave.getState()
        self.history.append(sample)
        self.newSample.emit(str(sample))

    @pyqtSlot()
    def setOpen(self):
        self.events.append(self.valveOpen)

    @pyqtSlot()
    def setClose(self):
        self.events.append(self.valveClose)

    @pyqtSlot()
    def setSwitchState(self):
        if self.isOpen():
            self.events.append(self.valveClose)
        else:
            self.events.append(self.valveOpen)

    def mouseReleaseEvent(self, event):
        self.setSwitchState()

    def retranslateUi(self, parent):
        self.label.setPixmap(QPixmap(self.ICONS[self.state]))

    def paintEvent(self, event=None, *args):
        self.label.setPixmap(QPixmap(self.ICONS[self.state]))

    def closeEvent(self, event=None):
        print("Shutting down %s" %self.__class__.__name__)
        self.events.append(self.onQuit)

# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::: #
if __name__ == '__main__':

    from FellesLab import run_gui


    class Ui_MainWindow(object):
        """ This code is normally generated by Qt Designer """

        def setupUi(self, MainWindow):
            """
            """

            MainWindow.resize(100,200)

            # Create the "Central Widget" and add a "Layout"
            self.centralwidget = QWidget(MainWindow)
            MainWindow.setCentralWidget(self.centralwidget)
            self.verticalLayout= QVBoxLayout(self.centralwidget)

            # Add a Temperature sensor and Label Widgets
            self.t1 = QFellesSolenoidValve(self.centralwidget)

            # Add Widgets to Layout
            self.verticalLayout.addWidget(self.t1)

            # Create the Menu bar
            self.menubar = QMenuBar(MainWindow)
            MainWindow.setMenuBar(self.menubar)
            # Create the Status Bar
            self.statusbar = QStatusBar(MainWindow)
            MainWindow.setStatusBar(self.statusbar)

            self.retranslateUi(MainWindow)

        def retranslateUi(self, MainWindow):
            """
            """
            pass

    run_gui(Ui_MainWindow)


