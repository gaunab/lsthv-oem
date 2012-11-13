import yaml


# Settings and personal Data are stored in settings.yaml

class beraterData:

    def __init__(self):
    	# Open the Settings-File
    	f_settings = open ("settings.yaml")
	
	data = yaml.load(f_settings)
	
	### Read all Fields from settings.yaml ###

	self.name = (data["name"] if "name" in data else "")
	self.firstname = (data["firstname"] if "firstname" in data else "")
	self.id = (data["id"] if "id" in data else "")
	# Bank-Connection
	self.bank = (data["bank"] if "bank" in data else "")
	self.bankid = (data["bankid"] if "bankid" in data else "")
	self.deposit = (data["deposit"] if "deposit" in data else "")
	# Contact / Adress
	self.street = (data["street"] if "street" in data else "")
	self.town = (data["town"] if "town" in data else "")
	# governmental things
	self.ustnr = (data["ustnr"] if "ustnr" in data else "")

    	f_settings.close()

    def save(self):
	data={}
	data["name"] = self.name
	data["firstname"] = self.firstname
	data["id"] = self.id
	data["bank"] = self.bank
	data["bankid"] = self.bankid
	data["deposit"] = self.deposit
	data["street"] = self.street
	data["town"] = self.town
	data["ustnr"] = self.ustnr

	f_settings = open("settings.yaml","w")
	yaml.dump(data, f_settings ,default_flow_style=False)
	f_settings.close()


