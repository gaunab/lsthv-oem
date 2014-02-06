#!env python
# -*- coding: utf-8 -*-
from PyQt4 import QtGui,QtCore

# Doing all the rendering
# http://pyqt.sourceforge.net/Docs/PyQt4/classes.html

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
        
        ### Define Table Columns in mm
        self.tableCols = [10,20,40,60,80,100,120,140]

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
        page.setPen(QtGui.QPen(QtGui.QBrush(2,1),15))     # Set Color to black = 2, with solid pattern = 1, Width to 10px
	y = self.ymm(10)
	page.drawImage(self.pagewidth - self.xmm(70),y - self.ymm(5),QtGui.QImage('logo.jpg').scaledToWidth(self.xmm(60)))
	page.setFont(self.headingFont)
	page.drawText(1,y,'Lohnsteuerhilfeverein')
	y = y + page.fontInfo().pixelSize()
	page.drawText(1,y,u"\u201eOberes Elbtal-Meißen\u201d e.V.")
	y = y + 2 * page.fontInfo().pixelSize()
	return y

    ###
    # Write Content of a Column
    ###
    def tableCol(self,page,col,y,text):
        print text
        print y 
        page.drawText(self.xmm(self.tableCols[col]),y,text) 
        if col > 0:
            page.drawLine(self.xmm(self.tableCols[col]), y-page.fontInfo().pixelSize(), self.xmm(self.tableCols[col]), y)



    def tableHead(self,page,y):
        y = y + self.ymm(1)                 # first create some distance to top

        headlines = ['Lfd','Mitgl.Nr.','Name','Vorname','Aufnahme','Bezahlt']
        col = 0
        for headline in headlines:
            self.tableCol(page,col,y,headline)
            col = col + 1

        y = y + self.ymm(1)                 # create some distance to the line
        
        for col in range(0,6):
            self.tableCol(page,col,y,'')

        page.drawLine(self.xmm(10),y,self.xmm(190),y)

        return y



    def create(self):
	pages = QtGui.QPainter(self.printer)
	
	printDev = pages.device;

	# Select font
        pages.setFont(self.tableFont)
	fontsize =  pages.fontInfo().pixelSize()
	pages.begin(self.printer)
	# Now let's do the drawing of the Pages
	  
	y = self.heading(pages) 	# Write Headline
        pages.setFont(self.tableFont)   # set Font
	y = self.tableHead(pages,y) + pages.fontInfo().pixelSize() # Create Tablehead, set Cursor to next line
        print y
	for i in range(self.table.rowCount()):		# i --> current Row of Table
	    # Fetch data from table
	    lfd = str(self.table.item(i,0).text())
	    mtglnr = str(self.table.item(i,1).text())
	    # now print to current row on paper
	    self.tableCol(pages,0,y,lfd)
	    self.tableCol(pages,1,y,mtglnr)

	    y = y + fontsize

	    if y > self.pagewidth - fontsize: ### End of page reached
		y = 0;
                y = y + self.tableHead(pages,y)

	pages.end()
	    
	return pages
