#!/usr/bin/python
# -*- coding: utf-8- -*-

"""
This Project is for calculating bils 

"""
import sys
from PyQt4 import QtGui,QtCore

class monthWindow(QtGui.QWidget):
    def __init__(self):
	super(monthWindow, self).__init__()

	self.initUI()

    def initUI(self):
	vbox = QtGui.QVBoxLayout() 		# Main Container
	
	buttonBox = QtGui.QGridLayout() 	# Container for Buttons

	
	# Creating Table
	table = QtGui.QTableWidget()
	table.setRowCount(3)
	table.setColumnCount(10)
	vbox.addWidget(table)


	# Creating Buttons
	btnAddEntry = QtGui.QPushButton(u"Eintrag hinzufügen")
	btnAddEntry.clicked.connect(table.insertRow(1))
	btnDelEntry = QtGui.QPushButton(u"Eintrag löschen")

	btnPrintPrev = QtGui.QPushButton(u"Auswertung")
	btnPrint     = QtGui.QPushButton(u"Drucken")
	
	btnAditional = QtGui.QPushButton(u"Sonstige Einnahmen")
		
	# Creating Button-Layout	
	buttonBox.addWidget(btnAddEntry,0,0)
	buttonBox.addWidget(btnDelEntry,1,0)
	buttonBox.addWidget(btnPrintPrev,0,1)
	buttonBox.addWidget(btnPrint,1,1)
	buttonBox.addWidget(btnAditional,0,2)



	vbox.addLayout(buttonBox) 		# Put ButtonBox into Main-Container
	self.setLayout(vbox)
	self.show()

def main():
    app = QtGui.QApplication(sys.argv)

    window = monthWindow()


    sys.exit(app.exec_())
 
if __name__ == '__main__' :
    main()
