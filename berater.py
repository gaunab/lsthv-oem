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
	self.setWindowTitle('XBerater') 		# 
	# self.setWindowIcon(QtGui.QIcon('icon.png'))   # set Icon (not yet)


	### Statusbar
#	self.statusBar().showMessage('')

	### Menubar
	exitAction = QtGui.QAction(QtGui.QIcon('exit.png'),'&Beenden',self)
	exitAction.setShortcut('Ctrl+Q')
	exitAction.setStatusTip('Programm Beenden')
	exitAction.triggered.connect(QtGui.qApp.quit)


#	menubar = self.menuBar()
#	fileMenu = menubar.addMenu('&Datei')
#	fileMenu.addAction(exitAction)

	### Add COntainer

	vbox = QtGui.QVBoxLayout()
	vbox.addStretch(1)

	### Add Buttons of Main-Window

	btn = QtGui.QPushButton('Button')
	btn.setToolTip('This is a <b>QPushButton</b> widget')
	vbox.addWidget(btn)

        btnQuit = QtGui.QPushButton('Beenden') 			 # Exit Button
	btnQuit.clicked.connect(QtCore.QCoreApplication.instance().quit ) # Exit function
	vbox.addWidget(btnQuit)

	self.setLayout(vbox)
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
