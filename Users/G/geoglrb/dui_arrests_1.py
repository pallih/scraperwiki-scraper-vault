import scraperwiki

html = scraperwiki.scrape("http://www.statisticbrain.com/number-of-dui-arrests-per-state/")
print html

import lxml.html           
root = lxml.html.fromstring(html)
mydiv = (root.cssselect("div.postcontent"))[0]
for tr in mydiv.cssselect("tr")[4:-2]:
    print lxml.html.tostring(tr)
tds = tr.cssselect("td")
data = {unique_keys=['state', 'DUIs', 'POP'], }
 print data
        scraperwiki.sqlite.save(unique_keys=['state', 'DUIs, 'POP'], data=data)



    # tr is a state's data. get content for each column. then store it.


    #        scraperwiki.sqlite.save(data=data)


   
import scraperwiki

html = scraperwiki.scrape("http://www.statisticbrain.com/number-of-dui-arrests-per-state/")
print html

import lxml.html           
root = lxml.html.fromstring(html)
mydiv = (root.cssselect("div.postcontent"))[0]
for tr in mydiv.cssselect("tr")[4:-2]:
    print lxml.html.tostring(tr)
tds = tr.cssselect("td")
data = {unique_keys=['state', 'DUIs', 'POP'], }
 print data
        scraperwiki.sqlite.save(unique_keys=['state', 'DUIs, 'POP'], data=data)



    # tr is a state's data. get content for each column. then store it.


    #        scraperwiki.sqlite.save(data=data)


   
