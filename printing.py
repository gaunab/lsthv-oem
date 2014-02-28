#!env python
# -*- coding: utf-8 -*-
from PyQt4 import QtGui,QtCore
import settings
# Doing all the rendering
# http://pyqt.sourceforge.net/Docs/PyQt4/classes.html

class printout:

    def __init__(self,table,window):
    	self.printer = QtGui.QPrinter(QtGui.QPrinter.HighResolution)
	self.table = table
	self.printDialog = QtGui.QPrintDialog(self.printer,window)
        self.data = window.month.data
        self.beraterData = settings.beraterData()                # load beraterdata

	# dialog.exec_()
	# handle the Printing
        self.printer.setPageMargins(20,20,20,20,0)
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
        self.tableCols = [0,20,40,60,80,100,120,140]

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
    # use type=1 for "Mitgliedsbeitragsabrechnung"
    #     type=2 for "Abrechnung der Beratervergütung"
    def heading(self,page,type=0):

	monthnames = [u"Januar",u"Februar",u"März",u"April",u"Mai",u"Juni",u"Juli",u"August",u"September",u"Oktober",u"November",u"Dezember"]
        y = 0
        page.setPen(QtGui.QPen(QtGui.QBrush(2,1),15))     # Set Color to black = 2, with solid pattern = 1, Width to 10px
	page.drawImage(self.pagewidth - self.xmm(60),y - self.ymm(5),QtGui.QImage('logo.jpg').scaledToWidth(self.xmm(60)))
	page.setFont(self.headingFont)
	page.drawText(1,y,'Lohnsteuerhilfeverein')
	y = y + page.fontInfo().pixelSize()
	page.drawText(1,y,u"\u201eOberes Elbtal-Meißen\u201d e.V.")
	y = y +  page.fontInfo().pixelSize()

        page.setFont(self.heading2Font)
        if type==1:
            page.drawText(1,y,u"Mitgliederbeitragsabrechnung")
        if type==2:
            page.drawText(1,y,u"Abrechnung der Beratervergütung")
        
        nextline =   page.fontInfo().pixelSize()
        # Print out the Month and Year
        page.setFont(self.tableFont)
        strmonat = QtCore.QString(monthnames[self.data["month"] -1 ]+" "+str(self.data["year"])) # put Monthname and Year to string
        widthmonat = QtGui.QFontMetrics(self.tableFont,self.printer).width(strmonat)             # determine width of this string
        page.drawText(self.pagewidth - widthmonat,y,strmonat)                                    # Now put this String align right to the right
                                                                                                 # pageborder
        y = y + nextline                                                                         # go on to the next line
        page.drawText(1,y,u"Berater: "+self.beraterData.name+", "+self.beraterData.firstname)
        if type==2:
            page.drawText(self.xmm(90) ,y,u"Beratungsstelle:")
        y = y +  page.fontInfo().pixelSize()
        page.drawText(1,y,u"BSL-Nr.: "+self.beraterData.id)
        if type==2:
            page.drawText(self.xmm(92) ,y,u""+self.beraterData.street)
            y = y +  page.fontInfo().pixelSize()
            page.drawText(self.xmm(92),y,u""+self.beraterData.town)

        y = y + 2 * page.fontInfo().pixelSize()
        
       


	return y

    ###
    # Write Content of a Column
    ###
    def tableCol(self,page,col,y,text):
        page.drawText(self.xmm(self.tableCols[col]),y,text) 
        if col > 0:
            page.drawLine(self.xmm(self.tableCols[col]), y-page.fontInfo().pixelSize(), self.xmm(self.tableCols[col]), y)



    def tableHead(self,page,y):

        
        ## Now there's the real Table-Stuff
        y = y + self.ymm(1)                 # first create some distance to top

        headlines = ['Lfd','Mitgl.Nr.','Name','Vorname','Aufnahme','Bezahlt']
        col = 0
        for headline in headlines:
            self.tableCol(page,col,y,headline)
            col = col + 1

        y = y + self.ymm(1)                 # create some distance to the line
        
        for col in range(0,6):
            self.tableCol(page,col,y,'')

        page.drawLine(self.xmm(0),y,self.xmm(170),y)

        return y

    def evaluationCell(self,page,col,y,text):
        cols = [10,60,110,160]                  # Startposition of cols for evaluationPage
        page.drawLine(self.xmm(cols[col]),y,self.xmm(cols[col+1]),y)
        y = y +  page.fontInfo().pixelSize()
        page.drawText(self.xmm(cols[col]),y,text)
        page.drawLine(self.xmm(cols[col]),y,self.xmm(cols[col+1]),y)

        return y

   

    def create(self):
        print self.data["month"]
        print self.data["year"]

        ### Set Sum's for evaluation-Page to 0 
        aufnahmeges = 0.0
        aufnahmeges_bez = 0.0
        beitragges= 0.0
        beitragges_bez = 0.0

        aufnahme = {}
        beitrag = {}

        # Create Output-Dev
	pages = QtGui.QPainter(self.printer)
	printDev = pages.device;

	# Select font
        pages.setFont(self.tableFont)
	fontsize =  pages.fontInfo().pixelSize()
	pages.begin(self.printer)
	# Now let's do the drawing of the Pages
	
	y = self.heading(pages,type=1) 	# Write Headline
        pages.setFont(self.tableFont)   # set Font
	y = self.tableHead(pages,y) + pages.fontInfo().pixelSize() # Create Tablehead, set Cursor to next line
        print y
	for i in range(self.table.rowCount()):		# i --> current Row of Table
	    # Fetch data from table
	    lfd = str(self.table.item(i,0).text())
	    mtglnr = str(self.table.item(i,1).text())
	    # now print to current row on paper
            for col in range(4):
                self.tableCol(pages,col,y,str(self.table.item(i,col).text()))
	    y = y + fontsize

	    if y > self.pagewidth - fontsize: ### End of page reached
		y = 0;
                y = y + self.tableHead(pages,y)

            ### Now let's calculate everything for evaluation
            aufnahmeges +=  float(self.table.item(i,4).text())
            aufnahmeges_bez +=  float(self.table.item(i,5).text())
            beitragges  +=  float(self.table.item(i,6).text())
            beitragges_bez  +=  float(self.table.item(i,7).text())
            
            # Now Sort per UST
            ust = str(self.table.item(i,8).text())
            if ust in aufnahme:
                aufnahme[ust] += float(self.table.item(i,4).text())
            if ust in beitrag:
                beitrag[ust] += float(self.table.item(i,6).text())
            


        # Now lets print the Final Page
        self.printer.newPage()
        y=self.heading(pages,type=2)
     
        # pages.drawLine(self.xmm(10),y,self.xmm(100),y)
        self.evaluationCell(pages,0,y,u"Gesamtumsatz")
        self.evaluationCell(pages,1,y,unicode(aufnahmeges))

        pages.end()
	   
	return pages
