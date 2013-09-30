import scraperwiki
import urllib2
import csv

# these four lines of code will parse any normal csv file on the web
url = "http://www.sidra.ibge.gov.br/bda/territorio/tabunit.asp?t=1&n=6&z=t&o=4"
f = urllib2.urlopen(url)
lines = f.readlines()
clist = list(csv.reader(lines))

# normally the first row is the header and the rest is the data
headers = clist[0]
print "The headers are:", headers
print "There are %d rows" % (len(clist) - 1)

# save each data record into the database
for rownumber in range(1, len(clist)):
    data = dict(zip(headers, clist[rownumber]))

    # unless you can see an obvious record index in your file 
    # you will need to index by row number
    data["rownumber"] = rownumber
    data["source"] = url

    scraperwiki.sqlite.save(unique_keys=["source", "rownumber"], data=data)









# ignore this bit, which generates the data
#
#def AddSomeData():
#    import scraperwiki
#    scraperwiki.datastore.save(unique_keys=["Name"], data={"Name":"Smith, John", "Phone number":99999}) 
#    for n in range(4, 15):
#        scraperwiki.datastore.save(unique_keys=["Name"], data={"Name":"Suzie %d" % n, "Phone number":10000+n})
#AddSomeData()
import scraperwiki
import urllib2
import csv

# these four lines of code will parse any normal csv file on the web
url = "http://www.sidra.ibge.gov.br/bda/territorio/tabunit.asp?t=1&n=6&z=t&o=4"
f = urllib2.urlopen(url)
lines = f.readlines()
clist = list(csv.reader(lines))

# normally the first row is the header and the rest is the data
headers = clist[0]
print "The headers are:", headers
print "There are %d rows" % (len(clist) - 1)

# save each data record into the database
for rownumber in range(1, len(clist)):
    data = dict(zip(headers, clist[rownumber]))

    # unless you can see an obvious record index in your file 
    # you will need to index by row number
    data["rownumber"] = rownumber
    data["source"] = url

    scraperwiki.sqlite.save(unique_keys=["source", "rownumber"], data=data)









# ignore this bit, which generates the data
#
#def AddSomeData():
#    import scraperwiki
#    scraperwiki.datastore.save(unique_keys=["Name"], data={"Name":"Smith, John", "Phone number":99999}) 
#    for n in range(4, 15):
#        scraperwiki.datastore.save(unique_keys=["Name"], data={"Name":"Suzie %d" % n, "Phone number":10000+n})
#AddSomeData()
