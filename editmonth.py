#!/usr/bin/python
# -*- coding: utf-8- -*-

"""
This Project is for calculating bils 

"""
import newmonth,month,printing,settings,monthlist,editpref 
import os,sys
import time
from datetime import date
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

    def event(self, event):
        if (event.type()== QtCore.QEvent.KeyPress) and (event.key()==QtCore.Qt.Key_Tab):
            self.emit(QtCore.SIGNAL("tabPressed"))
            return True

        if (event.type()== QtCore.QEvent.KeyPress) and ( (event.key()==QtCore.Qt.Key_Return) or (event.key()==QtCore.Qt.Key_Enter)  ) :
            self.emit(QtCore.SIGNAL("returnPressed"))
            return True
        return QtGui.QTableWidget.event(self, event)


class TableItem(QtGui.QTableWidgetItem):
    """ The main working area: Windows with table of current month """
    def __init__(self,text):
        super(TableItem,self).__init__(text)

    #def __init__(self):
    #    super(TableItem,self).__init__()

    def event(self, event):
        if (event.type()== QtCore.QEvent.KeyPress) and (event.key()==QtCore.Qt.Key_Tab):
            self.emit(QtCore.SIGNAL("tabPressed"))
            return True
        
        if (event.type()== QtCore.QEvent.KeyPress) and ( (event.key()==QtCore.Qt.Key_Return) or (event.key()==QtCore.Qt.Key_Enter)  ) :
            self.emit(QtCore.SIGNAL("returnPressed"))
            return True

        return QtGui.QTableWidgetItem.event(self, event)




class monthWindow(QtGui.QMainWindow):
    def openMonth(self):
        self.frmMonthList = monthlist.monthList(beraterdata)
    
    def createMonth(self):
        self.frmNewMonth = newmonth.newMonth(beraterdata)

    def openPrefs(self):
        self.frmSettingsWindow = editpref.prefWindow(beraterdata)

    def about(self):
         QtGui.QMessageBox.about(self,u"Informationen",u"Beraterabrechnung \n Versions-Datum: 14.06.15")

    
    def __init__(self,berater,monat=None):
        super(monthWindow,self).__init__()
        global beraterdata
        beraterdata = berater
        if (monat == None):
            monat = month.lsthvmonth(beraterdata)
            monthlist=['']
            fileList = os.listdir(".")                  # list of all Files
            fileList.sort()                         # sort files by name
            for filename in sorted(fileList) :                 # iterate through all files
                if filename.find("monat.yaml") != -1:   # only continue with month-yaml-files
                    monatfile = month.lsthvmonth(beraterdata)
                    if (monatfile.open(filename)):         # Only append to , if valid month
                        monthlist.append(filename)
            lastmonth = date.fromtimestamp(time.time() - (30 * 24 * 60 * 60))
            lastmonthfilename = "%4i%02imonat.yaml" %(int(lastmonth.year),int(lastmonth.month))
            if (lastmonthfilename in set(monthlist)):
                monat.open(lastmonthfilename)
            else:
                monat.data["month"] =   lastmonth.month        # examine Month-Number from ComboBox
                monat.data["year"] =    lastmonth.year                         # examine year from SpinBox
                monat.fee = monat.determineFee()

        monthwidget = monthWidget(beraterdata,monat)
        self.setWindowTitle('XBerater - Monat bearbeiten')                 # 
        self.setCentralWidget(monthwidget)
        self.show()

        # Create Menubar
        menubar = self.menuBar()
        filemenu = menubar.addMenu("&Datei")
        editmenu = menubar.addMenu("&Bearbeiten")
        settingsmenu = menubar.addMenu("&Einstellungen")
        menubar.addSeparator()
        helpmenu = menubar.addMenu("&Hilfe")

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

        previewAction = QtGui.QAction('Druckvorschau', self)
        previewAction.setShortcut('Ctrl+Shift+P')
        previewAction.setStatusTip(u"Druckvorschau für den aktuellen Monat")
        previewAction.triggered.connect(monthwidget.printPreview)
        
        addAction = QtGui.QAction(u"Neue Zeile einfügen", self)
        addAction.setShortcut('Ctrl++')
        addAction.setStatusTip(u'Fügt eine neue Zeile ein')
        addAction.triggered.connect(monthwidget.addEntry)

        removeAction = QtGui.QAction(u"Zeile löschen", self)
        removeAction.setShortcut('Ctrl+-')
        removeAction.setStatusTip('Entfernt die Markierte Zeile')
        removeAction.triggered.connect(monthwidget.delEntry)



        openAction = QtGui.QAction(u"Monat öffnen", self)
        openAction.setShortcut('Ctrl+o')
        openAction.setStatusTip(u"Einen anderen Monat öffnen")
        openAction.triggered.connect(self.openMonth)

        createAction = QtGui.QAction(u"Neuer Monat", self)
        createAction.setShortcut('Ctrl+n')
        createAction.setStatusTip(u"Einen neuen Monat anlegen")
        createAction.triggered.connect(self.createMonth)

        aboutAction =  QtGui.QAction(u"Version",self)
        aboutAction.setStatusTip(u"Informationen über die Programmversion")
        aboutAction.triggered.connect(self.about)

        openPref = QtGui.QAction(u"Beraterdaten", self)
        openPref.setStatusTip(u"Persönliche Beraterdaten bearbeiten")
        openPref.triggered.connect(self.openPrefs)

        filemenu.addAction(createAction)
        filemenu.addAction(openAction)
        filemenu.addAction(saveAction)
        filemenu.addSeparator()
        filemenu.addAction(printAction)
        filemenu.addAction(previewAction)
        filemenu.addSeparator()
        filemenu.addAction(exitAction)
        editmenu.addAction(addAction)
        editmenu.addAction(removeAction)
        settingsmenu.addAction(openPref)
        helpmenu.addAction(aboutAction)

        # Create StatusBar
        monthwidget.setStatusBar(self.statusBar())

