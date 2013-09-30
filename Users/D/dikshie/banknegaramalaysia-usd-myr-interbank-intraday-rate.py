import scraperwiki
from mechanize import Browser
from BeautifulSoup import BeautifulSoup
from lxml import html


mech = Browser()
url = "http://www.bnm.gov.my/index.php?ch=12&pg=800"
page = mech.open(url)
html1 = page.read()
tree = html.fromstring(html1)
table, = tree.xpath('//*[.="Trading Date"]/ancestor::table[1]')
soup1 = BeautifulSoup(html.tostring(table))
table = soup1.find("table")
for row in table.findAll('tr')[1:]:
    col=row.findAll('td')
    data = {'date': col[0].string , 'highest-rate': col[1].string, 'lowest-rate': col[2].string}
    scraperwiki.sqlite.save(unique_keys=['date'], data=data)

import scraperwiki
from mechanize import Browser
from BeautifulSoup import BeautifulSoup
from lxml import html


mech = Browser()
url = "http://www.bnm.gov.my/index.php?ch=12&pg=800"
page = mech.open(url)
html1 = page.read()
tree = html.fromstring(html1)
table, = tree.xpath('//*[.="Trading Date"]/ancestor::table[1]')
soup1 = BeautifulSoup(html.tostring(table))
table = soup1.find("table")
for row in table.findAll('tr')[1:]:
    col=row.findAll('td')
    data = {'date': col[0].string , 'highest-rate': col[1].string, 'lowest-rate': col[2].string}
    scraperwiki.sqlite.save(unique_keys=['date'], data=data)

