import scraperwiki
import lxml.html

# Blank Python

def get_root(url):
    return lxml.html.fromstring(scraperwiki.scrape(url))

def get_pagelist():
    url="http://bip.uml.lodz.pl/index.php?str=132"
    root=get_root(url)
    links=root.xpath("//li/div/a")
    return [(i.text_content(),"http://bip.uml.lodz.pl/index.php%s"%i.attrib["href"]) for i in links]

def get_commission(page):
    commission=page[0]
    url=page[1]
    root=get_root(url)
    participants=root.xpath("//div/table/tr/td[2]")
    for p in [i.text_content() for i in participants]:
        if p.strip():
            scraperwiki.sqlite.save(unique_keys=["unique"],data={"commission":commission, "participants":p, "unique":"%s-%s"%(commission,p)})


#delete datastore

scraperwiki.sqlite.execute("drop table if exists ttt")
scraperwiki.sqlite.commit()

for page in get_pagelist():
    get_commission(page)

import scraperwiki
import lxml.html

# Blank Python

def get_root(url):
    return lxml.html.fromstring(scraperwiki.scrape(url))

def get_pagelist():
    url="http://bip.uml.lodz.pl/index.php?str=132"
    root=get_root(url)
    links=root.xpath("//li/div/a")
    return [(i.text_content(),"http://bip.uml.lodz.pl/index.php%s"%i.attrib["href"]) for i in links]

def get_commission(page):
    commission=page[0]
    url=page[1]
    root=get_root(url)
    participants=root.xpath("//div/table/tr/td[2]")
    for p in [i.text_content() for i in participants]:
        if p.strip():
            scraperwiki.sqlite.save(unique_keys=["unique"],data={"commission":commission, "participants":p, "unique":"%s-%s"%(commission,p)})


#delete datastore

scraperwiki.sqlite.execute("drop table if exists ttt")
scraperwiki.sqlite.commit()

for page in get_pagelist():
    get_commission(page)

