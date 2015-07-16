#!/usr/bin/python
# -*- coding: utf-8- -*-

from PyQt4 import QtGui
from operator import itemgetter

class feeWidget(QtGui.QWidget):
    def __init__(self,fee):
        super(feeWidget, self).__init__()
        self.fee = fee
        self.initUI()
        self.loadentries()

    def initUI(self):
        
        maingrid = QtGui.QGridLayout()

        self.feeTable = QtGui.QTableWidget()
        self.feeTable.setColumnCount(3)
        self.feeTable.setHorizontalHeaderLabels(["Monat","Jahr",u"Vergütung"])

        maingrid.addWidget(self.feeTable,1,0,1,2)
        buttongrid = QtGui.QHBoxLayout()
        btnAddLine = QtGui.QPushButton(u"Hinzufügen")
        btnAddLine.clicked.connect(self.addNewEntry)
        btnDelLine = QtGui.QPushButton(u"Löschen")
        btnDelLine.clicked.connect(self.delEntry)
        maingrid.addWidget(btnAddLine,2,0)
        maingrid.addWidget(btnDelLine,2,1)


        self.setLayout(maingrid)

    def loadentries(self):
        if (len(self.fee) > 1):
            feelist = sorted(self.fee, key=itemgetter('from')) 
        else:
            feelist =  self.fee 
        for entry in feelist:
            fromstr = str(entry["from"])
            if len(fromstr) == 6:
                self.feeTable.insertRow(self.feeTable.rowCount())
                monthCell = QtGui.QTableWidgetItem(fromstr[4:])
                yearCell  = QtGui.QTableWidgetItem(fromstr[:4])
                valueCell = QtGui.QTableWidgetItem(str(entry["value"]))
                self.feeTable.setItem(self.feeTable.rowCount()-1,0,monthCell)
                self.feeTable.setItem(self.feeTable.rowCount()-1,1,yearCell)
                self.feeTable.setItem(self.feeTable.rowCount()-1,2,valueCell)

    def returnEntries(self):
        entries = []
        for line in range(self.feeTable.rowCount()):
            feeentry = {}
            try:
                fromvalue = "%i%02d" %(int(str(self.feeTable.item(line,1).text())), int(str(self.feeTable.item(line,0).text())))
                feeentry["from"] = int(fromvalue)
                feeentry["value"] = int(str(self.feeTable.item(line,2).text()))
            except(ValueError,AttributeError):
                feeentry["from"] = 2000
                feeentry["value"] = 0
                QtGui.QMessageBox.critical(self,u"Fehler",u"Fehler: Eintrag "+str(line+1) + u" enthält keine Zahl")



            entries.append(feeentry)

        return entries

    def addNewEntry(self):
        self.feeTable.insertRow(self.feeTable.rowCount())

    def delEntry(self):
        self.feeTable.removeRow(self.feeTable.currentRow())



