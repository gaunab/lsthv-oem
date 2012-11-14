#!/usr/bin/python
# -*- coding: utf-8- -*-

from PyQt4 import QtGui

class prefWindow(QtGui.QWidget):
    def __init__(self,berater):
	super(prefWindow, self).__init__()
	self.berater = berater
	self.initUI()

    def initUI(self):
	self.setWindowTitle(u"Beraterdaten")

	grid = QtGui.QGridLayout() 		# Main Container

	btnSave = QtGui.QPushButton(u"Speichern") # Save-Button
	btnSave.clicked.connect(self.save)

	btnClose = QtGui.QPushButton(u"Schließen")
	btnClose.clicked.connect(self.close())

	self.edtName = QtGui.QLineEdit()
	self.edtName.setText(self.berater.name)
	lblName = QtGui.QLabel(u"Name")
	
	self.edtFirstName = QtGui.QLineEdit()
	self.edtFirstName.setText(self.berater.firstname)
	lblFirstName = QtGui.QLabel(u"Vorname")
	
	self.edtId = QtGui.QLineEdit()
	self.edtId.setText(self.berater.id)
	lblId = QtGui.QLabel(u"Beraternummer")

	self.edtBank = QtGui.QLineEdit()
	self.edtBank.setText(self.berater.bank)
	lblBank = QtGui.QLabel(u"Bank")

	self.edtBankid = QtGui.QLineEdit()
	self.edtBankid.setText(self.berater.bankid)
	lblBankid = QtGui.QLabel(u"Bankleitzahl")
	
	self.edtBankKto = QtGui.QLineEdit()
	self.edtBankKto.setText(self.berater.deposit)
	lblBankKto = QtGui.QLabel(u"Kontonummer")
	
	self.edtStreet = QtGui.QLineEdit()
	self.edtStreet.setText(self.berater.street)
	lblStreet = QtGui.QLabel(u"Strasse")

	self.edtTown = QtGui.QLineEdit()
	self.edtTown.setText(self.berater.town)
	lblTown = QtGui.QLabel(u"Stadt")

	self.edtZip = QtGui.QLineEdit()
	self.edtZip.setText(self.berater.zip)
	lbZip = QtGui.QLabel(u"Postleitzahl")

	grid.addWidget(self.edtName,0,1)
	grid.addWidget(lblName,0,0)
	grid.addWidget(self.edtFirstName,1,1)
	grid.addWidget(lblFirstName,1,0)
	grid.addWidget(self.edtId,2,1)
	grid.addWidget(lblId,2,0)
	grid.addWidget(self.edtId,2,1)
	grid.addWidget(lblId,2,0)

	grid.addWidget(btnSave,3,0)
	self.setLayout(grid) 			# Grid for Layout
	self.show()


    def save(self):
	self.berater.name = unicode(self.edtName.text())
	self.berater.firstname = unicode(self.edtFirstName.text())
	self.berater.id = unicode(self.edtId.text())
	self.berater.bank = unicode(self.edtBank.text())
	self.berater.bankid = unicode(self.edtBankid.text())
	self.berater.deposit = unicode(self.edtBankKto.text())
	self.berater.street = unicode(self.edtStreet.text())
	self.berater.save()
