#!/usr/bin/python
# -*- coding: utf-8- -*-

"""
This Project is for calculating bils 

"""
import sys
from PyQt4 import QtGui,QtCore


class beraterApp(QtGui.QWidget):
    def __init__(self):
	super(beraterApp, self).__init__()

	self.initUI()


    ### Init The Window

    def initUI(self):
	self.setGeometry(300,300,250,150) 		# set Window properties
	self.setWindowTitle('XBerater') 		# 
	# self.setWindowIcon(QtGui.QIcon('icon.png'))   # set Icon (not yet)

	### Add Buttons of Main-Window

	btn = QtGui.QPushButton('Button',self)
	btn.setToolTip('This is a <b>QPushButton</b> widget')
	
	btnQuit = QtGui.QPushButton('Beenden',self) 			 # Exit Button
	btnQuit.clicked.connect(QtCore.QCoreApplication.instance().quit ) # Exit function

	self.show()
	
    def closeEvent(self, event):
	reply = QtGui.QMessageBox.question(self,'Beenden','Wirklich beenden?',QtGui.QMessageBox.Yes |
		QtGui.QMessageBox.No, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()  

def main():
    app = QtGui.QApplication(sys.argv)

    window = beraterApp()


    sys.exit(app.exec_())
 
if __name__ == '__main__' :
    main()
