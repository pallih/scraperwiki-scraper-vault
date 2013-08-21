import scraperwiki
import lxml.html
import json

html = scraperwiki.scrape("http://us.battle.net/sc2/en/game/unit/")
root = lxml.html.fromstring(html)

unit = []
i = 0
for tr in root.cssselect("tr.button-rollover"):
    tds = tr.cssselect("td")
    unit.append({
        'unit-title' : tds[0].text_content().strip(),
        'mineral' : tds[1].text_content(),
        'vespene' : tds[2].text_content(),
        'supply' : tds[3].text_content(),
        'buildtime' : tds[4].text_content(),
        'producer' : tds[5].text_content(),
        'life' : tds[6].text_content(),
        'energy' : tds[7].text_content(),
        'armor' : tds[8].text_content(),
    })
    i = i + 1
#    scraperwiki.sqlite.save(unique_keys=['unit-title'], data=unit)
print json.dumps(unit, sort_keys=True, indent=4)