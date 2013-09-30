# -*- coding: utf-8 -*-
import scraperwiki
from datetime import date, timedelta
import lxml.html  

yesterday = date.today() - timedelta(1)

html = scraperwiki.scrape("http://aplikace.policie.cz/statistiky-dopravnich-nehod/Default.aspx", {'ctl00$Application$ddlKraje':'Česká republika','ctl00$Application$txtDatum':'30.08.2011','ctl00$Application$cmdZobraz':'Zobrazit'})
html = html.replace('\t', '')
html = html.replace('\r', '')
html = html.replace('\n', '')

root = lxml.html.fromstring(html) 
table = root.cssselect("table#celacr")

for tr in table: 
    tds = tr.cssselect("tr")
    data = {
    'Date' : yesterday.strftime('%Y-%m-%d'), # take yesterdays stats
    'Number of accidents' : tds[16][1].text_content(),
    'Deaths' : tds[16][2].text_content(),
    'Severely wounded' : tds[16][3].text_content(),
    'Slightly wounded' : tds[16][4].text_content(),
    'Damage' : tds[16][5].text_content(),
    'Excessive speed' : tds[16][6].text_content(),
    'Giving priority in driving' : tds[16][7].text_content(),
    'Improper overtaking' : tds[16][8].text_content(),
    'Wrong way driving' : tds[16][9].text_content(),
    'Other cause' : tds[16][10].text_content(),
    'Influence of alcohol' : tds[16][11].text_content(),
    }
    scraperwiki.sqlite.save(unique_keys=["Date"], data=data)           
            

# -*- coding: utf-8 -*-
import scraperwiki
from datetime import date, timedelta
import lxml.html  

yesterday = date.today() - timedelta(1)

html = scraperwiki.scrape("http://aplikace.policie.cz/statistiky-dopravnich-nehod/Default.aspx", {'ctl00$Application$ddlKraje':'Česká republika','ctl00$Application$txtDatum':'30.08.2011','ctl00$Application$cmdZobraz':'Zobrazit'})
html = html.replace('\t', '')
html = html.replace('\r', '')
html = html.replace('\n', '')

root = lxml.html.fromstring(html) 
table = root.cssselect("table#celacr")

for tr in table: 
    tds = tr.cssselect("tr")
    data = {
    'Date' : yesterday.strftime('%Y-%m-%d'), # take yesterdays stats
    'Number of accidents' : tds[16][1].text_content(),
    'Deaths' : tds[16][2].text_content(),
    'Severely wounded' : tds[16][3].text_content(),
    'Slightly wounded' : tds[16][4].text_content(),
    'Damage' : tds[16][5].text_content(),
    'Excessive speed' : tds[16][6].text_content(),
    'Giving priority in driving' : tds[16][7].text_content(),
    'Improper overtaking' : tds[16][8].text_content(),
    'Wrong way driving' : tds[16][9].text_content(),
    'Other cause' : tds[16][10].text_content(),
    'Influence of alcohol' : tds[16][11].text_content(),
    }
    scraperwiki.sqlite.save(unique_keys=["Date"], data=data)           
            

