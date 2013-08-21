import scraperwiki

# Blank Python
import scraperwiki
html = scraperwiki.scrape("http://www.cacities.org/resource_files/20455.city%20list.pdf")
print html
import lxml.html
root = lxml.html.fromstring(html)
for tr in root.cssselect("div[align='left'] tr.tcont"):
    tds = tr.cssselect("td")
    data = {
      'city_name' : tds[0].text_content(),
      'population' : int(tds[4].text_content())
    }
    print data
    scraperwiki.sqlite.save(unique_keys=['city_name'], data=data)
