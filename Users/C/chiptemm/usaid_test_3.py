import scraperwiki
from lxml import html
from HTMLParser import HTMLParser
import urllib2
import re
import string
import json
import pprint

pp = pprint.PrettyPrinter(indent=4)
URL = "http://map.usaid.gov/MapData?r=projects&l=&w="
PROJECT_URL = "http://map.usaid.gov/MapData?d=%s&r=detail"



class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    if(html is None):
        html=''
    s.feed(html)
    return s.get_data()

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
    #aproject["url"] = project["attributes"]["url"]
    #aproject["type"] = project["attributes"]["type"]
    #aproject["public_name"] = project["Public_Name__c"]
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
    #aproject["photo"] = theproject_data["Public_Photo__c"]
    #aproject["theme"] = theproject_data["Project_Theme__c"]
    aproject["description_txt"] = strip_tags(theproject_data["Project_Description__c"])
    aproject["description_html"] = theproject_data["Project_Description__c"]
    aproject["primary_initiative"] = theproject_data["Primary_Initiative__c"]
    #aproject["provinces"] = theproject_data["Provinces__c"]


    if ((theproject_data["ImpMechs_Projects__r"] is not None) and (theproject_data["ImpMechs_Projects__r"]["records"] is not None)):
        for record in theproject_data["ImpMechs_Projects__r"]["records"]:
            ##aproject["impmechs_record_type"] = record["attributes"]["type"]
            ##aproject["impmechs_url"] = record["attributes"]["url"]
            #aproject["impmechs_number_type"] = record["Implementing_Mechanism_Number__r"]["attributes"]["type"]
            #aproject["impmechs_number_url"] = record["Implementing_Mechanism_Number__r"]["attributes"]["url"]
            aproject["impmechs_award_amt"] = record["Implementing_Mechanism_Number__r"]["Award_Amount__c"]
            aproject["impmechs_primary_partner"] = record["Implementing_Mechanism_Number__r"]["Partner_Name__c"]

    pp.pprint(aproject)
    scraperwiki.sqlite.save(unique_keys=["id"],
            data=aproject)

#printable_data = json.dumps(thedata)
#pp.pprint(printable_data)