#this is forked off from the original version so I can create a list of missing sids so that i can then get their basic info quickly. rather than entering it in by hand
import scraperwiki

def getbasicLink():
    parturl = "http://www.fsa.gov.uk/register/psdFirmBasicDetails.do?sid="
    sidlist = [274223,296686,301022,316406]

    for d in sidlist:
        basicurl = parturl+str(d)
        scraperwiki.sqlite.save(unique_keys=["SID"], data={"SID": d, "Url": basicurl}, table_name = 'BasicUrl')

try:
    scraperwiki.sqlite.execute("create table BasicUrl(SID string, Url string)")
except:
    print "Table already exists."

getbasicLink()





#this is forked off from the original version so I can create a list of missing sids so that i can then get their basic info quickly. rather than entering it in by hand
import scraperwiki

def getbasicLink():
    parturl = "http://www.fsa.gov.uk/register/psdFirmBasicDetails.do?sid="
    sidlist = [274223,296686,301022,316406]

    for d in sidlist:
        basicurl = parturl+str(d)
        scraperwiki.sqlite.save(unique_keys=["SID"], data={"SID": d, "Url": basicurl}, table_name = 'BasicUrl')

try:
    scraperwiki.sqlite.execute("create table BasicUrl(SID string, Url string)")
except:
    print "Table already exists."

getbasicLink()





