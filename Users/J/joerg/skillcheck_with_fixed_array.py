# -*- coding: utf-8 -*-

import scraperwiki
import csv
import lxml.etree
import lxml.html
import time
import dateutil.parser
import sys
import json
from datetime import datetime, date, timedelta
import urllib
import urllib2
from urlparse import urlparse
import re

scraperwiki.sqlite.attach("jobs_combined")
scraperwiki.sqlite.attach("jobs_combined_2")

scraperwiki.sqlite.save_var("offset",  200000, verbose=0)
scraperwiki.sqlite.save_var("offset2", 200000, verbose=0)

# Setup database connections
#jobCount  = scraperwiki.sqlite.select('count(*) from jobs_combined.swdata   where description like "%grails%" and region like "%berlin%"')[0]["count(*)"]
#jobCount2 = scraperwiki.sqlite.select('count(*) from jobs_combined_2.swdata where description like "%grails%" and region like "%berlin%"')[0]["count(*)"]
#print "Number of Jobs:   ", jobCount + jobCount2, ": ", jobCount, " +", jobCount2
#sys.exit()


# Setup database connections
#scraperwiki.sqlite.attach("jobs_combined")
#scraperwiki.sqlite.attach("jobs_combined_2")
jobCount  = scraperwiki.sqlite.select('count(*) from jobs_combined.swdata')[0]["count(*)"]
jobCount2 = scraperwiki.sqlite.select('count(*) from jobs_combined_2.swdata')[0]["count(*)"]
print "Number of Jobs:   ", jobCount + jobCount2, ": ", jobCount, " +", jobCount2

# Build list of Skills
skills = []
skillCSVFile = scraperwiki.scrape("https://docs.google.com/spreadsheet/pub?key=0Aoevfvsr8NYhdGZFNkVZZTRtQzlMSThzUjQ1LU9VTXc&range=A2%3AA2000&output=csv")
reader = csv.reader(skillCSVFile.splitlines())
for row in reader:
    try: skills.append(row[0].decode('utf-8'))
    except: print sys.exc_info() # pass
print "Number of Skills: ", len(skills)

# Setup database
#scraperwiki.sqlite.execute("drop table if exists swdata")
try:    scraperwiki.sqlite.execute("create table swdata (oldID, id INTEGER PRIMARY KEY AUTOINCREMENT)")
except: print "Table 'swdata' already exists."
try:    scraperwiki.sqlite.execute('CREATE INDEX IF NOT EXISTS oldID_index ON swdata (oldID)')
except: print sys.exc_info() # pass

# Start 1
count        = 0
windowLength = 1000
windowCount  = (jobCount / windowLength) + 1
offset       = scraperwiki.sqlite.get_var("offset", 0)
#offset = 1000000
startFound   = False
print "Jobs Combined 1: Start or continue from offset: ", offset
for window in range(windowCount):
    jobs = scraperwiki.sqlite.select('* from jobs_combined.swdata LIMIT '+str(windowLength)+' OFFSET '+str(offset), verbose=0 )
    for record in jobs:
        count = count + 1
        if count%1000 == 0: print "Jobs processed upto:", offset
        try:
            regionText = record["region"]
            if  regionText.count(',') >= 3: continue
        except: pass #print "   regionText.count:", regionText.count(',')

        if scraperwiki.sqlite.select("id from swdata where oldID='"+record["oldID"]+"' LIMIT 1", verbose=0): continue

        try:    del record["id"]
        except: pass #print sys.exc_info() # pass
        try:        description   = record["description"].lower()
        except:
            try:    description   = record["description"].decode('utf-8').lower()
            except: description   = record["description"]
        jobSkills = ""
        separator = ""
        if description:
            description   = description.replace(',',' ').replace('.',' ').replace(';',' ').replace(':',' ').replace('!',' ').replace('?',' ')
            for skill in skills:
                if skill.lower() in description:
                    jobSkills = skill + separator + jobSkills
                    separator = ","
        # skills could get associated with date/time and co-occurances
        record["skills"] = jobSkills #json.dumps(jobSkills)
        try:
            if record["skills"] == None or record["skills"] == [] or record["skills"] == "[]" or record["skills"] == "['']":
                record["skills"] = ""
        except: print sys.exc_info() # pass

        #save in datastore
        if (record["skills"] != None and record["skills"] != "" and record["skills"] != []):
            scraperwiki.sqlite.save(unique_keys=[], data=record, table_name='swdata', verbose=0)

    offset = offset + windowLength
    scraperwiki.sqlite.save_var("offset", offset, verbose=0)

# Start 2
windowCount  = (jobCount2 / windowLength) + 1
offset2      = scraperwiki.sqlite.get_var("offset2", 0, verbose=0)
#offset2 = 1000000
startFound   = False
print "Jobs Combined 2: Start or continue from offset: ", offset2
for window in range(windowCount):
    jobs = scraperwiki.sqlite.select('* from jobs_combined_2.swdata LIMIT '+str(windowLength)+' OFFSET '+str(offset2), verbose=0 )
    for record in jobs:
        count = count + 1
        if count%1000 == 0: print "Jobs processed upto:", offset2
        try:
            regionText = record["region"]
            if  regionText.count(',') >= 3: continue
        except: pass #print "No region found for:", record["id"]

        if scraperwiki.sqlite.select("id from swdata where oldID='"+record["oldID"]+"' LIMIT 1", verbose=0): continue

        try:    del record["id"]
        except: pass #print sys.exc_info() # pass
        try:        description   = record["description"].lower()
        except:
            try:    description   = record["description"].decode('utf-8').lower()
            except: description   = record["description"]
        if description: description   = description.replace(',',' ').replace('.',' ').replace(';',' ').replace('!',' ').replace('?',' ')
        jobSkills = ""
        separator = ""
        if description:
            for skill in skills:
                if skill.lower() in description:
                    jobSkills = skill + separator + jobSkills
                    separator = ","
        # skills could get associated with date/time and co-occurances
        record["skills"] = jobSkills #json.dumps(jobSkills)
        try:
            if record["skills"] == None or record["skills"] == [] or record["skills"] == "[]" or record["skills"] == "['']":
                record["skills"] = ""
        except: print sys.exc_info() # pass
    
        #save in datastore
        if (record["skills"] != None and record["skills"] != "" and record["skills"] != []):
            scraperwiki.sqlite.save(unique_keys=[], data=record, table_name='swdata', verbose=0)

    offset2 = offset2 + windowLength
    scraperwiki.sqlite.save_var("offset2", offset2, verbose=0)

