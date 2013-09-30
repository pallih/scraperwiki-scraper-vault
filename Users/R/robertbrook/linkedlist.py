import scraperwiki
import lxml.html
          
html = scraperwiki.scrape("http://daringfireball.net/linked/")

root = lxml.html.fromstring(html)

for el in root.cssselect("dt a"):           
    link = el.attrib['href']
    if "daringfireball" not in link:
        data = {
            'text' : el.text,
            'link' : link
        }
        scraperwiki.sqlite.save(unique_keys=['text'], data=data)

import scraperwiki
import lxml.html
          
html = scraperwiki.scrape("http://daringfireball.net/linked/")

root = lxml.html.fromstring(html)

for el in root.cssselect("dt a"):           
    link = el.attrib['href']
    if "daringfireball" not in link:
        data = {
            'text' : el.text,
            'link' : link
        }
        scraperwiki.sqlite.save(unique_keys=['text'], data=data)

