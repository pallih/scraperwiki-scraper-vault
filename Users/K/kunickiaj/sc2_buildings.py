import scraperwiki
import lxml.html

urls = {
    "Protoss" : "http://www.theuen.com/buildings/protoss",
    "Terran" : "http://www.theuen.com/buildings/terran",
    "Zerg" : "http://www.theuen.com/buildings/zerg"
}

for race, url in urls.iteritems():
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    
    div = root.cssselect("div.item-list")[0]
    
    for tr in div.cssselect("tr"):
        tds = tr.cssselect("td")
        if len(tds) > 0:
            building = {
                'race' : race,
                'building' : tds[0].cssselect("span")[0].text_content().strip(),
                'minerals' : tds[1].text_content().strip(),
                'vespene' : tds[2].text_content().strip(),
                'buildtime' : tds[3].text_content().strip(),
            }
            if len(building['vespene']) == 0:
                building['vespene'] = 0
            scraperwiki.sqlite.save(unique_keys=['building'], data=building)
import scraperwiki
import lxml.html

urls = {
    "Protoss" : "http://www.theuen.com/buildings/protoss",
    "Terran" : "http://www.theuen.com/buildings/terran",
    "Zerg" : "http://www.theuen.com/buildings/zerg"
}

for race, url in urls.iteritems():
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    
    div = root.cssselect("div.item-list")[0]
    
    for tr in div.cssselect("tr"):
        tds = tr.cssselect("td")
        if len(tds) > 0:
            building = {
                'race' : race,
                'building' : tds[0].cssselect("span")[0].text_content().strip(),
                'minerals' : tds[1].text_content().strip(),
                'vespene' : tds[2].text_content().strip(),
                'buildtime' : tds[3].text_content().strip(),
            }
            if len(building['vespene']) == 0:
                building['vespene'] = 0
            scraperwiki.sqlite.save(unique_keys=['building'], data=building)
