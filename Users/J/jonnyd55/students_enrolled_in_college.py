from urllib2 import urlopen
from lxml.html import fromstring, tostring
import scraperwiki
import datetime
keyify = scraperwiki.swimport('keyify').keyify

#call the page
page = urlopen('http://dashboard.ed.gov/statecomparison.aspx?i=j&id=0&wt=40')
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
headers = [th.text_content() for th in rows[0].cssselect('th')]

#pull headers from database
expected_headers = ['State', 'Total', u'\xa0','White', 'Black', 'Hispanic', 'Asian', 'Native Hawaiian/Pacific Islander', 'American Indian/Alaska Native', 'Two or more races']
assert headers == expected_headers, headers

#format header terms
#headers[6] = 'HawaiiPacIsl'
#headers[7] = 'AmInd'


#start loop on third row
for row in rows[1:]:
    values = [td.text_content()  for td in row.cssselect('td,th')]
    data = dict(zip(headers,values))
    print data
    for key in [u'\xa0', 'Black', 'Hispanic', 'Asian', 'Native Hawaiian/Pacific Islander', 'American Indian/Alaska Native', 'Two or more races' ]:
        if not data.has_key(key):
            pass
        elif data[key] in  [u'\u2014',u'\u2021', u'\xa0',u'\xe2\x80\xa1', '&#226;&#128;&#161;']:
            del data[key]
        else:
            data[key] = float (data[key])

    for key, value in data.items():
        del(data[key])
        data[keyify(key)] = value

    scraperwiki.sqlite.save(['State'], data, 'enroll')

#print headers



for tr in table.cssselect('tr')[1:]:
    cellvalues = [td.text_content() for td in tr.cssselect('td')]
    print cellvalues

from urllib2 import urlopen
from lxml.html import fromstring, tostring
import scraperwiki
import datetime
keyify = scraperwiki.swimport('keyify').keyify

#call the page
page = urlopen('http://dashboard.ed.gov/statecomparison.aspx?i=j&id=0&wt=40')
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
headers = [th.text_content() for th in rows[0].cssselect('th')]

#pull headers from database
expected_headers = ['State', 'Total', u'\xa0','White', 'Black', 'Hispanic', 'Asian', 'Native Hawaiian/Pacific Islander', 'American Indian/Alaska Native', 'Two or more races']
assert headers == expected_headers, headers

#format header terms
#headers[6] = 'HawaiiPacIsl'
#headers[7] = 'AmInd'


#start loop on third row
for row in rows[1:]:
    values = [td.text_content()  for td in row.cssselect('td,th')]
    data = dict(zip(headers,values))
    print data
    for key in [u'\xa0', 'Black', 'Hispanic', 'Asian', 'Native Hawaiian/Pacific Islander', 'American Indian/Alaska Native', 'Two or more races' ]:
        if not data.has_key(key):
            pass
        elif data[key] in  [u'\u2014',u'\u2021', u'\xa0',u'\xe2\x80\xa1', '&#226;&#128;&#161;']:
            del data[key]
        else:
            data[key] = float (data[key])

    for key, value in data.items():
        del(data[key])
        data[keyify(key)] = value

    scraperwiki.sqlite.save(['State'], data, 'enroll')

#print headers



for tr in table.cssselect('tr')[1:]:
    cellvalues = [td.text_content() for td in tr.cssselect('td')]
    print cellvalues

