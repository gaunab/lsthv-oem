#!/usr/bin/python
# -*- coding: utf-8- -*-

from PyQt4 import QtGui

class ustWidget(QtGui.QWidget):
    def __init__(self,ust):
	super(ustWidget, self).__init__()
	self.ust = ust
	self.initUI()

    def initUI(self):
        
        lblDesc = QtGui.QLabel(u"Umsatzsteuer-Verlauf")
        maingrid = QtGui.QGridLayout()
        maingrid.addWidget(lblDesc,0,0,1,2)

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

    def addNewEntry(self):
        self.ustTable.insertRow(self.ustTable.rowCount())

    def delEntry(self):
        self.ustTable.removeRow(self.ustTable.currentRow())



