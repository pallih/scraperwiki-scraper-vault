import urlparse
import scraperwiki




def scrape_table(root):
    import lxml.html
    root = lxml.html.fromstring(html)
    for tr in root.cssselect("div[class='well'] tr"):
        tds = tr.cssselect("td")
        data = {
                'Min Sale Offer' : tds[4].text_content(), 'Sale volume' :
tds[4].get('title'), 'Max Buy Offer' : tds[5].text_content(), 'Buy volume' :
tds[5].get('title'), 'item' : tds[0].text_content(), 'margin' : tds[6].text_content()
                }
        scraperwiki.sqlite.save(unique_keys=['item'], data=data)




url="http://www.gw2spidy.com/type/5/-1/%d?sort_name=asc"
for page in range(1,21):
    html = scraperwiki.scrape(url % page)
    scrape_table(html)

import urlparse
import scraperwiki




def scrape_table(root):
    import lxml.html
    root = lxml.html.fromstring(html)
    for tr in root.cssselect("div[class='well'] tr"):
        tds = tr.cssselect("td")
        data = {
                'Min Sale Offer' : tds[4].text_content(), 'Sale volume' :
tds[4].get('title'), 'Max Buy Offer' : tds[5].text_content(), 'Buy volume' :
tds[5].get('title'), 'item' : tds[0].text_content(), 'margin' : tds[6].text_content()
                }
        scraperwiki.sqlite.save(unique_keys=['item'], data=data)




url="http://www.gw2spidy.com/type/5/-1/%d?sort_name=asc"
for page in range(1,21):
    html = scraperwiki.scrape(url % page)
    scrape_table(html)

