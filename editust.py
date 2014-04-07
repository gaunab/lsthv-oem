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
        grid = QtGui.QGridLayout()
        grid.addWidget(lblDesc,0,0)
        

        self.setLayout(grid)


