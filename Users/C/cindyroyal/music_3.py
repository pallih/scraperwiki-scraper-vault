import scraperwiki
html = scraperwiki.scrape("http://governor.state.tx.us/music/musicians/talent/talent")
print html

import lxml.html
root = lxml.html.fromstring(html)
for tr in root.cssselect("div[style='text-align: center'] tr"):
    tds = tr.cssselect("td")
    if len(tds)==4:
        data = {
            'name' : tds[0].text_content(),
            'city' : tds[1].text_content(),
            'type' : tds[2].text_content(),
            'number' : tds[3].text_content()
'song' : tds[2].text_content()
        }
        print data
