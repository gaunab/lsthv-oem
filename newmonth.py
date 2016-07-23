#!/usr/bin/python
# -*- coding: utf-8- -*-

import os
import sys
import month
import editmonth,settings
import time
from datetime import date
from PyQt4 import QtGui,QtCore,Qt


class newMonth(QtGui.QWidget):
    def __init__(self,beraterdata):
        super(newMonth,self).__init__()
        self.beraterdata=beraterdata
        self.initUI()

    def initUI(self):
        monthnames = [u"Januar",u"Februar",u"März",u"April",u"Mai",u"Juni",u"Juli",u"August",u"September",u"Oktober",u"November",u"Dezember"]
        grid = QtGui.QGridLayout()                                 # Main Container

        self.monthselector = QtGui.QComboBox()                         # ComboBox as List of Months
        grid.addWidget(self.monthselector,0,1)                         # Add Table to Window
        grid.addWidget(QtGui.QLabel("Monat:"),0,0)
        
        i = 0
        for monat in monthnames:                  # Add all found months to Table
            self.monthselector.insertItem(i,monat) # Add Item to table
            i += 1

        self.edtyear = QtGui.QSpinBox()
        grid.addWidget(self.edtyear,1,1)
        grid.addWidget(QtGui.QLabel("Jahr:"),1,0)
        self.edtyear.setMinimum(2010)
        self.edtyear.setMaximum(2050)

        btnOpen = QtGui.QPushButton(u"Monat anlegen")
        grid.addWidget(btnOpen,2,0,1,2)
        # Connect Signals to open selected Month
        #self.table.doubleClicked.connect(self.openMonth)
        btnOpen.clicked.connect(self.createMonth)

        # Preselect Month and year
        
        lastmonth = date.fromtimestamp(time.time() - (30 * 24 * 60 * 60))
        self.edtyear.setValue(lastmonth.year)
        self.monthselector.setCurrentIndex(lastmonth.month-1)

        # Finally show Window

        self.setLayout(grid)
        self.show()

    def createMonth(self):
        monat = month.lsthvmonth(self.beraterdata)                    # create new Month-Object
        monat.data["month"] =  self.monthselector.currentIndex()+1    # examine Month-Number from ComboBox
        monat.data["year"] = self.edtyear.value()                     # examine year from SpinBox
        monat.determineFee() 
        self.monthWin = editmonth.monthWindow(self.beraterdata,monat) # open new Month in editmonth-Window
        self.close()

def main():
    app = QtGui.QApplication(sys.argv)
    monthcreate = newMonth()

    sys.exit(app.exec_())

if __name__ == '__main__' :
    main()
