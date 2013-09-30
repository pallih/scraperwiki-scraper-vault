import scraperwiki
from mechanize import Browser
from BeautifulSoup import BeautifulSoup
from lxml import html

mech = Browser()
url = "http://www.kemendag.go.id/statistik_perkembangan_impor_menurut_hs_6_digit/"
page1 = mech.open(url)
html1 = page1.read()
tree = html.fromstring(html1)
table, = tree.xpath('//*[.="HS"]/ancestor::table[1]')
soup1 = BeautifulSoup(html.tostring(table))
table = soup1.find("table", cellspacing=1)
for row in table.findAll('tr')[1:]:
    col=row.findAll('td')
    data = {'HS':col[1].string, 'Description': col[2].string, '2006': col[3].string, '2007': col[4].string, '2008': col[5].string, '2009': col[6].string, '2010': col[7].string, 'Januari-Sept-2010': col[8].string, 'Januari-Sept-2011': col[9].string}
    scraperwiki.sqlite.save(unique_keys=['HS'], data=data)import scraperwiki
from mechanize import Browser
from BeautifulSoup import BeautifulSoup
from lxml import html

mech = Browser()
url = "http://www.kemendag.go.id/statistik_perkembangan_impor_menurut_hs_6_digit/"
page1 = mech.open(url)
html1 = page1.read()
tree = html.fromstring(html1)
table, = tree.xpath('//*[.="HS"]/ancestor::table[1]')
soup1 = BeautifulSoup(html.tostring(table))
table = soup1.find("table", cellspacing=1)
for row in table.findAll('tr')[1:]:
    col=row.findAll('td')
    data = {'HS':col[1].string, 'Description': col[2].string, '2006': col[3].string, '2007': col[4].string, '2008': col[5].string, '2009': col[6].string, '2010': col[7].string, 'Januari-Sept-2010': col[8].string, 'Januari-Sept-2011': col[9].string}
    scraperwiki.sqlite.save(unique_keys=['HS'], data=data)