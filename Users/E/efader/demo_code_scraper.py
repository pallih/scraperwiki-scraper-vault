import scraperwiki           
html = scraperwiki.scrape("http://www.youtube.com/clinique/")
print html


import lxml.html           
root = lxml.html.fromstring(html)
for tr in root.cssselect("div[align='left'] tr.tcont"):
    tds = tr.cssselect("td")
    data = {
      'country' : tds[0].text_content(),
    }
    print dataimport scraperwiki           
html = scraperwiki.scrape("http://www.youtube.com/clinique/")
print html


import lxml.html           
root = lxml.html.fromstring(html)
for tr in root.cssselect("div[align='left'] tr.tcont"):
    tds = tr.cssselect("td")
    data = {
      'country' : tds[0].text_content(),
    }
    print data