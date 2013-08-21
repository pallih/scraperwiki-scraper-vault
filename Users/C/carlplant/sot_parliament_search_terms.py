import scraperwiki
import lxml.html
import dateutil.parser 
from datetime import date

record = {}

html = scraperwiki.scrape("http://www.parliament.uk/search/results/?type=advanced&adv_all=stoke+on+trent&adv_datesearch=after&adv_datefrom=01/02/2013&filter=debates,handeb,commwa,lordshd,lordswa,hanidx")
root = lxml.html.fromstring(html)

today = date.today()
print today

print today.strptime(today, '%d/%m/%Y').date()

"""def urlLists(linkUrl):
    
    html2 = scraperwiki.scrape(linkUrl)
    root2 = lxml.html.fromstring(html2)
    cells = root.cssselect('div#wrapper div#content') 
    for cellsInfo in cells:
        detail = row.cssselect('p') 
        textDetail = detail[0].text_content()
        print textDetail
        if detail:
            record['detail'] = "stokementionedtoday"
            record['ScrapeDate'] = date.today()          
            #scraperwiki.sqlite.save(unique_keys=[], data=record)


tr = root.cssselect('ul#results li') #select all of the tr elements
#print tr
for row in tr:
    
    link = row.cssselect('h4 a') 
    if link:
        linkUrl = link[0].attrib.get('href')
        record['linkTtile'] = link[0].text_content()
        record['Linkurl'] = link[0].attrib.get('href')
        urlLists(linkUrl)"""

