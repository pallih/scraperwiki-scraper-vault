###############################################################################
# UK Political Parties scraper
###############################################################################

import scraperwiki
import mechanize
from BeautifulSoup import BeautifulSoup

starting_url = 'http://registers.electoralcommission.org.uk/regulatory-issues/regpoliticalparties.cfm?ec=%7Bts%20%272010%2D09%2D20%2014%3A35%3A43%27%7D'
br = mechanize.Browser()
br.open(starting_url)
br.select_form(nr=0)
br.submit()
soup = BeautifulSoup(br.response().read())

table = soup.findAll('ul')
items = table[1].findAll('li')
moreinfo = []
for item in items:
    moreinfo.append('http://registers.electoralcommission.org.uk' + item.findAll('a')[0]['href'])
print moreinfo
    #record = { "name" : name , "website" : website , "latestreport" : latestreport, "moreinfo" : moreinfo, "scheduled" : scheduled }
    # save records to the datastore
    #scraperwiki.datastore.save(["name"], record) 

for parties in moreinfo:
    print parties
    html = scraperwiki.scrape(parties)
    soup = BeautifulSoup(html)
    name = soup.findAll('h2')[0].contents[0]
    table = soup.findAll('table')[0]
    trs = table.findAll('tr')
    for tr in trs:
        try:
            field = tr.findAll('td')[0].contents[0].contents[0]
        except:
            try:
                field = tr.findAll('td')[0].contents[0]
            except:
                field = ''
        try:
            if field=="Has emblems:":
                try:
                    tr.findAll('a')[0].contents[0]
                    value = "Yes"
                except:
                    value = "No"
            else:
                value = tr.findAll('td')[1].contents[0]
        except:
            value= ''
        print name, field, value
###############################################################################
# UK Political Parties scraper
###############################################################################

import scraperwiki
import mechanize
from BeautifulSoup import BeautifulSoup

starting_url = 'http://registers.electoralcommission.org.uk/regulatory-issues/regpoliticalparties.cfm?ec=%7Bts%20%272010%2D09%2D20%2014%3A35%3A43%27%7D'
br = mechanize.Browser()
br.open(starting_url)
br.select_form(nr=0)
br.submit()
soup = BeautifulSoup(br.response().read())

table = soup.findAll('ul')
items = table[1].findAll('li')
moreinfo = []
for item in items:
    moreinfo.append('http://registers.electoralcommission.org.uk' + item.findAll('a')[0]['href'])
print moreinfo
    #record = { "name" : name , "website" : website , "latestreport" : latestreport, "moreinfo" : moreinfo, "scheduled" : scheduled }
    # save records to the datastore
    #scraperwiki.datastore.save(["name"], record) 

for parties in moreinfo:
    print parties
    html = scraperwiki.scrape(parties)
    soup = BeautifulSoup(html)
    name = soup.findAll('h2')[0].contents[0]
    table = soup.findAll('table')[0]
    trs = table.findAll('tr')
    for tr in trs:
        try:
            field = tr.findAll('td')[0].contents[0].contents[0]
        except:
            try:
                field = tr.findAll('td')[0].contents[0]
            except:
                field = ''
        try:
            if field=="Has emblems:":
                try:
                    tr.findAll('a')[0].contents[0]
                    value = "Yes"
                except:
                    value = "No"
            else:
                value = tr.findAll('td')[1].contents[0]
        except:
            value= ''
        print name, field, value
