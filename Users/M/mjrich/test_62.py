# Blank Python
import scraperwiki
import lxml.html 




def page_scrape(html):
    full_list = []
    root = lxml.html.fromstring(html)
    for orderedlist in root.cssselect("ol"):
        for li in orderedlist:
            for (counter, a) in enumerate(li):
                full_list += [(a.text)]
    return full_list


url = "http://www.beliebte-vornamen.de/jahrgang/j1999"
html = scraperwiki.scrape(url)

print page_scrape(html)



#years = range(1890, 2012)
#for y in years:
#    data = {}
#    url = "http://www.beliebte-vornamen.de/jahrgang/j%d" % (y)
#    html = scraperwiki.scrape(url)
#    data['year'] = y
#    data['names'] = page_scrape(html)
#    scraperwiki.sqlite.save(["year"], data) 






