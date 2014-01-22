#!env python
# -*- coding: utf-8 -*-
from PyQt4 import QtGui,QtCore

# Doing all the rendering


class printout:

    def __init__(self,table,window):
    	self.printer = QtGui.QPrinter(QtGui.QPrinter.HighResolution)
	self.table = table
	self.printDialog = QtGui.QPrintDialog(self.printer,window)

	# dialog.exec_()
	# handle the Printing   

	self.pagewidth = self.printer.pageRect().width()
	self.pagewidthMM = self.printer.pageRect(0).width()
	self.pageheight = self.printer.pageRect().height()
	self.pageheightMM = self.printer.pageRect(0).height()

	### Define Fonts
	self.tableFont = QtGui.QFont('Helvetica',12) 		# Normal font
        self.tableHeadFont = QtGui.QFont('Helvetica',12,75)     # Bold font
	self.headingFont = QtGui.QFont('Helvetica',20,75) 	# Big Heading
	self.heading2Font = QtGui.QFont('Helvetica',15,50) 	# Paper Description Font


    # Calculate from mm to px
    def xmm(self,xpos):
	return int(( xpos * self.pagewidth ) / self.pagewidthMM)

    def ymm(self,ypos):
	return int(( ypos * self.pageheight ) / self.pageheightMM)


    # Show Printer selection dialog, do the printing if everything is fine 
    def dialog(self):
	if self.printDialog.exec_() == QtGui.QDialog.Accepted:
	    self.create()
	
    # create the printing-content and send it to the printer

    def heading(self,page):
	y = self.ymm(10)
	page.drawImage(self.pagewidth - self.xmm(70),y - self.ymm(5),QtGui.QImage('logo.jpg').scaledToWidth(self.xmm(60)))
	page.setFont(self.headingFont)
	page.drawText(1,y,'Lohnsteuerhilfeverein')
	y = y + page.fontInfo().pixelSize()
	page.drawText(1,y,u"\u201eOberes Elbtal-Meißen\u201d e.V.")
	y = y + 2 * page.fontInfo().pixelSize()



	

	return y


    def create(self):
	pages = QtGui.QPainter(self.printer)
	
	printDev = pages.device;

	# Select font
        pages.setFont(self.tableFont)
	fontsize =  pages.fontInfo().pixelSize()
	pages.begin(self.printer)
	# Now let's do the drawing of the Pages
	  
	y = 0; 				# Set Cursor to first line
	y = y + self.heading(pages) 	# Write Headline
        pages.setFont(self.tableFont)   # set Font
	
	for i in range(self.table.rowCount()):		# i --> current Row of Table
	    print "printing entry" + str(i)
	    
	    # Fetch data from table
	    lfd = str(self.table.item(i,0).text())
	    mtglnr = str(self.table.item(i,1).text())
	    # now print to current row on paper
	    pages.drawText(1,y,lfd)
	    pages.drawText(self.xmm(20),y,mtglnr)
	    
	    y = y + fontsize

	    if y > self.pagewidth - fontsize: ### End of page reached
		y = 0;
	pages.end()
	    
	return pages
