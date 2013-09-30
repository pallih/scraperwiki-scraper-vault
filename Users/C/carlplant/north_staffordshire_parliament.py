import scraperwiki
import lxml.html
from datetime import date 


record = {}

html = scraperwiki.scrape("http://www.parliament.uk/search/results/?type=advanced&adv_exact=north+staffordshire&adv_datesearch=after&adv_datefrom=01/02/2013&filter=debates,handeb,commwa,hanidx")
root = lxml.html.fromstring(html)


def urlLists(linkUrl):
    
    html2 = scraperwiki.scrape(linkUrl)
    root2 = lxml.html.fromstring(html2)
    cells = root.cssselect('div#wrapper div#content-small') 
    for cellsInfo in cells:
        detail = row.cssselect('p') 
        if detail:
            record['detail'] = "nstaffsmentionedtoday"
            record['ScrapeDate'] = date.today()          
            scraperwiki.sqlite.save(unique_keys=[], data=record)


tr = root.cssselect('ul#results li') #select all of the tr elements
#print tr
for row in tr:
    
    link = row.cssselect('h4 a') 
    if link:
        linkUrl = link[0].attrib.get('href')
        record['linkTtile'] = link[0].text_content()
        record['Linkurl'] = link[0].attrib.get('href')
        urlLists(linkUrl)

import scraperwiki
import lxml.html
from datetime import date 


record = {}

html = scraperwiki.scrape("http://www.parliament.uk/search/results/?type=advanced&adv_exact=north+staffordshire&adv_datesearch=after&adv_datefrom=01/02/2013&filter=debates,handeb,commwa,hanidx")
root = lxml.html.fromstring(html)


def urlLists(linkUrl):
    
    html2 = scraperwiki.scrape(linkUrl)
    root2 = lxml.html.fromstring(html2)
    cells = root.cssselect('div#wrapper div#content-small') 
    for cellsInfo in cells:
        detail = row.cssselect('p') 
        if detail:
            record['detail'] = "nstaffsmentionedtoday"
            record['ScrapeDate'] = date.today()          
            scraperwiki.sqlite.save(unique_keys=[], data=record)


tr = root.cssselect('ul#results li') #select all of the tr elements
#print tr
for row in tr:
    
    link = row.cssselect('h4 a') 
    if link:
        linkUrl = link[0].attrib.get('href')
        record['linkTtile'] = link[0].text_content()
        record['Linkurl'] = link[0].attrib.get('href')
        urlLists(linkUrl)