print count, " jobs processed in total."

companyCount = 55260 
#companyCount = len(scraperwiki.sqlite.execute('select count(*) as count from swdata group by company, region')['data'])
print companyCount, " different company locations found."

# Setup database
#scraperwiki.sqlite.execute("drop table if exists company_data")
try: scraperwiki.sqlite.execute("create table company_data (id INTEGER PRIMARY KEY AUTOINCREMENT)")
except: print "Table 'company_data' already exists."
try:
    scraperwiki.sqlite.execute('CREATE INDEX IF NOT EXISTS company_region_index ON company_data (company, region)')
    scraperwiki.sqlite.execute('CREATE INDEX IF NOT EXISTS company_index ON company_data (company)')
    scraperwiki.sqlite.execute('CREATE INDEX IF NOT EXISTS region_index ON company_data (region)')
    scraperwiki.sqlite.commit()
except: print sys.exc_info() # pass

windowLength  = 1000
windowCount   = (companyCount / windowLength) + 1
companyOffset = scraperwiki.sqlite.get_var("offset_company", 0, verbose=0)
print "Companies Combined: Start or continue from offset: ", companyOffset 
for window in range(windowCount):
    # Group companies and combine data
    companies = scraperwiki.sqlite.select( 'company, region, date, country, group_concat(skills) AS skills, group_concat(tags) AS tags, group_concat(contactInfo) AS contactInfo, group_concat(companyURL) AS companyURL, group_concat(logoURL) AS logoURL FROM swdata GROUP BY company, region LIMIT '+str(windowLength)+' OFFSET '+str(companyOffset),  verbose=0)

    for row in companies:
        if row["company"] == None or row["region"] == None: continue
        try:    companyExists = scraperwiki.sqlite.select("* FROM company_data WHERE company='"+row["company"]+"' AND region='"+row["region"]+"'", verbose=0)[0]
        except: companyExists = None
        try:
            regionText = row["region"]
            if  regionText.count(',') > 3: continue
        except: pass #print "No region found for:", row["id"]
    
        try:
            try:    skills = row["skills"]
            except: skills = ""
            if skills == None: skills = ""
            skillList     = skills.replace("["," ").replace("]"," ").replace('"'," ").replace("'"," ").split(',')
            skillListUTF8 = [s.strip().encode('utf-8') for s in skillList ]
            if companyExists: skillListUTF8 = skillListUTF8 + json.loads(companyExists["skills"])
            compactedList = list(set(skillListUTF8))
            row["skills"] = json.dumps(compactedList)
        except: pass
    #        print row["skills"]
    #        print companyExists["skills"]
    #        print sys.exc_info() # pass
    #        raise
    
        try:
            try:    tags = row["tags"]
            except: tags = ""
            if tags == None: tags = ""
            tagList       = tags.replace("["," ").replace("]"," ").replace(' u"'," ").replace(" u'"," ").replace('"'," ").replace("'"," ").split(',')
            tagListUTF8   = [s.strip().encode('utf-8') for s in tagList ]
            if companyExists: tagListUTF8   = tagListUTF8 + json.loads(companyExists["tags"])
            compactedList = list(set(tagListUTF8))
            row["tags"]   = json.dumps(compactedList)
        except: pass
    #        print row["tags"]
    #        print companyExists["tags"]
    #        print sys.exc_info() # pass
    #        raise
    
        try:
            try:    companyURL = row["companyURL"]
            except: companyURL = ""
            if companyURL == None: companyURL = ""
            compList       = companyURL.split(',')
            compListUTF8   = [s.strip().encode('utf-8') for s in compList ]
            if companyExists: compListUTF8   = compListUTF8 + json.loads(companyExists["companyURL"])
            compactedList  = list(set(compListUTF8))
            row["companyURL"] = json.dumps(compactedList)
        except: pass
    #        print sys.exc_info() # pass
    #        raise
    
        try:
            try:    logoURL = row["logoURL"]
            except: logoURL = ""
            if logoURL == None: logoURL = ""
            logoList       = logoURL.split(',')
            logoListUTF8   = [s.strip().encode('utf-8') for s in logoList ]
            if companyExists: logoListUTF8   = logoListUTF8 + json.loads(companyExists["logoURL"])
            compactedList  = list(set(logoListUTF8))
            row["logoURL"]  = json.dumps(compactedList)
        except: pass
    #        print row["logoURL"]
    #        print companyExists["logoURL"]
    #        print sys.exc_info() # pass
    #        raise
    
        try:
            try:    contactInfo = row["contactInfo"]
            except: contactInfo = ""
            if companyExists: contactInfo = json.loads(companyExists["contactInfo"]).append(contactInfo)
            row["contactInfo"]  = json.dumps(contactInfo)
        except: pass
    #        print row["contactInfo"]
    #        print companyExists["contactInfo"]
    #        print sys.exc_info() # pass
    #        raise
    
        if not companyExists: 
            # save new row
            scraperwiki.sqlite.save(unique_keys=[], data=row, table_name='company_data', verbose=0)
        else: 
            #update existing company
            row["id"] = companyExists["id"]
            scraperwiki.sqlite.save(["id"], data=row, table_name='company_data', verbose=0)

