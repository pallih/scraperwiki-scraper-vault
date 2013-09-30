import scraperwiki


scraperwiki.sqlite.save_var('data_columns', ['id', 'name', 'adress', 'city', 'postcode', 'country', 'Virksomhedstype'])

ftUrl = 'http://ec.europa.eu/competition/elojade/isef/index.cfm'



import lxml.html
root = lxml.html.fromstring(ftUrl)
for tr in root.cssselect("div[align='left'] tr.tcont"):
    tds = tr.cssselect("td")
    data = {
      'Navn' : tds[0].text_content(),
      'Adresse' : int(tds[4].text_content())
    }
    print data

data=ftUrl

import scraperwiki


scraperwiki.sqlite.save_var('data_columns', ['id', 'name', 'adress', 'city', 'postcode', 'country', 'Virksomhedstype'])

ftUrl = 'http://ec.europa.eu/competition/elojade/isef/index.cfm'



import lxml.html
root = lxml.html.fromstring(ftUrl)
for tr in root.cssselect("div[align='left'] tr.tcont"):
    tds = tr.cssselect("td")
    data = {
      'Navn' : tds[0].text_content(),
      'Adresse' : int(tds[4].text_content())
    }
    print data

data=ftUrl

