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

@summary
@author:       Sigve Karolius
@organization  Department of Chemical Engineering, NTNU, Norway
@contact       sigve.karolius@ntnu.no
@license       Free (GPL.v3) !!! Distributed as-is !!!
@requires      Python 2.7.x or higher
@since         2017-06-16
@version       0.1

"""

#from PyQt5.QtCore import (QTimer, pyqtSignal, QThread, QObject, pyqtProperty,
#                         Qt, pyqtSlot)
#from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QWidget, QDialog)
#from PyQt5.QtGui import QIcon, QPixmap

from PyQt4.QtCore import (QTimer, pyqtSignal, QThread, QObject, pyqtProperty,
                         Qt, pyqtSlot)

from PyQt4.QtGui import (QIcon, QPixmap, QApplication, QMainWindow, QWidget,
                         QAction, QDialog, QMessageBox)


from felleslab.communication import AdaptorBaseClass
from collections import defaultdict, deque
from time import sleep, time
from serial import SerialException


try:
    _encoding = QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig)


# Parent Widget class ------------------------------------------------------- #
class QFellesWidgetBaseClass(QWidget):
    """
    @brief     Base class for **all** FellesLab widgets
    """

    newSample = pyqtSignal(str)
    getSample = pyqtSignal(float, name="PerformSampling")
    statusMessage = pyqtSignal(str)

    meta = { "type"         : None,
             "name"         : None,
             "unit"         : None,
             "channel"      : None,                # Register used for sampling
             "portname"     : "/dev/ttyUSB0",     # Computer communication port
             "slaveaddress" : 0,              # Address in the physical network
             "baudrate"     : 19200,                      # Communication speed
    }

    _slave        = None                                      # Slave unit type

    ___refs___ = []
    ___ports___ = defaultdict(list)

    def __init__(self, parent=None):
        """
        """
        self.meta = self.__class__.meta.copy()
        super(QFellesWidgetBaseClass, self).__init__(parent)
        self.__class__.___refs___.append(self)
        self._id = hex(id(self))
        self.events = [ ]
        self._history = deque(maxlen=100)

        #                  !!! Hack Warning !!!
        # The following "if statements" are a "hack" to ensure the widgets do
        # not throw errors when used in QtDesigner. The problem is that it is
        # "my" MainWindow (FellesGui) that contains the signals for
        # initialisation and terminating the felles widgets.

        self.initUi(parent)                         # Initialise user interface
        self.show()                          # Display Widget in User Interface

    def initUi(self, parent=None):
        """
        @brief  Method instantiating widget in the UI
        """
        raise NotImplementedError("You idiot...")

    def onInit(self):
        pass

    def onQuit(self):
        pass

    def closeEvent(self, event=None):
        print("- - - -")

    def onEvent(self):
        while self.events:
            event = self.events.pop(0)
            event.emit()

    @pyqtProperty(list)
    def history(self):
        return self._history

    @history.setter
    def history(self, val):
        self._history.append(val)

    #@pyqtSlot()
    def setSlave(self):
        """
        @param  portname      str (optional)  RS485 connection port
        @param  slaveaddress  int (optional)  Address of unit in the network
        """
        if self._slave:
            print("Type\t: %s:" %(self.meta["type"]))
            print("Unit\t: %s:" %(self._slave.__class__.__name__))
            print("Name\t: %s" %self.meta["name"])
            print("Port\t: %s" %self.meta["portname"])
            print("Rate\t: %s" %self.meta["baudrate"])
            print("Address\t: %s" %self.meta["slaveaddress"])
            print("Channel\t: %s" %self.meta["channel"])
            self.slave = self.__class__._slave(**self.meta)
            self.__class__.___ports___[str(self.meta["portname"])].append(self._id)
            #sleep(0.1)
            self.getSample.connect(self.setSample)
            #sleep(0.1)
            self.onInit()
            self.statusMessage.emit("Hello")
            #sleep(0.1)

    @pyqtSlot()
    def setSample(self):
        raise NotImplementedError("You idiot...")

    @pyqtProperty(str)
    def portname(self):
        return self.meta["portname"]

    @portname.setter
    def portname(self, string):
        self.__class__.___ports___[str(self.meta["portname"])].append(self._id)
        self.meta["portname"] = str(string)
        print string

    @pyqtProperty(int)
    def channel(self):
        return self.meta["channel"]

    @channel.setter
    def channel(self, val):
        self.meta["channel"] = int(val)

    @pyqtProperty(int)
    def baudrate(self):
        return self.meta["baudrate"]

    @baudrate.setter
    def baudrate(self, val):
        _baudrates = [ int(i*9600) for i in [1,2,3,4] ]
        self.meta["baudrate"] = int(val)

    @classmethod
    def findWidget(cls, _id):
        """
        @brief   Locate a widget based on the _id
        """
        for obj in cls.___refs___:
            if obj._id != _id:
                continue
            return obj

    @classmethod
    def findWidgetsAttachedToPort(cls, portname):
        """
        @brief   Locate a widget based on the _id
        """
        return [cls.findWidget(_id) for _id in cls.___ports___[portname]]

# Thread class -------------------------------------------------------------- #
class FellesThread(QThread):

    priorities = { "Highest": 5, "High": 4, "Idle": 0, "Inheerit": 7, "Low": 2,
                 "Lowest": 1, "Normal": 3}

    def __init__ (self, port):
        super(FellesThread, self).__init__()
        self.widgets = QFellesWidgetBaseClass.findWidgetsAttachedToPort(port)

        print("\nInitialising Thread for port '%s' " %port)
        for widget in self.widgets:
            print("Initialising -------------------------- Widget")
            widget.setSlave()

        self.portname = port

        self.started = time()                                  # Set Start time
        self.start()                                             # Start Thread
        self.setPriority(self.priorities["Highest"])

    def sample(self, timestamp):
        """
        @brief    "Sampling Loop" over all widgets
        @param    timestamp  float  (required)  Time when sampling is performed
        @details
                  There are multiple hacks here...

                  1. Sampling is sequential, but all samples receive the same
                     time. Ugly...
                  2. Asynchronous sampling within a thread is not permitted.
                     The reason for this is limitations in the communication
                     protocol (RS485).
                  3. Start/Pause/Resume/Restart is done as "events", i.e.
                     between sampling loops.
        """
        for widget in self.widgets:
            widget.getSample.emit(timestamp)

    def event(self, timestamp):
        """
        @brief    "Event loop", execute control or user actions
        """
        for widget in self.widgets:
            widget.onEvent()

    def run(self):
        """
        @brief    Method performing the sampling (executed by `self.start()`)
        @details
                  !!Yet another hack!!
                  The thread is put to sleep between the "sample" and "event"
                  loops. The network connection seems to be overloaded if I
                  do not do this,
        """
        while self.isRunning():
            dt = time() - self.started
            self.sample(dt)                  # Perform sampling for all widgets
            self.msleep(100)                             # Put Thread "to sleep"
            self.event(dt)                                      # Handle events

    def quit(self):
        """
        @brief   Method terminating the sampling
        """
        print("\nTerminating Thread for port '%s' " %self.portname)
        while self.widgets:
            widget = self.widgets.pop()
            try:
                widget.close()
            except Exception as e:
                print e


# Gui class ----------------------------------------------------------------- #
class FellesGui(QMainWindow):
    """
    """
    startSampling  = pyqtSignal()
    pauseSampling  = pyqtSignal()
    stopSampling   = pyqtSignal()

    terminateThreads = pyqtSignal()

    def __init__(self, Ui_MainWindow, timeout=1000):
        super(FellesGui, self).__init__()

        self.setAttribute(Qt.WA_DeleteOnClose)

        self.exitAction = QAction('Quit', self)
        self.exitAction.setShortcut('Ctrl+Q')
        self.exitAction.setStatusTip('Quit application')
        print("Push 'Ctrl+Q' to quit the application")
        self.exitAction.triggered.connect(self.close)

        # Create Widget for the purpose of updating the widgets periodically
        #self.timer = QTimer()
        #self.timer.timeout.connect(self.paintEvent)
        #self.timer.start(timeout)

        # --> Instantiate UI  !!! This is where the widgets are initiated !!!
        self.buildUi(Ui_MainWindow)

        # --> Setup the Menu Bar
        self.fileMenu = self.menuBar().addMenu('&File')
        self.fileMenu.addAction(self.exitAction)

        # --> Order widgets to connect to their slaves
        #self.initialiseSlaves.emit()
        # -->  Initialise "Threads" performing the sampling
        #print QFellesWidgetBaseClass.___ports___.keys()
        ports = ["/dev/ttyUSB0"] # QFellesWidgetBaseClass.___ports___.keys()

        self.threads = [ FellesThread(port) for port in ports ]
        for thread in self.threads:
            self.terminateThreads.connect(thread.quit)

        self.statusBar().showMessage('Idling...')

    def buildUi(self, Ui_MainWindow):
        self.statusBar().showMessage('Initialising Modules')
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

    def closeEvent(self, event):
        """ Method executed when application is closed
        """
        txt   = "Are you sure to quit?"
        reply = QMessageBox.question(self, 'Message', txt,
                                   QMessageBox.Yes, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.terminateThreads.emit()
            event.accept()
        else:
            event.ignore()

# --------------------------------------------------------------------------- #
def run_gui(Ui_MainWindow):
    """ Function launching a application
    """
    import sys
    app = QApplication(sys.argv)
    myapp = FellesGui(Ui_MainWindow)
    myapp.show()
    return sys.exit(app.exec_())


# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::: #
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    myapp = FellesGui()
    myapp.show()
    sys.exit(app.exec_())
