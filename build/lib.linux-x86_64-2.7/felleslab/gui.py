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
                         QAction, QDialog)


from felleslab.communication import AdaptorBaseClass
from collections import defaultdict
from time import sleep, time
from serial import SerialException


try:
    _encoding = QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig)



class FellesException(Exception):
    pass


# Parent Widget class ------------------------------------------------------- #
class QFellesDialog(QDialog):

    def initUi(self):
        pass

    def resizeEvent(self, event):
        """ Called every time window is resized
        """
        pass

    def closeEvent(self, event):
        """ Called when window is closed """
        print("Closing Dialog")

# Parent Widget class ------------------------------------------------------- #
class QFellesWidgetBaseClass(QWidget):
    """
    """

    sampling_pause = pyqtSignal()
    sampling_start = pyqtSignal()
    sampling_stop  = pyqtSignal()
    sampling_reset = pyqtSignal(str)

    sample_failed   = pyqtSignal()
    sample_acquired = pyqtSignal()

    def __init__(self, parent=None):
      super(QFellesWidgetBaseClass, self).__init__(parent)

    def paintEvent(self, event=None):
        pass

    def closeEvent(self, event=None):
        print("- - - -")

# Thread class -------------------------------------------------------------- #
class FellesThread(QThread):

    RATE = 0.1
    SAVE = True # Event()

    ___refs___ = []

    def __init__ (self, portname):
        super(FellesThread, self).__init__()

        self.slaves = AdaptorBaseClass.getAdaptors(portname)
        self.portname = portname
        self.daemon = True                          # Use a daemonic thread

        self._data = defaultdict(dict)
        self.events = []

        self.started = time()                              # Set Start time
        self.___refs___.append(self)

        self.start()                                         # Start Thread

    def __setitem__(self, key, val):
        if not key in self._data:
            self._data[key] = val
        else:
            self._data[key].update(val)

    def __getitem__(self, key):
        return self._data[key]

    def sample_loop(self, timestamp, save, *args, **kwargs):
        """
        @brief     Loop over all slaves obtaining MVs
        """
        for slave in self.slaves:
            try:
                #if self.__class__.SAVE.is_set():
                #if SerialportThread.SAVE:
                self[timestamp] = slave.sample(timestamp)
                #else:
                #    slave.sample(timestamp, savedata)
            except IOError as e:
                print("Failed to read measurement:\n\t\t\t\t %s" %(e))
            except SerialException as e:
                print("Serial Exception")
                print(e)
                raise e
            except ValueError as e:
                print("Value Error")
                print(e)
                raise e
            except Exception as e:
                print("Exception")
                print(e)
                raise e

    def event_loop(self):
        """
        @brief     Loop over all slaves obtaining MVs
        """
        for slave in self.slaves:
            try:
                slave.onEvent()
            except Exception as e:
                pass

    def run(self):
        """
        @brief     Method performing the sampling (executed by `self.start()`).
        """
        while True:
            self.dt = time() - self.started
            self.sample_loop(self.dt, self.__class__.SAVE)             # Sample
            self.event_loop()                                          # Sample
            sleep(self.RATE)                                 # Put Thread "to sleep"

    @pyqtSlot()
    def onQuit(self):
        print("Quitting")

    @classmethod
    def set_event(self, adaptor, action, destination):
        self.events.append((adaptor, action))

    @classmethod
    def save_sampling(cls):
        #from csv import DictWriter
        #cls.SAVE.clear()
        cls.SAVE = False
        for thread in cls.___refs___:
            print(thread._data)

    @classmethod
    def start_sampling(cls):
        cls.SAVE = True

    @classmethod
    def pause_sampling(cls):
        cls.SAVE = False

    @classmethod
    def addToThread(cls, slave):
        print("Adding slave to thread")
        for thread in cls.___refs___:
            if thread.portname == slave.portname:
                thread.addSlave(slave)
                return
        asdfa = FellesThread(slave.portname)
        asdfa.addSlave(slave)

    @classmethod
    def reset_sampling(cls):
        """ """
        #cls.SAVE.clear()
        cls.SAVE = True
        for thread in cls.___refs___:
            for slave in thread.slaves:
                slave()._buffer.clear()
            thread._data.clear()
            thread.started = time()

    def addSlave(self, slave):
        self.slaves.append(slave)

# Gui class ----------------------------------------------------------------- #
class FellesGui(QMainWindow):
    """
    """
    init_sampling = pyqtSignal()
    quit_sampling = pyqtSignal()
    closing = pyqtSignal()

    def __init__(self, Ui_MainWindow, timeout=1000):
        super(FellesGui, self).__init__()

        self.setAttribute(Qt.WA_DeleteOnClose)

        exitAction = QAction('Quit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Quit application')
        print("Push 'Ctrl+Q' to quit the application")
        exitAction.triggered.connect(self.close)

        # Create Widget for the purpose of updating the widgets periodically
        #self.timer = QTimer()
        #self.timer.timeout.connect(self.paintEvent)
        #self.timer.start(timeout)

        # !! This is where the widgets are initiated !!
        self.buildUi(Ui_MainWindow)

        # Setup the Menu Bar
        fileMenu = self.menuBar().addMenu('&File')
        fileMenu.addAction(exitAction)

        # Order widgets to connect to their slaves
        self.init_sampling.emit()

        # Start the threads performing the sampling
        sampling_threads = [ FellesThread(port) for port in AdaptorBaseClass.getPorts() ]

        #self.statusBar().showMessage.connect(FellesThread.sample_failed)
        self.statusBar().showMessage('Idling...')

    def buildUi(self, Ui_MainWindow):
        self.statusBar().showMessage('Initialising Modules')
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

    def closeEvent(self, event):
        print("User has clicked the red x on the main window")

        # option #1
        # if you want to trigger a cleanup specifically when
        # this widget is closed, as opposed to destroyed
        #for i in xrange(self.layout().count()):
        #    item = self.layout.itemAt(i)
        #    widget = item.widget()       
        #    if widget:
        #        try:
        #            widget.close()
        #        except:
        #            pass
        #print(dir(event))
        # Or Option #3 - emit a custom signal
        self.closing.emit()

        super(FellesGui, self).closeEvent(event)
        event.accept()

#    def paintEvent(self, event=None, *args):
#        pass

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
