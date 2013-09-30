import scraperwiki

html = scraperwiki.scrape("http://orka.sejm.gov.pl/SQL.nsf/posglos?OpenAgent&6")

import lxml.html           
root = lxml.html.fromstring(html)
for tr in root.cssselect("table[width=350] tr"):
    tds = tr.cssselect("td")
    
    try:
        try:
            prevSession=int(tds[0].text_content())
        except:
            None
        data = {
          'session' : prevSession,
          'date' : tds[1].text_content(),
          'noDecisions' : tds[2].text_content(),
          'url': next(tds[1].iterlinks())[2]
        }
        #print data
        scraperwiki.sqlite.save(unique_keys=['date'], data=data)
    except: continue
    import scraperwiki

html = scraperwiki.scrape("http://orka.sejm.gov.pl/SQL.nsf/posglos?OpenAgent&6")

import lxml.html           
root = lxml.html.fromstring(html)
for tr in root.cssselect("table[width=350] tr"):
    tds = tr.cssselect("td")
    
    try:
        try:
            prevSession=int(tds[0].text_content())
        except:
            None
        data = {
          'session' : prevSession,
          'date' : tds[1].text_content(),
          'noDecisions' : tds[2].text_content(),
          'url': next(tds[1].iterlinks())[2]
        }
        #print data
        scraperwiki.sqlite.save(unique_keys=['date'], data=data)
    except: continue
    