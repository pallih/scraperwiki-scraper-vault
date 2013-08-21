"""
Collects information from various ScraperWiki school data scrapers. Gets it
  into something resembling a canonical format.

Currently works on council data from: Derbyshire, County Durham, Hertfordshire,
  Leicestershire, Lincolnshire, Northumberland, Nottinghamshire.

Documentation of the keys produced is contained in the source code.
"""


import csv
import urllib
import re
from scraperwiki import datastore


def main():

    transformers = [Derbyshire(),
                    CountyDurham(),
                    Hertfordshire(),
                    Leicestershire(),
                    Lincolnshire(),
                    Northumberland(),
                    Nottinghamshire()]

    # should we stop if a transformer raises an exception?
    debug_mode = True 

    # process the data
    naughtylist = []
    for t in transformers:
        print "Processing " + t.scraper
        if debug_mode:
            t.run()
        else:
            try:
                t.run()
            except Exception:
                naughtylist.append(t)
        print "... %d records generated"%t.count
        print ""

    # report on the keys used
    outkeys = set()
    for t in transformers:
        t.complain()
        outkeys.update(t.outkeys)
    outkeylist = list(outkeys)
    outkeylist.sort()
    print "Output keys produced:"
    print ", ".join(outkeylist)
    print ""

    # report on which don't have documentation
    keydoc = keydocumentation()
    undocumentedkeys = [k for k in outkeylist if not k in keydoc]
    if len(undocumentedkeys) > 0:
        print "Undocumented output keys produced:"
        print ", ".join(undocumentedkeys)
        print ""

    # report any keys we've documented but haven't actually used
    unuseddoc = [k for k in keydoc.iterkeys() if not k in outkeylist]
    if len(unuseddoc) > 0:
        print "Documented keys which are not produced:"
        print ", ".join(unuseddoc)
        print ""

    # report on any transformers which failed to run
    if len(naughtylist) > 0:
        print "Transformers failed to run for the following scrapers:"
        print ", ".join(t.name() for t in naughtylist)
        print ""
    
    
def keydocumentation():
    d = {}

    d["Schoolname"] = "The official name of the school"
    d["Schoolname_short"] = "An abbreviated form of the schoolname"
    d["Address"] = "Postal address (without postcode), as a list of lines separated by ' / '"
    d["Postcode"] =  "Postcode (corresponding to postal address)"
    d["Email"] = "A contact email address for the school"
    d["Website"] = "The school's website"
    d["Telephone"] = "The school's phone number"
    d["Telephone2"] = "An alternative phone number"
    d["Fax"] = "The school's fax number"

    d["Number_of_students"] = "The number of students at the school"
    d["Age_Range"] = "Ages of students at the school, in the format eg. 7-18 or 4-11"
    d["Sex"] = "The sex of students at the school: 'mixed'/'boys'/'girls'/'unknown'"

    d["Headteacher_Name"] = "Name of the school's headteacher"
    d["Headteacher_Title"] = "Their title (eg. Mr, Ms, etc)"
    
    d["Authority"] = "The council responsible for the school"
    d["Category"] = "The type of school by governance model"
    d["Phase"] = "The type of school by rough age (eg. Primary, Secondary, etc.)"
    d["Type"] = "The type of school by specialism"

    d["School_Dinner"] = "A link to a page storing up-to-date school dinner menus"
    d["Map"] = "A link to a map of the school location provided by the council"
    d["Ofsted_report"] = "A link to the most recent Ofsted report into the school"
    d["KS3_tables"] = "A link to the most recent Key Stage 3 performance tables"
    d["KS4_tables"] = "A link to the most recent Key Stage 3 performance tables"
    d["District"] = "The electoral district containing the school"

    d["DCSF_short"] = "DCSF code number for the school; last four digits"
    d["DCSF_long"] = "DCSF code number for the school; all eight digits"
    d["URN"] = "School's Unique Reference Number"

    d["Linked_Schools"] = "A list of schools enjoying some connection, specified as a list of schoolnames separated by '; '"
    d["Has_nursery"] = "'Yes' if school has a nursery unit"
    d["Special_unit"] = "'Yes' if school has a special unit"
    d["Special_base"] = "'Yes' if school has a special base"
    d["Contact_Job"] = "The job title of a contact for the school"
    d["Contact_Name"] = "The name of that contact"
    d["Contact_Title"] = "Their title (eg. Mr, Ms, etc)"

    d["Admissions_Officer_Name"] = "Name of the school's admissions officer"
    d["Education_Welfare_Officer_Name"] = "Name of the school's Education Welfare Officer"
    d["Attendance_Improvement_Officer_Name"] = "Name of the school's attendance improvement officer"
    d["District_School_Effectiveness_Advisor_Name"] = "Name of the school's district school effectiveness adviser"

    return d


