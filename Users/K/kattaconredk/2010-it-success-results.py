import urllib
import csv

# fill in the input file here
url = "http://en.wikipedia.org/wiki/Forbes_Global_2000"

fin = urllib.urlopen(url)
lines = fin.readlines()
for line in lines:
    print line

clist = list(csv.reader(lines))
print clist

headers = clist.pop(0)
print "There are %d columns and %d rows" % (len(headers), len(clist))
print "Headers:", headers

for row in clist[:10]:
    print dict(zip(headers, row))


def AddSomeData():
    import scraperwiki
    scraperwiki.datastore.save(unique_keys=["Rank"], data={"Rank":"1","Company Name":"JP Morgan Chase", "Head Quarters":"USA","Industry":"Banking","Revenue(billions$)":"115.63","Profit(billions$)":"11.65","Assets(billions$)":"2,031.99","Market value(billions$)":"166.19"}) 

    scraperwiki.datastore.save(unique_keys=["Rank"], data={"Rank":"2","Company Name":"General Electrical", "Head Quarters":"USA","Industry":"Conglomerate","Revenue(billions$)":"156.78","Profit(billions$)":"11.03","Assets(billions$)":"781.82","Market value(billions$)":"169.65"}) 

    scraperwiki.datastore.save(unique_keys=["Rank"], data={"Rank":"3","Company Name":"Bank of America", "Head Quarters":"USA","Industry":"Banking","Revenue(billions$)":"150.45","Profit(billions$)":"6.28","Assets(billions$)":"2,223.30","Market value(billions$)":"167.63"})
 
    scraperwiki.datastore.save(unique_keys=["Rank"], data={"Rank":"4","Company Name":"ExxonMobil", "Head Quarters":"USA","Industry":"Oil and Gas","Revenue(billions$)":"275.56","Profit(billions$)":"19.28","Assets(billions$)":"233.32","Market value(billions$)":"308.77"})

    scraperwiki.datastore.save(unique_keys=["Rank"], data={"Rank":"5","Company Name":"ICBC", "Head Quarters":"China","Industry":"Banking","Revenue(billions$)":"71.86","Profit(billions$)":"16.27","Assets(billions$)":"1,428.46","Market value(billions$)":"242.23"})

    scraperwiki.datastore.save(unique_keys=["Rank"], data={"Rank":"6","Company Name":"Banco Santander", "Head Quarters":"Spain","Industry":"Banking","Revenue(billions$)":"109.57","Profit(billions$)":"12.34","Assets(billions$)":"1,438.68","Market value(billions$)":"107.12"})

    scraperwiki.datastore.save(unique_keys=["Rank"], data={"Rank":"7","Company Name":"Wells Fargo", "Head Quarters":"USA","Industry":"Banking","Revenue(billions$)":"98.64","Profit(billions$)":"12.28","Assets(billions$)":"1,243.65","Market value(billions$)":"141.69"})

    scraperwiki.datastore.save(unique_keys=["Rank"], data={"Rank":"8","Company Name":"HSBC", "Head Quarters":"UK","Industry":"Banking","Revenue(billions$)":"103.74","Profit(billions$)":"5.83","Assets(billions$)":"2,355.83","Market value(billions$)":"178.27"})

    scraperwiki.datastore.save(unique_keys=["Rank"], data={"Rank":"9","Company Name":"Royal Dutch Shell", "Head Quarters":"NL/UK","Industry":"Oil and Gas","Revenue(billions$)":"278.19","Profit(billions$)":"12.52","Assets(billions$)":"287.64","Market value(billions$)":"168.63"})

    scraperwiki.datastore.save(unique_keys=["Rank"], data={"Rank":"10","Company Name":"BP", "Head Quarters":"UK","Industry":"Oil and Gas","Revenue(billions$)":"239.27","Profit(billions$)":"16.58","Assets(billions$)":"235.45","Market value(billions$)":"167.13"})