# Info
allRows = scraperwiki.sqlite.execute('SELECT count(*) FROM company_data;')
scraperwiki.sqlite.commit()
print "Count of all companies was: ", allRows["data"][0]

scraperwiki.sqlite.save_var("offset", 0)
scraperwiki.sqlite.save_var("offset2", 0)
scraperwiki.sqlite.save_var("offset_company", 0)

sys.exit()





# Cleanup 1: Remove corrupt data
corruptRows = scraperwiki.sqlite.execute("SELECT count(*) FROM company_data WHERE company IS NULL OR company='';")
scraperwiki.sqlite.commit()
print "Starting to clean up database: ", corruptRows["data"][0]
corruptRows = scraperwiki.sqlite.execute("DELETE FROM company_data WHERE (company IS NULL)")
corruptRows = scraperwiki.sqlite.execute("DELETE FROM company_data WHERE (company='')")
scraperwiki.sqlite.commit()

# Cleanup 2: Correct data
corruptRows = scraperwiki.sqlite.execute("SELECT count(*) FROM company_data WHERE company like '- %';")
print "Starting to correct database (company): ", corruptRows["data"][0]
corruptRows = scraperwiki.sqlite.select("* FROM company_data WHERE company like '- %';")
for row in corruptRows:
    row["company"] = re.sub("^- ", "", row["company"]).strip()
    scraperwiki.sqlite.save(["id"], data=row, table_name='company_data', verbose=0)

# Cleanup 3: De-duplicate
duplicates = scraperwiki.sqlite.execute("SELECT count(*) FROM company_data WHERE id NOT IN (SELECT MAX(id) FROM company_data GROUP BY company, region);")
scraperwiki.sqlite.commit()
print "Starting to remove duplicates: ", duplicates["data"][0]
duplicates = scraperwiki.sqlite.execute("DELETE FROM company_data WHERE id NOT IN (SELECT MAX(id) FROM company_data GROUP BY company, region);")
scraperwiki.sqlite.commit()

#sys.exit()

# Cleanup 4: companies and combine data
#companies = scraperwiki.sqlite.select( '* FROM company_data WHERE skills LIKE "%Flex%";' )
#for row in companies:
#    try:
#        try:    skills = row["skills"]
#        except: skills = ""
#        skillList     = skills.replace("[","").replace("]","").replace('"',"").replace("'","").split(',')
#        skillListUTF8 = [s.strip().encode('utf-8') for s in skillList ]
#        compactedList = list(set(skillListUTF8))
#        if "Flex" in compactedList: compactedList.remove("Flex") # temporary cleanup
#        row["skills"] = compactedList
#    except: print sys.exc_info() # pass
#    try:
#        try:    tags = row["tags"]
#        except: tags = ""
#        tagList       = tags.replace("[","").replace("]","").replace('"',"").replace("'","").split(',')
#        tagListUTF8   = [s.strip().encode('utf-8') for s in tagList ]
#        compactedList = list(set(tagListUTF8))
#        row["tags"]   = compactedList
#    except: print sys.exc_info() # pass
#    scraperwiki.sqlite.save(["id"], data=row, table_name='company_data', verbose=0)