def addressCase(s):
    "Puts All Words Except the Short Ones into Title Case"
    return " ".join(addressCaseWord(w) for w in s.split(" "))


def addressCaseWord(w):
    "Puts a Word into Title Case Unless it is Short"
    w = w.title()
    if w in ["The","In","Into","Of","It","Is","And","On"]:
        return w.lower()
    else:
        return w


def removeTitle(n):
    "Replaces a name with title with the name alone"
    title = re.compile("^(Mr?s?\\.?)|(Miss)|(Dr\\.?)\\w+")
    return title.sub("",n)
    

def extractTitle(n):
    "Removes a title from a name"
    title = re.compile("^(?:Mr?s?\\.?|Miss|Dr\\.?\\w+)")
    m = title.match(n)
    if m:
        return m.group()
    else:
        return ""


def bossjob(j):
    "Is this job synonymous with 'Headteacher'?"
    return j in ["Headteacher","Principal"]
  

class TracingDict(dict):
    "Like a dictionary, but remembers which keys have been accessed by get"

    def __init__(self):
        dict.__init__(self)
        self.accessed = set()

    def __getitem__(self,key):
        self.accessed.add(key)
        return dict.__getitem__(self,key)

    def get(self,key,default):
        self.accessed.add(key)
        return dict.get(self,key,default)

    def unaccessed(self):
        return set(self.iterkeys()) - self.accessed


def getScraperWiki(scraper):
    """
    An iterator that scrapes the results of a scraperwiki scraper and returns
    key/value dicts.

    Based directly on code by Julian Todd.
    """

    url = "http://scraperwiki.com/scrapers/export/%s/" % scraper
    s = urllib.urlopen(url)
    c = csv.reader(s)
    headers = c.next()
    # print scraper, headers
    for row in c:
        r = TracingDict()
        for k, v in zip(headers, row):
            if v:
                r[k] = v
        yield r


class Transformer():
    """
    A class whose objects transform the output of a certain scraper.

    Must be subclassed to be useful. Subclasses may find it useful to define:
      self.transform   (the most important thing: function that takes the old
                        dictionary and returns the new)
      self.scraper     (the name of a scraper)
      self.discards    (a list of fields whose information is considered
                        useless)
      self.unique_keys (the eventual unique keys of the finished dictionary;
                        defaults to ["Schoolname"] which may not in fact be
                        unique)
    """

    def __init__(self):
        self.unaccessed_inkeys = set()
        self.outkeys = set()
        self.out = {}
        self.discards = []
        self.unique_keys = ["Schoolname"]
        self.count = 0

    def indicts(self):
        return getScraperWiki(self.scraper)

    def outdicts(self):
        for d in self.indicts():
            self.count += 1
            o = self.transform(d)
            self.outkeys.update(o.iterkeys())
            for k in self.discards:
                d.get(k,None)
            self.unaccessed_inkeys.update(d.unaccessed())
            yield o

    def run(self):
        for d in self.outdicts():
            datastore.save(unique_keys=self.unique_keys, data=d)
            print "     - " + self.recordname(d)
            
    def recordname(self,d):
        return "; ".join(d[k] for k in self.unique_keys)

    def name(self):
        return self.scraper

    def complain(self):
        "Displays unaccessed fields"
        if len(self.unaccessed_inkeys) > 0:
            print "Input keys not used by " + self.name() + ":"
            for a in self.unaccessed_inkeys:
                print " - " + a
            print ""




