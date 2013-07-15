from PyQt4 import QtGui,QtCore

# Doing all the rendering



def createPrintOutput(printer,table):
    pages = QtGui.QPainter(printer)
    
    print "Painter-Device: "
    printDev = pages.device;
    print printer.pageRect().width()
    
    pages.begin(printer)
    # Now let's do the drawing of the Pages
  
    ### Head of each page
    pages.drawText(1,30,"Hallo")

    pages.drawText(100,40,"Hallo Du")


    pages.end()
    
    return pages
