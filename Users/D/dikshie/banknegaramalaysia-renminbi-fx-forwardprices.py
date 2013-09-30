import scraperwiki
from mechanize import Browser
from BeautifulSoup import BeautifulSoup
from lxml import html
import time

mech = Browser()
url = "http://www.bnm.gov.my/index.php?ch=12&pg=852"
page = mech.open(url)
html1 = page.read()
tree = html.fromstring(html1)
table, = tree.xpath('//*[.="Tenure"]/ancestor::table[1]')
soup1 = BeautifulSoup(html.tostring(table))
table = soup1.find("table")
now=time.time()
for row in table.findAll('tr')[1:]:
    col=row.findAll('td')
    data = {'time': now , 'Tenure': col[0].string , 'Buying': col[1].string, 'Selling': col[2].string }
    scraperwiki.sqlite.save(unique_keys=['time'], data=data)
    now=now+1
import scraperwiki
from mechanize import Browser
from BeautifulSoup import BeautifulSoup
from lxml import html
import time

mech = Browser()
url = "http://www.bnm.gov.my/index.php?ch=12&pg=852"
page = mech.open(url)
html1 = page.read()
tree = html.fromstring(html1)
table, = tree.xpath('//*[.="Tenure"]/ancestor::table[1]')
soup1 = BeautifulSoup(html.tostring(table))
table = soup1.find("table")
now=time.time()
for row in table.findAll('tr')[1:]:
    col=row.findAll('td')
    data = {'time': now , 'Tenure': col[0].string , 'Buying': col[1].string, 'Selling': col[2].string }
    scraperwiki.sqlite.save(unique_keys=['time'], data=data)
    now=now+1
