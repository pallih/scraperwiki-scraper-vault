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

skipsearches = 1
skiprecords = 1

baseurl = 'http://www.freereg.org.uk/cgi/'
surnames = ['Skynner', 'Skinner', 'Skiner']

page = scraperwiki.scrape(baseurl + "Search.pl")
root = lxml.html.fromstring(page)

radios = root.cssselect("input[name='RecordType']")
recordtypes = [y.get('value') for y in radios]

options = root.cssselect("select[name='County'] option")
countys = [y.get('value') for y in options]

data = {}
myerrors = 0
myskips = 0
myadded = 0

mysql = "SurnameRecordtypeCounty from Searches"
presearches = scraperwiki.sqlite.select(mysql)


for recordtype in recordtypes:
    mysql = "Url from " + recordtype
    predata = scraperwiki.sqlite.select(mysql)

    for surname in surnames:

        for county in countys:
            searchdata = {'SurnameRecordtypeCounty': (surname + recordtype + county)}
            if searchdata in presearches and skipsearches:
                myskips = myskips + 1
                print(myskips, " Skipped ", surname, recordtype, county)
                continue

            try:
                page = scraperwiki.scrape("http://www.freereg.org.uk/cgi/Search.pl", {'RecordType':recordtype, 'Surname':surname, 'County':county, 'Action':"Search" } ) 
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
                                        else:

                                            scraperwiki.sqlite.save(unique_keys=['Url'], data=data, table_name=recordtype)
                                            myadded = myadded + 1
                                            print myadded, recordtype, surname, county
            scraperwiki.sqlite.save(unique_keys=['SurnameRecordtypeCounty'], data=searchdata, table_name='Searches')

print "Error Count = ", myerrors
print "Skipped Count = ", myskips
print "Added Count = ", myadded