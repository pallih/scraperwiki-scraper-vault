import scraperwiki

# Blank Python

html = scraperwiki.scrape('http://www.statisticbrain.com/blizzard-entertainment-statistics/')
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
            'Blizzard_Game_Title' : tds[0].text_content(),
            'Unit_Sold' : tds[2].text_content(),
            'Revenue' : tds[1].text_content()            
        }
        print data
        i+=1

        scraperwiki.sqlite.save(unique_keys=['Blizzard_Game_Title'], data=data)