class monthWidget(QtGui.QWidget):

 
#    # Determine UST
#    def getUST(self):
#        ustlist = sorted(self.beraterData.ust, key=itemgetter('from')) 
#        thismonth = "%i%02i" %(self.month.data["year"], self.month.data["month"])
#        thismonth = int(thismonth)
#        
#        ust = ustlist[0]["value"]
#        for date in ustlist:
#            if thismonth >= date["from"]:
#                ust = date["value"]
#
#        return ust        

    def onContextMenu(self,point):
        self.contextMenu.exec_(self.table.mapToGlobal(point))

    def __init__(self,beraterdata,month):
        super(monthWidget, self).__init__()
        self.month = month
        self.initUI()                                 # Initialating Month Widget
        self.beraterData = beraterdata
        self.ust = self.month.ustdec * 100
        self.fee = self.month.fee
        self.loadMonth(month)                         # Load Data into Table

    def initUI(self):
        vbox = QtGui.QVBoxLayout()                 # Main Container
        
        buttonBox = QtGui.QGridLayout()         # Container for Buttons

        self.lblMonth = QtGui.QLabel(u"Monat: %02i.%04i " %(self.month.data["month"],self.month.data["year"]) )
        self.lblEvaluation = QtGui.QLabel(u"Vergütung: %0.2f€" %(self.month.evaluation()["payout"]))       # Write payout to Status-Bar
        self.month.fee = self.month.determineFee()
        self.lblFee = QtGui.QLabel(u"Vergütungssatz: %0.2f" %(self.month.fee))       # Write Fee to Status-Bar
        # vbox.addWidget(lblMonth)
        # Creating Table
        # self.table = QtGui.QTableWidget()
        self.table = BeraterTable()
        self.table.setRowCount(0)
        self.table.setColumnCount(8)

        self.table.setHorizontalHeaderLabels(['Mitgl. Nr.','Name','Vorname',u"Aufnahmegebühr €",u"\u21D2 Bezahlt €",u"Beitrag €",u"\u21D2 Bezahlt €",u"USt [%]"])

        vbox.addWidget(self.table)

        self.table.itemChanged.connect(self.valueFormat)
        self.connect(self.table, QtCore.SIGNAL("tabPressed"), self.nextCell)
        self.connect(self.table, QtCore.SIGNAL("returnPressed"), self.nextCell)
        self.table.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.connect(self.table,QtCore.SIGNAL('customContextMenuRequested(const QPoint&)'),self.onContextMenu)

        # Creating Buttons
        btnAddEntry = QtGui.QPushButton(u"Eintrag hinzufügen")
        btnAddEntry.clicked.connect(self.addEntry)
        btnDelEntry = QtGui.QPushButton(u"Eintrag löschen")
        btnDelEntry.clicked.connect(self.delEntry)
        btnPrintPrev = QtGui.QPushButton(u"Druckvorschau")
        btnPrintPrev.clicked.connect(self.printPreview)        
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
        #buttonBox.addWidget(btnAditional,0,2)
        buttonBox.addWidget(btnSave,0,4)

        self.contextMenu = QtGui.QMenu(self)
        addAction = QtGui.QAction(u"Neue Zeile einfügen", self)
        addAction.setShortcut('Ctrl++')
        addAction.setStatusTip(u'Fügt eine neue Zeile ein')
        addAction.triggered.connect(self.addEntry)

        removeAction = QtGui.QAction(u"Zeile löschen", self)
        removeAction.setShortcut('Ctrl+-')
        removeAction.setStatusTip('Entfernt die Markierte Zeile')
        removeAction.triggered.connect(self.delEntry)

        previewAction = QtGui.QAction(u"Druckvorschau", self)
        previewAction.setShortcut('Ctrl+Shift+P')
        previewAction.setStatusTip('Vorschau für das Drucken')
        previewAction.triggered.connect(self.printPreview)

        self.contextMenu.addAction(addAction)
        self.contextMenu.addAction(removeAction)

        vbox.addLayout(buttonBox)                 # Put ButtonBox into Main-Container
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
        
            readerrors = 0                         # Counting errors on reading the data-file
            if ("table" in month.data) :
                for entry in month.data["table"]:         # Iterate through all Data-Lines
                    self.table.insertRow(self.table.rowCount())         # insert new Row at end of table

                    # now fill the table with life
                    try:
                        # continue reading with next line after finding an error
                        # self.table.setItem(self.table.rowCount()-1,0,QtGui.QTableWidgetItem(unicode(entry["lfd"])))         
                        self.table.setItem(self.table.rowCount()-1,0,TableItem((entry["mtgl-nr"])))
                        self.table.setItem(self.table.rowCount()-1,1,TableItem((entry["name"])))
                        self.table.setItem(self.table.rowCount()-1,2,TableItem((entry["firstname"])))
                        self.table.setItem(self.table.rowCount()-1,3,TableItem((entry["aufnahmegeb"])))
                        self.table.setItem(self.table.rowCount()-1,4,TableItem((entry["aufnahmepayed"])))
                        self.table.setItem(self.table.rowCount()-1,5,TableItem((entry["beitrag"])))
                        self.table.setItem(self.table.rowCount()-1,6,TableItem((entry["beitragpayed"])))
                        self.table.setItem(self.table.rowCount()-1,7,TableItem((entry["ust"])))
                    except (KeyError) as name:         
                        readerrors+=1                         # only Count Errors
            else:                                                           # Empty table
