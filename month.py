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
    """ Store all Data of a single month
    
    All Data is stored in field self.data. All single entries are stored in
    date["table"] while additional incomes are stored in ["misc_income"]

    
    """

    def __init__(self,beraterdata):
        """ Create a new lsthvmonth instance 

        Parameters
        ----------

        beraterdata: beraterData 
            Give personal Information like fee and ust for calculations within this month
        
        """
        self.data = {}
        self.berater = beraterdata
        self.ustdec = 0.19
        self.fee = 0.0

    def evaluation(self):
        """ Calculate everything for Evaluation sheet
        
        Returns:
        --------
        list with calculated data. Following keys are used:
           "aufnahmeges" : Summe aller Aufnahmegebühren 
           "aufnahmeges_bez" : Summer der Bezahlten Aufnahmegebühren
           "beitragges" : Summe aller Beiträge
           "beitragges_bez" : Summe der gezahlten Beiträge
           "aufnahme" : 
           "beitrag" _:
           "beitragnetto"   
           "aufnahmenetto" 
           "payout" : Was der Berater ausgezahlt bekommt
           "societypayment" : Was an den Verein bezahlt wird
           "misc": sonstige Beiträge, die eingenommen wurden
        """
        beitrag = {}                                                                # list of sums of beitrag one for each ust
        aufnahme = {}                                                               # list of sums of aufnahme one for each ust
        beitragnetto = {}                                                           # see above
        aufnahmenetto = {}                                                          

        aufnahmeges = 0
        aufnahmeges_bez = 0
        beitragges = 0
        beitragges_bez = 0
        misc = self.miscSum()
        
        if ("table" in self.data):
            for entry in self.data["table"]:                                            # go through all entries 
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

        
        verguetungssatz = strToFloat(self.fee)
        payout = (beitragges * (verguetungssatz)) + (aufnahmeges * (2.0/3.0))      # BeraterVerguetung berechnen
        societypayment = payout - (beitragges + aufnahmeges - beitragges_bez - aufnahmeges_bez )
        print(societypayment)

        return {"aufnahmeges" : aufnahmeges,
                "aufnahmeges_bez": aufnahmeges_bez,
                "beitragges" : beitragges,
                "beitragges_bez" : beitragges_bez,
                "aufnahme" : aufnahme,
                "beitrag" : beitrag,
                "beitragnetto" : beitragnetto,
                "aufnahmenetto" : aufnahmenetto,
                "payout" : payout,
                "societypayment": societypayment,
                "misc": misc}

    def save(self):
        if ("month" in self.data and "year" in self.data):
            f_month = open(str(self.data["year"])+"%02i" %(self.data["month"]) +"monat.yaml","w")        
            yaml.safe_dump(self.data,f_month, default_flow_style=False, encoding='utf-8', tags=False)
            f_month.close()
            return True
        else:
            return False        

    def miscSum(self):
        """ Caclculate Sum of misc """
        sum = 0.0
        if self.data.has_key("misc"):
            for entry in self.data["misc"]:
                sum += strToFloat(entry["value"])
        return sum

    def determineUst(self):
        """ Determine UST-Value for this month """
        ustList = sorted(self.berater.ust,key=lambda x: x['from'])
        ustList.reverse()
        thismonth = "%4i%2i" %(self.data["year"],self.data["month"])
        ustValue = 17

        for ust in ustList:
            if thismonth >= str(ust["from"]):
                ustValue = ust["value"]

        return ustValue / 100

    def determineFee(self):
        """ Determine Fee-Value for this month """
        feeList = sorted(self.berater.fee,key=lambda x: x['from'])
        thismonth = "%4i%02i" %(self.data["year"],self.data["month"])
        feeValue = "70"
        for fee in feeList:
            if thismonth >= str(fee["from"]):
                feeValue = fee["value"]

        feeValue = float(feeValue)
        return feeValue / 100

    def open(self,filename):        
        f_month = open(filename,"r")
        try:                                         # Try to load File as YAML
            self.data = yaml.load(f_month)
        except:
            return False                         # Not a valid YAML-File
        f_month.close() 
        # Now Check for Data-Structure: month, yeaar, data
        if self.data["month"] and  self.data["year"] :

            self.ust = self.determineUst()
            self.fee = self.determineFee()
            return True
        else: 
            return False
