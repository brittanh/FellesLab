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
from PyQt4.QtGui import QIcon, QPixmap, QFont, QMainWindow, QLabel, QWidget, QPushButton,  QHBoxLayout, QVBoxLayout, QMenuBar, QStatusBar, QAbstractButton, QDialog


from felleslab.equipment.solenoidvalve import SolenoidValve
from felleslab import icons


valve_closed = ":icons/valves/48x48_solenoid_closed.png"
valve_open = ":icons/valves/48x48_solenoid_open.png"
valve_void = ":icons/valves/48x48_solenoid.png"


# Valve Widget -------------------------------------------------------------- #
class QFellesSolenoidValve(QWidget):
    """
    @brief     Widget
    """

    valveOpen = pyqtSignal(name="openValve")
    valveClose = pyqtSignal(name="closeValve")

    def __init__(self, parent=None):
        super(QFellesSolenoidValve, self).__init__(parent)

        self.ICONS = [ QPixmap(valve_closed), QPixmap(valve_open), QPixmap(valve_void) ]

        self.meta = { "type": "Position",
                 "name": "Valve",
                 "unit": "[-]",
                 "channel" : 0,
                 "portname" : "/dev/ttyUSB0",
                 "slaveaddress": 1,
                 "baudrate" : 19200,
                }

        self._state = -1 # <-- set-point
        self._initialState = 0 # <-- initial set-point
        self._finalState = 0 # <-- final set-point

        self.initUi(parent)
        if parent:
            self.initSlaves()


        #self.valveOpen.connect()

        # Display Widget in User Interface
        self.show()

    def initUi(self, parent=None):
        """ Generates the user interface """
        self.label = QLabel(parent)
        self.label.setObjectName("Solenoid Valve")
        self.label.setPixmap(self.ICONS[self.state])

        _layout = QHBoxLayout()
        _layout.addWidget(self.label)
        self.setLayout(_layout)

    def isOpen(self):
        self.state = 0

    def isClosed(self):
        self.state = 1

    @pyqtSlot()
    def setOpen(self):
        self.slave.event_queue.append((self.slave.setOpen, self.isOpen))

    @pyqtSlot()
    def setClose(self):
        self.slave.event_queue.append((self.slave.setClose, self.isClosed))

    @pyqtSlot()
    def setSwitchState(self):
        if self.state == 0:
            self.slave.event_queue.append((self.slave.setClose, self.isClosed))
        else:
            self.slave.event_queue.append((self.slave.setOpen, self.isOpen))

    @pyqtProperty(bool)
    def openOnInit(self):
        return self._initialState

    @openOnInit.setter
    def openOnInit(self, openOnInit):
        self._initialState = 0 if openOnInit else 1

    @pyqtProperty(bool)
    def openOnQuit(self):
        return self._finalState

    @openOnQuit.setter
    def openOnQuit(self,openOnQuit):
        self._finalState = 0 if openOnQuit else 1

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        self._state = value
        self.paintEvent()

    def mouseReleaseEvent(self, event):
        self.setSwitchState()

    def retranslateUi(self, parent):
        self.label.setPixmap(self.ICONS[self.state])

    def initSlaves(self):
        self.slave = SolenoidValve(**self.meta)
        self.state = 1

    def paintEvent(self, event=None, *args):
        self.label.setPixmap(self.ICONS[self.state])

    def setProperty(self, key, val):
        self.meta[key] = val

    def closeEvent(self, event):
        self.slave.event_queue.append((self.slave.onQuit, None))


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


