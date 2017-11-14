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
    
    @summary       Start, Stop, Pause Buttons
    @author:       Brittany Hall
    @organization  Department of Chemical Engineering, NTNU, Norway
    @contact       brittanh@stud.ntnu.no
    @license       Free (GPL.v3) !!! Distributed as-is !!!
    @requires      Python 2.7.x or higher
    @since         2017-10-25
    @version       0.1
    
    """

import sys
from PyQt4.QtGui import (QPushButton, QWidget, QIcon, QApplication, QPixmap, QHBoxLayout, QVBoxLayout, QMainWindow)
from PyQt4.QtCore import (QCoreApplication, pyqtSlot)
#from felleslab.icons import *

#Just for testing purposes
class MainWindow(QMainWindow):

    def __init__(self, parent = None):

        super(MainWindow, self).__init__(parent)
        self.button_widget = ButtonWidget(self)
        self.setCentralWidget(self.button_widget)
        self.setWindowTitle('Two Tank Experiment')
        self.setWindowIcon(QIcon('chemistry-lab-instrument.svg'))

class ButtonWidget(QWidget):

    def __init__(self, parent):
        super(ButtonWidget, self).__init__()
        self._state = 0 #default state of idle
        self.initUI()
        self.StartButton.clicked.connect(self.on_click)
        self.PauseButton.clicked.connect(self.on_click)
        self.StopButton.clicked.connect(self.on_click)

    @property
    def state(self):
        return self._state
    
    @state.setter
    def state(self, value):
        """
            TODO: possible state values: 0, 1, 2. CHECK!
        """
        self._state = value
    
    def initUI(self):
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
        icon_start.addPixmap(QPixmap('play.svg'), QIcon.Normal)
        icon_start.addPixmap(QPixmap('play_disabled.svg'), QIcon.Disabled)
        self.StartButton.setIcon(icon_start)
        icon_pause.addPixmap(QPixmap('pause.svg'), QIcon.Normal)
        icon_pause.addPixmap(QPixmap('pause_disabled.svg'), QIcon.Disabled)
        self.PauseButton.setIcon(icon_pause)
        icon_stop.addPixmap(QPixmap('stop.svg'), QIcon.Normal)
        icon_stop.addPixmap(QPixmap('stop_disabled.svg'), QIcon.Disabled)
        self.StopButton.setIcon(icon_stop)
        
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
    
#        vbox = QVBoxLayout()
#        vbox.addStretch(1)
#        vbox.addLayout(hbox)

        self.setLayout(hbox)
    
    
    @pyqtSlot()
    def on_click(self, event=None):
        sending_button = self.sender() #getting button name
        btn_name = str(sending_button.objectName())
        if btn_name == 'Start':
            old_state = self.state
            self.state = 1 #changing state to sampling
            self.StartButton.setDisabled(True)
            self.PauseButton.setEnabled(True)
            self.StopButton.setEnabled(True)
        elif btn_name == 'Pause':
            old_state = self.state
            self.state = 2 #changing state to paused
            self.StartButton.setEnabled(True)
            self.PauseButton.setDisabled(True)
            self.StopButton.setEnabled(True)
        elif btn_name == 'Stop':
            old_state = self.state
            self.state = 0 #changing state to idle
            self.StartButton.setEnabled(True)
            self.PauseButton.setDisabled(True)
            self.StopButton.setDisabled(True)

def main():
    app = QApplication(sys.argv)
    GUI = MainWindow()
    GUI.show()
    sys.exit(app.exec_())

main()