### helper functions for common dictionary manipulations

def copy_keys(source,target,l):
    "Copies all keys in l from source into target"
    for k in l:
        if k in source:
            target[k] = source[k]

def rename_keys(source,target,m):
    for (k,v) in m.iteritems():
        if k in source:
            target[v] = source[k]




class CountyDurham(Transformer):

    def __init__(self):
        Transformer.__init__(self)
        self.scraper = "county-durham-council-schools"

    def transform(self,d):
        def sanitiseName(n):
            "Durham have a weird habit of sticking dots after given names"
            return re.compile("([a-z])\\.").sub("\\1",n)

        o = {}
        o["Authority"] = "Durham County Council"
        copy_keys(d,o,["Email","Fax","Telephone","Postcode",
                       "Website","Ofsted_report"])
        rename_keys(d,o,{"schoolname":"Schoolname",
                         "Type":"Phase",
                         "Reference":"DCSF_short"})
        o["Address"] = addressCase(d.get("Address",""))
        agerange = re.compile("([0-9]*) years to ([0-9]*) years")
        o["Age_Range"] = agerange.sub("\\1-\\2",d.get("Age_Range",""))
        o["Headteacher_Name"] = removeTitle(d.get("Principal",""))
        o["Headteacher_Title"] = sanitiseName(extractTitle(d.get("Principal","")))
        return o


class Derbyshire(Transformer):

    def __init__(self):
        Transformer.__init__(self)
        self.scraper = "derbyshire-council-schools"
        self.discards.append("Map_of_School_Normal_Area")

    def transform(self,d):
        o = {}

        copy_keys(d,o,["Telephone","Address","Postcode","Email","Website","Fax"])
        rename_keys(d,o,{"Name":"Schoolname",
                         "School_Type":"Category",
                         "Ofsted":"Ofsted_report",
                         "Map_of_Main_School_Site":"Map",
                         "DfES_Number":"DCSF_short",
                         "Headteacher":"Headteacher_Name"})

        agerange = re.compile("([0-9]*) to ([0-9]*) yrs")
        o["Age_Range"] = agerange.sub("\\1-\\2",d.get("Age_Range",""))

        return o


class Hertfordshire(Transformer):

    def __init__(self):
        Transformer.__init__(self)
        self.scraper = "hertfordshire-schools"
        self.discards.append("LatLng")
        self.discards.append("Short_Code_or_Comnet_no")

    def transform(self,d):
        o = {}
        o["Authority"] = "Hertfordshire County Council"
        copy_keys(d,o,["Fax","Telephone",
                       "Postcode","Area","Category","Division","District"])
        rename_keys(d,o,{"Web_Address":"Website",
                         "Special_Base":"Special_base",
                         "Special_Unit":"Special_unit",
                         "Correspondence_Name":"Schoolname",
                         "name":"Schoolname_short",
                         "School_Number":"Number_of_students",  ### THIS IS WHAT IT MEANS ISN'T IT?
                         "Head_Teacher":"Headteacher_Name",
                         "District_School_Effectiveness_Advisor":"District_School_Effectiveness_Advisor_Name",
                         "Attendance_Improvement_Officer":"Attendance_Improvement_Officer_Name",
                         "Admissions_Officer":"Admissions_Officer_Name",
                         "DCSF_Number":"DCSF_short",
                         "Email_Admin":"Email"})
        o["Address"] = addressCase(d.get("Address",""))
        o["Has_nursery"] = d.get("Nursery_Class","")

        phaseandsex = d.get("Type","Unknown Unknown").split(" ")
        assert len(phaseandsex) == 2
        o["Phase"] = phaseandsex[0]
        sextable = {"Mixed":"mixed","Male":"boys","Female":"girls"}
        o["Sex"] = sextable[phaseandsex[1]]
        return o
        
        
