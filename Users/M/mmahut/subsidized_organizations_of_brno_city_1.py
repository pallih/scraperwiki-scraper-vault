# -*- coding: utf-8 -*-
import scraperwiki
import lxml.html
import re
html = scraperwiki.scrape("http://www.brno.cz/sprava-mesta/urady-a-instituce-v-brne/mestske-organizace-a-spolecnosti")
root = lxml.html.fromstring(html) 
el = root.cssselect("div#c924 br")
prog = re.compile('^(.*) \((\d+) %\)$')

for item in el:
    if "%" in item.tail:
        result = prog.match(item.tail)
        print "Found item with %"
        if result is not None:
            print "And it's not Null"
            name = result.group(1)
            podiel = result.group(2)
    else:
        name = item.tail 
        podiel = None
    data = {
        'Name' : name,
        'Share' : podiel,
    }
    scraperwiki.sqlite.save(unique_keys=["Name"], data=data)
