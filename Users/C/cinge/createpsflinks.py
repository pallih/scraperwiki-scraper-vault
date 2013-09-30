import scraperwiki

scraperwiki.sqlite.attach("psfscraper")
data = scraperwiki.sqlite.select("* from psfscraper.Firms order by SID")

def getbasicLink (data):
    parturl = "http://www.fsa.gov.uk/register/psdFirmBasicDetails.do?sid="
    for d in data:
        basicurl = parturl+str(d["SID"])
        scraperwiki.sqlite.save(unique_keys=["SID"], data={"SID": d["SID"], "Url": basicurl}, table_name = 'BasicUrl')

try:
    scraperwiki.sqlite.execute("create table BasicUrl(SID string, Url string)")
except:
    print "Table already exists."

getbasicLink (data)





import scraperwiki

scraperwiki.sqlite.attach("psfscraper")
data = scraperwiki.sqlite.select("* from psfscraper.Firms order by SID")

def getbasicLink (data):
    parturl = "http://www.fsa.gov.uk/register/psdFirmBasicDetails.do?sid="
    for d in data:
        basicurl = parturl+str(d["SID"])
        scraperwiki.sqlite.save(unique_keys=["SID"], data={"SID": d["SID"], "Url": basicurl}, table_name = 'BasicUrl')

try:
    scraperwiki.sqlite.execute("create table BasicUrl(SID string, Url string)")
except:
    print "Table already exists."

getbasicLink (data)





