#!/usr/bin/python
# -*- coding: utf-8- -*-

"""
This Project is for calculating bils 

"""
import sys
from PyQt4 import QtGui,QtCore
import editpref
import monthlist
import newmonth
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
	btnOpenMonth.clicked.connect(self.monthList)
	
	btnNewMonth = QtGui.QPushButton('Neuer Monat')
	btnNewMonth.setToolTip('einen neuen Monat anlegen')
	btnNewMonth.clicked.connect(self.newMonth)
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

    def monthList(self):
	self.frmMonthList = monthlist.monthList(self.berater)

    def newMonth(self):
	self.frmNewMonth = newmonth.newMonth()

    def editPref(self):
	# print("Hallo welt")
	self.frmPrefs = editpref.prefWindow(self.berater)

def main():
    app = QtGui.QApplication(sys.argv)            # Create new QT4 app
    berater = settings.beraterData()              # load settings and personal information
    window = beraterApp(berater)                  # create MainMenu
    if (not berater.saved):
        QtGui.QMessageBox.critical(window,'Bitte Beraterdaten Eingeben','Konnte Beraterdaten nicht laden.\nBitte geben Sie die Beraterdaten ein.')
    sys.exit(app.exec_())
 
if __name__ == '__main__' :
    main()
