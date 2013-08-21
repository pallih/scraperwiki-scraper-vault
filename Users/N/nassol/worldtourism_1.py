import scraperwiki
html = scraperwiki.scrape('http://www.statisticbrain.com/tourism-statistics/')
print html

import lxml.html
root = lxml.html.fromstring(html)
i = 0
for tr in root.cssselect("tr") :

    if i == 11 :
        break
    
    tds = tr.cssselect("td")
    print len(tds)
    if len(tds)==3:
        data = {
            'index' : tds[0].text_content(),
            'annual_visitors_millions' : tds[2].text_content(),
            'country' : tds[1].text_content()            
        }
        print data
        i+=1

        scraperwiki.sqlite.save(unique_keys=['index'], data=data)


