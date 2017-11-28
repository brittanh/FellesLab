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
    @since         2017-11-15
    @version       0.1
    
    """
import sys
from PyQt4.QtGui import (QGroupBox, QLabel, QDoubleSpinBox, QGridLayout, QHBoxLayout,
                         QApplication, QWidget, QMainWindow, QVBoxLayout,
                         QRadioButton, QSlider, QMenuBar, QStatusBar, QTextEdit)
from PyQt4.QtCore import (pyqtSignal, pyqtSlot, Qt)
from felleslab.core import QFellesWidgetBaseClass

#Discrete PID Controller algorithm ------------------------------------------#
class QFellesPIDAlgorithm(QFellesWidgetBaseClass):
    
    """
    @brief: Widget that contains a discrete PID controller algorithm
    """
    PID = pyqtSignal(float)
    
    def iniUi(self, parent=None):
        #Update widget meta data
        self.meta["type"] = "PIDAlgorithm"
        self.meta["name"] = "foobar"
        self.meta["unit"] = "--"
        
        self.label = QLabel(parent)
        self.label.setObjectName("PID Algorithm")
        
        #creating widget box
        font = QFont()
        font.setFamily('Lucida')
        font.setPointSize(14)
        self.algo = QLabel("Discrete PID Algorithm")
        #self.algo.readyOnly = True
        self.console.setFont(font)

        self.Kc = 1 #proportional gain
        self.Ki = 2 #integral gain
        self.Kd = 3 #derivative gain
        self.Derivative = 0 #derivative value
        self.Integral = 0 #integral value
        self.MVsp= 0 #MV setpoint
        self.CVsp = 0#CV setpoint
        self.error = 0.0
        self.current_value = 1 #current sample value
        self.PID.connect(update)
        
    @pyqtSlot()
    def update(self):
        """
        Calculate PID output value for given reference input and feedback
        """
        self.error = self.set_point - current_value

        self.P_value = self.Kp * self.error
        self.D_value = self.kd * (self.error - self.Derivative)
        self.Derivative = self.error
        self.Integral = self.Integral + self.error

        self.I_value = self.Integral * self.Ki

        PID = self.P_value + self.I_value + self.D_value
        
        self.PID.emit(PID)

# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::#
if __name__ == '__main__':
    
    from felleslab import run_gui
    import sys
    
    class Ui_MainWindow(object):
        """ This code is normally generated by Qt Designer """
        
        def setupUi(self, MainWindow):
            """
                """
            MainWindow.resize(100,200)
            #Create central widget and add a Layout
            self.centralwidget = QWidget(MainWindow)
            MainWindow.setCentralWidget(self.centralwidget)
            self.verticalLayout= QVBoxLayout(self.centralwidget)
            
            # Add a Temperature sensor and Label Widgets
            self.t1 = QFellesPIDAlgorithm(self.centralwidget)
            
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
