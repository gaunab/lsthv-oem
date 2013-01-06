#!/usr/bin/python
# -*- coding: utf-8- -*-

import os
import sys
import month
import editmonth

from PyQt4 import QtGui,QtCore,Qt

### monthItem - ListWidgetItem with propability to save month data
class monthItem(QtGui.QListWidgetItem):
    def __init__(self,monat):
	super(monthItem, self).__init__()
	self.monat = monat

    def month(self):
    	return self.monat

class monthList(QtGui.QWidget):
    def __init__(self):
	super(monthList, self).__init__()

	self.monthlist = []
	self.findMonths()
	self.initUI()


    def initUI(self):
	monthnames = [u"Januar",u"Februar",u"März",u"April",u"Mai",u"Juni",u"Juli",u"August",u"September",u"Oktober",u"November",u"Dezember"]
	vbox = QtGui.QVBoxLayout() 		# Main Container

	self.table = QtGui.QListWidget() 		# Table as List of Months
#	table.setColumnCount(1) 		# Only one col
#	table.setHorizontalHeaderLabels([""])
#	table.takeHorizontalHeaderItem(0)
	vbox.addWidget(self.table) 			# Add Table to Window

	for monat in self.monthlist:  		# Add all found months to Table
	    item = monthItem(monat)     	# Create new ListItem with month-data
	    item.setText(monthnames[monat.data['month']-1]+" "+str(monat.data['year'])) # Set Text in TableItem
	    item.setFlags(QtCore.Qt.ItemFlags(33)) 	# Make item selectable but not editable
	    self.table.insertItem(self.table.count()-1,item) # Add Item to table

	btnOpen = QtGui.QPushButton(u"Öffnen")
	vbox.addWidget(btnOpen)

	# Connect Signals to open selected Month
	self.table.doubleClicked.connect(self.openMonth)
	btnOpen.clicked.connect(self.openMonth)

	# Finally show Window
	self.setLayout(vbox)
	self.show()

    #open selected Month - needs table/list as parameter
    def openMonth(self):
	self.monthWin = editmonth.monthWindow(self.table.currentItem().month())

    def findMonths(self):
	fileList = os.listdir(".")  		# list of all Files
	for filename in fileList: 		# iterate through all files
	    if filename.find("monat.yaml") != -1:   # only continue with month-yaml-files
		monat = month.lsthvmonth()
		if (monat.open(filename)): 	# Only append to , if valid month
		    self.monthlist.append(monat)
		else:
		    print "rejecting"+filename


def main():
    app = QtGui.QApplication(sys.argv)
    filelist = monthList()

    sys.exit(app.exec_())

if __name__ == '__main__' :
    main()
