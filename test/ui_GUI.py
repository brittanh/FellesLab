# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GUI.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
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
        MainWindow.resize(800, 600)
        MainWindow.setMaximumSize(QtCore.QSize(800, 16777215))
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.logoNTNU = QtGui.QLabel(self.centralwidget)
        self.logoNTNU.setGeometry(QtCore.QRect(500, 490, 301, 61))
        self.logoNTNU.setObjectName(_fromUtf8("logoNTNU"))
        self.Valve = QFellesSolenoidValve(self.centralwidget)
        self.Valve.setGeometry(QtCore.QRect(110, 320, 66, 66))
        self.Valve.setProperty("channel", 0)
        self.Valve.setProperty("slaveaddress", 0)
        self.Valve.setObjectName(_fromUtf8("Valve"))
        self.pushButton = QtGui.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(210, 220, 99, 27))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.pushButton_2 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(210, 270, 99, 27))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.Thermocouple = QFellesThermocouple(self.centralwidget)
        self.Thermocouple.setGeometry(QtCore.QRect(180, 60, 25, 34))
        self.Thermocouple.setProperty("channel", 0)
        self.Thermocouple.setProperty("slaveaddress", 0)
        self.Thermocouple.setObjectName(_fromUtf8("Thermocouple"))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(280, 90, 68, 17))
        self.label.setObjectName(_fromUtf8("label"))
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
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.logoNTNU.setText(_translate("MainWindow", "<html><head/><body><p><img src=\":/icons/NTNU_logo.png\"/></p></body></html>", None))
        self.Valve.setToolTip(_translate("MainWindow", "Tip", None))
        self.Valve.setWhatsThis(_translate("MainWindow", "What is this", None))
        self.Valve.setProperty("portname", _translate("MainWindow", "/dev/ttyUSB0", None))
        self.pushButton.setText(_translate("MainWindow", "PushButton", None))
        self.pushButton_2.setText(_translate("MainWindow", "PushButton", None))
        self.Thermocouple.setToolTip(_translate("MainWindow", "Tip", None))
        self.Thermocouple.setWhatsThis(_translate("MainWindow", "What is this", None))
        self.Thermocouple.setProperty("portname", _translate("MainWindow", "/dev/ttyUSB0", None))
        self.label.setText(_translate("MainWindow", "TextLabel", None))

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

