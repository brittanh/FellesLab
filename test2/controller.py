
# coding=utf-8

import sys

from PyQt4 import QtGui


class Window(QtGui.QWidget):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        
        # group box
        group_box = QtGui.QGroupBox('Controller Settings')  # the shortcut key is ALT + C
        
        # Spin buttons
        self.gain_label = QtGui.QLabel('Kc')
        #self.gain_label.setAlignment(QtGui.AlignCenter)
        self.gain = QtGui.QDoubleSpinBox()
        self.taui = QtGui.QDoubleSpinBox()
        self.taud = QtGui.QDoubleSpinBox()
        
        # Spin buttons
        rb_vlayout = QtGui.QVBoxLayout()
        rb_vlayout.addWidget(self.gain)
        rb_vlayout.addWidget(self.taui)
        rb_vlayout.addWidget(self.taud)
        group_box.setLayout(rb_vlayout)
        
        # vertical box layout
        vlayout = QtGui.QVBoxLayout()
        vlayout.addWidget(group_box)
        vlayout.addStretch()
        self.setLayout(vlayout)


application = QtGui.QApplication(sys.argv)

# window
window = Window()
window.setWindowTitle('Group Box')
window.resize(220, 100)
window.show()

sys.exit(application.exec_())
