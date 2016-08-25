#! /usr/local/bin/python
# -*- coding: utf-8- -*-

from PyQt4 import QtGui,QtCore,Qt
import month
import os,sys

"""
Edit additional incomes for a month. This creates a new Window with a table
where several Incomes can be stored.

"""
class MiscTable(QtGui.QTableWidget):
    def __init__(self):
        super(MiscTable,self).__init__()
        self.setSortingEnabled(True)
        self.setDragDropMode(QtGui.QAbstractItemView.InternalMove)
        self.setSelectionBehavior(QtGui.QTableView.SelectRows)
        self.setDropIndicatorShown(True)
        self.setAcceptDrops(True)
        self.setDragEnabled(True)

    def cellToFloat(self,col,row):
        try:
            value = str(self.item(col,row).text())
            value = value.replace(",",".")
            return float(value)
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

class miscWindow(QtGui.QMainWindow):
    def __init__(self,monat=None):
        super(miscWindow,self).__init__()
        self.miscwidget = miscWidget(monat)
        self.setCentralWidget(self.miscwidget)

        menubar = self.menuBar()
        filemenu = menubar.addMenu("&Datei")
        editmenu = menubar.addMenu("Bearbeiten")

        exitAction = QtGui.QAction(u"Schließen", self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip(u"Fenster Schließen")
        exitAction.triggered.connect(self.close)
        filemenu.addAction(exitAction)

        addRowAction =QtGui.QAction(u"Eintrag hinzufügen", self)
        addRowAction.setShortcut('Ctrl++')
        addRowAction.setStatusTip(u"Füge neue Zeile hinzu")
        addRowAction.triggered.connect(self.miscwidget.addNewEntry)

        delRowAction =QtGui.QAction(u"Eintrag löschen", self)
        delRowAction.setShortcut('Ctrl+-')
        delRowAction.setStatusTip(u"Lösche ausgewählte Zeile")
        delRowAction.triggered.connect(self.miscwidget.delEntry)
        editmenu.addAction(addRowAction)
        editmenu.addAction(delRowAction)

        self.miscwidget.setStatusBar(self.statusBar())
        self.show()


    def closeEvent(self, event):
        self.miscwidget.saveData()


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



class miscWidget(QtGui.QWidget):
    """ Edit/Add aditional incomes """

    def __init__(self,monat=None):
        """ Create new Misc-Window 

        Parameters:
        ----------

        month: current month object

        """
        super(miscWidget, self).__init__()
        self.monat  = monat
        self.lblSum = QtGui.QLabel("Summe: ")
        self.initUI()
        self.loadData()
        self.show()

    def initUI(self):
        """ Create all new items for misc window """
        self.setWindowTitle(u"Sonstige Einnahmen")
        maingrid = QtGui.QVBoxLayout()       
        buttongrid  = QtGui.QHBoxLayout()
        btnAddLine = QtGui.QPushButton(u"Hinzufügen")
        btnAddLine.clicked.connect(self.addNewEntry)
        btnDelLine = QtGui.QPushButton(u"Löschen")
        btnDelLine.clicked.connect(self.delEntry)

        self.miscTable = MiscTable()       # Create new Table
        self.miscTable.setColumnCount(2)
        self.miscTable.setHorizontalHeaderLabels([u"Beschreibung",u"Betrag in €"])

        self.miscTable.itemChanged.connect(self.valueFormat)
        
        buttongrid.addWidget(btnAddLine)
        buttongrid.addWidget(btnDelLine)

        maingrid.addWidget(self.miscTable)
        maingrid.addItem(buttongrid)

        self.setLayout(maingrid) 		    # Grid for Layout
        self.show()

    def addNewEntry(self):
        self.miscTable.insertRow(self.miscTable.rowCount())

    def delEntry(self):
        self.miscTable.removeRow(self.miscTable.currentRow())


    def setStatusBar(self,bar):
        self.statusbar = bar
        self.statusbar.addWidget(self.lblSum)

    def valueFormat(self,editItem):
        """ Format number Cells """
        red = QtGui.QColor()
        red.setRgb(200,0,0)                      
        black = QtGui.QColor()
        black.setRgb(0,0,0) 
        # editItem.setTextColor(black)                              # on default all Columns are black
        if editItem.column() in [1]:                                # Format only Currency-Related cols
            origText = editItem.text().replace(",",".")             # First replace all ,s as they're entered in Germany with .s
            try:
                newText = u"%0.2f" %(float(origText))
                editItem.setText(newText.replace(".",","))          # now convert .s back to ,s
                editItem.setTextColor(black)
            except:                                                 # in case the number could not be formatted - print the cell in red
                editItem.setTextColor(red)
            self.updateSum()
            

        elif editItem.column() in [0]:                            # Convert first Letter of Names to Capital letter
            itemtext = str(editItem.text()).title()
            editItem.setText(itemtext)

    def updateSum(self):
        """ Update Sum in Statusbar """

        sumOfMisc = 0.0
        for row in range(self.miscTable.rowCount()):
            if self.miscTable.item(row,1) is None:
                value = "0.00"
            else:
                value = self.miscTable.item(row,1).text()
            
            value = value.replace(",",".")             # First replace all ,s as they're entered in Germany with .s
            try:
                sumOfMisc += float(value)
            except:
                pass

        self.lblSum.setText(u"Summe: %0.2f €" %sumOfMisc)

    def loadData(self):
        """ Load Data from month-object """
        readerrors = 0
        if ("misc" in self.monat.data) :
            for entry in self.monat.data["misc"]:         # Iterate through all Data-Lines
                self.miscTable.insertRow(self.miscTable.rowCount())         # insert new Row at end of table
                
                try:
                    self.miscTable.setItem(self.miscTable.rowCount()-1,0,TableItem((entry["text"])))
                    self.miscTable.setItem(self.miscTable.rowCount()-1,1,TableItem((str(entry["value"]))))
                except (KeyError) as name:         
                    readerrors+=1                         # only Count Errors
        else:                                             # Empty table
            self.addNewEntry()

        if readerrors:
            QtGui.QMessageBox.critical(self,"Fehler",unicode(str(readerrors)+u" Datensätze konnten nicht gelesen werden oder waren unvollständig.\n \n Bitte überprüfen Sie die Daten"))

    def saveData(self):
        """ Save Data back to month Object """

        data = []
        print(self.miscTable.rowCount())
        for row in range(self.miscTable.rowCount()):
            if (self.miscTable.item(row,0) is None):
                text = unicode("")
            else:
                text = unicode(self.miscTable.item(row,0).text())
            value = self.miscTable.cellToFloat(row,1)
            print(value)
            print("Saving misc entry: %s %f" %(text,value))

            data.append({'text':text,'value':value})
            self.monat.data["misc"] = data

def main():
    app = QtGui.QApplication(sys.argv)

    window = miscWidget("Monat")


    sys.exit(app.exec_())
 
if __name__ == '__main__' :
    main()
