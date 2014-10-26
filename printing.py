#!env python
# -*- coding: utf-8 -*-
from PyQt4 import QtGui,QtCore
import settings
import time
# Doing all the rendering
# http://pyqt.sourceforge.net/Docs/PyQt4/classes.html


###
# Convert a TableCell to FLoat
###
def cellToFloat(cell):
    origText = cell.text().replace(",",".")             # First replace all ,s as they're entered in Germany with .s
    return float(origText)

# Class for Cells in TablePainter
class tablePainterCell:
    def __init__(self,text,border={},align='none'):
        self.text = text
        self.border = border
	self.align=align

    def setPainter(self,painter):
        self.painter = painter

    def getBorders(self,key):
        if key in self.border:
            return self.border[key]
        else:
            return False
    def setBorders(self,key,value):
        self.border[key] = value

    def getText(self):
        return self.text

    def setText(self,text):
        self.text = text

    def textWidth(self):
       # int QFontMetrics.width (self, QString text, int length = -1)
       return QtGui.QFontMetrics(self.painter.font()).width(self.text)

    def getAlign(self):
	return self.align

    def setAlign(self,align):
	if (align in ['none','left','right','center']):
	    self.align=align
	    return True
	else:
	    return False

class tablePainterRow:
    def __init__(self,painter,col,border={}):
        self.data = []                                  # List of all cells of this row
        self.col = col
        self.painter = painter
        self.borders = border


    def append(self,data):
            self.data.append(data)

    def get(self,col):
        # print "Row is throwing %s back" %(self.data[col])
	return self.data[col]

    def setBorders(self,key,value):
        self.borders[key] = value

    def getBorders(self,key):
        if key in self.borders:
            return self.borders[key]
        else:
            return False


class tablePainter:

    def __init__(self,painter,col):
        self.data= []                                   # List of all Rows
        self.painter = painter                          # Painter to draw on
        self.col = col                                  # Number of cols
        self.colwidth = {}                              # manually set minimum widths 
	self.align= ['left' for x in range(col)]
	
    # Add a line of data (string)
    def appendRow(self,data,borders={}):
        row = tablePainterRow(self.painter,self.col,borders)    # Create a new row
        for i in range(min(len(data),self.col)):        # Add only up to col datas
           row.append(data[i])
        self.data.append(row)

    # Set minimum colwidth 
    def setColMinWidth(self,col,width):
        if (type(col) == int and type(width) == int):
            self.colwidth[col] = width
        else:
            raise Exception("Not an Integer")

    #set Text-Align for Col
    def setColAlign(self,col,align):
	if align in ['left','right','center']:
	    self.align[col] = align
	    return True
	else:
	    return False

    # Calculate the Width a Col would need
    def __calcColWidthDemand(self,col): 
        width = 0.0
        for row in self.data:                           # go through all rows
            cell = row.get(col)
            cell.setPainter(self.painter)
            width = max(cell.textWidth(),width)       # check whether col in current row needs to be wider - set new width

        return width

    def printOut(self,startPoint):

        colwidths = []                                  # find out how wide every col should be
        for col in range(self.col):

            if col in self.colwidth:                    # try to find a manually set min-width for this row
                manualWidth = self.colwidth[col]
            else:
                manualWidth = 0                         # if no min-value was set -> take 0 as min-width
            colwidths.append(max(manualWidth,self.__calcColWidthDemand(col))) # Set width of col

        y = startPoint.y()
	lineheight = self.painter.fontInfo().pixelSize() 
        for row in self.data:
            x = startPoint.x()
            for col in range(self.col):                 # go through all elements from this row
                text = row.get(col).getText()                     # fetch Text from Row-Elemen
		# Now draw line on the left side:
		if  row.get(col).getBorders('left'):
		    self.painter.drawLine(x,y,x,y-lineheight)
		if  row.get(col).getBorders('top'):
		    self.painter.drawLine(x,y-lineheight,x+colwidths[col],y-lineheight)
		if  row.get(col).getBorders('right'):
		    self.painter.drawLine(x+colwidths[col],y-lineheight,x+colwidths[col],y)
		if  row.get(col).getBorders('bottom'):
		    self.painter.drawLine(x,y,x+colwidths[col],y)

		align = row.get(col).getAlign() 
		if (align == 'none'):
		    align = self.align[col] 
		if (align == 'left'):
		    textx = x
		if (align == 'right'):
		    textx = x + colwidths[col] - row.get(col).textWidth()
		if (align == 'center'):
		    textx = x + int(colwidths[col] / 2) - int(row.get(col).textWidth() / 2)
                self.painter.drawText(textx,y,text)         # draw ElementText on page
                x += colwidths[col]                     # add Width of col to x
                x += 10                                 # add some space

            if row.getBorders('top'):
                self.painter.drawLine(startPoint.x(),y - self.painter.fontInfo().pixelSize()  ,x,y- self.painter.fontInfo().pixelSize()  ) # Draw line below row
            if row.getBorders('bottom'):
                self.painter.drawLine(startPoint.x(),y,x,y) # Draw line below row

            y += self.painter.fontInfo().pixelSize()    # go to next line





        return QtCore.QPoint(x,y)

