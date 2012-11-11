import yaml

class beraterData:

    def __init__(self):
    	# Open the Settings-File
    	f_settings = open ("settings.yaml")
	
	data = yaml.load(f_settings)
	
	self.name = data["name"]
	self.firstname = data["firstname"]
	self.id = data["id"]
	# Bank-Connection
	self.bank = data["bank"]
	self.bankid = data["bankid"]
	self.deposit = data["deposit"]
	# Contact / Adress
	self.street = data["street"]
	self.town = data["town"]
	# governmental things
	self.ustnr = data["ustnr"]

    	f_settings.close()

    def save(self):
	data={}
	data["name"] = self.name
	data["firstname"] = self.firstname
	data["id"] = self.id
	data["bank"] = self.bank

	f_settings = open("settings.yaml","w")
	yaml.dump(data, f_settings)
	f_settings.close()


berater = beraterData()
print berater.name
