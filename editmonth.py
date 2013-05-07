#!/usr/bin/python
# -*- coding: utf-8- -*-

"""
This Project is for calculating bils 

"""
import month
import sys
from PyQt4 import QtGui,QtCore

class monthWindow(QtGui.QWidget):

    def __init__(self,month):
	super(monthWindow, self).__init__()
	print "Opening Month"
	self.initUI() 				# Initilasing QT Window
	self.month = month
	self.loadMonth(month) 			# Load Data into Table
	
    def initUI(self):
	vbox = QtGui.QVBoxLayout() 		# Main Container
	
	buttonBox = QtGui.QGridLayout() 	# Container for Buttons

	
	# Creating Table
	self.table = QtGui.QTableWidget()
	self.table.setRowCount(0)
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
        btnPrint.clicked.connect(self.handlePrint)	
	btnAditional = QtGui.QPushButton(u"Sonstige Einnahmen")
	
	btnSave = QtGui.QPushButton(u"Speichern")
	btnSave.clicked.connect(self.save)

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

    # Load Month Data into Grid
    def loadMonth(self,month):
	
	    readerrors = 0 			# Counting errors on reading the data-file

	    for entry in month.data["table"]: 	# Iterate through all Data-Lines
		self.table.insertRow(self.table.rowCount()) 	# insert new Row at end of table

		# now fill the table with life
		try:
		    # continue reading with next line after finding an error
    		    self.table.setItem(self.table.rowCount()-1,0,QtGui.QTableWidgetItem(unicode(entry["lfd"]))) 	
    		    self.table.setItem(self.table.rowCount()-1,1,QtGui.QTableWidgetItem(unicode(entry["mtgl-nr"])))
    		    self.table.setItem(self.table.rowCount()-1,2,QtGui.QTableWidgetItem(unicode(entry["name"])))
    		    self.table.setItem(self.table.rowCount()-1,3,QtGui.QTableWidgetItem(unicode(entry["firstname"])))
    		    self.table.setItem(self.table.rowCount()-1,4,QtGui.QTableWidgetItem(unicode(entry["aufnahmegeb"])))
    		    self.table.setItem(self.table.rowCount()-1,5,QtGui.QTableWidgetItem(unicode(entry["aufnahmepayed"])))
    		    self.table.setItem(self.table.rowCount()-1,6,QtGui.QTableWidgetItem(unicode(entry["beitrag"])))
    		    self.table.setItem(self.table.rowCount()-1,7,QtGui.QTableWidgetItem(unicode(entry["beitragpayed"])))
		except (KeyError), name: 	
		    readerrors+=1 			# only Count Errors

	    if readerrors:
		QtGui.QMessageBox.critical(self,"Fehler",unicode(str(readerrors)+u" Datensätze konnten nicht gelesen werden oder waren unvollständig.\n \n Bitte überprüfen Sie die Daten"))

#	except:
#	    return False



    # Adding new Rows	
    def addEntry(self):
	if (self.table.currentRow() == -1):
	    self.table.insertRow(0)
	else:
	    self.table.insertRow(self.table.currentRow()) 	# insert new Row at Current selected
	

    # Delete a Row
    def delEntry(self):
	self.table.removeRow(self.table.currentRow())   # Delete the current Row

    # Save monthdata
    def save(self):
	# First write Table-Content to Month-Object
	data = []
	for row in range(self.table.rowCount()):
	    data.append({'lfd':self.table.item(row,0).text().toUtf8().data(),
		    	 'mtgl-nr':self.table.item(row,1).text().toUtf8().data(),
		    	 'name':self.table.item(row,2).text().toUtf8().data(),
		    	 'firstname':self.table.item(row,3).text().toUtf8().data(),
		    	 'aufnahmegeb':self.table.item(row,4).text().toUtf8().data(),
		    	 'aufnahmepayed':self.table.item(row,5).text().toUtf8().data(),
		    	 'beitrag':self.table.item(row,6).text().toUtf8().data(),
		    	 'beitragpayed':self.table.item(row,7).text().toUtf8().data(), 
			}
		    )

	self.month.data["table"] = data
	self.month.save()

    def handlePrint(self):
    	printer = QtGui.QPrinter(QtGui.QPrinter.HighResolution)
	dialog = QtGui.QPrintDialog(printer,self)
	dialog.exec_()
	# if dialog.exec_() == QtGui.QDialog.Accepted:
	# handle the Printing   

def main():
    app = QtGui.QApplication(sys.argv)

    window = monthWindow("hallo")


    sys.exit(app.exec_())
 
if __name__ == '__main__' :
    main()
