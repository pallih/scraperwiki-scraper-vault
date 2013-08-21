import scraperwiki
import lxml.html



#SETUP
baseurl = 'http://eciresults.ap.nic.in/Constituencywise'
constituency_xpath = '//form/div/input [@id = "HdnFldUttarPradesh"]'
result_xpath = '//table[@width="100%"]//table[@width="50%"]//table/tr' #this is probably not good performance wise - but fine for now

# This is the state code for Uttar Pradesh
state = 's24' 
#Other states are:
# S05 Goa
# S14 Manipur
# S19 Punjab
# S28 Uttarakhand

states = {'Uttar Pradesh':'s24', 'Goa':'s05', 'Manipur': 's14', 'Punjab':'s19','Uttarakhand':'s28'}

#DEFS
def process_constituency(number, constituency):
    record = {}
    record['constituency'] = constituency
    print 'Processing ', constituency
    html = scraperwiki.scrape(baseurl+state+number+'.htm')
    root = lxml.html.fromstring(html)
    results = root.xpath (result_xpath)
    for x in results[3:-1]: #skip the first 3 tr's and the last one
        record['candidate'] = x[0].text
        record['party'] = x[1].text
        record['votes'] =  x[2].text
        scraperwiki.sqlite.save(unique_keys=['candidate', 'constituency'], data=record, table_name='uttar-pradesh-elections')   
    

#######################

#Scrape the first page to get the list of constituencies
html = scraperwiki.scrape('http://eciresults.ap.nic.in/ConstituencywiseS2489.htm')

#The list of constituencies for Uttar Pradesh is in this markup:
# <input type="hidden" id="HdnFldUttarPradesh" value=

#Lets get that list with values to add to our baseurl


root = lxml.html.fromstring(html)
content = root.xpath (constituency_xpath)

for c in content:
    constituencies = c.attrib['value']


# A list of numbers and the name of the constituency
constituencies = constituencies.split(';')

# And now we iterate through the list
for c in constituencies:
    process_constituency( c.split(',')[0].strip(),c.split(',')[1] )