class printout:

    def __init__(self,table,window,printer):
    	self.printer = printer
	self.table = table
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
	self.tableFont = QtGui.QFont('Arial',10) 		# Normal font
        self.tableHeadFont = QtGui.QFont('Arial',12,75)     # Bold font
	self.headingFont = QtGui.QFont('Arial',20,75) 	# Big Heading
	self.heading2Font = QtGui.QFont('Arial',15,50) 	# Paper Description Font
        
        ### Define Table Columns in mm
        self.tableCols = [0,10,25,55,85,105,125,145,160]

    # Calculate from mm to px
    def xmm(self,xpos):
	return int(( xpos * self.pagewidth ) / self.pagewidthMM)

    def ymm(self,ypos):
	return int(( ypos * self.pageheight ) / self.pageheightMM)


	
    # create the printing-content and send it to the printer
    # use type=1 for "Mitgliedsbeitragsabrechnung"
    #     type=2 for "Abrechnung der Beratervergütung"
    def heading(self,page,type=0):

	monthnames = [u"Januar",u"Februar",u"März",u"April",u"Mai",u"Juni",u"Juli",u"August",u"September",u"Oktober",u"November",u"Dezember"]
        y = 0
        page.setPen(QtGui.QPen(QtGui.QBrush(2,1),15))     # Set Color to black = 2, with solid pattern = 1, Width to 10px
	page.drawImage(self.pagewidth - self.xmm(60),y - self.ymm(5),QtGui.QImage("./logo.png","png").scaledToWidth(self.xmm(60)))
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
        page.drawText(1,y,u"Steuernummer: "+self.beraterData.ustnr)
        if type==2:
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
        
	tableRow = [tablePainterCell(u"Gesamtumsatz",{'left':True,'top':True}),
		tablePainterCell(u"%0.2f€ " %(evaluation["aufnahmeges"] + evaluation["beitragges"]),{'top':True,'right':True},align='right'),
                    tablePainterCell(""),
                    tablePainterCell(""),
		    ]
        evaluationTable.appendRow(tableRow)
	evaluationTable.appendRow([tablePainterCell(u"direkt bezahlte",{'left':True,}),
	    tablePainterCell(u"%0.2f€ " %(evaluation["aufnahmeges_bez"] + evaluation["beitragges_bez"]),{'right':True},align='right' ), 
                                   tablePainterCell(""), 
                                   tablePainterCell("")])
        for ust in evaluation["aufnahme"]: # Draw the following lines for all appearing USTs
            ustdec = ust / 100
            #beitragnetto = beitrag[ust] / (1+ustdec)
            #aufnahmenetto = aufnahme[ust] / (1+ustdec)
#	    evaluationTable.setColMinWidth(0,100)
	    evaluationTable.setColMinWidth(1,self.xmm(30))
	    evaluationTable.setColMinWidth(2,self.xmm(30))
	    evaluationTable.setColMinWidth(3,self.xmm(30))