# Cleanup Tags and remove unspecific rows (based on region)
whitelist = ['at', 'as', '','in','the','and', 'or', 'not', 'a', 'on', 'an', 'of', 'with', 'plus', 'over', '*', '(', ')', '[', ']', '-', '+', '/', 'any', 'along', 'is', 'year', 'years', 'year(s)', 'this', 'that', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'we', 'are', 'center', 'u', 'problem', 'solving', 'inbound', 'technical', '&', 'skill', 'set', "troubleshooting", "customer", "basic", "calls", "issues", "aptitude", "care", "outbound", "presentation", "relationship", "and/or", "people", "verbal", "written", "company", "full", "writing", "regulations","sr","jr", "training", "domain", "security", "global", "site", "environment;", "experience", "active", "model;", "administration;communicate", "maintaining", "troubleshooting", "business", "00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "15", "20", "25", "0+", "1+", "2+", "3+", "4+", "5+", "6+", "7+", "8+", "9+", "10+", "15+", "20+", "25+", "1.0", "4.5", "thorough", "multiple", "skills", "to", "directory", "in-person", "users;create", "documents", "users;provide", "advanced", "sites", "oversight", "required", "applications", "systems", "for", "supplier", "clearance", "secret", "military", "designing", "using", "language", "Natural", "complex", "environment", "environment.", "applications", "tuning", "gate", "experience", "well", "version", "yrs", "degree", "either", "primary", "focus", "development", "keywords:", "group", "software", "custom", "parts", "use", "communication", "excellent", "cycle", "solid", "intelligence", "life", "application", "requirements", "test", "cases", "preferred", "other", "specialist", "device", "driver", "applicable", "hands", "requires", "equivalent", "must", "salesforce.c", "techniques", "live", "senior", "junior", "lead", "big", "first", "minimum", "broad", "in-depth", "related", "area", "recent", "strong", "growing", "relevant", "building", "relationa", "structured", "proven", "field", "solutions", "star", "45", "components", "science", "position", "computer", "bachelor", "bachelors", "bs", "write", "3-5", "2-5", "automate", "line", "technologies", "30", "null", "40", "trade", "shows","state", "local", "structured", "practices", "bachelor s", "standard", "w", "analys", "minimum", "mid-level", "work", "internals", "international", "multi-cultural", "implementation", "etc", "them", "team", "work", "positive", "mentor", "members", "supervise", "contractors", "motivate", "take", "assigned", "accountability", "action", "influence", "their", "many", "wide", "golden", "driven", "commercial", "above", "seeking co-founders", "out", "should", "have", "general", "about", "similar", "based", "through", "preferably", "role", "basics", "solution", "concepts", "oriented", "change", "below", "details", "see", "worksite", "description", "project", "execution", "implementaion", "into", "helpful", "entering", "cost", "transactional", "disposition", "implementation", "review", "contractual", "payble", "contractual", "proposals", "audit", "hand", "such", "including", "challenging", "throughput", "enbler", "good", "great", "creds", "self", "impressive", "flexible", "internships", "blogging", "1213", "bound", "modules", "tele", "tools", "code", "24", "5-15", "from", "commands", "6500", "7600", "75", "andy", "certified", "plans", "2010", "2013", "2000", "2003", "estate", "mergers",  "real", "7-10", "4-5", "5-7", "2-3", "all", "major", "minor", "working", "description", "job", "2008", "gathering", "mid", "510k", "master s", "human", "generalist", "specialist", "resources", "professional", "against", "ava", "progressively", "within", "benefit", "benefits", "policies", "you ll", "like", "queues", "ideally", "income", "front", "fixed", "stored", "Allen", "pro", "12x", "rich", "core", "large", "manner", "direct", "clients", "activities", "inside", "schedule", "able", "3-0", "35", "can", "following", "months", "be", "intern", "extern", "external", "internal", "experiene", "open", "cancelation", "practical", "account", "process", "extension", "packaged", "document", "methodologies", "investment", "nose", "ad-hoc", "specialization", "incentives", "incentive", "staffing", "staff", "hands-on", "expert", "level", "reviewing", "accounts", "expertise", "approval", "board", "impedance", "2nd", "also", "migration", "activating", "end", "3rd", "provide", "support", "shared", "users", "phone", "resource", "held", "prefer", "devices", "person", "assistance", "scripting", "unified", "develop", "execute", "locations", "---", "validat", "troubleshoot", "some", "compents", "entry", "associated", "seeting", "directly", "eg", "2005+", "import", "russian", "2005", "higher", "desired", "also", "left-hand", "order", "needed", "previous", "product", "city", "interest", "player", "1-2", "least", "new", "requests", "rollout", "candidate", "certification", "surrounding", "executing", "industrial", "follow", "decisions", "availability", "discipline", "current", "thinking", "languages", "entities", "coaching", "supporting", "developed", "various", "routing", "recompile", "very", "possible", "balancing", "background", "procedures", "switches", "subsidiaries", "adhering", "banking", "each", "analytical", "essential", "accessible", "6K", "financial", "methods", "profiling", "phone", "audits", "best", "phases", "on-demand", "factors", "proficient", "while", "research", "access", "external", "across", "be", "transaction", "ability", "parent", "processing", "affiliates", "understanding", "desired", "leadership", "mentoring", "packages", "swift", "verifiable", "both", "certifications", "high", "shift", "compliance", "outside-the-box", "addition", "periodic", "tactical", "operating", "backup", "processor", "load", "completion", "via", "manage", "environments", "strategic", "clear", "least", "backups", "specializing", "facilitative", "detail-oriented", "service", "shells", "multilayer", "objectives", "support", "fast", "next", "call", "teamwork", "more", "releases", "fundamentals", "banking", "goals", "fail-over", "analyst", "sound", "organizations", "7-9", "graphic", "F5", "theories", "will", "expertise", "demonstrate", "outing", "proactive", "process", "7k", "candidates", "analysis", "need", "demonstration", "functions", "recovery", "provide", "make", "storage", "detail", "recommended", "simultaneous", "functionality", "achieving", "hop", "extremely", "switching", "exemplify", "independent", "product", "collaborative", "specifications", "clear", "time", "4k", "judgment", "ability", "remote", "sets", "instruments", "failover", "documentation", "lines", "supervision", "enterprise", "management", "travel", "paced", "minimal"
]
whitelist = list(set(whitelist))

#corruptRows = scraperwiki.sqlite.execute("SELECT count(*) FROM company_data WHERE tags like 'u %';")
print "Starting to correct database (tags): ALL"#, corruptRows["data"][0]
corruptRows = scraperwiki.sqlite.select("* FROM company_data;")

for row in corruptRows:
    if row["tags"] == None or row["tags"] == "": continue
    cleanTags = []
    for tag in json.loads(row["tags"]):
        tag = tag.replace("AND(","").replace("(","").replace(")","").replace(";","") # warn: no "." or ":" due to "vert.x"
        if tag != "PL/SQL" and tag != "C/C++" and tag != "TCP/IP"  and tag != "COM/DCOM" and "/" in tag:
            subTags = tag.split("/")
            for subTag in subTags:
                cleanTags.append(subTag.strip())
        else:
            tag= re.sub("^-",  "", tag)
            tag= re.sub("^u ", "", tag)
            tag= re.sub("\.$", "", tag)
            tag= re.sub("-$",  "", tag)
#            tag= re.sub("[/\*]$", "", tag)
            cleanTags.append(tag.strip())
    cleanTags   = [x for x in cleanTags if x.lower() not in whitelist]
    cleanTags   = list(set(cleanTags))
    row["tags"] = json.dumps(cleanTags)

    regionText = row["region"]
    if (regionText.count(',') < 3 and regionText.lower() != "usa" and regionText.lower() != "deutschland") or regionText.endswith("USA"):
        scraperwiki.sqlite.save(["id"], data=row, table_name='company_data', verbose=0)
    else:
#        print "Removing row :", row["id"], " with region:", regionText
#        if not regionText.endswith("USA"): # exclude regions such as "New York County, New York, NY, USA"
        scraperwiki.sqlite.execute("DELETE FROM company_data WHERE id=" + str(row["id"]))
        scraperwiki.sqlite.commit()

print "The End."

# Info
allRows = scraperwiki.sqlite.execute('SELECT count(*) FROM company_data;')
scraperwiki.sqlite.commit()
print "Count of all companies was: ", allRows["data"][0]

