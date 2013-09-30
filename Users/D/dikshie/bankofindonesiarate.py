import scraperwiki
from mechanize import Browser
from BeautifulSoup import BeautifulSoup
from lxml import html
import sqlite3,os

mech = Browser()
url = "http://www.bi.go.id/web/id/Moneter/BI+Rate/Data+BI+Rate/"
page1 = mech.open(url)
html1 = page1.read()
tree = html.fromstring(html1)
table, = tree.xpath('//*[.="Tanggal"]/ancestor::table[1]')
soup1 = BeautifulSoup(html.tostring(table))
table = soup1.find("table", cellspacing=1)
for row in table.findAll('tr')[1:]:
    col=row.findAll('td')
    data={'datemonthyear': col[0].string,'rate': col[1].string
    }
    print data
    scraperwiki.sqlite.save(unique_keys=['datemonthyear'], data=data)import scraperwiki
from mechanize import Browser
from BeautifulSoup import BeautifulSoup
from lxml import html
import sqlite3,os

mech = Browser()
url = "http://www.bi.go.id/web/id/Moneter/BI+Rate/Data+BI+Rate/"
page1 = mech.open(url)
html1 = page1.read()
tree = html.fromstring(html1)
table, = tree.xpath('//*[.="Tanggal"]/ancestor::table[1]')
soup1 = BeautifulSoup(html.tostring(table))
table = soup1.find("table", cellspacing=1)
for row in table.findAll('tr')[1:]:
    col=row.findAll('td')
    data={'datemonthyear': col[0].string,'rate': col[1].string
    }
    print data
    scraperwiki.sqlite.save(unique_keys=['datemonthyear'], data=data)