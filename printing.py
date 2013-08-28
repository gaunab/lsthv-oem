from PyQt4 import QtGui,QtCore

# Doing all the rendering





def createPrintOutput(printer,table):
    pages = QtGui.QPainter(printer)
    
    printDev = pages.device;
    pagewidth = printer.pageRect().width()
    pagewidthMM = printer.pageRect(0).width()
    pageheight = printer.pageRect().height()
    pageheightMM = printer.pageRect(0).height()
    
    print "Page :"+str(pagewidth) + " or in mm: " + str(pagewidthMM)
    fontsize =  pages.fontInfo().pixelSize()
    pages.begin(printer)
    # Now let's do the drawing of the Pages
      
    print range(table.rowCount()) 
    y = 0; 				# Set Cursor to first line
    for i in range(table.rowCount()):		# i --> current Row of Table
	print "printing entry" + str(i)
	
	# Fetch data from table
	lfd = str(table.item(i,0).text())
	mtglnr = str(table.item(i,1).text())
	# now print to current row on paper
	pages.drawText(1,y,lfd)
	pages.drawText(1000,y,mtglnr)
	
	y = y + fontsize

	if y > pagewidth - fontsize: ### End of page reached
	    y = 0;
    pages.end()
	
    return pages
