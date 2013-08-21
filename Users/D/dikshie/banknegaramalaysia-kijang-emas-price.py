import scraperwiki
from mechanize import Browser
from BeautifulSoup import BeautifulSoup
from lxml import html
import sqlite3,os
import time

mech = Browser()
url = "http://www.bnm.gov.my/index.php?ch=12&pg=141"
page = mech.open(url)
html1 = page.read()
tree = html.fromstring(html1)
table, = tree.xpath('//*[.="Date"]/ancestor::table[1]')
soup1 = BeautifulSoup(html.tostring(table))
table = soup1.find("table")
for row in table.findAll('tr')[2:]:
    col=row.findAll('td')
    data = {'date': col[0].string, '1-oz-selling': col[1].string, '1-oz-buying': col[2].string, 'half-oz-selling': col[3].string, 'half-oz-buying': col[4].string, 'quater-oz-selling': col[5].string, 'quater-oz-buying': col[6].string}
    scraperwiki.sqlite.save(unique_keys=['date'], data=data)
