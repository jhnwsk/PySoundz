#!/usr/bin/python

import sys
from PyQt4 import QtGui, QtCore


class Icon(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Icon')
        self.setWindowIcon(QtGui.QIcon('icons/web.png'))

class MessageBox(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('message box')


    def closeEvent(self, event):
        reply = QtGui.QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QtGui.QMessageBox.Yes | 
            QtGui.QMessageBox.No, QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

class PySoundzGUI(QtGui.QWidget):

    def __init__(self):
        super(PySoundzGUI, self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('PySoundz')
        self.setGeometry(300, 300, 250, 150)
        
        names = ['filter1',
                 'filter2']
        
        grid = QtGui.QGridLayout()
        
        j = 0
        for name in names:
            # buttons for filter names
            checkBox = QtGui.QCheckBox(name)
            grid.addWidget(checkBox, j, 0)
            # sliders for amount
            slider = QtGui.QSlider(QtCore.Qt.Horizontal)
            slider.setFocusPolicy(QtCore.Qt.NoFocus)
            slider.setGeometry(30,40,100,30)
            self.connect(slider, QtCore.SIGNAL('valueChanged(int)'), self.changeValue)
            grid.addWidget(slider, j, 1)

            j += 1
        
        button = QtGui.QPushButton('play that shit!')
        grid.addWidget(button, j, 0)
        self.setLayout(grid)

    def changeValue(self, value):
        if value == 0:
            self.label.setPixmap(QtGui.QPixmap('mute.png'))
        elif value > 0 and value <= 30:
            self.label.setPixmap(QtGui.QPixmap('min.png'))
        elif value > 30 and value < 80:
            self.label.setPixmap(QtGui.QPixmap('med.png'))
        else:
            self.label.setPixmap(QtGui.QPixmap('max.png'))

if __name__ == '__main__':
  
    app = QtGui.QApplication(sys.argv)
    ex = PySoundzGUI()
    ex.show()
    app.exec_()
else:
    app = QtGui.QApplication(sys.argv)

    icon = Icon()
    icon.show()
    qb = MessageBox()
    qb.show()

sys.exit(app.exec_())
