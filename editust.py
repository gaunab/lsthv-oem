#!/usr/bin/python
# -*- coding: utf-8- -*-

from PyQt4 import QtGui

class ustWidget(QtGui.QWidget):
    def __init__(self,ust):
	super(prefWindow, self).__init__()
	self.ust = ust
	self.initUI()

    def initUI(self):
        
        lblDesc = QtGui.QLabel(u"Umsatzsteuer")
        grid = QtGui.QGridLayout()
        grid.addWidget(lblDesc,1,1)

        self.setLayout(gird)


