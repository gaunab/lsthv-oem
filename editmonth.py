#!/usr/bin/python
# -*- coding: utf-8- -*-

"""
This Project is for calculating bils 

"""
import month,printing,settings,monthlist 
import sys
from PyQt4 import QtGui,QtCore
from operator import itemgetter

class BeraterTable(QtGui.QTableWidget):
    def __init__(self):
        super(BeraterTable,self).__init__()

    def cellToFloat(self,col,row):
        try:
            text = str(self.item(col,row).text())
            text.replace(",",".")
            return float(text)

        except:
            return 0.0

class monthWindow(QtGui.QMainWindow):
    def openMonth(self):
	self.frmMonthList = monthlist.monthList()
    
    def __init__(self,month):
        super(monthWindow,self).__init__()
        monthwidget = monthWidget(month)
        self.setCentralWidget(monthwidget)
        self.show()
        print "New Window"

        # Create Menubar
        menubar = self.menuBar()
        filemenu = menubar.addMenu("Datei")
        editmenu = menubar.addMenu("Bearbeiten")

        exitAction = QtGui.QAction(u"Schließen", self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Programm Beenden')
        exitAction.triggered.connect(self.close)

        saveAction = QtGui.QAction('Speichern', self)
        saveAction.setShortcut('Ctrl+S')
        saveAction.setStatusTip('Aktuellen Monat speichern')
        saveAction.triggered.connect(monthwidget.save)

        printAction = QtGui.QAction('Drucken', self)
        printAction.setShortcut('Ctrl+P')
        printAction.setStatusTip('Aktuellen Monat drucken')
        printAction.triggered.connect(monthwidget.handlePrint)

        addAction = QtGui.QAction(u"Neue Zeile einfügen", self)
        addAction.setShortcut('Ctrl++')
        addAction.setStatusTip('Fügt eine neue Zeile ein')
        addAction.triggered.connect(monthwidget.addEntry)

        removeAction = QtGui.QAction(u"Zeile löschen", self)
        removeAction.setShortcut('Ctrl+-')
        removeAction.setStatusTip('Entfernt die Markierte Zeile')
        removeAction.triggered.connect(monthwidget.delEntry)

        openAction = QtGui.QAction(u"Monat öffnen", self)
        openAction.setShortcut('Ctrl+o')
        openAction.setStatusTip(u"Einen anderen Monat öffnen")
        openAction.triggered.connect(self.openMonth)

        filemenu.addAction(openAction)
        filemenu.addAction(saveAction)
        filemenu.addAction(printAction)
        filemenu.addAction(exitAction)
        editmenu.addAction(addAction)
        editmenu.addAction(removeAction)


class monthWidget(QtGui.QWidget):

 
    # Determine UST
    def getUST(self):
        ustlist = sorted(self.beraterData.ust, key=itemgetter('from')) 
        thismonth = "%i%02i" %(self.month.data["year"], self.month.data["month"])
        thismonth = int(thismonth)
        
        ust = ustlist[0]["value"]
        for date in ustlist:
            if thismonth >= date["from"]:
                ust = date["value"]

        return ust	

    def __init__(self,month):
	super(monthWidget, self).__init__()
	print "Opening Month"
	self.month = month
	self.initUI() 				# Initialating Month Widget
	self.loadMonth(month) 			# Load Data into Table
        self.beraterData = settings.beraterData()
        self.ust = self.getUST()

    def initUI(self):
	vbox = QtGui.QVBoxLayout() 		# Main Container
	
	buttonBox = QtGui.QGridLayout() 	# Container for Buttons

        lblMonth = QtGui.QLabel(u"Monat: "+str(self.month.data["month"]) + "." + str(self.month.data["year"]))
        vbox.addWidget(lblMonth)
	# Creating Table
	# self.table = QtGui.QTableWidget()
        self.table = BeraterTable()
	self.table.setRowCount(0)
	self.table.setColumnCount(8)

	self.table.setHorizontalHeaderLabels(['Mitgl. Nr.','Name','Vorname',u"Aufnahmegebühr",u"-> Bezahlt",u"Beitrag",u"-> Bezahlt",u"USt"])

	vbox.addWidget(self.table)

        self.table.itemChanged.connect(self.valueFormat)

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


    # Format Data for number-cols
    def valueFormat(self,editItem):
        red = QtGui.QColor()
        red.setRgb(200,0,0)                      
        black = QtGui.QColor()
        black.setRgb(0,0,0)                       
        # editItem.setTextColor(black)                              # on default all Columns are black
        if editItem.column() in [3,4,5,6,7]:                        # Format only Currency-Related cols
            origText = editItem.text().replace(",",".")             # First replace all ,s as they're entered in Germany with .s
            try:
                newText = u"%0.2f" %(float(origText))
                editItem.setText(newText.replace(".",","))          # now convert .s back to ,s
                editItem.setTextColor(black)
            except:                                                 # in case the number could not be formatted - print the cell in red
                editItem.setTextColor(red)

        elif editItem.column() in [1,2]:                            # Convert first Letter of Names to Capital letter
            itemtext = str(editItem.text()).title()
            editItem.setText(itemtext)
                

    # Load Month Data into Grid
    def loadMonth(self,month):
	
	    readerrors = 0 			# Counting errors on reading the data-file
            if ("table" in month.data) :
                for entry in month.data["table"]: 	# Iterate through all Data-Lines
                    self.table.insertRow(self.table.rowCount()) 	# insert new Row at end of table

                    # now fill the table with life
                    try:
                        # continue reading with next line after finding an error
                        # self.table.setItem(self.table.rowCount()-1,0,QtGui.QTableWidgetItem(unicode(entry["lfd"]))) 	
                        self.table.setItem(self.table.rowCount()-1,0,QtGui.QTableWidgetItem(unicode(entry["mtgl-nr"])))
                        self.table.setItem(self.table.rowCount()-1,1,QtGui.QTableWidgetItem(unicode(entry["name"])))
                        self.table.setItem(self.table.rowCount()-1,2,QtGui.QTableWidgetItem(unicode(entry["firstname"])))
                        self.table.setItem(self.table.rowCount()-1,3,QtGui.QTableWidgetItem(unicode(entry["aufnahmegeb"])))
                        self.table.setItem(self.table.rowCount()-1,4,QtGui.QTableWidgetItem(unicode(entry["aufnahmepayed"])))
                        self.table.setItem(self.table.rowCount()-1,5,QtGui.QTableWidgetItem(unicode(entry["beitrag"])))
                        self.table.setItem(self.table.rowCount()-1,6,QtGui.QTableWidgetItem(unicode(entry["beitragpayed"])))
                        self.table.setItem(self.table.rowCount()-1,7,QtGui.QTableWidgetItem(unicode(entry["ust"])))
                    except (KeyError), name: 	
                        readerrors+=1 			# only Count Errors
            else:                                                           # Empty table
                self.table.insertRow(1)                                     # Create new empty Line

	    if readerrors:
		QtGui.QMessageBox.critical(self,"Fehler",unicode(str(readerrors)+u" Datensätze konnten nicht gelesen werden oder waren unvollständig.\n \n Bitte überprüfen Sie die Daten"))

#	except:
#	    return False



    # Adding new Rows	
    def addEntry(self):
	if (self.table.currentRow() == -1):
	    self.table.insertRow(0)
            self.table.setItem(0,7,QtGui.QTableWidgetItem(unicode("%0.2f"))) %(self.ust)
	else:
	    self.table.insertRow(self.table.currentRow()) 	# insert new Row at Current selected
            self.table.setItem(self.table.currentRow()-1,7,QtGui.QTableWidgetItem(u"%0.2f" %(float(self.ust)) ))
	

    # Delete a Row
    def delEntry(self):
	self.table.removeRow(self.table.currentRow())   # Delete the current Row

    # Save monthdata
    def save(self):
	# First write Table-Content to Month-Object
	data = []
	for row in range(self.table.rowCount()):

            if (self.table.item(row,0) is None):
                mtglnr = ""
            else:
                mtglnr = self.table.item(row,0).text().toUtf8().data()

            if (self.table.item(row,1) is None):
                name = ""
            else:
                name = self.table.item(row,1).text().toUtf8().data()

            if (self.table.item(row,2) is None):
                firstname = ""
            else:
                firsname = self.table.item(row,2).text().toUtf8().data()

            if (self.table.item(row,3) is None):
                aufnahmegeb = "0,00"
            else:
                aufnahmegeb = self.table.item(row,3).text().toUtf8().data()

            if (self.table.item(row,4) is None):
                aufnahmepayed = "0.00"
            else:
                aufnahmepayed = self.table.item(row,4).text().toUtf8().data()

            if (self.table.item(row,5) is None):
                beitrag = "0.00"
            else:
                beitrag = self.table.item(row,5).text().toUtf8().data()

            if (self.table.item(row,6) is None):
                beitragpayed = "0.00"
            else:
                beitragpayed = self.table.item(row,6).text().toUtf8().data()
	    
            if (self.table.item(row,7) is None):
                ust = "%0.2f" %(self.ust)
            else:
                ust = self.table.item(row,7).text().toUtf8().data()

            data.append({'lfd':row+1,
		    	 'mtgl-nr':mtglnr,
                         'name':name,
		    	 'firstname':firstname,
		    	 'aufnahmegeb':aufnahmegeb,
		    	 'aufnahmepayed':aufnahmepayed,
		    	 'beitrag':beitrag,
		    	 'beitragpayed':beitragpayed, 
                         'ust':ust
			}
		    )

	self.month.data["table"] = data
	self.month.save()

    def handlePrint(self):
	printdata = printing.printout(self.table,self)
	printdata.dialog()



def main():
    app = QtGui.QApplication(sys.argv)

    window = monthWindow("hallo")


    sys.exit(app.exec_())
 
if __name__ == '__main__' :
    main()
