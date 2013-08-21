import scraperwiki

html = scraperwiki.scrape("http://www.statisticbrain.com/number-of-dui-arrests-per-state/") 
print html

import lxml.html           
root = lxml.html.fromstring(html)
mydiv = (root.cssselect("div.postcontent"))[0]
for tr in mydiv.cssselect("tr")[4:-2]:

    print lxml.html.tostring(tr)
    tds = tr.cssselect("td")
    data = {
            'state' : tds[0].text_content(),
            'DUIs' : tds[1].text_content(), 'POP' : tds[2].text_content()
        }
    scraperwiki.sqlite.save(unique_keys=['state', 'DUIs', 'POP'], data=data) 

    


    





