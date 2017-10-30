# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GUI.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

USB = '/dev/tty.usbserial'

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
        MainWindow.resize(800, 600)
        MainWindow.setMaximumSize(QtCore.QSize(800, 16777215))
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.logoNTNU = QtGui.QLabel(self.centralwidget)
        self.logoNTNU.setGeometry(QtCore.QRect(500, 490, 301, 61))
        self.logoNTNU.setObjectName(_fromUtf8("logoNTNU"))
        self.Valve = QFellesSolenoidValve(self.centralwidget)
        self.Valve.setGeometry(QtCore.QRect(110, 320, 66, 66))
        self.Valve.setProperty("slaveaddress", 1)
        self.Valve.setProperty("channel", 0)
        self.Valve.setProperty("initialState", 1)
        self.Valve.setProperty("finalState", 1)
        self.Valve.setObjectName(_fromUtf8("Valve"))
        self.pushButton = QtGui.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(210, 220, 99, 27))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.pushButton_2 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(210, 270, 99, 27))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.Thermocouple = QFellesThermocouple(self.centralwidget)
        self.Thermocouple.setGeometry(QtCore.QRect(360, 100, 25, 34))
        self.Thermocouple.setProperty("slaveaddress", 2)
        self.Thermocouple.setProperty("channel", 0)
        self.Thermocouple.setObjectName(_fromUtf8("Thermocouple"))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(450, 110, 68, 17))
        self.label.setObjectName(_fromUtf8("label"))
        self.Valve_2 = QFellesSolenoidValve(self.centralwidget)
        self.Valve_2.setGeometry(QtCore.QRect(320, 320, 66, 66))
        self.Valve_2.setProperty("slaveaddress", 1)
        self.Valve_2.setProperty("channel", 0)
        self.Valve_2.setProperty("initialState", 1)
        self.Valve_2.setProperty("finalState", 1)
        self.Valve_2.setObjectName(_fromUtf8("Valve_2"))
        self.Thermocouple_2 = QFellesThermocouple(self.centralwidget)
        self.Thermocouple_2.setGeometry(QtCore.QRect(360, 150, 25, 34))
        self.Thermocouple_2.setProperty("slaveaddress", 2)
        self.Thermocouple_2.setProperty("channel", 1)
        self.Thermocouple_2.setObjectName(_fromUtf8("Thermocouple_2"))
        self.Thermocouple_3 = QFellesThermocouple(self.centralwidget)
        self.Thermocouple_3.setGeometry(QtCore.QRect(360, 200, 25, 34))
        self.Thermocouple_3.setProperty("slaveaddress", 2)
        self.Thermocouple_3.setProperty("channel", 2)
        self.Thermocouple_3.setObjectName(_fromUtf8("Thermocouple_3"))
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(440, 160, 68, 17))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_3 = QtGui.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(430, 210, 68, 17))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL(_fromUtf8("clicked()")), self.Valve.setOpen)
        QtCore.QObject.connect(self.pushButton_2, QtCore.SIGNAL(_fromUtf8("clicked()")), self.Valve.setClose)
        QtCore.QObject.connect(self.Thermocouple, QtCore.SIGNAL(_fromUtf8("newSample(QString)")), self.label.setText)
        QtCore.QObject.connect(self.Thermocouple_2, QtCore.SIGNAL(_fromUtf8("newSample(QString)")), self.label_2.setText)
        QtCore.QObject.connect(self.Thermocouple_3, QtCore.SIGNAL(_fromUtf8("newSample(QString)")), self.label_3.setText)
        QtCore.QObject.connect(self.Valve, QtCore.SIGNAL(_fromUtf8("valveClosed()")), self.Valve_2.setOpen)
        QtCore.QObject.connect(self.Valve_2, QtCore.SIGNAL(_fromUtf8("valveClosed()")), self.Valve.setClose)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.logoNTNU.setText(_translate("MainWindow", "<html><head/><body><p><img src=\":/icons/NTNU_logo.png\"/></p></body></html>", None))
        self.Valve.setToolTip(_translate("MainWindow", "Solenoid Valve", None))
        self.Valve.setWhatsThis(_translate("MainWindow", "Solenoid valve", None))
        self.Valve.setProperty("portname", _translate("MainWindow", USB, None))
        self.pushButton.setText(_translate("MainWindow", "PushButton", None))
        self.pushButton_2.setText(_translate("MainWindow", "PushButton", None))
        self.Thermocouple.setToolTip(_translate("MainWindow", "Tip", None))
        self.Thermocouple.setWhatsThis(_translate("MainWindow", "What is this", None))
        self.Thermocouple.setProperty("portname", _translate("MainWindow", USB, None))
        self.label.setText(_translate("MainWindow", "TextLabel", None))
        self.Valve_2.setToolTip(_translate("MainWindow", "Tip", None))
        self.Valve_2.setWhatsThis(_translate("MainWindow", "What is this", None))
        self.Valve_2.setProperty("portname", _translate("MainWindow", USB, None))
        self.Thermocouple_2.setToolTip(_translate("MainWindow", "Tip", None))
        self.Thermocouple_2.setWhatsThis(_translate("MainWindow", "What is this", None))
        self.Thermocouple_2.setProperty("portname", _translate("MainWindow", USB, None))
        self.Thermocouple_3.setToolTip(_translate("MainWindow", "Tip", None))
        self.Thermocouple_3.setWhatsThis(_translate("MainWindow", "What is this", None))
        self.Thermocouple_3.setProperty("portname", _translate("MainWindow", USB, None))
        self.label_2.setText(_translate("MainWindow", "TextLabel", None))
        self.label_3.setText(_translate("MainWindow", "TextLabel", None))

from felleslab.qt_widgets.solenoidvalve import QFellesSolenoidValve
from felleslab.qt_widgets.thermocouple import QFellesThermocouple
import icons_rc

class MainWindow(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None, f=QtCore.Qt.WindowFlags()):
        QtGui.QMainWindow.__init__(self, parent, f)

        self.setupUi(self)


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

