import scraperwiki
from BeautifulSoup import BeautifulSoup
import re


html = scraperwiki.scrape("http://council.nyc.gov/html/members/members.shtml")
raw = BeautifulSoup(html)

members = raw.find(id="members_table")

#print members

#print members.prettify()

i = 0;

rows = members.findAll('tr')
for tr in rows:
    cols = tr.findAll('td')
    #for td in cols:
        #print i
       # i += 1
       # member = td.a.string
       # print member



table = raw.find("table", id="members_table")

for row in table.findAll('tr')[1:]:
    col = row.findAll('td')

    # mail = col[0].string
    member = col[1].find('a').string
    district = col[2].string
    boro = col[3].string
    party = col[4].string


    record = {
        'member':   member,
        'district': district,
        'boro':     boro,
        'party':    party
    }
    #print record

    scraperwiki.sqlite.save(unique_keys=['member'], data=record)import scraperwiki
from BeautifulSoup import BeautifulSoup
import re


html = scraperwiki.scrape("http://council.nyc.gov/html/members/members.shtml")
raw = BeautifulSoup(html)

members = raw.find(id="members_table")

#print members

#print members.prettify()

i = 0;

rows = members.findAll('tr')
for tr in rows:
    cols = tr.findAll('td')
    #for td in cols:
        #print i
       # i += 1
       # member = td.a.string
       # print member



table = raw.find("table", id="members_table")

for row in table.findAll('tr')[1:]:
    col = row.findAll('td')

    # mail = col[0].string
    member = col[1].find('a').string
    district = col[2].string
    boro = col[3].string
    party = col[4].string


    record = {
        'member':   member,
        'district': district,
        'boro':     boro,
        'party':    party
    }
    #print record

    scraperwiki.sqlite.save(unique_keys=['member'], data=record)