#	    evaluationTable.setColMinWidth(2,100)
	    evaluationTable.appendRow([tablePainterCell("",{'left':True}),
                                       tablePainterCell(""),
				       tablePainterCell("Nettobetrag",align='center'),
				       tablePainterCell("Umsatzsteuer (%0.0f%%)" %(ust),{'right':True},align='center')],{'top':True})
	    evaluationTable.appendRow([tablePainterCell(u"Mitgliedsbeiträge",{'left':True}),
                                       tablePainterCell(u"%0.2f€ " %(evaluation["beitrag"][ust]),align='right'), 
                                       tablePainterCell(u"%0.2f€ " %(evaluation["beitragnetto"][ust]),align='right'),
				       tablePainterCell(u"%0.2f€ " %(evaluation["beitragnetto"][ust]*ustdec),{'right':True},align='right')  ])
	    evaluationTable.appendRow([tablePainterCell(u"Aufnahmegebühren",{'left':True}),
                                       tablePainterCell(u"%0.2f€ " %(evaluation["aufnahme"][ust]),align='right'), 
                                       tablePainterCell(u"%0.2f€ " %(evaluation["aufnahmenetto"][ust]),align='right') ,
				       tablePainterCell(u"%0.2f€ " %(evaluation["aufnahmenetto"][ust]*ustdec),{'right':True},align='right') ])
	    evaluationTable.appendRow([tablePainterCell(u"Vergütung Berater",{'left':True}),
                                       tablePainterCell(u"%0.2f€ " %(evaluation["payout"]),align='right'),
                                       tablePainterCell(u"%0.2f€ " %(evaluation["payout"] / (1+ self.window.month.ustdec)),align='right'),
				       tablePainterCell(u"%0.2f€ " %(evaluation["payout"] - evaluation["payout"] / (1+ self.window.month.ustdec)),{'right':True},align='right') ])

        
        evaluationTable.appendRow([tablePainterCell(u"sonstige vereinnahmte Beträge",{'left':True}),
                                   tablePainterCell(u"%0.2f€ " %(evaluation["misc"]),{'right':True},align='right'),
                                   tablePainterCell(""),
                                   tablePainterCell("")],
                                  {"top":True})
        if evaluation["payout"] >= 0:
	    evaluationTable.appendRow([tablePainterCell(u"vom Verein zu zahlen",{'left':True,'bottom':True}),
		tablePainterCell(u"%0.2f€ " %(evaluation["payout"]),{'right':True,'bottom':True},align='right'),
                                       tablePainterCell(""),
                                       tablePainterCell("")])
        else:
	    evaluationTable.appendRow([tablePainterCell(u"an Verein zu zahlen",{'left':True,'bottom':True}),
		tablePainterCell(u"%0.2f€ " %(-evaluation["payout"]),{'right':True,'bottom':True},align='right'),
                                       tablePainterCell(""),
                                       tablePainterCell("")])

        y = evaluationTable.printOut(QtCore.QPoint(1,y)).y()



        # pages.drawLine(self.xmm(10),y,self.xmm(100),y)
      #  self.evaluationCell(pages,0,y,u"Gesamtumsatz")
      #  outstr = u"%0.2f €" %(aufnahmeges + beitragges)
      #  self.evaluationCell(pages,1,y,outstr) 

	y += fontsize + self.ymm(1)
       # self.evaluationCell(pages,0,y,u"direkt bezahlte")
       # outstr = u"%0.2f €" %(aufnahmeges_bez + beitragges_bez)
       # self.evaluationCell(pages,1,y,outstr) 
        pages.drawText(self.xmm(self.tableCols[0]),y,u"Die Vergütungsabrechnung gilt als angenommen, wenn der Vorstand nicht binnen eines Monats") 
	y += fontsize + self.ymm(1)
        pages.drawText(self.xmm(self.tableCols[0]),y,u"nach Eingang schriftlich widerspricht.") 
        y += fontsize + self.ymm(10)

        if evaluation["payout"] >= 0:
            pages.drawText(self.xmm(self.tableCols[0]),y,u"Mein Guthaben bitte ich auf mein Konto bei %s" %(self.beraterData.bank)) 
            y += fontsize + self.ymm(1)
            pages.drawText(self.xmm(self.tableCols[0]),y,u" BIC: %s; IBAN: %s; zu überweisen" %(self.beraterData.bic,self.beraterData.iban)) 
        else:
            pages.drawText(self.xmm(self.tableCols[0]),y,u"Den Betrag zugunsten des Vereins habe ich heute vertragsgemäß auf das Konto des Vereins bei") 
            y += fontsize + self.ymm(1)
            pages.drawText(self.xmm(self.tableCols[0]),y,u"Sparkasse Meißen; BIC: SOLADES1MEI; IBAN: DE03850550003000007007; überwiesen") 

        y += fontsize + self.ymm(30)

        pages.drawText(self.xmm(self.tableCols[0]),y,u"Datum: %s   Unterschrift des Beraters: ..............................................." %(time.strftime("%d.%m.%Y")) ) 
        y +=  self.ymm(1)

        pages.drawLine(self.xmm(0),y,self.xmm(170),y)

        pages.end()
	   
	return pages


