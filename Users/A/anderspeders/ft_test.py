import scraperwiki

scraperwiki.sqlite.save_var('data_columns', ['id', 'name', 'adress', 'city', 'postcode', 'country', 'Virksomhedstype'])

ftUrl = 'http://www.finanstilsynet.dk/Tal-og-fakta/Virksomheder-under-tilsyn/VUT-vis-virksomhed.aspx?id='

startNumber = 5001

for number in range(startNumber, startNumber+10):
    startUrl = ftUrl + str(number)
    print startUrl

import lxml.html
root = lxml.html.fromstring(startUrl)
for tr in root.cssselect("div[align='left'] tr.tcont"):
    tds = tr.cssselect("td")
    data = {
      'Navn' : tds[0].text_content(),
      'Adresse' : int(tds[4].text_content())
    }
    print data

scraperwiki.sqlite.save(unique_keys=['country'], data=startUrl)

