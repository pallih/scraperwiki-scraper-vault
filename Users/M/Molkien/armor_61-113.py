import urlparse
import scraperwiki
import lxml.html


def scrape_table(root):
    root = lxml.html.fromstring(html)
    for tr in root.cssselect("div[class='well'] tr"):
        tds = tr.cssselect("td")
        data = {
                'item' : tds[0].text_content(), 'Min Sale Offer' : tds[4].text_content()
                }
        scraperwiki.sqlite.save(unique_keys=['item'], data=data)


url="http://www.gw2spidy.com/type/0/-1/%d?sort_name=asc"
for page in range(61,113):
   html=scraperwiki.scrape(url % page)
   scrape_table(html)