#                self.table.insertRow(1)                                     # Create new empty Line
#                self.table.setRowCount(1)
                self.addEntry()

            if readerrors:
                QtGui.QMessageBox.critical(self,"Fehler",unicode(str(readerrors)+u" Datensätze konnten nicht gelesen werden oder waren unvollständig.\n \n Bitte überprüfen Sie die Daten"))

            self.month.determineFee()
            self.lblFee.setText(u"Vergütungssatz: %0.2f" %(self.month.fee))       # Write Fee to Status-Bar

#        except:
#            return False



    # Adding new Rows        
    def addEntry(self):
        if (self.table.currentRow() == -1):
            self.table.insertRow(0)
            for i in range(7):
                self.table.setItem(0,i,TableItem(u""))
            self.table.setItem(0,7,TableItem(u"%0.2f" %(self.ust) ))
        else:
            self.table.insertRow(self.table.currentRow()+1)         # insert new Row at Current selected
            for i in range(7):
                self.table.setItem(self.table.currentRow()+1,i,TableItem(u""))
            self.table.setItem(self.table.currentRow()+1,7,TableItem(u"%0.2f" %(float(self.ust)) ))

        self.updatedata()
  
    def nextCell(self):
        curRow = self.table.currentRow() 
        curCol = self.table.currentColumn() 
        if (curCol >= self.table.columnCount() -1):
            if (curRow >= self.table.rowCount() - 1):
                    self.addEntry()
            self.table.setCurrentCell(self.table.rowCount()-1,0)
        else:
            self.table.setCurrentCell(curRow,curCol+1)

  
    def setStatusBar(self,bar):
        self.statusbar = bar
        self.statusbar.addWidget(self.lblMonth)
        self.statusbar.addWidget(self.lblEvaluation)
        self.statusbar.addWidget(self.lblFee)
    # Delete a Row
    def delEntry(self):
        self.table.removeRow(self.table.currentRow())   # Delete the current Row
        self.updatedata()

    # Update monthdata
    def updatedata(self):
        # First write Table-Content to Month-Object
        data = []
        for row in range(self.table.rowCount()):

            if (self.table.item(row,0) is None):
                mtglnr = ""
            else:
                mtglnr = self.table.item(row,0).text()

            if (self.table.item(row,1) is None):
                name = ""
            else:
                name = self.table.item(row,1).text()

            if (self.table.item(row,2) is None):
                firstname = ""
            else:
                firstname = self.table.item(row,2).text()

            if (self.table.item(row,3) is None):
                aufnahmegeb = "0,00"
            else:
                aufnahmegeb = self.table.item(row,3).text()

            if (self.table.item(row,4) is None):
                aufnahmepayed = "0.00"
            else:
                aufnahmepayed = self.table.item(row,4).text()

            if (self.table.item(row,5) is None):
                beitrag = "0.00"
            else:
                beitrag = self.table.item(row,5).text()

            if (self.table.item(row,6) is None):
                beitragpayed = "0.00"
            else:
                beitragpayed = self.table.item(row,6).text()
            
            if (self.table.item(row,7) is None):
                ust = "%0.2f" %(self.ust)
            else:
                ust = self.table.item(row,7).text()

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

        self.month.data["table"] = data                                                             # update data-block in month
        self.lblEvaluation.setText(u"Vergütung: %0.2f€" %(self.month.evaluation()["payout"]))       # Write payout to Status-Bar

    def save(self):
        self.updatedata()
        self.month.save()
        self.statusbar.showMessage(u"Monat wurde erfolgreich gespeichert",2000)

    def handlePrint(self):
        printer = QtGui.QPrinter(QtGui.QPrinter.HighResolution)
        printDialog = QtGui.QPrintDialog(printer,self)
        if printDialog.exec_() == QtGui.QDialog.Accepted:
            self.printout(printer)


    def printout(self,printer):
        printdata = printing.printout(self.table,self,printer)
        printdata.create()


    def printPreview(self):
        printer = QtGui.QPrinter(QtGui.QPrinter.HighResolution)
        previewDialog = QtGui.QPrintPreviewDialog(printer)
        self.connect(previewDialog,QtCore.SIGNAL("paintRequested (QPrinter *)"),self.printout)
        # previewDialog.paintRequested.connect(pages)
        previewDialog.exec_()

    def handlePaintRequest(self, printer):
        self.view.render(QtGui.QPainter(printer))

def main():
    app = QtGui.QApplication(sys.argv)

    window = monthWindow("hallo")


    sys.exit(app.exec_())
 
if __name__ == '__main__' :
    main()
