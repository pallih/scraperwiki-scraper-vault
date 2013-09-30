import scraperwiki

superdictionary = {}
superlist       = []


superdictionary['1'] = {"a":1, "b":"Foo"}

string = "c"
string2 = "d"
superdictionary['1'].update({string:"Bar"})
superdictionary['1'].update({string2:"asBar"})


akey = 3
superdictionary[akey] = {"a":2, "b":"Grue", "c":"Gnu"}
superdictionary[akey].update({string2:"asBardeof"})


for subdictionary in superdictionary:
    superlist.append(superdictionary[subdictionary])

print superlist[1]
print superlist[0]

print superlist
print "------------"

print superdictionary[akey]

scraperwiki.sqlite.save(["a"], superlist)

#    scraperwiki.sqlite.save(unique_keys=["link"], data={"link":url, "title":title, "date":date, "replies":total_replies, a:b})
import scraperwiki

superdictionary = {}
superlist       = []


superdictionary['1'] = {"a":1, "b":"Foo"}

string = "c"
string2 = "d"
superdictionary['1'].update({string:"Bar"})
superdictionary['1'].update({string2:"asBar"})


akey = 3
superdictionary[akey] = {"a":2, "b":"Grue", "c":"Gnu"}
superdictionary[akey].update({string2:"asBardeof"})


for subdictionary in superdictionary:
    superlist.append(superdictionary[subdictionary])

print superlist[1]
print superlist[0]

print superlist
print "------------"

print superdictionary[akey]

scraperwiki.sqlite.save(["a"], superlist)

#    scraperwiki.sqlite.save(unique_keys=["link"], data={"link":url, "title":title, "date":date, "replies":total_replies, a:b})
