## Collaborators: Andy Siegel, Richard McGovern, Jay Dahlstrom, Isaiah Berg, John Williams
## Geog 495 Scraper
## 
##
## DESCRIPTION : Prints a list for each band in the the 2011 Battle of the Geek Bands
##               containing the band name, number of band members, and a URL linking
##               to their performance on youtube.

import scraperwiki
html = scraperwiki.scrape("http://www.seattleinteractive.com/2011/battleofthegeekbands")
print html

import lxml.html
root = lxml.html.fromstring(html)

for h6 in root.cssselect("div.grid_10 h6"):
    
    data = {
        'bandName' : h6.text[2:],
        'numMembers' : int(h6.getnext().getchildren()[0].tail),
        'url' : h6.getnext().getnext().getchildren()[0].attrib['src']
    }
    print data.values()
    scraperwiki.sqlite.save(unique_keys=['bandName'], data=data)## Collaborators: Andy Siegel, Richard McGovern, Jay Dahlstrom, Isaiah Berg, John Williams
## Geog 495 Scraper
## 
##
## DESCRIPTION : Prints a list for each band in the the 2011 Battle of the Geek Bands
##               containing the band name, number of band members, and a URL linking
##               to their performance on youtube.

import scraperwiki
html = scraperwiki.scrape("http://www.seattleinteractive.com/2011/battleofthegeekbands")
print html

import lxml.html
root = lxml.html.fromstring(html)

for h6 in root.cssselect("div.grid_10 h6"):
    
    data = {
        'bandName' : h6.text[2:],
        'numMembers' : int(h6.getnext().getchildren()[0].tail),
        'url' : h6.getnext().getnext().getchildren()[0].attrib['src']
    }
    print data.values()
    scraperwiki.sqlite.save(unique_keys=['bandName'], data=data)