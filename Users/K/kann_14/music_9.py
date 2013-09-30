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
            'city' : tds[1].text_content()
        }
        scraperwiki.sqlite.save(unique_keys=['name'], data=data)
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
            'city' : tds[1].text_content()
        }
        scraperwiki.sqlite.save(unique_keys=['name'], data=data)
