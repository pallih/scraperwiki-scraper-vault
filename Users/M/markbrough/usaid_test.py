import scraperwiki
from lxml import html
import urllib2
import re
import string
import json
import pprint

pp = pprint.PrettyPrinter(indent=4)
URL = "http://map.usaid.gov/MapData?r=projects&l=&w="
PROJECT_URL = "http://map.usaid.gov/MapData?d=%s&r=detail"

def fixdata(data):
    newdata = data.lstrip('(')
    newdata = newdata.rstrip(');')
    return newdata

req = urllib2.Request(URL)
webfile = urllib2.urlopen(req)
data = webfile.read()

thedata = json.loads(fixdata(data))

for project in thedata:
    aproject = {}
    aproject["url"] = project["attributes"]["url"]
    aproject["type"] = project["attributes"]["type"]
    aproject["public_name"] = project["Public_Name__c"]
    aproject["id"] = project["Id"]
    aproject["name"] = project["Project_Name__c"]

    project_id = aproject["id"]
    req = urllib2.Request(PROJECT_URL % (aproject["id"]))
    webfile = urllib2.urlopen(req)
    data = webfile.read()
    theproject_data = json.loads(fixdata(data))

    aproject["mission_name"] = theproject_data["MissionName__c"]
    aproject["sector"] = theproject_data["Sector_Name__c"]
    aproject["start_date"] = theproject_data["Start_Date__c"]
    aproject["end_date"] = theproject_data["End_Date__c"]
    aproject["photo"] = theproject_data["Public_Photo__c"]
    aproject["theme"] = theproject_data["Project_Theme__c"]
    aproject["description"] = theproject_data["Project_Description__c"]
    aproject["primary_initiative"] = theproject_data["Primary_Initiative__c"]
    aproject["provinces"] = theproject_data["Provinces__c"]

    if (theproject_data["ImpMechs_Projects__r"] is not None):
        if (theproject_data["ImpMechs_Projects__r"]["totalSize"] is not None):
            aproject["impmechs_totalsize"] = theproject_data["ImpMechs_Projects__r"]["totalSize"]
        if (theproject_data["ImpMechs_Projects__r"]["done"] is not None):
            aproject["impmechs_done"] = theproject_data["ImpMechs_Projects__r"]["done"]

    if ((theproject_data["ImpMechs_Projects__r"] is not None) and (theproject_data["ImpMechs_Projects__r"]["records"] is not None)):
        for record in theproject_data["ImpMechs_Projects__r"]["records"]:
            aproject["impmechs_record_type"] = record["attributes"]["type"]
            aproject["impmechs_url"] = record["attributes"]["url"]
            aproject["impmechs_number_type"] = record["Implementing_Mechanism_Number__r"]["attributes"]["type"]
            aproject["impmechs_number_url"] = record["Implementing_Mechanism_Number__r"]["attributes"]["url"]
            aproject["impmechs_award_amt"] = record["Implementing_Mechanism_Number__r"]["Award_Amount__c"]
            #Looks like this element changed @USAID, causing script to fail so updating to new element name Mar12,2013 
            aproject["impmechs_primary_partner"] = record["Implementing_Mechanism_Number__r"]["Partner_Name__c"]

    pp.pprint(aproject)
    scraperwiki.sqlite.save(unique_keys=["id"],
            data=aproject)

#printable_data = json.dumps(thedata)
#pp.pprint(printable_data)import scraperwiki
from lxml import html
import urllib2
import re
import string
import json
import pprint

pp = pprint.PrettyPrinter(indent=4)
URL = "http://map.usaid.gov/MapData?r=projects&l=&w="
PROJECT_URL = "http://map.usaid.gov/MapData?d=%s&r=detail"

def fixdata(data):
    newdata = data.lstrip('(')
    newdata = newdata.rstrip(');')
    return newdata

req = urllib2.Request(URL)
webfile = urllib2.urlopen(req)
data = webfile.read()

thedata = json.loads(fixdata(data))

for project in thedata:
    aproject = {}
    aproject["url"] = project["attributes"]["url"]
    aproject["type"] = project["attributes"]["type"]
    aproject["public_name"] = project["Public_Name__c"]
    aproject["id"] = project["Id"]
    aproject["name"] = project["Project_Name__c"]

    project_id = aproject["id"]
    req = urllib2.Request(PROJECT_URL % (aproject["id"]))
    webfile = urllib2.urlopen(req)
    data = webfile.read()
    theproject_data = json.loads(fixdata(data))

    aproject["mission_name"] = theproject_data["MissionName__c"]
    aproject["sector"] = theproject_data["Sector_Name__c"]
    aproject["start_date"] = theproject_data["Start_Date__c"]
    aproject["end_date"] = theproject_data["End_Date__c"]
    aproject["photo"] = theproject_data["Public_Photo__c"]
    aproject["theme"] = theproject_data["Project_Theme__c"]
    aproject["description"] = theproject_data["Project_Description__c"]
    aproject["primary_initiative"] = theproject_data["Primary_Initiative__c"]
    aproject["provinces"] = theproject_data["Provinces__c"]

    if (theproject_data["ImpMechs_Projects__r"] is not None):
        if (theproject_data["ImpMechs_Projects__r"]["totalSize"] is not None):
            aproject["impmechs_totalsize"] = theproject_data["ImpMechs_Projects__r"]["totalSize"]
        if (theproject_data["ImpMechs_Projects__r"]["done"] is not None):
            aproject["impmechs_done"] = theproject_data["ImpMechs_Projects__r"]["done"]

    if ((theproject_data["ImpMechs_Projects__r"] is not None) and (theproject_data["ImpMechs_Projects__r"]["records"] is not None)):
        for record in theproject_data["ImpMechs_Projects__r"]["records"]:
            aproject["impmechs_record_type"] = record["attributes"]["type"]
            aproject["impmechs_url"] = record["attributes"]["url"]
            aproject["impmechs_number_type"] = record["Implementing_Mechanism_Number__r"]["attributes"]["type"]
            aproject["impmechs_number_url"] = record["Implementing_Mechanism_Number__r"]["attributes"]["url"]
            aproject["impmechs_award_amt"] = record["Implementing_Mechanism_Number__r"]["Award_Amount__c"]
            #Looks like this element changed @USAID, causing script to fail so updating to new element name Mar12,2013 
            aproject["impmechs_primary_partner"] = record["Implementing_Mechanism_Number__r"]["Partner_Name__c"]

    pp.pprint(aproject)
    scraperwiki.sqlite.save(unique_keys=["id"],
            data=aproject)

#printable_data = json.dumps(thedata)
#pp.pprint(printable_data)