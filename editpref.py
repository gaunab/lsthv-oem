#!/usr/bin/python
# -*- coding: utf-8- -*-

from PyQt4 import QtGui,QtCore
import editust,editfee

class beraterLineEdit(QtGui.QLineEdit):
    def __init__(self, *args):
        QtGui.QLineEdit.__init__(self, *args)
        
    def event(self, event):
        if (event.type()== QtCore.QEvent.KeyPress) and ( (event.key()==QtCore.Qt.Key_Return) or (event.key()==QtCore.Qt.Key_Enter)  ) :
            self.emit(QtCore.SIGNAL("nextElement"));
            return True

        return QtGui.QLineEdit.event(self, event)

class prefWindow(QtGui.QWidget):
    def __init__(self,berater):
        super(prefWindow, self).__init__()
        self.berater = berater
        self.initUI()

    def event(self,event):
        return QtGui.QWidget.event(self, event)

    def initUI(self):
        self.setWindowTitle(u"Beraterdaten")

        grid = QtGui.QGridLayout() 		    # In Tab Container
        maingrid = QtGui.QVBoxLayout()              # Main Container

        btnSave = QtGui.QPushButton(u"Speichern")   # Save-Button
        btnSave.clicked.connect(self.save)

        btnClose = QtGui.QPushButton(u"Schließen")  # Close Button
        btnClose.clicked.connect(self.close)

        cntButtons = QtGui.QWidget()
        cntButtonsLayout = QtGui.QHBoxLayout()
        cntButtonsLayout.addWidget(btnSave)
        cntButtonsLayout.addWidget(btnClose)
        cntButtons.setLayout(cntButtonsLayout)

        tabWidget = QtGui.QTabWidget()
        generalPrefs = QtGui.QWidget()

        self.edtName = beraterLineEdit()
        self.edtName.setText(self.berater.name)
        lblName = QtGui.QLabel(u"Name")
	
        self.edtFirstName = QtGui.QLineEdit()
        self.edtFirstName.setText(self.berater.firstname)
        lblFirstName = QtGui.QLabel(u"Vorname")
	
        self.edtId = QtGui.QLineEdit()
        self.edtId.setText(self.berater.id)
        lblId = QtGui.QLabel(u"Beraternummer")

        self.edtUstnr = QtGui.QLineEdit()
        self.edtUstnr.setText(self.berater.ustnr)
        lblUstnr = QtGui.QLabel(u"Steuernummer")
	
        self.edtBank = QtGui.QLineEdit()
        self.edtBank.setText(self.berater.bank)
        lblBank = QtGui.QLabel(u"Bank")

        self.edtBic = QtGui.QLineEdit()
        self.edtBic.setText(self.berater.bic)
        lblBic = QtGui.QLabel(u"BIC")
	
        self.edtIban = QtGui.QLineEdit()
        self.edtIban.setText(self.berater.iban)
        lblIban = QtGui.QLabel(u"IBAN")
	
        self.edtStreet = QtGui.QLineEdit()
        self.edtStreet.setText(self.berater.street)
        lblStreet = QtGui.QLabel(u"Strasse")

        self.edtTown = QtGui.QLineEdit()
        self.edtTown.setText(self.berater.town)
        lblTown = QtGui.QLabel(u"Ort")

        self.edtZip = QtGui.QLineEdit()
        self.edtZip.setText(self.berater.zip)
        lblZip = QtGui.QLabel(u"Postleitzahl")

        self.edtFee = QtGui.QLineEdit()
        # self.edtFee.setText(self.berater.fee)
        lblFee = QtGui.QLabel(u"Vergütungssatz (in %)")

        self.ustwidget = editust.ustWidget(self.berater.ust)
        self.feewidget = editfee.feeWidget(self.berater.fee)


        self.connect(self,QtCore.SIGNAL("returnPressed"),self.focusNextChild)

        grid.addWidget(self.edtName,0,1)
        grid.addWidget(lblName,0,0)
        grid.addWidget(self.edtFirstName,1,1)
        grid.addWidget(lblFirstName,1,0)
        grid.addWidget(self.edtId,2,1)
        grid.addWidget(lblId,2,0)
        grid.addWidget(self.edtUstnr,3,1)
        grid.addWidget(lblUstnr,3,0)
        grid.addWidget(self.edtStreet,4,1)
        grid.addWidget(lblStreet,4,0)
        grid.addWidget(self.edtTown,5,1)
        grid.addWidget(lblTown,5,0)
        grid.addWidget(self.edtZip,6,1)
        grid.addWidget(lblZip,6,0)
        grid.addWidget(self.edtBank,7,1)
        grid.addWidget(lblBank,7,0)
        grid.addWidget(self.edtIban,8,1)
        grid.addWidget(lblIban,8,0)
        grid.addWidget(self.edtBic,9,1)
        grid.addWidget(lblBic,9,0)
        grid.addWidget(self.edtFee,10,1)
        grid.addWidget(lblFee,10,0)