sys.exit()

# -*- coding: utf-8 -*-

import scraperwiki
import csv
import lxml.etree
import lxml.html
import time
import dateutil.parser
import sys
import json
from datetime import datetime, date, timedelta
import urllib
import urllib2
from urlparse import urlparse
import re

scraperwiki.sqlite.attach("jobs_combined")
scraperwiki.sqlite.attach("jobs_combined_2")

scraperwiki.sqlite.save_var("offset",  200000, verbose=0)
scraperwiki.sqlite.save_var("offset2", 200000, verbose=0)

# Setup database connections
#jobCount  = scraperwiki.sqlite.select('count(*) from jobs_combined.swdata   where description like "%grails%" and region like "%berlin%"')[0]["count(*)"]
#jobCount2 = scraperwiki.sqlite.select('count(*) from jobs_combined_2.swdata where description like "%grails%" and region like "%berlin%"')[0]["count(*)"]
#print "Number of Jobs:   ", jobCount + jobCount2, ": ", jobCount, " +", jobCount2
#sys.exit()


# Setup database connections
#scraperwiki.sqlite.attach("jobs_combined")
#scraperwiki.sqlite.attach("jobs_combined_2")
jobCount  = scraperwiki.sqlite.select('count(*) from jobs_combined.swdata')[0]["count(*)"]
jobCount2 = scraperwiki.sqlite.select('count(*) from jobs_combined_2.swdata')[0]["count(*)"]
print "Number of Jobs:   ", jobCount + jobCount2, ": ", jobCount, " +", jobCount2

# Build list of Skills
skills = []
skillCSVFile = scraperwiki.scrape("https://docs.google.com/spreadsheet/pub?key=0Aoevfvsr8NYhdGZFNkVZZTRtQzlMSThzUjQ1LU9VTXc&range=A2%3AA2000&output=csv")
reader = csv.reader(skillCSVFile.splitlines())
for row in reader:
    try: skills.append(row[0].decode('utf-8'))
    except: print sys.exc_info() # pass
print "Number of Skills: ", len(skills)

# Setup database
#scraperwiki.sqlite.execute("drop table if exists swdata")
try:    scraperwiki.sqlite.execute("create table swdata (oldID, id INTEGER PRIMARY KEY AUTOINCREMENT)")
except: print "Table 'swdata' already exists."
try:    scraperwiki.sqlite.execute('CREATE INDEX IF NOT EXISTS oldID_index ON swdata (oldID)')
except: print sys.exc_info() # pass

# Start 1
count        = 0
windowLength = 1000
windowCount  = (jobCount / windowLength) + 1
offset       = scraperwiki.sqlite.get_var("offset", 0)
#offset = 1000000
startFound   = False
print "Jobs Combined 1: Start or continue from offset: ", offset
for window in range(windowCount):
    jobs = scraperwiki.sqlite.select('* from jobs_combined.swdata LIMIT '+str(windowLength)+' OFFSET '+str(offset), verbose=0 )
    for record in jobs:
        count = count + 1
        if count%1000 == 0: print "Jobs processed upto:", offset
        try:
            regionText = record["region"]
            if  regionText.count(',') >= 3: continue
        except: pass #print "   regionText.count:", regionText.count(',')

        if scraperwiki.sqlite.select("id from swdata where oldID='"+record["oldID"]+"' LIMIT 1", verbose=0): continue

        try:    del record["id"]
        except: pass #print sys.exc_info() # pass
        try:        description   = record["description"].lower()
        except:
            try:    description   = record["description"].decode('utf-8').lower()
            except: description   = record["description"]
        jobSkills = ""
        separator = ""
        if description:
            description   = description.replace(',',' ').replace('.',' ').replace(';',' ').replace(':',' ').replace('!',' ').replace('?',' ')
            for skill in skills:
                if skill.lower() in description:
                    jobSkills = skill + separator + jobSkills
                    separator = ","
        # skills could get associated with date/time and co-occurances
        record["skills"] = jobSkills #json.dumps(jobSkills)
        try:
            if record["skills"] == None or record["skills"] == [] or record["skills"] == "[]" or record["skills"] == "['']":
                record["skills"] = ""
        except: print sys.exc_info() # pass

        #save in datastore
        if (record["skills"] != None and record["skills"] != "" and record["skills"] != []):
            scraperwiki.sqlite.save(unique_keys=[], data=record, table_name='swdata', verbose=0)

    offset = offset + windowLength
    scraperwiki.sqlite.save_var("offset", offset, verbose=0)

# Start 2
windowCount  = (jobCount2 / windowLength) + 1
offset2      = scraperwiki.sqlite.get_var("offset2", 0, verbose=0)
#offset2 = 1000000
startFound   = False
print "Jobs Combined 2: Start or continue from offset: ", offset2
for window in range(windowCount):
    jobs = scraperwiki.sqlite.select('* from jobs_combined_2.swdata LIMIT '+str(windowLength)+' OFFSET '+str(offset2), verbose=0 )
    for record in jobs:
        count = count + 1
        if count%1000 == 0: print "Jobs processed upto:", offset2
        try:
            regionText = record["region"]
            if  regionText.count(',') >= 3: continue
        except: pass #print "No region found for:", record["id"]

        if scraperwiki.sqlite.select("id from swdata where oldID='"+record["oldID"]+"' LIMIT 1", verbose=0): continue

        try:    del record["id"]
        except: pass #print sys.exc_info() # pass
        try:        description   = record["description"].lower()
        except:
            try:    description   = record["description"].decode('utf-8').lower()
            except: description   = record["description"]
        if description: description   = description.replace(',',' ').replace('.',' ').replace(';',' ').replace('!',' ').replace('?',' ')
        jobSkills = ""
        separator = ""
        if description:
            for skill in skills:
                if skill.lower() in description:
                    jobSkills = skill + separator + jobSkills
                    separator = ","
        # skills could get associated with date/time and co-occurances
        record["skills"] = jobSkills #json.dumps(jobSkills)
        try:
            if record["skills"] == None or record["skills"] == [] or record["skills"] == "[]" or record["skills"] == "['']":
                record["skills"] = ""
        except: print sys.exc_info() # pass
    
        #save in datastore
        if (record["skills"] != None and record["skills"] != "" and record["skills"] != []):
            scraperwiki.sqlite.save(unique_keys=[], data=record, table_name='swdata', verbose=0)

    offset2 = offset2 + windowLength
    scraperwiki.sqlite.save_var("offset2", offset2, verbose=0)

