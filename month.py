#!/usr/bin/python
# -*- coding: utf-8- -*-

import yaml

class lsthvmonth:

    def __init__(self):
	self.data = {}

    def save(self):
	if ("month" in self.data and "year" in self.data):
    	    f_month = open(self.data["month"]+self.data["year"]+".yaml","w")	
    	    yaml.dump(self.data,f_month, default_flow_style=False)
    	    f_month.close()
	    return True
	else:
	    return False	


    def open(self,filename):	
	f_month = open(filename,"r")
	self.data = yaml.load(f_month)
	f_month.close()

