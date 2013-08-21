##########################
# Be gentle. 2 days ago i had never programed with python before
#
# this program scrapes the freereg.org.uk geneology site for all
#    entries in any combination of surname, recordtype & county
#
##########################

import scraperwiki
import lxml.html 
import httplib2
from BeautifulSoup import BeautifulSoup, SoupStrainer
import re
import itertools

skipsearches = 1 #1 to skip previous searches
skiprecords = 1 #1 to skip previous result records
maxcountys = 10 #max countys to search for with every cycle. currently 10
baseurl = 'http://www.freereg.org.uk/cgi/'
surnames = ['Skinner', 'Skynner', 'Skiner']
forename = ''

def mygrouper(n, iterable):
    args = [iter(iterable)] * n
    return list(([e for e in t if e != None] for t in itertools.izip_longest(*args)))

page = scraperwiki.scrape(baseurl + "Search.pl")
root = lxml.html.fromstring(page)




radios = root.cssselect("input[name='RecordType']")
recordtypes = [y.get('value') for y in radios]

options = root.cssselect("select[name='County'] option")
allcountys = [y.get('value') for y in options]
countys = mygrouper(maxcountys,allcountys)

data = {}
myerrors = 0
myskips = 0
myadded = 0

allsurnames = "".join(str(x) for x in surnames)

mysql = "SurnameRecordtypeCounty from Searches"
try:
    presearches = scraperwiki.sqlite.select(mysql)
except:
    presearches = []


for recordtype in recordtypes:
    for surname in surnames:
        mysql = "Url from " + forename + allsurnames
        try:
            predata = scraperwiki.sqlite.select(mysql)
        except:
            predata = []


        for county in countys:
            searchurl = baseurl + "Search.pl?RecordType=" + recordtype + "&Surname=" + surname + "&Forename=" + forename + "&Action=Search&County=" + "&County=".join(str(x) for x in county)
            countyonlystr = "".join(str(x) for x in county)
            searchdata = {'SurnameRecordtypeCounty': (forename + surname + recordtype + countyonlystr)}
            if searchdata in presearches and skipsearches:
                myskips = myskips + 1
                print(myskips, " Skipped ", surname, recordtype, county)
                continue

            try:
                if forename:
                    print "did forname "
                    page = scraperwiki.scrape(searchurl) 
                else:
                    print "Trying ", searchurl
                    page = scraperwiki.scrape(searchurl)
#                    page = scraperwiki.scrape("http://www.freereg.org.uk/cgi/Search.pl", {'RecordType':recordtype, 'Surname':surname, 'County':county, 'Action':"Search" } )
            except:
                myerrors = myerrors + 1
                print "error ", myerrors, " failed to open search Url for ", recordtype, county, surname
                continue
            else:
                
                
                for link in BeautifulSoup(page, parseOnlyThese=SoupStrainer('a')):
                    if link.has_key('href'): 
                        if '&RecordID=' in link['href']:
                            recurl = link['href'].replace('./',baseurl)
                            recline = {'Url': recurl}
                            if recline in predata and skiprecords:
                                myskips = myskips + 1
                                print(myskips, " Skipped " + recurl)
                            else:
                                try:
                                    page = scraperwiki.scrape(recurl)
                                except:
                                    myerrors = myerrors + 1
                                    print myerrors, " failed to open record ", recurl
                                    continue
                                else:
                                    root = lxml.html.fromstring(page)
                                    data.clear()
                                    data['Type'] = recordtype
                                    data['Url'] = str(recurl)
                                    for tr in root.cssselect("table[border='1'] tr"):
                                        tds = tr.cssselect("td")
                                        try:
                                            if tds[1].text_content():
                                                data[str(tds[0].text_content())] = str(tds[1].text_content())
                                            else:
                                                data[str(tds[0].text_content())] = ""
                                        except:
                                            continue
                                    scraperwiki.sqlite.save(unique_keys=['Url'], data=data, table_name=(forename + allsurnames))
                                    myadded = myadded + 1
                                    print myadded, recordtype, surname, countyonlystr
            scraperwiki.sqlite.save(unique_keys=['SurnameRecordtypeCounty'], data=searchdata, table_name='Searches')

print "Error Count = ", myerrors
print "Skipped Count = ", myskips
print "Added Count = ", myadded