import yaml
import os.path

# Settings and personal Data are stored in settings.yaml

class beraterData:

    def __init__(self):
        
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
	# Contact / Adress
	self.street = (data["street"] if "street" in data else "")
	self.town = (data["town"] if "town" in data else "")
	# governmental things
	self.ustnr = (data["ustnr"] if "ustnr" in data else "")
	self.zip = (data["zip"] if "zip" in data else "")
        self.ust = data["ust"]


        if (len(self.iban) > 0):
            if (self.checkiban()):
                print "IBAN correct"
            else:
                print "IBAN incorrect"

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

	f_settings = open("settings.yaml","w")
	yaml.dump(data, f_settings ,default_flow_style=False)
	f_settings.close()


