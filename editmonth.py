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
	self.table = QtGui.QTableWidget()
	self.table.setRowCount(3)
	self.table.setColumnCount(9)

	self.table.setHorizontalHeaderLabels(['Lfd','Mitgl. Nr.','Name','Vorname',u"Aufnahmegebühr",u"-> Bezahlt",u"Beitrag",u"-> Bezahlt",u"USt"])
	vbox.addWidget(self.table)


	# Creating Buttons
	btnAddEntry = QtGui.QPushButton(u"Eintrag hinzufügen")
	btnAddEntry.clicked.connect(self.addEntry)
	btnDelEntry = QtGui.QPushButton(u"Eintrag löschen")
	btnDelEntry.clicked.connect(self.delEntry)
	btnPrintPrev = QtGui.QPushButton(u"Auswertung")
	btnPrint     = QtGui.QPushButton(u"Drucken")
	
	btnAditional = QtGui.QPushButton(u"Sonstige Einnahmen")
	
	btnSave = QtGui.QPushButton(u"Speichern")

	# Creating Button-Layout	
	buttonBox.addWidget(btnAddEntry,0,0)
	buttonBox.addWidget(btnDelEntry,1,0)
	buttonBox.addWidget(btnPrintPrev,0,1)
	buttonBox.addWidget(btnPrint,1,1)
	buttonBox.addWidget(btnAditional,0,2)
	buttonBox.addWidget(btnSave,0,4)

	vbox.addLayout(buttonBox) 		# Put ButtonBox into Main-Container
	self.setLayout(vbox)
	self.show()

    # Adding new Rows	
    def addEntry(self):
	if (self.table.currentRow() == -1):
	    self.table.insertRow(0)
	else:
	    self.table.insertRow(self.table.currentRow()) 	# insert new Row at Current selected
	

    # Delete a Row
    def delEntry(self):
	self.table.removeRow(self.table.currentRow())   # Delete the current Row


def main():
    app = QtGui.QApplication(sys.argv)

    window = monthWindow()


    sys.exit(app.exec_())
 
if __name__ == '__main__' :
    main()
