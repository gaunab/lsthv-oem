#!/usr/bin/python
# -*- coding: utf-8- -*-

"""
This Project is for calculating bils 

"""
import sys
from PyQt4 import QtGui,QtCore
import editpref 
import settings


class beraterApp(QtGui.QWidget):
    def __init__(self,berater):
	super(beraterApp, self).__init__()

	self.berater = berater
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

	btnOpenMonth = QtGui.QPushButton(u"Monat öffnen")
	
	btnNewMonth = QtGui.QPushButton('Neuer Monat')
	btnNewMonth.setToolTip('This is a <b>QPushButton</b> widget')
	vbox.addWidget(btnOpenMonth)
	vbox.addWidget(btnNewMonth)

	btnEditPref = QtGui.QPushButton(u"Beraterdaten")
	btnEditPref.clicked.connect(self.editPref)
	vbox.addWidget(btnEditPref)

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

    def editPref(self):
	# print("Hallo welt")
	self.frmPrefs = editpref.prefWindow(self.berater)

def main():
    app = QtGui.QApplication(sys.argv)

    berater = settings.beraterData()
    window = beraterApp(berater)

    sys.exit(app.exec_())
 
if __name__ == '__main__' :
    main()