class Leicestershire(Transformer):

    def __init__(self):
        Transformer.__init__(self)
        self.scraper = "leicestershire-council-schools"

    def transform(self,d):
        o = {}
        o["Authority"] = "Leicestershire County Council"
        rename_keys(d,o,{"unit":"Special_unit",
                         "web":"Website",
                         "type":"Phase",
                         "dfes":"DCSF_short",
                         "office":"Telephone2",
                         "ages":"Age_Range",
                         "number":"Number_of_students",  ### THIS IS WHAT IT MEANS ISN'T IT?
                         "denom":"Category",
                         "schoolname":"Schoolname",
                         "fax":"Fax",
                         "postcode":"Postcode",
                         "email":"Email",
                         "phone":"Telephone"})
        o["Address"] = addressCase(d.get("address",""))
        o["Headteacher_Name"] = removeTitle(d.get("head",""))
        o["Headteacher_Title"] = extractTitle(d.get("head",""))
        o["Has_nursery"] = d.get("nursery","")
        return o


class Lincolnshire(Transformer):

    def __init__(self):
        Transformer.__init__(self)
        self.scraper = "lincolnshire-council-schools"

    def transform(self,d):
        o = {}
        o["Authority"] = "Lincolnshire County Council"

        # patch the address from the constituent parts
        l = []
        if "Street1" in d:
            l.append(d["Street1"])
        if "Street2" in d:
            l.append(d["Street2"])
        if "Locality" in d:
            l.append(d["Locality"])
        if "Town" in d:
            l.append(d["Town"])
        l.append("Lincolnshire")
        o["Address"] =  " / ".join(l)

        # get sex of school into appropriate form
        sextable = {"":"unknown", "A":"mixed", "M":"boys", "F":"girls"}
        o["Sex"] = sextable[d.get("Gender","")]

        # names of folk
        reconstructedName = (d.get("Initials","")+" "+d.get("Surname","")).strip(" ")
        o["Contact_Name"] = reconstructedName
        if bossjob(d.get("Contact_Job","")):
            o["Headteacher_Name"] = reconstructedName
            o["Headteacher_Title"] = d.get("Contact_Title","")

        # everything else...
        copy_keys(d,o,["Postcode","Fax","Phase","Category","Email"])
        rename_keys(d,o,{"School_Name":"Schoolname",
                         "Phone":"Telephone",
                         "School_Type":"Type",
                         "Full_DCSF_Number":"DCSF_long",
                         "Job_Title":"Contact_Job",
                         "Title":"Contact_Title"})

        return o


class Northumberland(Transformer):

    def __init__(self):
        Transformer.__init__(self)
        self.scraper = "northumberland-council-schools"

    def transform(self,d):
        o = {}
        copy_keys(d,o,["Postcode","Address","Telephone","Schoolname","Website","Fax","Email"])
        rename_keys(d,o,{"HeadTeacher":"Headteacher_Name"})
        return o


class Nottinghamshire(Transformer):

    def __init__(self):
        Transformer.__init__(self)
        self.scraper = "nottingham-council-schools"

    def transform(self,d):
        o = {}

        copy_keys(d,o,["Schoolname","Fax","Area","Address","Postcode",
                       "Ofsted_report","Linked_Schools"])
        rename_keys(d,o,{"School_e-mail":"Email",
                         "Tel":"Telephone",
                         "DfES_number":"DCSF_short",
                         "Unique_Reference_Number_(URN)":"URN",
                         "School_website":"Website",
                         "School_phase":"Phase",
                         "View_map":"Map",
                         "See_what's_on_the_school_dinner_menu":"School_Dinner",
                         "Expected_number_of_full_time_pupils":"Number_of_students",
                         "Key_Stage_3_performance_tables":"KS3_tables",
                         "Key_Stage_4_performance_tables":"KS4_tables",
                         "Education_Welfare_Officer":"Education_Welfare_Officer_Name"})

        o["Headteacher_Name"] = d.get("Head",d.get("School_Leader",""))

        a = d.get("Acting_Head","")
        if a != "":
            o["Contact_Name"] = a
            o["Contact_Job"] = "Acting Headteacher"

        agerange = re.compile("([0-9]*) years to ([0-9]*) years")
        o["Age_Range"] = agerange.sub("\\1-\\2",d.get("Age_range",""))

        return o


main()


