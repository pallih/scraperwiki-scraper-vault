import scraperwiki
import lxml.html



#SETUP
baseurl = 'http://eciresults.ap.nic.in/Constituencywise'
constituency_xpath = '//form/div/input [@id = "HdnFldTripura"]'
result_xpath = '//table[@width="100%"]//table[@width="50%"]//table/tr' #this is probably not good performance wise - but fine for now

# This is the state code for Tripura
state = 's23' 
states = {'Tripura':'s23'}

#DEFS
def process_constituency(number, constituency):
    record = {}
    record['constituency'] = constituency
    print 'Processing ', constituency
    html = scraperwiki.scrape(baseurl+state+number+'.htm')
    root = lxml.html.fromstring(html)
    results = root.xpath (result_xpath)
    #for x in results[3:5]: #skip the first 3 tr's and get the top 2
    for x in results[3:-1]: #skip the first 3 tr's and the last one
        record['candidate'] = x[0].text
        record['party'] = x[1].text
        record['votes'] =  x[2].text
        #print record
        scraperwiki.sqlite.save(unique_keys=['candidate', 'constituency'], data=record, table_name='tripura-elections')   
    

#######################

#Scrape the first page to get the list of constituencies
html = scraperwiki.scrape('http://eciresults.ap.nic.in/ConstituencywiseS236.htm')

#The list of constituencies for Himachal is in this markup:
# <input type="hidden" id="hdnFldHimachal" value=

#Lets get that list with values to add to our baseurl


root = lxml.html.fromstring(html)
content = root.xpath (constituency_xpath)

for c in content:
    constituencies = c.attrib['value']


# A list of numbers and the name of the constituency
constituencies = constituencies.split(';')

# And now we iterate through the list
for c in constituencies:
    #print 'Processing Srini', c
    if c != '':
        process_constituency( c.split(',')[0].strip(),c.split(',')[1] )

import scraperwiki
import lxml.html



#SETUP
baseurl = 'http://eciresults.ap.nic.in/Constituencywise'
constituency_xpath = '//form/div/input [@id = "HdnFldTripura"]'
result_xpath = '//table[@width="100%"]//table[@width="50%"]//table/tr' #this is probably not good performance wise - but fine for now

# This is the state code for Tripura
state = 's23' 
states = {'Tripura':'s23'}

#DEFS
def process_constituency(number, constituency):
    record = {}
    record['constituency'] = constituency
    print 'Processing ', constituency
    html = scraperwiki.scrape(baseurl+state+number+'.htm')
    root = lxml.html.fromstring(html)
    results = root.xpath (result_xpath)
    #for x in results[3:5]: #skip the first 3 tr's and get the top 2
    for x in results[3:-1]: #skip the first 3 tr's and the last one
        record['candidate'] = x[0].text
        record['party'] = x[1].text
        record['votes'] =  x[2].text
        #print record
        scraperwiki.sqlite.save(unique_keys=['candidate', 'constituency'], data=record, table_name='tripura-elections')   
    

#######################

#Scrape the first page to get the list of constituencies
html = scraperwiki.scrape('http://eciresults.ap.nic.in/ConstituencywiseS236.htm')

#The list of constituencies for Himachal is in this markup:
# <input type="hidden" id="hdnFldHimachal" value=

#Lets get that list with values to add to our baseurl


root = lxml.html.fromstring(html)
content = root.xpath (constituency_xpath)

for c in content:
    constituencies = c.attrib['value']


# A list of numbers and the name of the constituency
constituencies = constituencies.split(';')

# And now we iterate through the list
for c in constituencies:
    #print 'Processing Srini', c
    if c != '':
        process_constituency( c.split(',')[0].strip(),c.split(',')[1] )

