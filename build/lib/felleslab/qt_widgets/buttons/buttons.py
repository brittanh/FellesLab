#!/usr/bin/python
# -*- coding: ascii -*-
"""
oooooooooooo       oooo oooo                    ooooo                 .o8
`888'     `8       `888 `888                    `888'                "888
 888       .ooooo.  888  888  .ooooo.  .oooo.o   888         .oooo.   888oooo.
 888oooo8 d88' `88b 888  888 d88' `88bd88(  "8   888        `P  )88b  d88' `88b
 888    " 888ooo888 888  888 888ooo888`"Y88b.    888         .oP"888  888   888
 888      888    .o 888  888 888    .oo.  )88b   888       od8(  888  888   888
o888o     `Y8bod8P'o888oo888o`Y8bod8P'8""888P'  o888ooooood8`Y888""8o `Y8bod8P'

@summary
@author        Brittany Hall
@organization  Department of Chemical Engineering, NTNU, Norway
@contact       brittanh@stud.ntnu.no
@license       Free (GPL.v3) !!! Distributed as-is !!!
@requires      Python 2.7.x or higher
@since         2017-11-05
@version       0.1

"""


from PyQt4.QtGui import (QPushButton, QWidget, QIcon, QApplication, QPixmap,
                         QHBoxLayout, QVBoxLayout, QMainWindow, QMenuBar,
                         QStatusBar, QLabel, QIcon)
from PyQt4.QtCore import (QCoreApplication, pyqtSlot, pyqtSignal)
from felleslab.core import QFellesWidgetBaseClass
from felleslab import icons

# Thermocouple Widget ------------------------------------------------------- #
class QFellesButtons(QFellesWidgetBaseClass):
    """
    @brief     Widget
    """
    Start = pyqtSignal(int)
    Stop = pyqtSignal(int)
    Pause = pyqtSignal(int)
    
    def initUi(self, parent=None):
        """ Generates the user interface """
        #Update widget meta data
        self.meta["type"] = "Buttons"
        self.meta["name"] = "foobar"
        self.meta["unit"] = "--"
        self._state = 0                                  #Default state of idle
        
        #Defining Buttons
        self.StartButton = QPushButton("Start")
        self.StartButton.setObjectName('Start')
        self.PauseButton= QPushButton("Pause")
        self.PauseButton.setObjectName('Pause')
        self.StopButton = QPushButton("Stop")
        self.StopButton.setObjectName('Stop')
        
        #Button icons
        icon_start = QIcon()
        icon_pause = QIcon()
        icon_stop = QIcon()
        icon_start.addPixmap(QPixmap(":icons/buttons/48x48_play.png"), QIcon.Normal)
        icon_start.addPixmap(QPixmap(":icons/buttons/48x48_play_disabled.png"), QIcon.Disabled)
        self.StartButton.setIcon(icon_start)
        icon_pause.addPixmap(QPixmap(":icons/buttons/48x48_pause.png"), QIcon.Normal)
        icon_pause.addPixmap(QPixmap(":icons/buttons/48x48_pause_disabled.png"), QIcon.Disabled)
        self.PauseButton.setIcon(icon_pause)
        icon_stop.addPixmap(QPixmap(":icons/buttons/48x48_stop.png"), QIcon.Normal)
        icon_stop.addPixmap(QPixmap(":icons/buttons/48x48_stop_disabled.png"), QIcon.Disabled)
        self.StopButton.setIcon(icon_stop)
        
        #Specifying desired actions
        self.StartButton.clicked.connect(self.on_click)
        self.PauseButton.clicked.connect(self.on_click)
        self.StopButton.clicked.connect(self.on_click)
    
        #Specifying button settings for initial state
        if self.state == 0: #idle (default state)
            self.StartButton.setEnabled(True)
            self.PauseButton.setDisabled(True)
            self.StopButton.setDisabled(True)
        elif self.state == 1: #sampling
            self.StartButton.setDisabled(True)
            self.PauseButton.setEnabled(True)
            self.StopButton.setEnabled(True)
        elif self.state == 2: #paused
            self.StartButton.setEnabled(True)
            self.PauseButton.setDisabled(True)
            self.StopButton.setEnabled(True)
    
        #Defining Layout
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.StartButton)
        hbox.addWidget(self.PauseButton)
        hbox.addWidget(self.StopButton)
        
        self.setLayout(hbox)

    
    @property
    def state(self):
        return self._state
    
    @state.setter
    def state(self, value):
        """
            TODO: possible state values: 0, 1, 2. CHECK!
            """
        self._state = value
    
    @pyqtSlot()
    def on_click(self, event=None):
        sending_button = self.sender()                     #Getting button name
        btn_name = str(sending_button.objectName())
        if btn_name == 'Start':
            old_state = self.state
            self.state = 1                          #Changing state to sampling
            self.Start.emit(self.state)                     #Emitting new state
            self.StartButton.setDisabled(True)
            self.PauseButton.setEnabled(True)
            self.StopButton.setEnabled(True)
        elif btn_name == 'Pause':
            old_state = self.state
            self.state = 2                            #Changing state to paused
            self.Pause.emit(self.state)                     #Emitting new state
            self.StartButton.setEnabled(True)
            self.PauseButton.setDisabled(True)
            self.StopButton.setEnabled(True)
        elif btn_name == 'Stop':
            old_state = self.state
            self.state = 0                              #Changing state to idle
            self.Stop.emit(self.state)                      #Emitting new state
            self.StartButton.setEnabled(True)
            self.PauseButton.setDisabled(True)
            self.StopButton.setDisabled(True)

    def closeEvent(self, event=None):
        print("Shutting down %s" %self.__class__.__name__)


# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::: #
if __name__ == '__main__':
    #from PyQt5.QtWidgets import QApplication
    from PyQt4.QtGui import QApplication
    from felleslab import run_gui

    try:
        _encoding = QApplication.UnicodeUTF8
        def _translate(context, text, disambig):
            return QApplication.translate(context, text, disambig, _encoding)
    except AttributeError:
        def _translate(context, text, disambig):
            return QApplication.translate(context, text, disambig)

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
            self.t1 = QFellesButtons(self.centralwidget)
            self.label = QLabel(self.centralwidget)

            # Add Widgets to Layout
            self.verticalLayout.addWidget(self.t1)
            self.verticalLayout.addWidget(self.label)

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
            self.t1.setProperty("slaveaddress", _translate("MainWindow", "2", None))


    run_gui(Ui_MainWindow)


