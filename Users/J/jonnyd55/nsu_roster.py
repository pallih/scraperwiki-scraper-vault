from urllib2 import urlopen
from lxml.html import fromstring, tostring
from scraperwiki.sqlite import save
import scraperwiki


#call the page
page = urlopen('http://www.sportsnetwork.com/merge/tsnform.aspx?c=hamptonroads&page=cfoot2/conf/meac/roster.aspx?id=578')
rawtext = page.read()
html = fromstring(rawtext)

#Name the table you are trying to build
tables = html.cssselect('table')
#Call the first table
table = tables[3]

#print the entire table
print tostring(table)

#get the rows inside table 0
rows = table.cssselect('tr')
#headers = [th.text_content() for th in rows[0].cssselect('th')]

#pull headers from database
#expected_headers = ['State', 'Total', u'\xa0','White', 'Black', 'Hispanic', 'Asian', 'Native Hawaiian/Pacific Islander', 'American Indian/Alaska Native', 'Two or more races']
#assert headers == expected_headers, headers

#format header terms
#headers[6] = 'HawaiiPacIsl'
#headers[7] = 'AmInd'


#start loop on third row
#for row in rows[0]:
#    values = [td.text_content()  for td in row.cssselect('td')]
#    data = (dict(values))


    #data = dict(zip(values))
#    print rows
#    for key in [u'\xa0', 'Black', 'Hispanic', 'Asian', 'Native Hawaiian/Pacific Islander', 'American Indian/Alaska Native', 'Two or more races' ]:
#        if not data.has_key(key):
#            pass
#        elif data[key] in  [u'\u2014',u'\u2021', u'\xa0',u'\xe2\x80\xa1', '&#226;&#128;&#161;']:
#            del data[key]
#        else:
#            data[key] = float (data[key])

#    for key, value in data.items():
#        del(data[key])
#        data[keyify(key)] = value

#print headers



#for tr in table.cssselect('tr')[0:]:
#    cellvalues = [td.text_content() for td in tr.cssselect('td')]
#    print cellvalues
#   save([], cellvalues)


#    scraperwiki.sqlite.save(cellvalues, 'roster')
from urllib2 import urlopen
from lxml.html import fromstring, tostring
from scraperwiki.sqlite import save
import scraperwiki


#call the page
page = urlopen('http://www.sportsnetwork.com/merge/tsnform.aspx?c=hamptonroads&page=cfoot2/conf/meac/roster.aspx?id=578')
rawtext = page.read()
html = fromstring(rawtext)

#Name the table you are trying to build
tables = html.cssselect('table')
#Call the first table
table = tables[3]

#print the entire table
print tostring(table)

#get the rows inside table 0
rows = table.cssselect('tr')
#headers = [th.text_content() for th in rows[0].cssselect('th')]

#pull headers from database
#expected_headers = ['State', 'Total', u'\xa0','White', 'Black', 'Hispanic', 'Asian', 'Native Hawaiian/Pacific Islander', 'American Indian/Alaska Native', 'Two or more races']
#assert headers == expected_headers, headers

#format header terms
#headers[6] = 'HawaiiPacIsl'
#headers[7] = 'AmInd'


#start loop on third row
#for row in rows[0]:
#    values = [td.text_content()  for td in row.cssselect('td')]
#    data = (dict(values))


    #data = dict(zip(values))
#    print rows
#    for key in [u'\xa0', 'Black', 'Hispanic', 'Asian', 'Native Hawaiian/Pacific Islander', 'American Indian/Alaska Native', 'Two or more races' ]:
#        if not data.has_key(key):
#            pass
#        elif data[key] in  [u'\u2014',u'\u2021', u'\xa0',u'\xe2\x80\xa1', '&#226;&#128;&#161;']:
#            del data[key]
#        else:
#            data[key] = float (data[key])

#    for key, value in data.items():
#        del(data[key])
#        data[keyify(key)] = value

#print headers



#for tr in table.cssselect('tr')[0:]:
#    cellvalues = [td.text_content() for td in tr.cssselect('td')]
#    print cellvalues
#   save([], cellvalues)


#    scraperwiki.sqlite.save(cellvalues, 'roster')
