import scraperwiki
import lxml.html

html = scraperwiki.scrape("http://us.battle.net/sc2/en/game/unit/")
root = lxml.html.fromstring(html)

unit_names = []

units = root.cssselect("td.unit-title span.unit-thumb-54x49 span")
for unit in units:
        unit_names.append(unit.attrib['class'])

for unit_name in unit_names:
    html = scraperwiki.scrape("http://us.battle.net/sc2/en/game/unit/" + unit_name)
    root = lxml.html.fromstring(html)

    unit = dict()
    unit['unit-title'] = root.cssselect("title")[0].text_content().split(' ', 1)[0]
    for tr in root.cssselect("div.basic-stats tr"):
        key = tr.cssselect("td.title")[0].text_content().lower().strip(': \t\n\r')
        if key == "race":
            value = tr.cssselect("td.content")[0].text_content().strip(' \t\n\r')
            unit[key] = value
    for tr in root.cssselect("div.production-stats tr"):
        key = tr.cssselect("td.title")[0].text_content().lower().strip(': \t\n\r')    
        if key == "cost":
            minerals, vespene = tr.cssselect("td.content")[0].text_content().strip(' \t\n\r').split()
            unit["minerals"] = minerals
            if vespene == "-":
                vespene = 0
            unit["vespene"] = vespene
        else:
            value = tr.cssselect("td.content")[0].text_content().strip(' \t\n\r')
            unit[key] = value
    
    scraperwiki.sqlite.save(unique_keys=['unit-title'], data=unit)