print count, " jobs processed in total."

companyCount = 55260 
#companyCount = len(scraperwiki.sqlite.execute('select count(*) as count from swdata group by company, region')['data'])
print companyCount, " different company locations found."

# Setup database
#scraperwiki.sqlite.execute("drop table if exists company_data")
try: scraperwiki.sqlite.execute("create table company_data (id INTEGER PRIMARY KEY AUTOINCREMENT)")
except: print "Table 'company_data' already exists."
try:
    scraperwiki.sqlite.execute('CREATE INDEX IF NOT EXISTS company_region_index ON company_data (company, region)')
    scraperwiki.sqlite.execute('CREATE INDEX IF NOT EXISTS company_index ON company_data (company)')
    scraperwiki.sqlite.execute('CREATE INDEX IF NOT EXISTS region_index ON company_data (region)')
    scraperwiki.sqlite.commit()
except: print sys.exc_info() # pass

windowLength  = 1000
windowCount   = (companyCount / windowLength) + 1
companyOffset = scraperwiki.sqlite.get_var("offset_company", 0, verbose=0)
print "Companies Combined: Start or continue from offset: ", companyOffset 
for window in range(windowCount):
    # Group companies and combine data
    companies = scraperwiki.sqlite.select( 'company, region, date, country, group_concat(skills) AS skills, group_concat(tags) AS tags, group_concat(contactInfo) AS contactInfo, group_concat(companyURL) AS companyURL, group_concat(logoURL) AS logoURL FROM swdata GROUP BY company, region LIMIT '+str(windowLength)+' OFFSET '+str(companyOffset),  verbose=0)

    for row in companies:
        if row["company"] == None or row["region"] == None: continue
        try:    companyExists = scraperwiki.sqlite.select("* FROM company_data WHERE company='"+row["company"]+"' AND region='"+row["region"]+"'", verbose=0)[0]
        except: companyExists = None
        try:
            regionText = row["region"]
            if  regionText.count(',') > 3: continue
        except: pass #print "No region found for:", row["id"]
    
        try:
            try:    skills = row["skills"]
            except: skills = ""
            if skills == None: skills = ""
            skillList     = skills.replace("["," ").replace("]"," ").replace('"'," ").replace("'"," ").split(',')
            skillListUTF8 = [s.strip().encode('utf-8') for s in skillList ]
            if companyExists: skillListUTF8 = skillListUTF8 + json.loads(companyExists["skills"])
            compactedList = list(set(skillListUTF8))
            row["skills"] = json.dumps(compactedList)
        except: pass
    #        print row["skills"]
    #        print companyExists["skills"]
    #        print sys.exc_info() # pass
    #        raise
    
        try:
            try:    tags = row["tags"]
            except: tags = ""
            if tags == None: tags = ""
            tagList       = tags.replace("["," ").replace("]"," ").replace(' u"'," ").replace(" u'"," ").replace('"'," ").replace("'"," ").split(',')
            tagListUTF8   = [s.strip().encode('utf-8') for s in tagList ]
            if companyExists: tagListUTF8   = tagListUTF8 + json.loads(companyExists["tags"])
            compactedList = list(set(tagListUTF8))
            row["tags"]   = json.dumps(compactedList)
        except: pass
    #        print row["tags"]
    #        print companyExists["tags"]
    #        print sys.exc_info() # pass
    #        raise
    
        try:
            try:    companyURL = row["companyURL"]
            except: companyURL = ""
            if companyURL == None: companyURL = ""
            compList       = companyURL.split(',')
            compListUTF8   = [s.strip().encode('utf-8') for s in compList ]
            if companyExists: compListUTF8   = compListUTF8 + json.loads(companyExists["companyURL"])
            compactedList  = list(set(compListUTF8))
            row["companyURL"] = json.dumps(compactedList)
        except: pass
    #        print sys.exc_info() # pass
    #        raise
    
        try:
            try:    logoURL = row["logoURL"]
            except: logoURL = ""
            if logoURL == None: logoURL = ""
            logoList       = logoURL.split(',')
            logoListUTF8   = [s.strip().encode('utf-8') for s in logoList ]
            if companyExists: logoListUTF8   = logoListUTF8 + json.loads(companyExists["logoURL"])
            compactedList  = list(set(logoListUTF8))
            row["logoURL"]  = json.dumps(compactedList)
        except: pass
    #        print row["logoURL"]
    #        print companyExists["logoURL"]
    #        print sys.exc_info() # pass
    #        raise
    
        try:
            try:    contactInfo = row["contactInfo"]
            except: contactInfo = ""
            if companyExists: contactInfo = json.loads(companyExists["contactInfo"]).append(contactInfo)
            row["contactInfo"]  = json.dumps(contactInfo)
        except: pass
    #        print row["contactInfo"]
    #        print companyExists["contactInfo"]
    #        print sys.exc_info() # pass
    #        raise
    
        if not companyExists: 
            # save new row
            scraperwiki.sqlite.save(unique_keys=[], data=row, table_name='company_data', verbose=0)
        else: 
            #update existing company
            row["id"] = companyExists["id"]
            scraperwiki.sqlite.save(["id"], data=row, table_name='company_data', verbose=0)

