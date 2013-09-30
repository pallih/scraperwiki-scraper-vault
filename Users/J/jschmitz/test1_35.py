import scraperwiki           
html = scraperwiki.scrape("http://emma.msrb.org/MarketActivity/RecentTrades.aspx")
print html
import lxml.html           
root = lxml.html.fromstring(html)
for tr in root.cssselect("div[align='left'] tr"):
    tds = tr.cssselect("td")
    if len(tds)==12:
        data = {
            'country' : tds[0].text_content(),
            'years_inschool' : int(tds[4].text_content()),
            'men' : int(tds[7].text_content()),
            'women': int(tds[10].text_content()),
            'years' : int(tds[1].text_content())
        }
        scraperwiki.sqlite.save(unique_keys=['country'], data=data)

import scraperwiki           
html = scraperwiki.scrape("http://emma.msrb.org/MarketActivity/RecentTrades.aspx")
print html
import lxml.html           
root = lxml.html.fromstring(html)
for tr in root.cssselect("div[align='left'] tr"):
    tds = tr.cssselect("td")
    if len(tds)==12:
        data = {
            'country' : tds[0].text_content(),
            'years_inschool' : int(tds[4].text_content()),
            'men' : int(tds[7].text_content()),
            'women': int(tds[10].text_content()),
            'years' : int(tds[1].text_content())
        }
        scraperwiki.sqlite.save(unique_keys=['country'], data=data)

