#!env python
# -*- coding: utf-8 -*-
from PyQt4 import QtGui,QtCore
import settings
# Doing all the rendering
# http://pyqt.sourceforge.net/Docs/PyQt4/classes.html


###
# Convert a TableCell to FLoat
###
def cellToFloat(cell):
    origText = cell.text().replace(",",".")             # First replace all ,s as they're entered in Germany with .s
    return float(origText)


class tablePainterRow:
    def __init__(self,painter,col):
        self.data = []                                  # List of all fields of this row
        self.col = col
        self.painter = painter

    def append(self,data):
            self.data.append(data)

    def get(self,col):
        print "Row is throwing %s back" %(self.data[col])
        return self.data[col]

    def textWidth(self,col):
       # int QFontMetrics.width (self, QString text, int length = -1)
       return QtGui.QFontMetrics(self.painter.font()).width(self.data[col])

class tablePainter:

    def __init__(self,painter,col):
        self.data= []                                   # List of all Rows
        self.painter = painter                          # Painter to draw on
        self.col = col                                  # Number of cols
        self.colwidth = {}                              # manually set minimum widths 

    # Add a line of data (string)
    def appendRow(self,data):
        print "Create new Row:" 
        row = tablePainterRow(self.painter,self.col)                 # Create a new row
        for i in range(min(len(data),self.col)):        # Add only up to col datas
           row.append(data[i])
           print "  -Add %s" %(data[i])
        self.data.append(row)

    # Set minimum colwidth 
    def setColMinWidth(self,col,width):
        if (type(col) == int and type(width) == int):
            self.colwidth[col] = width
        else:
            raise Exception("Not an Integer")



    # Calculate the Width a Col would need
    def __calcColWidthDemand(self,col): 
        width = 0.0
        for row in self.data:                           # go through all rows
            width = max(row.textWidth(col),width)       # check whether col in current row needs to be wider - set new width

        return width

    def printOut(self,startPoint):

        colwidths = []                                  # find out how wide every col should be
        for row in range(self.col):

            if row in self.colwidth:                    # try to find a manually set min-width for this row
                manualWidth = self.colwidth
            else:
                manualWidth = 0                         # if no min-value was set -> take 0 as min-width

            colwidths.append(max(manualWidth,self.__calcColWidthDemand(row))) # Set width of col

        y = startPoint.y()
        for row in self.data:
            x = startPoint.x()
            for col in range(self.col):                 # go through all elements from this row
                text = row.get(col)                     # fetch Text from Row-Elemen
                print text
                self.painter.drawText(x,y,text)         # draw ElementText on page
                x += colwidths[col]                     # add Width of col to x
                x += 10                                 # add some space

            y += self.painter.fontInfo().pixelSize()    # go to next line

        return QtCore.QPoint(x,y)

class printout:

    def __init__(self,table,window):
    	self.printer = QtGui.QPrinter(QtGui.QPrinter.HighResolution)
	self.table = table
	self.printDialog = QtGui.QPrintDialog(self.printer,window)
        self.data = window.month.data
        self.window = window
        self.beraterData = settings.beraterData()                # load beraterdata

	# dialog.exec_()
	# handle the Printing
        self.printer.setPageMargins(20,20,20,20,0)
	self.pagewidth = self.printer.pageRect().width()
	self.pagewidthMM = self.printer.pageRect(0).width()
	self.pageheight = self.printer.pageRect().height()
	self.pageheightMM = self.printer.pageRect(0).height()

	### Define Fonts
	self.tableFont = QtGui.QFont('Helvetica',10) 		# Normal font
        self.tableHeadFont = QtGui.QFont('Helvetica',12,75)     # Bold font
	self.headingFont = QtGui.QFont('Helvetica',20,75) 	# Big Heading
	self.heading2Font = QtGui.QFont('Helvetica',15,50) 	# Paper Description Font
        
        ### Define Table Columns in mm
        self.tableCols = [0,10,25,55,85,105,125,145,160]

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

        headlines = ['Lfd','Mitgl.Nr.','Name','Vorname','Aufnahme','Bezahlt','Beitrag','Bezahlt','USt']
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

        self.table.drawFrame(pages)
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
	    lfd = str(i)
            self.tableCol(pages,0,y,str(i+1))             # print Entry-Number
	    # now print to current row on paper
            for col in range(8):
                self.tableCol(pages,col+1,y,str(self.table.item(i,col).text())) # print all cols
	    y = y + fontsize

	    if y > self.pagewidth - fontsize: ### End of page reached
		y = 0;
                y = y + self.tableHead(pages,y)
