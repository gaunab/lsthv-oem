#!/usr/bin/python
# -*- coding: utf-8- -*-

import yaml
import settings

def strToFloat(input):
    try:
        text = str(input)
        text = text.replace(",",".")
        return float(text)

    except:
        return 0.0
    
class lsthvmonth:

    def __init__(self,beraterdata):
	self.data = {}
        self.berater = beraterdata
        self.ustdec = 0.19

    def evaluation(self):
        beitrag = {}                                                                # list of sums of beitrag one for each ust
        aufnahme = {}                                                               # list of sums of aufnahme one for each ust
        beitragnetto = {}                                                           # see above
        aufnahmenetto = {}                                                          

        aufnahmeges = 0
        aufnahmeges_bez = 0
        beitragges = 0
        beitragges_bez = 0
        misc = 0

        for entry in self.data["table"]:                                            # go through all entries 
            print entry["aufnahmegeb"]
            aufnahmeges += strToFloat(entry["aufnahmegeb"])                         # sum all aufnahmegebuehr
            aufnahmeges_bez += strToFloat(entry["aufnahmepayed"])                   # sum all payed aufnhame
            beitragges += strToFloat(entry["beitrag"])                              # sum all beitraege
            beitragges_bez += strToFloat(entry["beitragpayed"])                     # sum all payed beitraege

            thisUst = strToFloat(entry["ust"])                                      # get ust of current entry

            if thisUst in aufnahme: 
                aufnahme[thisUst] += strToFloat(entry["aufnahmegeb"])               # add aufnhamegebuehr to aufnahme of current ust
            else:
                aufnahme[thisUst] = strToFloat(entry["aufnahmegeb"])                # if this is first aufnhame with this ust - create one

            if thisUst in beitrag:
                beitrag[thisUst] += strToFloat(entry["beitrag"])                    # add beitrag to beitragsum of current ust
            else:
                beitrag[thisUst] = strToFloat(entry["beitrag"])                     # if this is first beitrag with this ust - create one

        for ust in aufnahme:                                                        # now calculate net-sums
            ustdec = ust / 100                                                      # recalculate ust from percentage to decimal value
            beitragnetto[ust] = beitrag[ust] / (1+ustdec)                           # calculate net-sum for beitrag
            aufnahmenetto[ust] = aufnahme[ust] / (1+ustdec)                         # calculate net-sum for aufnahme


        verguetungssatz = strToFloat(self.berater.fee)
        payout = beitragges * (verguetungssatz / 100) + aufnahmeges * (2/3)         # BeraterVerguetung berechnen


        return {"aufnahmeges" : aufnahmeges,
                "aufnahmeges_bez": aufnahmeges_bez,
                "beitragges" : beitragges,
                "beitragges_bez" : beitragges_bez,
                "aufnahme" : aufnahme,
                "beitrag" : beitrag,
                "beitragnetto" : beitragnetto,
                "aufnahmenetto" : aufnahmenetto,
                "payout" : payout,
                "misc": misc}

    def save(self):
	if ("month" in self.data and "year" in self.data):
    	    f_month = open(str(self.data["year"])+"%02i" %(self.data["month"]) +"monat.yaml","w")	
    	    yaml.dump(self.data,f_month, default_flow_style=False)
    	    f_month.close()
	    return True
	else:
	    return False	

    # Determine UST-Value for this month
    def determineUst(self):
        ustList = sorted(self.berater.ust,key=lambda x: x['from'])
        ustList.reverse()
        thismonth = "%4i%2i" %(self.data["year"],self.data["month"])
        ustValue = 17

        for ust in ustList:
            if thismonth >= ust["from"]:
                ustValue = ust["value"]

        
        return ustValue / 100

    def open(self,filename):	
	f_month = open(filename,"r")
	try: 					# Try to load File as YAML
	    self.data = yaml.load(f_month)
	except:
	    return False 			# Not a valid YAML-File
	f_month.close() 
	# Now Check for Data-Structure: month, yeaar, data
	if self.data["month"] and  self.data["year"] :

            self.determineUst()
	    return True
	else: 
	    return False
