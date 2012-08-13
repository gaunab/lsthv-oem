#!/usr/bin/python
# -*- coding: utf-8- -*-

from PyQt4 import QtGui

class prefWindow(QtGui.QWidget):
    def __init__(self):
	super(prefWindow, self).__init__()

	self.initUI()

    def initUI(self):
	self.setWindowTitle(u"Beraterdaten")

	grid = QtGui.QGridLayout() 		# Main Container

	edtName = QtGui.QLineEdit()
	lblName = QtGui.QLabel(u"Name")
	edtFirstName = QtGui.QLineEdit()
	lblFirstName = QtGui.QLabel(u"Vorname")
	grid.addWidget(edtName,0,1)
	grid.addWidget(lblName,0,0)
	grid.addWidget(edtFirstName,1,1)
	grid.addWidget(lblFirstName,1,0)
	self.setLayout(grid) 			# Grid for Layout
	self.show()