AddSomeData()

import urllib
import csv

# fill in the input file here
url = "http://en.wikipedia.org/wiki/Forbes_Global_2000"

fin = urllib.urlopen(url)
lines = fin.readlines()
for line in lines:
    print line

clist = list(csv.reader(lines))
print clist

headers = clist.pop(0)
print "There are %d columns and %d rows" % (len(headers), len(clist))
print "Headers:", headers

for row in clist[:10]:
    print dict(zip(headers, row))


def AddSomeData():
    import scraperwiki
    scraperwiki.datastore.save(unique_keys=["Rank"], data={"Rank":"1","Company Name":"JP Morgan Chase", "Head Quarters":"USA","Industry":"Banking","Revenue(billions$)":"115.63","Profit(billions$)":"11.65","Assets(billions$)":"2,031.99","Market value(billions$)":"166.19"}) 

    scraperwiki.datastore.save(unique_keys=["Rank"], data={"Rank":"2","Company Name":"General Electrical", "Head Quarters":"USA","Industry":"Conglomerate","Revenue(billions$)":"156.78","Profit(billions$)":"11.03","Assets(billions$)":"781.82","Market value(billions$)":"169.65"}) 

    scraperwiki.datastore.save(unique_keys=["Rank"], data={"Rank":"3","Company Name":"Bank of America", "Head Quarters":"USA","Industry":"Banking","Revenue(billions$)":"150.45","Profit(billions$)":"6.28","Assets(billions$)":"2,223.30","Market value(billions$)":"167.63"})
 
    scraperwiki.datastore.save(unique_keys=["Rank"], data={"Rank":"4","Company Name":"ExxonMobil", "Head Quarters":"USA","Industry":"Oil and Gas","Revenue(billions$)":"275.56","Profit(billions$)":"19.28","Assets(billions$)":"233.32","Market value(billions$)":"308.77"})

    scraperwiki.datastore.save(unique_keys=["Rank"], data={"Rank":"5","Company Name":"ICBC", "Head Quarters":"China","Industry":"Banking","Revenue(billions$)":"71.86","Profit(billions$)":"16.27","Assets(billions$)":"1,428.46","Market value(billions$)":"242.23"})

    scraperwiki.datastore.save(unique_keys=["Rank"], data={"Rank":"6","Company Name":"Banco Santander", "Head Quarters":"Spain","Industry":"Banking","Revenue(billions$)":"109.57","Profit(billions$)":"12.34","Assets(billions$)":"1,438.68","Market value(billions$)":"107.12"})

    scraperwiki.datastore.save(unique_keys=["Rank"], data={"Rank":"7","Company Name":"Wells Fargo", "Head Quarters":"USA","Industry":"Banking","Revenue(billions$)":"98.64","Profit(billions$)":"12.28","Assets(billions$)":"1,243.65","Market value(billions$)":"141.69"})

    scraperwiki.datastore.save(unique_keys=["Rank"], data={"Rank":"8","Company Name":"HSBC", "Head Quarters":"UK","Industry":"Banking","Revenue(billions$)":"103.74","Profit(billions$)":"5.83","Assets(billions$)":"2,355.83","Market value(billions$)":"178.27"})

    scraperwiki.datastore.save(unique_keys=["Rank"], data={"Rank":"9","Company Name":"Royal Dutch Shell", "Head Quarters":"NL/UK","Industry":"Oil and Gas","Revenue(billions$)":"278.19","Profit(billions$)":"12.52","Assets(billions$)":"287.64","Market value(billions$)":"168.63"})

    scraperwiki.datastore.save(unique_keys=["Rank"], data={"Rank":"10","Company Name":"BP", "Head Quarters":"UK","Industry":"Oil and Gas","Revenue(billions$)":"239.27","Profit(billions$)":"16.58","Assets(billions$)":"235.45","Market value(billions$)":"167.13"})

AddSomeData()

