from urllib2 import urlopen
from lxml.html import fromstring, tostring
import scraperwiki
import datetime
  
#call the page
page = urlopen('http://dashboard.ed.gov/statecomparison.aspx?i=e&id=0&wt=40')
rawtext = page.read()
html = fromstring(rawtext)

#Name the table you are trying to build
tables = html.cssselect('table')
#Call the first table
table = tables[0]

#print the entire table
print tostring(table)

#get the rows inside table 0
rows = table.cssselect('tr')
headers = [str(th.text_content())  for th in rows[0].cssselect('th')]

#pull headers from database
assert headers == ['State', 'Total', 'White', 'Black', 'Hispanic', 'Asian/Pacific Islander', 'American Indian/ Alaska Native'] 

#format header terms
headers[5] = 'Asian'
headers[6] = 'AmerInd'

#start loop on third row
for row in rows[2:]: 
    values = [td.text_content()  for td in row.cssselect('td,th')]
    data = dict(zip(headers,values))
    for key in ['Total', 'White', 'Black', 'Hispanic', 'Asian', 'AmerInd']:
        if data[key] in  ['-', u'\u2014',u'\u2021']:
            del data[key]
        else:
            data[key] = float (data[key])
    print data
    scraperwiki.sqlite.save(['State'], data)

print headers



for tr in table.cssselect('tr')[1:]:
    cellvalues = [td.text_content() for td in tr.cssselect('td')]

