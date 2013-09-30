import scraperwiki

# Blank Python
import scraperwiki
html = scraperwiki.scrape("http://projects.propublica.org/bailout/programs/1-capital-purchase-program")
print html
import lxml.html
root = lxml.html.fromstring(html)
for tr in root.cssselect("tbody[''] tr.subject"):
    tds = tr.cssselect("td")
    data = {
      'Name' : tds[0].text_content}
    scraperwiki.sqlite.save(unique_keys=['Name'], data=data)




import scraperwiki

# Blank Python
import scraperwiki
html = scraperwiki.scrape("http://projects.propublica.org/bailout/programs/1-capital-purchase-program")
print html
import lxml.html
root = lxml.html.fromstring(html)
for tr in root.cssselect("tbody[''] tr.subject"):
    tds = tr.cssselect("td")
    data = {
      'Name' : tds[0].text_content}
    scraperwiki.sqlite.save(unique_keys=['Name'], data=data)




