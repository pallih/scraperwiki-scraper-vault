import scraperwiki
import lxml.html
from lxml import etree

#delete the datastore and check url1's parameters before running
#search is 'Oxford' during testing as this returns a smaller number of results than 'London'

def getLink(row):#taken from https://scraperwiki.com/scrapers/tmp3world-1/
    ''' The getLink function gets a row and returns link '''
    link = row.cssselect('a')
    return link[0].get('href')



#run an initial query embedded in the url (TWEAK THIS TO CHANGE RESULT SET) 
url1="http://www.ukctg.nihr.ac.uk/search?query=nation:England+location:Oxford+status:Recruiting&resultsfrom=1&resultsto=10&advanced=true&pagesize=10"

#get the total number of query results from the webpage
html1= scraperwiki.scrape(url1) 
root = lxml.html.fromstring(html1)
el = root.cssselect("div#colwide strong")[0] #get the first strong element in the div named colwide - this happens to be the number of results returned by the search
totalresults = el.text
totalresults = "".join(totalresults.split())#element returns with lots of white space - removed here
print "Total search results: %s " %totalresults

#this site allows you to specify apparently arbitrary numbers of results on a single returned page so interpolate total into url
url2="http://www.ukctg.nihr.ac.uk/search?query=nation:England+location:Oxford+status:Recruiting&resultsfrom=1&resultsto=%s&advanced=true&pagesize=10" %totalresults

#get all results on one page - you can expect this to take a while
html2= scraperwiki.scrape(url2)

#putting this into root overwrites original variable contents and thus reduces memory requirement?
root = lxml.html.fromstring(html2)
tds = root.cssselect('td') # get all the <td> tags
for tr in root.cssselect("table[id='resultstable'] tr"):
    tds = tr.cssselect("td")
    if len(tds)==5:
        data = {
            'condition' : tds[0].text_content().strip(),#numbers in square brackets are the columns from left
            'public_title' : tds[2].text_content().strip(),
            'location' : tds[3].text_content().strip(),
            'reference' : getLink(tr)[14:]#skip first 14 chars of link value - a directory name in this case
        }
        scraperwiki.sqlite.save(unique_keys=['reference'], data=data)
import scraperwiki
import lxml.html
from lxml import etree

#delete the datastore and check url1's parameters before running
#search is 'Oxford' during testing as this returns a smaller number of results than 'London'

def getLink(row):#taken from https://scraperwiki.com/scrapers/tmp3world-1/
    ''' The getLink function gets a row and returns link '''
    link = row.cssselect('a')
    return link[0].get('href')



#run an initial query embedded in the url (TWEAK THIS TO CHANGE RESULT SET) 
url1="http://www.ukctg.nihr.ac.uk/search?query=nation:England+location:Oxford+status:Recruiting&resultsfrom=1&resultsto=10&advanced=true&pagesize=10"

#get the total number of query results from the webpage
html1= scraperwiki.scrape(url1) 
root = lxml.html.fromstring(html1)
el = root.cssselect("div#colwide strong")[0] #get the first strong element in the div named colwide - this happens to be the number of results returned by the search
totalresults = el.text
totalresults = "".join(totalresults.split())#element returns with lots of white space - removed here
print "Total search results: %s " %totalresults

#this site allows you to specify apparently arbitrary numbers of results on a single returned page so interpolate total into url
url2="http://www.ukctg.nihr.ac.uk/search?query=nation:England+location:Oxford+status:Recruiting&resultsfrom=1&resultsto=%s&advanced=true&pagesize=10" %totalresults

#get all results on one page - you can expect this to take a while
html2= scraperwiki.scrape(url2)

#putting this into root overwrites original variable contents and thus reduces memory requirement?
root = lxml.html.fromstring(html2)
tds = root.cssselect('td') # get all the <td> tags
for tr in root.cssselect("table[id='resultstable'] tr"):
    tds = tr.cssselect("td")
    if len(tds)==5:
        data = {
            'condition' : tds[0].text_content().strip(),#numbers in square brackets are the columns from left
            'public_title' : tds[2].text_content().strip(),
            'location' : tds[3].text_content().strip(),
            'reference' : getLink(tr)[14:]#skip first 14 chars of link value - a directory name in this case
        }
        scraperwiki.sqlite.save(unique_keys=['reference'], data=data)
