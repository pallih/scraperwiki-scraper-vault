import scraperwiki
import lxml.html
import datetime
import dateutil.parser

#Get official speeches recorded by the Prime Ministers office at http://www.number10.gov.uk

base = 'http://www.dpm.cabinetoffice.gov.uk'

#the dpm site is broken (the next buttons dont work propoerly, so we'll index the pages we're sent to and presence check againt them later
pages = []
links = []
html = scraperwiki.scrape(base+'/speeches/');

print html

root = lxml.html.fromstring(html)
next = root.cssselect(".pane-content .pager .pager-next a")

while True:

    #grab links
    for node in root.cssselect(".view-content dl.search-results dt.title"):
        link = node.cssselect("a")
        print "Saving link:"+link[0].text_content()
        links.append(link[0].get('href'))

    #if there's a next page and it's not already in the list then then grab it
    if(len(next)>0 and not next[0].get('href') in pages):
        pages.append(next[0].get('href'))
        print 'Getting next page'+next[0].get('href')
        html = scraperwiki.scrape(base+next[0].get('href'))
        root = lxml.html.fromstring(html)
        next = root.cssselect(".pane-content .pager .pager-next a")        
    else:
        print 'Already grabbed page '+next[0].get('href')
        break

for link in links

    
