'''
Created on 24-02-2011

@author: johnDonson
'''

import sys

from PyQt4 import QtGui, QtCore
from theSound import Sound

class PySoundzGUI(QtGui.QWidget):

    
    def __init__(self):
        super(PySoundzGUI, self).__init__()
        self.assignFilterValues()
        self.initUI()

    def assignFilterValues(self):
        self.filters = [('filter1', QtGui.QCheckBox('filter1'),QtGui.QLCDNumber(self)),
                 ('filter2',QtGui.QCheckBox('filter2'),QtGui.QLCDNumber(self))]
    
    def initUI(self):
        self.setWindowTitle('PySoundz')
        self.setGeometry(300, 300, 250, 150)
        
        grid = QtGui.QGridLayout()
        
        j = 0
        for filter in self.filters:
            # buttons for filter names
            checkBox = filter[1]
            grid.addWidget(checkBox, j, 0)
            # sliders for amount
            lcd = filter[2]
            grid.addWidget(lcd, j, 1)
            
            slider = QtGui.QSlider(QtCore.Qt.Horizontal)
            slider.setFocusPolicy(QtCore.Qt.NoFocus)
            slider.setGeometry(30, 40, 100, 30)
            self.connect(slider, QtCore.SIGNAL('valueChanged(int)'), lcd, QtCore.SLOT('display(int)'))
            grid.addWidget(slider, j+1, 1)

            j += 2
        
        self.button = QtGui.QPushButton('play that shit!')
        self.connect(self.button, QtCore.SIGNAL('clicked()'), self.generateWave)
        grid.addWidget(self.button, j, 0)
        
        self.pbar = QtGui.QProgressBar(self)
        self.pbar.setGeometry(30, 40, 200, 25)
        grid.addWidget(self.pbar, j, 1)
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
            
    def generateWave(self):
        self.sound = Sound()
        self.sound.generateWave(filter(lambda (x,y,z) : y.isChecked(), self.filters), self.pbar)
            
    def closeEvent(self, event):
        reply = QtGui.QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QtGui.QMessageBox.Yes | 
            QtGui.QMessageBox.No, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
    

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    ex = PySoundzGUI()
    ex.show()
    app.exec_()

sys.exit(app.exec_())
