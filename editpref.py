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
	btnClose.clicked.connect(self.close)

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
	lblZip = QtGui.QLabel(u"Postleitzahl")

	grid.addWidget(self.edtName,0,1)
	grid.addWidget(lblName,0,0)
	grid.addWidget(self.edtFirstName,1,1)
	grid.addWidget(lblFirstName,1,0)
	grid.addWidget(self.edtId,2,1)
	grid.addWidget(lblId,2,0)
	grid.addWidget(self.edtId,2,1)
	grid.addWidget(lblId,2,0)
	grid.addWidget(self.edtStreet,3,1)
	grid.addWidget(lblStreet,3,0)
	grid.addWidget(self.edtTown,4,1)
	grid.addWidget(lblTown,4,0)
	grid.addWidget(self.edtZip,5,1)
	grid.addWidget(lblZip,5,0)
	grid.addWidget(self.edtBank,6,1)
	grid.addWidget(lblBank,6,0)
	grid.addWidget(self.edtBankid,7,1)
	grid.addWidget(lblBankid,7,0)
	grid.addWidget(self.edtBankKto,8,1)
	grid.addWidget(lblBankKto,8,0)

	grid.addWidget(btnSave,10,0)
	grid.addWidget(btnClose,10,1)
	self.setLayout(grid) 			# Grid for Layout
	self.show()

    # Checking for changes 
    def closeEvent(self, event):
	changed = False
	if (unicode(self.berater.name) != unicode(self.edtName.text())) or (unicode(self.berater.firstname) != unicode(self.edtFirstName.text())) or (unicode(self.berater.id) != unicode(self.edtId.text())) or unicode(self.berater.bank) != unicode(self.edtBank.text()) or unicode(self.berater.bankid) != unicode(self.edtBankid.text()) or unicode(self.berater.deposit) != unicode(self.edtBankKto.text()) or unicode(self.berater.street) != unicode(self.edtStreet.text()) or unicode(self.berater.town) != unicode(self.edtTown.text()) or unicode(self.berater.zip) != unicode(self.edtZip.text()):
	    changed = True

	if (changed == True):
	    msgBox = QtGui.QMessageBox();
	    msgBox.setText(u"Ihre Daten wurden verändert..");
	    msgBox.setInformativeText(u"Möchten Sie die Änderungen Speichern?");
	    msgBox.setStandardButtons(QtGui.QMessageBox.Save | QtGui.QMessageBox.Discard | QtGui.QMessageBox.Cancel);
	    msgBox.setDefaultButton(QtGui.QMessageBox.Save);
	    ret = msgBox.exec_();
	    if ret == QtGui.QMessageBox.Save:
		self.save()
		event.accept()
	    else:
		if ret == QtGui.QMessageBox.Discard:
		    event.accept()
		else:
		    event.ignore()
	else:
	    event.accept()
	
	    

    # Saving Personal Data to berater Object, save to file afterwards
    def save(self):
	self.berater.name = unicode(self.edtName.text())
	self.berater.firstname = unicode(self.edtFirstName.text())
	self.berater.id = unicode(self.edtId.text())
	self.berater.bank = unicode(self.edtBank.text())
	self.berater.bankid = unicode(self.edtBankid.text())
	self.berater.deposit = unicode(self.edtBankKto.text())
	self.berater.street = unicode(self.edtStreet.text())
	self.berater.town = unicode(self.edtTown.text())
	self.berater.zip = unicode(self.edtZip.text())
	self.berater.save()