# Info
allRows = scraperwiki.sqlite.execute('SELECT count(*) FROM company_data;')
scraperwiki.sqlite.commit()
print "Count of all companies was: ", allRows["data"][0]

scraperwiki.sqlite.save_var("offset", 0)
scraperwiki.sqlite.save_var("offset2", 0)
scraperwiki.sqlite.save_var("offset_company", 0)

sys.exit()





# Cleanup 1: Remove corrupt data
corruptRows = scraperwiki.sqlite.execute("SELECT count(*) FROM company_data WHERE company IS NULL OR company='';")
scraperwiki.sqlite.commit()
print "Starting to clean up database: ", corruptRows["data"][0]
corruptRows = scraperwiki.sqlite.execute("DELETE FROM company_data WHERE (company IS NULL)")
corruptRows = scraperwiki.sqlite.execute("DELETE FROM company_data WHERE (company='')")
scraperwiki.sqlite.commit()

# Cleanup 2: Correct data
corruptRows = scraperwiki.sqlite.execute("SELECT count(*) FROM company_data WHERE company like '- %';")
print "Starting to correct database (company): ", corruptRows["data"][0]
corruptRows = scraperwiki.sqlite.select("* FROM company_data WHERE company like '- %';")
for row in corruptRows:
    row["company"] = re.sub("^- ", "", row["company"]).strip()
    scraperwiki.sqlite.save(["id"], data=row, table_name='company_data', verbose=0)

# Cleanup 3: De-duplicate
duplicates = scraperwiki.sqlite.execute("SELECT count(*) FROM company_data WHERE id NOT IN (SELECT MAX(id) FROM company_data GROUP BY company, region);")
scraperwiki.sqlite.commit()
print "Starting to remove duplicates: ", duplicates["data"][0]
duplicates = scraperwiki.sqlite.execute("DELETE FROM company_data WHERE id NOT IN (SELECT MAX(id) FROM company_data GROUP BY company, region);")
scraperwiki.sqlite.commit()

#sys.exit()

# Cleanup 4: companies and combine data
#companies = scraperwiki.sqlite.select( '* FROM company_data WHERE skills LIKE "%Flex%";' )
#for row in companies:
#    try:
#        try:    skills = row["skills"]
#        except: skills = ""
#        skillList     = skills.replace("[","").replace("]","").replace('"',"").replace("'","").split(',')
#        skillListUTF8 = [s.strip().encode('utf-8') for s in skillList ]
#        compactedList = list(set(skillListUTF8))
#        if "Flex" in compactedList: compactedList.remove("Flex") # temporary cleanup
#        row["skills"] = compactedList
#    except: print sys.exc_info() # pass
#    try:
#        try:    tags = row["tags"]
#        except: tags = ""
#        tagList       = tags.replace("[","").replace("]","").replace('"',"").replace("'","").split(',')
#        tagListUTF8   = [s.strip().encode('utf-8') for s in tagList ]
#        compactedList = list(set(tagListUTF8))
#        row["tags"]   = compactedList
#    except: print sys.exc_info() # pass
#    scraperwiki.sqlite.save(["id"], data=row, table_name='company_data', verbose=0)