#        grid.addWidget(ustgroupBox,11,1)
       
        generalPrefs.setLayout(grid)
        tabWidget.insertTab(1,generalPrefs,u"Beratereinstellungen")
        tabWidget.insertTab(2,self.ustwidget,u"Umsatzsteuer") 
        tabWidget.insertTab(3,self.feewidget,u"Vergütung")
        maingrid.addWidget(tabWidget)
        maingrid.addWidget(cntButtons)

        self.setLayout(maingrid) 			# Grid for Layout
        self.show()

    # Checking for changes 
    def closeEvent(self, event):
        changed = False
        if ((self.berater.name) != (self.edtName.text())) or ((self.berater.firstname) != (self.edtFirstName.text())) or ((self.berater.id) != (self.edtId.text())) or (self.berater.bank) != (self.edtBank.text()) or (self.berater.bic) != (self.edtBic.text()) or (self.berater.iban) != (self.edtIban.text()) or (self.berater.street) != (self.edtStreet.text()) or (self.berater.town) != (self.edtTown.text()) or (self.berater.zip) != (self.edtZip.text()):
            changed = True

        if (changed == True):
            msgBox = QtGui.QMessageBox();
            msgBox.setText(u"Ihre Daten wurden verändert..");
            msgBox.setInformativeText(u"Möchten Sie die Änderungen Speichern?");
            msgBox.setStandardButtons(QtGui.QMessageBox.Save | QtGui.QMessageBox.Discard | QtGui.QMessageBox.Cancel);
            msgBox.setButtonText(QtGui.QMessageBox.Save ,"Speichern");
            msgBox.setButtonText(QtGui.QMessageBox.Discard ,"Nicht speichern");
            msgBox.setButtonText(QtGui.QMessageBox.Cancel,"Abbrechen");
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
        self.berater.name = (self.edtName.text()).rstrip()                           # Convert Edit-Field to unicode string, remove all trailing whitespaces
        self.berater.firstname = (self.edtFirstName.text()).rstrip()
        self.berater.id = (self.edtId.text()).rstrip()
        self.berater.bank = (self.edtBank.text()).rstrip()
        self.berater.bic = (self.edtBic.text()).rstrip()
        self.berater.iban = (self.edtIban.text()).rstrip()
        self.berater.ustnr = (self.edtUstnr.text()).rstrip()
        if (not self.berater.checkiban()):                                                  # Check if IBAN is correct
            msgBox = QtGui.QMessageBox();
            msgBox.setText(u"Die IBAN ist inkorrekt.\nBitte überprüfen Sie Ihre Eingabe.");
            msgBox.exec_()
        self.berater.street = (self.edtStreet.text()).rstrip()
        self.berater.town = (self.edtTown.text()).rstrip()
        self.berater.zip = (self.edtZip.text()).rstrip()
        self.berater.fee = self.feewidget.returnEntries()
        self.berater.ust = self.ustwidget.returnEntries()
        self.berater.save()
