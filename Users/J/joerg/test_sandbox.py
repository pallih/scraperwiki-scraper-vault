import scraperwiki
import lxml.etree
import lxml.html
import time
from itertools import groupby
import re

# Blank Python
scraperwiki.sqlite.execute("drop table if exists swdata")

myList = ["Alpha", "Beta", "Gamma", "Alpha", "", '']
print myList, type(myList )

import pickle
listPickled = pickle.dumps(myList )
list1= pickle.loads(listPickled)
print "\nPickle:"
print listPickled, type(listPickled) 
print list1, type(list1)
print list(set(list1))

import json
listJSON= json.dumps(myList)
list2 = json.loads(listJSON)# Return a Unicode List
list2 = [s.encode('utf-8') for s in list2 ]
print "\nJSON:"
print listJSON, type(listJSON)
print list2, type(list2)
print list(set(list2))

record = {}
record["id"] = 1
record["list"] = myList
record["listJSON"] = json.dumps(myList)
record["listStr1"] = '"Alpha", "Beta", "Gamma", "Alpha"'
record["listStr2"] = 'Alpha,Beta,Gamma,Alpha'
record["newList1"] = ""
record["newList2"] = []
record["newList3"] = [""]
scraperwiki.sqlite.save(["id"], record)
rows = scraperwiki.sqlite.select( '''* from swdata''' )
print "list",     rows[0]["list"],     type(rows[0]["list"])
print "listJSON", rows[0]["listJSON"], type(rows[0]["listJSON"])
print "listStr1", rows[0]["listStr1"], type(rows[0]["listStr1"])
print "listStr2", rows[0]["listStr2"], type(rows[0]["listStr2"])

#print "list",     json.loads(rows[0]["list"]),     type(json.loads(rows[0]["list"]))
print "listJSON", json.loads(rows[0]["listJSON"]), type(json.loads(rows[0]["listJSON"]))
print "listUTF8", [s.encode('utf-8') for s in json.loads(rows[0]["listJSON"])], type([s.encode('utf-8') for s in json.loads(rows[0]["listJSON"])])
#print "listStr1", json.loads(rows[0]["listStr1"]), type(json.loads(rows[0]["listStr1"]))
#print "listStr2", json.loads(rows[0]["listStr2"]), type(json.loads(rows[0]["listStr2"]))

print len(rows[0]["newList1"]), rows[0]["newList1"]
print len(rows[0]["newList2"]), rows[0]["newList2"]
print len(rows[0]["newList3"]), rows[0]["newList3"]

skillList     = rows[0]["listStr2"].replace("[","").replace("]","").split(',') # Read string from DB and convert into list
compactedList = list(set(skillList))                                     # Remove Duplicates
while "" in compactedList: compactedList.remove("")                      # Remove empty entries (e.g. '')
skillListUTF8 = [s.encode('utf-8') for s in compactedList]               # Convert Unicode into UTF-8
print skillListUTF8


record = {}
record["id"] = 123
record["key1"] = "OldValue1"
record["key2"] = "OldValue2"
record["key3"] = "OldValue3"
scraperwiki.sqlite.save(["id"], record)

record["key1"] = "NewValue1"
record["key2"] = None
scraperwiki.sqlite.save(["id"], record)

for aList in myList:
    if True: 
        print "next"
        continue
    print "not next"

testString1 = "- This - is a -Test-for regex"
testString2 = " - This - is a -Test-for regex"
print re.sub("^- ", "", testString1).strip()
print re.sub("^- ", "", testString2).strip()

#scraperwiki.sqlite.execute("DELETE FROM swdata WHERE (newList1 IS NULL)")
#scraperwiki.sqlite.execute("DELETE FROM swdata WHERE (newList1='')")
#scraperwiki.sqlite.commit()
