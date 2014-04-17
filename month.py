#!/usr/bin/python
# -*- coding: utf-8- -*-

import yaml

class lsthvmonth:

    def __init__(self):
	self.data = {}

    def save(self):
	if ("month" in self.data and "year" in self.data):
    	    f_month = open(str(self.data["year"])+"%02i" %(self.data["month"]) +"monat.yaml","w")	
    	    yaml.dump(self.data,f_month, default_flow_style=False)
    	    f_month.close()
	    return True
	else:
	    return False	


    def open(self,filename):	
	f_month = open(filename,"r")
	try: 					# Try to load File as YAML
	    self.data = yaml.load(f_month)
	except:
	    return False 			# Not a valid YAML-File
	f_month.close() 
	# Now Check for Data-Structure: month, yeaar, data
	if self.data["month"] and  self.data["year"] :
	    return True
	else: 
	    return False