###############
#            ### Now let's calculate everything for evaluation
#            try:
#                aufnahmeges +=  cellToFloat(self.table.item(i,3))
#                aufnahmeges_bez +=  cellToFloat(self.table.item(i,4))
#                beitragges  +=  cellToFloat(self.table.item(i,5))
#                beitragges_bez  += cellToFloat(self.table.item(i,6))
#
#                # Now add Values to matching UST
#                ust = cellToFloat(self.table.item(i,7))
#                 
#                if ust in aufnahme:
#                    aufnahme[ust] += cellToFloat(self.table.item(i,4))
#                else:
#                    aufnahme[ust] = cellToFloat(self.table.item(i,4))
#
#                if ust in beitrag:
#                    beitrag[ust] += cellToFloat(self.table.item(i,5))
#                else:
#                    beitrag[ust] = cellToFloat(self.table.item(i,5))
#            except:
#                QtGui.QMessageBox.warning(self.window,u"Fehler",u"Eintrag %i konnte nicht gelesen werden:\nkein gültiges Zahlenformat" %(i+1))
#            
################            

        # Now lets print the Final Page
        self.printer.newPage()
        y=self.heading(pages,type=2)
     
        y += self.ymm(10)


        evaluationTable = tablePainter(pages,4)
        
        evaluation = self.window.month.evaluation()
        
        tableRow = [u"Gesamtumsatz",
                    u"%0.2f€" %(evaluation["aufnahmeges"] + evaluation["beitragges"]),
                    "",
                    ""]
        evaluationTable.appendRow(tableRow)
        evaluationTable.appendRow([u"direkt bezahlte",u"%0.2f€" %(evaluation["aufnahmeges_bez"] + evaluation["beitragges_bez"]) , "", ""])
        for ust in evaluation["aufnahme"]: # Draw the following lines for all appearing USTs
            ustdec = ust / 100
            beitragnetto = beitrag[ust] / (1+ustdec)
            aufnahmenetto = aufnahme[ust] / (1+ustdec)
            evaluationTable.appendRow(["","","Nettobetrag","Umsatzsteuer (%0.2f)" %(ust)])
            evaluationTable.appendRow([u"Mitgliedsbeiträge",u"%0.2f€" %(evaluation["beitrag"][ust]), 
                                       u"%0.2f€" %(evaluation["beitragnetto"][ust]),
                                       u"%0.2f€" %(evaluation["beitragnetto"][ust]*ustdec)  ])
            evaluationTable.appendRow([u"Aufnahmegebühren",u"%0.2f€" %(evaluation["aufnahme"][ust]), 
                                       u"%0.2f€" %(evaluation["aufnahmenetto"][ust]) ,
                                       u"%0.2f€" %(evaluation["aufnahmenetto"][ust]*ustdec) ])

            evaluationTable.appendRow([u"Vergütung Berater",u"%0.2f€" %(evaluation["payout"]),
                                       u"%0.2f€" %(evaluation["payout"] / (1+ month.ustdec)),
                                       u"%0.2f€" %(evaluation["payout"] - evaluation["payout"] / (1+ month.ustdec)) ])
        evaluationTable.printOut(QtCore.QPoint(1,y))



        # pages.drawLine(self.xmm(10),y,self.xmm(100),y)
      #  self.evaluationCell(pages,0,y,u"Gesamtumsatz")
      #  outstr = u"%0.2f €" %(aufnahmeges + beitragges)
      #  self.evaluationCell(pages,1,y,outstr) 

	y += fontsize + self.ymm(1)
       # self.evaluationCell(pages,0,y,u"direkt bezahlte")
       # outstr = u"%0.2f €" %(aufnahmeges_bez + beitragges_bez)
       # self.evaluationCell(pages,1,y,outstr) 



        pages.end()
	   
	return pages


