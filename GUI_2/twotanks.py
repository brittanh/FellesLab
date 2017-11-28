# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'twotanks.ui'
#
# Created by: PyQt4 UI code generator 4.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(1096, 800)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.Buttons = QFellesButtons(self.centralwidget)
        self.Buttons.setGeometry(QtCore.QRect(200, 690, 721, 61))
        self.Buttons.setProperty("slaveaddress", 0)
        self.Buttons.setProperty("channel", 0)
        self.Buttons.setObjectName(_fromUtf8("Buttons"))
        self.Controller = QFellesController(self.centralwidget)
        self.Controller.setGeometry(QtCore.QRect(650, 40, 361, 131))
        self.Controller.setProperty("slaveaddress", 0)
        self.Controller.setProperty("channel", 0)
        self.Controller.setObjectName(_fromUtf8("Controller"))
        self.Valve = QFellesSolenoidValve(self.centralwidget)
        self.Valve.setGeometry(QtCore.QRect(110, 360, 81, 81))
        self.Valve.setProperty("slaveaddress", 0)
        self.Valve.setProperty("channel", 0)
        self.Valve.setObjectName(_fromUtf8("Valve"))
        self.Valve_2 = QFellesSolenoidValve(self.centralwidget)
        self.Valve_2.setGeometry(QtCore.QRect(430, 360, 72, 72))
        self.Valve_2.setProperty("slaveaddress", 0)
        self.Valve_2.setProperty("channel", 0)
        self.Valve_2.setObjectName(_fromUtf8("Valve_2"))
        self.Thermocouple = QFellesThermocouple(self.centralwidget)
        self.Thermocouple.setGeometry(QtCore.QRect(390, 510, 41, 41))
        self.Thermocouple.setProperty("slaveaddress", 0)
        self.Thermocouple.setProperty("channel", 0)
        self.Thermocouple.setObjectName(_fromUtf8("Thermocouple"))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(50, 80, 231, 221))
        self.label.setText(_fromUtf8(""))
        self.label.setPixmap(QtGui.QPixmap(_fromUtf8(":/tank/tank/200x200_tank.svg")))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(350, 70, 211, 231))
        self.label_2.setText(_fromUtf8(""))
        self.label_2.setPixmap(QtGui.QPixmap(_fromUtf8(":/tank/tank/200x200_tank.svg")))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_12 = QtGui.QLabel(self.centralwidget)
        self.label_12.setGeometry(QtCore.QRect(340, 500, 56, 51))
        self.label_12.setText(_fromUtf8(""))
        self.label_12.setPixmap(QtGui.QPixmap(_fromUtf8(":/instruments/instruments/48x48_temperature_recorder.svg")))
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.Plot = QFellesPlot(self.centralwidget)
        self.Plot.setGeometry(QtCore.QRect(600, 160, 481, 481))
        self.Plot.setProperty("slaveaddress", 0)
        self.Plot.setProperty("channel", 0)
        self.Plot.setObjectName(_fromUtf8("Plot"))
        self.label_3 = QtGui.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(140, 470, 321, 20))
        self.label_3.setText(_fromUtf8(""))
        self.label_3.setPixmap(QtGui.QPixmap(_fromUtf8(":/misc/misc/horizontal_connector_long.svg")))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.label_5 = QtGui.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(30, 50, 121, 20))
        self.label_5.setText(_fromUtf8(""))
        self.label_5.setPixmap(QtGui.QPixmap(_fromUtf8(":/misc/misc/horizontal_connector_long.svg")))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.label_6 = QtGui.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(140, 60, 21, 31))
        self.label_6.setText(_fromUtf8(""))
        self.label_6.setPixmap(QtGui.QPixmap(_fromUtf8(":/misc/misc/vertical_connector.svg")))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.label_7 = QtGui.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(440, 60, 21, 31))
        self.label_7.setText(_fromUtf8(""))
        self.label_7.setPixmap(QtGui.QPixmap(_fromUtf8(":/misc/misc/vertical_connector.svg")))
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.label_8 = QtGui.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(130, 290, 21, 91))
        self.label_8.setText(_fromUtf8(""))
        self.label_8.setPixmap(QtGui.QPixmap(_fromUtf8(":/misc/misc/vertical_connector.svg")))
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.label_9 = QtGui.QLabel(self.centralwidget)
        self.label_9.setGeometry(QtCore.QRect(450, 290, 21, 91))
        self.label_9.setText(_fromUtf8(""))
        self.label_9.setPixmap(QtGui.QPixmap(_fromUtf8(":/misc/misc/vertical_connector.svg")))
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.label_10 = QtGui.QLabel(self.centralwidget)
        self.label_10.setGeometry(QtCore.QRect(450, 420, 21, 61))
        self.label_10.setText(_fromUtf8(""))
        self.label_10.setPixmap(QtGui.QPixmap(_fromUtf8(":/misc/misc/vertical_connector.svg")))
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.label_11 = QtGui.QLabel(self.centralwidget)
        self.label_11.setGeometry(QtCore.QRect(130, 420, 21, 61))
        self.label_11.setText(_fromUtf8(""))
        self.label_11.setPixmap(QtGui.QPixmap(_fromUtf8(":/misc/misc/vertical_connector.svg")))
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.label_13 = QtGui.QLabel(self.centralwidget)
        self.label_13.setGeometry(QtCore.QRect(290, 480, 21, 91))
        self.label_13.setText(_fromUtf8(""))
        self.label_13.setPixmap(QtGui.QPixmap(_fromUtf8(":/misc/misc/vertical_connector.svg")))
        self.label_13.setObjectName(_fromUtf8("label_13"))
        self.label_14 = QtGui.QLabel(self.centralwidget)
        self.label_14.setGeometry(QtCore.QRect(300, 510, 41, 21))
        self.label_14.setText(_fromUtf8(""))
        self.label_14.setPixmap(QtGui.QPixmap(_fromUtf8(":/misc/misc/horizontal_connector_long.svg")))
        self.label_14.setObjectName(_fromUtf8("label_14"))
        self.label_15 = QtGui.QLabel(self.centralwidget)
        self.label_15.setGeometry(QtCore.QRect(450, 50, 121, 20))
        self.label_15.setText(_fromUtf8(""))
        self.label_15.setPixmap(QtGui.QPixmap(_fromUtf8(":/misc/misc/horizontal_connector_long.svg")))
        self.label_15.setObjectName(_fromUtf8("label_15"))
        self.label_7.raise_()
        self.label_9.raise_()
        self.label_8.raise_()
        self.label_11.raise_()
        self.Buttons.raise_()
        self.Controller.raise_()
        self.Valve.raise_()
        self.Valve_2.raise_()
        self.Thermocouple.raise_()
        self.label.raise_()
        self.label_2.raise_()
        self.label_12.raise_()
        self.Plot.raise_()
        self.label_3.raise_()
        self.label_5.raise_()
        self.label_6.raise_()
        self.label_10.raise_()
        self.label_13.raise_()
        self.label_14.raise_()
        self.label_15.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1096, 22))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.Thermocouple, QtCore.SIGNAL(_fromUtf8("newSample(QString)")), self.Plot.cUpdate)
        QtCore.QObject.connect(self.Valve, QtCore.SIGNAL(_fromUtf8("newSample(QString)")), self.Plot.cUpdate)
        QtCore.QObject.connect(self.Valve_2, QtCore.SIGNAL(_fromUtf8("newSample(QString)")), self.Plot.cUpdate)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.Buttons.setToolTip(_translate("MainWindow", "Tip", None))
        self.Buttons.setWhatsThis(_translate("MainWindow", "What is this", None))
        self.Buttons.setProperty("portname", _translate("MainWindow", "/dev/ttyUSB0", None))
        self.Controller.setToolTip(_translate("MainWindow", "Tip", None))
        self.Controller.setWhatsThis(_translate("MainWindow", "What is this", None))
        self.Controller.setProperty("portname", _translate("MainWindow", "/dev/ttyUSB0", None))
        self.Valve.setToolTip(_translate("MainWindow", "Tip", None))
        self.Valve.setWhatsThis(_translate("MainWindow", "What is this", None))
        self.Valve.setProperty("portname", _translate("MainWindow", "/dev/ttyUSB0", None))
        self.Valve_2.setToolTip(_translate("MainWindow", "Tip", None))
        self.Valve_2.setWhatsThis(_translate("MainWindow", "What is this", None))
        self.Valve_2.setProperty("portname", _translate("MainWindow", "/dev/ttyUSB0", None))
        self.Thermocouple.setToolTip(_translate("MainWindow", "Tip", None))
        self.Thermocouple.setWhatsThis(_translate("MainWindow", "What is this", None))
        self.Thermocouple.setProperty("portname", _translate("MainWindow", "/dev/ttyUSB0", None))
        self.Plot.setToolTip(_translate("MainWindow", "Tip", None))
        self.Plot.setWhatsThis(_translate("MainWindow", "What is this", None))
        self.Plot.setProperty("portname", _translate("MainWindow", "/dev/ttyUSB0", None))

from felleslab.qt_widgets.buttons import QFellesButtons
from felleslab.qt_widgets.controller import QFellesController
from felleslab.qt_widgets.plot import QFellesPlot
from felleslab.qt_widgets.solenoidvalve import QFellesSolenoidValve
from felleslab.qt_widgets.thermocouple import QFellesThermocouple
import icons_rc
