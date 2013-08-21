import BeautifulSoup
import urllib2
import re
from xml.dom.minidom import Document
import hashlib
import datetime
import scraperwiki

class Activities:        
    def create_activity(self):
        activity = Activity()
        return activity
    
    def finish(self):
        pass
        
class Thing:
    required_fields = []
    placeholders = {}
    id = None
    name = None
    
    def __init__(self):
        self.data = {}
    
    def add_field(self, name, contents):
        text = contents.strip()
        if name == "Name": self.name = text
        elif name == "ActivitySourceID": self.id = text
        self.data[name] = text 
    
    def try_placeholder(self, field):
        try:
            self.add_field(field, self.placeholders[field])
        except KeyError:
            print "Error: Required field '"+field+"' is missing. ("+self.id+", "+self.name+")"
    
    def finish(self):
        for field in self.required_fields:
            try:
                tmp = self.data[field]
            except KeyError:
                self.try_placeholder(field)

class Venue(Thing):
    required_fields = ["ProviderVenueID", "Name", "BuildingNameNo", "Postcode", "ContactForename", "ContactSurname", "ContactPhone" ]
    placeholders = {"ContactPhone":"n/a","ContactForename":"-","ContactSurname":"-"}
    forenamemissing = False
    
    def try_placeholder(self, field):
        if field == "BuildingNameNo": self.add_field("BuildingNameNo", self.name)
        elif field == "ContactForename":
            self.forenamemissing = True
        elif field == "ContactSurname":
            if self.forenamemissing:
                self.add_field("ContactForename", "General")
                self.add_field("ContactSurname", "enquiries")
            else:
                self.add_field("ContactSurname", "-")
        else: Thing.try_placeholder(self, field)

class Activity(Thing):
    required_fields = ["ActivitySourceID", "Name", "Description", "Starts", "Ends", "ContactName", "ContactNumber"]
    placeholders = {"ContactName":"General enquiries", "ContactNumber":"n/a"}
    
    def __init__(self):
        self.venue = Venue()
        Thing.__init__(self)
    
    def finish(self):
        self.venue.finish()
        Thing.finish(self)
        scraperwiki.datastore.save(["ActivitySourceID"], self.data)
        
def mkdate(date):
    try:
        d = datetime.datetime.strptime(date, "%a %d %b %Y %I.%M%p")
    except ValueError:
        d = datetime.datetime.strptime(date, "%a %d %b %Y %I%p")
    return d.strftime("%Y-%m-%dT%H:%M:%S")

url = "http://www.youth.luton.gov.uk/13.cfm?p=881"
html = urllib2.urlopen(url).read()
page = BeautifulSoup.BeautifulSoup(html, convertEntities=BeautifulSoup.BeautifulSoup.HTML_ENTITIES)

activities = Activities()

tables = page.findAll(lambda tag: len(tag.attrs) == 3 and tag.name == "table")
for table in tables:
    i=0
    activity = activities.create_activity()
    date = ""
    for cell in table.findAll("td"):
        #print str(i)+" "+str(cell)
        if i==0:
            activity.add_field("ActivitySourceID", hashlib.sha1(str(cell.a.contents[0]).strip()).hexdigest())
            activity.add_field("Name", str(cell.a.contents[0].split("-")[1]))
        elif i==1:
            date = " ".join(str(cell.contents[0]).split()[0:4]).strip(" \r\n\t")
        elif i==2:
            text = str(cell)
            activity.add_field("Description", re.search("<td><p>(.*?)<" , text).group(1))
            activity.add_field("Cost", re.search(">Cost: (.*?)<" , text).group(1))
            activity.add_field("ContactNumber", re.search(">Tel: (.*?)<" , text).group(1))
            
            loc = re.search("Location(</strong>){0,1}<br />(.*?)<br />(.*?)<br />(.*?)<br />(.*?)<br />" , text)
            #for i in range(2,6): print loc.group(i)
            activity.venue.add_field("ProviderVenueID", hashlib.sha1(str(loc.group(2)).strip()).hexdigest())
            activity.venue.add_field("Name", str(loc.group(2)))
            activity.venue.add_field("Postcode", str(loc.group(5)))
            activity.venue.add_field("ContactForename", "General")
            activity.venue.add_field("ContactSurname", "enquiries")
            activity.venue.add_field("ContactPhone", "n/a")
            
            t = re.search(">Time: (.*?)<" , text)
            if t != None:
                words = t.group(1).split()
            else:
                words = ["12.00am", "-", "11.59pm"]
            time = words[0] + words[-1]
            """if len(words) > 3:
                activity2 = activity.cloneNode(True)
                activities.appendChild(activity2)"""
            activity.add_field("Starts", mkdate(date+" "+words[0]))
            activity.add_field("Ends", mkdate(date+" "+words[2]))
            """if len(words) > 3:
                add_node(activity2, "Starts", mkdate(date+" "+words[4]))
                add_node(activity2, "Ends", mkdate(date+" "+words[6]))"""
            
            activity.finish()
        i+=1
               
activities.finish()
