# -*- coding: utf-8- -*-
import yaml
import os.path
from PyQt4 import QtGui,QtCore,Qt
# Settings and personal Data are stored in settings.yaml

class beraterData:

    def __init__(self):
        
        self.checkPath()
            # Open the Settings-File
        if (os.path.isfile("settings.yaml")):
            f_settings = open ("settings.yaml")
            data = yaml.load(f_settings)
            f_settings.close()
            self.saved= True
        else:
            data = yaml.load("saved: false")
            self.saved = False

        ### Read all Fields from settings.yaml ###
        self.name = (data["name"] if "name" in data else "")
        self.firstname = (data["firstname"] if "firstname" in data else "")
        self.id = (data["id"] if "id" in data else "")
        # Bank-Connection
        self.bank = (data["bank"] if "bank" in data else "")
        self.bic = (data["bic"] if "bic" in data else "")
        self.iban = (data["iban"] if "iban" in data else "")
        # Contact / Address
        self.street = (data["street"] if "street" in data else "")
        self.town = (data["town"] if "town" in data else "")
        # governmental things
        self.ustnr = (data["ustnr"] if "ustnr" in data else "")
        self.zip = (data["zip"] if "zip" in data else "")
        self.fee = (data["fee"] if "fee" in data else "")
        self.ust = (data["ust"] if "ust" in data else [])
        

#        if (len(self.iban) > 0):
#            if (self.checkiban()):
#                print "IBAN correct"
#            else:
#                print "IBAN incorrect"

        if (len(self.ust) == 0):
            self.ust.append({"from": "200701",  "value": 19})

    def checkiban(self):
        if (len(self.iban) < 20):
            return False

        try:
            iban = self.iban.upper()                                                # Make Sure all Letters are Capitals
            country = str(ord(iban[0])-55) + str(ord(iban[1])-55)                   # Every Letter gets a Value beginning with 10 for A
            checksum = iban[2] + iban[3]                                            # Fetch Checksum
            bban = iban[4:]                                                         # Fetch bban
        except ValueError:
            return False
        
        if (int(bban + country + checksum) % 97 == 1 ):                              # Now put everything together and check if modulo 97 is 1
            return True
        else:
            return False

    def save(self):
        data={}
        data["name"] = self.name
        data["firstname"] = self.firstname
        data["id"] = self.id
        data["bank"] = self.bank
        data["bic"] = self.bic
        data["iban"] = self.iban
        data["street"] = self.street
        data["town"] = self.town
        data["ustnr"] = self.ustnr
        data["zip"] = self.zip
        data["ust"] = self.ust
        data["fee"] = self.fee

        f_settings = open("settings.yaml","w")
        yaml.dump(data, f_settings ,default_flow_style=False)
        f_settings.close()

    # Check Config Path, create it if needed, set variable
    def checkPath(self):
        self.path = '.'
        if (os.name == 'posix') :               
            self.path = ("%s/.beraterdata") %(os.getenv('HOME'))

        if (os.name == 'nt'):
            self.path = ("%s\\beraterdata") %(os.getenv('APPDATA'))
        
        if ( not os.path.isdir(self.path)):
            try:
                os.makedirs(self.path)
            except OSError:
#                print "Could not create AppDir"
                msgbox = QtGui.QMessageBox("Fehler",u" Das Arbeitsverzeichnis konnte nicht erstellt werden. Bitte Prüfen Sie, ob das Verzeichnis %s bereits existiert." %(self.path),QtGui.QMessageBox.Critical,QtGui.QMessageBox.Ok,0,0)
                msgbox.show()
                msgbox.exec_()
                return False
        os.chdir(self.path)
        return True
        

    def getPath(self):
        return self.path
