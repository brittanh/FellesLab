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
    @since         2017-11-01
    @version       0.1
    
"""
import sys

from PyQt4.QtGui import (QGroupBox, QLabel, QDoubleSpinBox, QGridLayout, QHBoxLayout,
                         QApplication, QWidget, QMainWindow)
from PyQt4.QtCore import (pyqtSignal, pyqtSlot)
from felleslab.core import QFellesWidgetBaseClass
from time import time

#Controller Widget -----------------------------------------------------------#
class QFellesController(QFellesWidgetBaseClass):
    """
    @brief: Widget representing a controller
    """
    proportional = pyqtSignal(float)
    integral = pyqtSignal(float)
    derivative = pyqtSignal(float)
    MV_sp = pyqtSignal(float)
    CV_sp = pyqtSignal(float)

    def __init__(self, parent=None):
        super(ControllerWidget, self).__init__()
        self.initUI()
        self.on.toggled.connect(self.btnstate)
        self.setpoint.valueChanged[str].connect(self.CVSetPoint)
        self.gain.valueChanged[str].connect(self.controllersettings)
        self.taui.valueChanged[str].connect(self.controllersettings)
        self.taud.valueChanged[str].connect(self.controllersettings)
        self.MV_manual.sliderReleased.connect(self.mv_state)

    def initUI(self):
        #Group box
        group_box = QGroupBox('Controller Settings')
        #Spin button Labels
        gain = "K<sub>c</sub>"
        Kc = gain.decode('utf-8')
        self.gain_label = QLabel(Kc)
        self.gain_label.setStyleSheet("font:25pt")
        time1 = "&#964;<sub>i</sub>"
        taui = time1.decode('utf-8')
        self.taui_label = QLabel(taui)
        self.taui_label.setStyleSheet("font:25pt ")
        time2 = "&#964;<sub>d</sub>"
        taud = time2.decode('utf-8')
        self.taud_label = QLabel(taud)
        self.taud_label.setStyleSheet("font:25pt")
        
        #Spin buttons
        self.gain = QDoubleSpinBox()                           #Controller gain
        self.taui = QDoubleSpinBox()         #Controller integral time constant
        self.taud = QDoubleSpinBox()       #Controller derivative time constant
        self.GAIN_0 = self.gain.value()
        self.TAUI_0 = self.taui.value()
        self.TAUD_0 = self.taud.value()
        self.gain.setKeyboardTracking(False)
        self.taui.setKeyboardTracking(False)
        self.taud.setKeyboardTracking(False)
        #self.gain.setRange(minimum, maximum)
        self.gain_label.setBuddy(self.gain)
        self.taui_label.setBuddy(self.taui)
        self.taud_label.setBuddy(self.taud)
        self.setpoint = QDoubleSpinBox()          #Controlled variable setpoint
        self.setpoint.setHidden(True)
        self.setpoint_label = QLabel('CV Setpoint')
        self.setpoint_label.setBuddy(self.setpoint)
        
        #On-Off Buttons
        self.on = QRadioButton("Controller On")
        self.on.setChecked(False)               #Default to have controller off
        
        #Slider
        self.MV_manual = QSlider(Qt.Horizontal)
        self.MV_manual_label = QLabel('MV Setpoint')
        #self.MV_manual.setRange(minimum, maximum)
        
        #Layout
        controlsLayout = QGridLayout()
        controlsLayout.addWidget(self.gain_label,0,0)
        controlsLayout.addWidget(self.gain,0,1)
        controlsLayout.addWidget(self.setpoint_label,0,2)
        controlsLayout.addWidget(self.setpoint,0,3)
        controlsLayout.addWidget(self.taui_label,1,0)
        controlsLayout.addWidget(self.taui,1,1)
        controlsLayout.addWidget(self.MV_manual_label,1,2)
        controlsLayout.addWidget(self.MV_manual,1,3)
        controlsLayout.addWidget(self.taud_label,2,0)
        controlsLayout.addWidget(self.taud,2,1)
        controlsLayout.addWidget(self.on,2,2)
        controlsLayout.setRowStretch(3,1)
        
        layout = QHBoxLayout()
        layout.addLayout(controlsLayout)
        self.setLayout(layout)
    
    
    @pyqtSlot()
    def CVSetPoint(self, event=None):
        self.setpoint_value = self.setpoint.value()
        self.CV_sp.emit(self.setpoint_value)
    #print self.setpoint_value
    
    @pyqtSlot()
    def controllersettings(self, event=None):
        if self.gain.value() != self.GAIN_0:
            self.GAIN_0 = self.gain.value()
            self.gain_value = self.gain.value()
            self.proportional.emit(self.gain_value) #emitting Gain value
        #print self.gain_value
        elif self.taui.value() != self.TAUI_0:
            self.TAUI_0 = self.taui.value()
            self.taui_value = self.taui.value()
            self.integral.emit(self.taui_value)
        #print self.taui_value
        elif self.taud.value() != self.TAUD_0:
            self.TAUD_0 = self.taud.value()
            self.taud_value = self.taud.value()
            self.derivative.emit(self.taud_value)
    #print self.taud_value

    @pyqtSlot()
    def btnstate(self, event=None):
        if self.on.isChecked() == True:
            self.setpoint.setHidden(False)
            self.MV_manual.setHidden(True)
            #print "Controller is on"
        else:
            self.setpoint.setHidden(True)
            self.MV_manual.setHidden(False)
            #print "Controller is off"

    @pyqtSlot()
    def mv_state(self, event=None):
        MV_setpoint = self.MV_manual.value()
        self.MV_sp.emit(MV_setpoint)
        #print MV_setpoint

    def closeEvent(self, event=None):
        print("Shutting down %s" %self.__class__.__name__)
        self.onQuit()

# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::#
if __name__ == '__main__':
    import sys
    
    class Window(QMainWindow):
        def __init__(self, parent=None):
            super(Window, self).__init__(parent)
            self.controller = QFellesController(self)
            self.setCentralWidget(self.controller)
            self.setWindowTitle('Controller')
    
    application = QApplication(sys.argv)

    #Making window
    window = Window()
    window.resize(220, 100)
    window.show()

    sys.exit(application.exec_())