# Cleanup Tags and remove unspecific rows (based on region)
whitelist = ['at', 'as', '','in','the','and', 'or', 'not', 'a', 'on', 'an', 'of', 'with', 'plus', 'over', '*', '(', ')', '[', ']', '-', '+', '/', 'any', 'along', 'is', 'year', 'years', 'year(s)', 'this', 'that', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'we', 'are', 'center', 'u', 'problem', 'solving', 'inbound', 'technical', '&', 'skill', 'set', "troubleshooting", "customer", "basic", "calls", "issues", "aptitude", "care", "outbound", "presentation", "relationship", "and/or", "people", "verbal", "written", "company", "full", "writing", "regulations","sr","jr", "training", "domain", "security", "global", "site", "environment;", "experience", "active", "model;", "administration;communicate", "maintaining", "troubleshooting", "business", "00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "15", "20", "25", "0+", "1+", "2+", "3+", "4+", "5+", "6+", "7+", "8+", "9+", "10+", "15+", "20+", "25+", "1.0", "4.5", "thorough", "multiple", "skills", "to", "directory", "in-person", "users;create", "documents", "users;provide", "advanced", "sites", "oversight", "required", "applications", "systems", "for", "supplier", "clearance", "secret", "military", "designing", "using", "language", "Natural", "complex", "environment", "environment.", "applications", "tuning", "gate", "experience", "well", "version", "yrs", "degree", "either", "primary", "focus", "development", "keywords:", "group", "software", "custom", "parts", "use", "communication", "excellent", "cycle", "solid", "intelligence", "life", "application", "requirements", "test", "cases", "preferred", "other", "specialist", "device", "driver", "applicable", "hands", "requires", "equivalent", "must", "salesforce.c", "techniques", "live", "senior", "junior", "lead", "big", "first", "minimum", "broad", "in-depth", "related", "area", "recent", "strong", "growing", "relevant", "building", "relationa", "structured", "proven", "field", "solutions", "star", "45", "components", "science", "position", "computer", "bachelor", "bachelors", "bs", "write", "3-5", "2-5", "automate", "line", "technologies", "30", "null", "40", "trade", "shows","state", "local", "structured", "practices", "bachelor s", "standard", "w", "analys", "minimum", "mid-level", "work", "internals", "international", "multi-cultural", "implementation", "etc", "them", "team", "work", "positive", "mentor", "members", "supervise", "contractors", "motivate", "take", "assigned", "accountability", "action", "influence", "their", "many", "wide", "golden", "driven", "commercial", "above", "seeking co-founders", "out", "should", "have", "general", "about", "similar", "based", "through", "preferably", "role", "basics", "solution", "concepts", "oriented", "change", "below", "details", "see", "worksite", "description", "project", "execution", "implementaion", "into", "helpful", "entering", "cost", "transactional", "disposition", "implementation", "review", "contractual", "payble", "contractual", "proposals", "audit", "hand", "such", "including", "challenging", "throughput", "enbler", "good", "great", "creds", "self", "impressive", "flexible", "internships", "blogging", "1213", "bound", "modules", "tele", "tools", "code", "24", "5-15", "from", "commands", "6500", "7600", "75", "andy", "certified", "plans", "2010", "2013", "2000", "2003", "estate", "mergers",  "real", "7-10", "4-5", "5-7", "2-3", "all", "major", "minor", "working", "description", "job", "2008", "gathering", "mid", "510k", "master s", "human", "generalist", "specialist", "resources", "professional", "against", "ava", "progressively", "within", "benefit", "benefits", "policies", "you ll", "like", "queues", "ideally", "income", "front", "fixed", "stored", "Allen", "pro", "12x", "rich", "core", "large", "manner", "direct", "clients", "activities", "inside", "schedule", "able", "3-0", "35", "can", "following", "months", "be", "intern", "extern", "external", "internal", "experiene", "open", "cancelation", "practical", "account", "process", "extension", "packaged", "document", "methodologies", "investment", "nose", "ad-hoc", "specialization", "incentives", "incentive", "staffing", "staff", "hands-on", "expert", "level", "reviewing", "accounts", "expertise", "approval", "board", "impedance", "2nd", "also", "migration", "activating", "end", "3rd", "provide", "support", "shared", "users", "phone", "resource", "held", "prefer", "devices", "person", "assistance", "scripting", "unified", "develop", "execute", "locations", "---", "validat", "troubleshoot", "some", "compents", "entry", "associated", "seeting", "directly", "eg", "2005+", "import", "russian", "2005", "higher", "desired", "also", "left-hand", "order", "needed", "previous", "product", "city", "interest", "player", "1-2", "least", "new", "requests", "rollout", "candidate", "certification", "surrounding", "executing", "industrial", "follow", "decisions", "availability", "discipline", "current", "thinking", "languages", "entities", "coaching", "supporting", "developed", "various", "routing", "recompile", "very", "possible", "balancing", "background", "procedures", "switches", "subsidiaries", "adhering", "banking", "each", "analytical", "essential", "accessible", "6K", "financial", "methods", "profiling", "phone", "audits", "best", "phases", "on-demand", "factors", "proficient", "while", "research", "access", "external", "across", "be", "transaction", "ability", "parent", "processing", "affiliates", "understanding", "desired", "leadership", "mentoring", "packages", "swift", "verifiable", "both", "certifications", "high", "shift", "compliance", "outside-the-box", "addition", "periodic", "tactical", "operating", "backup", "processor", "load", "completion", "via", "manage", "environments", "strategic", "clear", "least", "backups", "specializing", "facilitative", "detail-oriented", "service", "shells", "multilayer", "objectives", "support", "fast", "next", "call", "teamwork", "more", "releases", "fundamentals", "banking", "goals", "fail-over", "analyst", "sound", "organizations", "7-9", "graphic", "F5", "theories", "will", "expertise", "demonstrate", "outing", "proactive", "process", "7k", "candidates", "analysis", "need", "demonstration", "functions", "recovery", "provide", "make", "storage", "detail", "recommended", "simultaneous", "functionality", "achieving", "hop", "extremely", "switching", "exemplify", "independent", "product", "collaborative", "specifications", "clear", "time", "4k", "judgment", "ability", "remote", "sets", "instruments", "failover", "documentation", "lines", "supervision", "enterprise", "management", "travel", "paced", "minimal"
]
whitelist = list(set(whitelist))

#corruptRows = scraperwiki.sqlite.execute("SELECT count(*) FROM company_data WHERE tags like 'u %';")
print "Starting to correct database (tags): ALL"#, corruptRows["data"][0]
corruptRows = scraperwiki.sqlite.select("* FROM company_data;")

for row in corruptRows:
    if row["tags"] == None or row["tags"] == "": continue
    cleanTags = []
    for tag in json.loads(row["tags"]):
        tag = tag.replace("AND(","").replace("(","").replace(")","").replace(";","") # warn: no "." or ":" due to "vert.x"
        if tag != "PL/SQL" and tag != "C/C++" and tag != "TCP/IP"  and tag != "COM/DCOM" and "/" in tag:
            subTags = tag.split("/")
            for subTag in subTags:
                cleanTags.append(subTag.strip())
        else:
            tag= re.sub("^-",  "", tag)
            tag= re.sub("^u ", "", tag)
            tag= re.sub("\.$", "", tag)
            tag= re.sub("-$",  "", tag)
#            tag= re.sub("[/\*]$", "", tag)
            cleanTags.append(tag.strip())
    cleanTags   = [x for x in cleanTags if x.lower() not in whitelist]
    cleanTags   = list(set(cleanTags))
    row["tags"] = json.dumps(cleanTags)

    regionText = row["region"]
    if (regionText.count(',') < 3 and regionText.lower() != "usa" and regionText.lower() != "deutschland") or regionText.endswith("USA"):
        scraperwiki.sqlite.save(["id"], data=row, table_name='company_data', verbose=0)
    else:
#        print "Removing row :", row["id"], " with region:", regionText
#        if not regionText.endswith("USA"): # exclude regions such as "New York County, New York, NY, USA"
        scraperwiki.sqlite.execute("DELETE FROM company_data WHERE id=" + str(row["id"]))
        scraperwiki.sqlite.commit()

print "The End."

# Info
allRows = scraperwiki.sqlite.execute('SELECT count(*) FROM company_data;')
scraperwiki.sqlite.commit()
print "Count of all companies was: ", allRows["data"][0]

sys.exit()

