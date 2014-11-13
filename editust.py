#!/usr/bin/python
# -*- coding: utf-8- -*-

from PyQt4 import QtGui
from operator import itemgetter

class ustWidget(QtGui.QWidget):
    def __init__(self,ust):
        super(ustWidget, self).__init__()
        self.ust = ust
        self.initUI()
        self.loadentries()

    def initUI(self):
        
        maingrid = QtGui.QGridLayout()

        self.ustTable = QtGui.QTableWidget()
        self.ustTable.setColumnCount(3)
        self.ustTable.setHorizontalHeaderLabels(['Monat','Jahr','USt-Satz'])

        maingrid.addWidget(self.ustTable,1,0,1,2)
        buttongrid = QtGui.QHBoxLayout()
        btnAddLine = QtGui.QPushButton(u"Hinzufügen")
        btnAddLine.clicked.connect(self.addNewEntry)
        btnDelLine = QtGui.QPushButton(u"Löschen")
        btnDelLine.clicked.connect(self.delEntry)
        maingrid.addWidget(btnAddLine,2,0)
        maingrid.addWidget(btnDelLine,2,1)


        self.setLayout(maingrid)

    def loadentries(self):
        if (len(self.ust) > 1):
            ustlist = sorted(self.ust, key=itemgetter('from')) 
        else:
            ustlist =  self.ust 
        for entry in ustlist:
            fromstr = str(entry["from"])
            if len(fromstr) == 6:
                self.ustTable.insertRow(self.ustTable.rowCount())
                monthCell = QtGui.QTableWidgetItem(fromstr[4:])
                yearCell  = QtGui.QTableWidgetItem(fromstr[:4])
                valueCell = QtGui.QTableWidgetItem(str(entry["value"]))
                self.ustTable.setItem(self.ustTable.rowCount()-1,0,monthCell)
                self.ustTable.setItem(self.ustTable.rowCount()-1,1,yearCell)
                self.ustTable.setItem(self.ustTable.rowCount()-1,2,valueCell)

    def returnEntries(self):
        entries = []
        for line in range(self.ustTable.rowCount()):
            ustentry = {}
            try:
                fromvalue = "%i%02d" %(int(str(self.ustTable.item(line,1).text())), int(str(self.ustTable.item(line,0).text())))
                ustentry["from"] = int(fromvalue)
                ustentry["value"] = int(str(self.ustTable.item(line,2).text()))
            except(ValueError,AttributeError):
                ustentry["from"] = 2000
                ustentry["value"] = 0
                QtGui.QMessageBox.critical(self,u"Fehler",u"Fehler: Eintrag "+str(line+1) + u" enthält keine Zahl")



            entries.append(ustentry)

        return entries

    def addNewEntry(self):
        self.ustTable.insertRow(self.ustTable.rowCount())

    def delEntry(self):
        self.ustTable.removeRow(self.ustTable.currentRow())



