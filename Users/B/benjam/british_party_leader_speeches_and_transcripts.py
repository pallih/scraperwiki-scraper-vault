import scraperwiki
import lxml.html
import datetime
import dateutil.parser

#Get official speeches recorded by the Prime Ministers office at http://www.number10.gov.uk

base = 'http://www.number10.gov.uk'
links = []
html = scraperwiki.scrape(base+'/news-type/speeches-and-transcripts/');

print html

root = lxml.html.fromstring(html)
next = root.cssselect("#main-content .listing-pagination .next a")

while True:
    for node in root.cssselect("#main-content .news-listing-item"):
        link = node.cssselect("h3 a")
        print "Saving link:"+link[0].text_content()
        links.append(link[0].get('href'))

    if(len(next)>0):
        print 'Getting next page'+next[0].get('href')
        html = scraperwiki.scrape(base+next[0].get('href'))
        root = lxml.html.fromstring(html)
        next = root.cssselect("#main-content .listing-pagination .next a")
    else:
        break


for link in links:
    print 'Fetching link: '+link
    html = scraperwiki.scrape(link)
    root = lxml.html.fromstring(html)
    
    data = {        
        'source': link,
        'speaker' : 'Prime Minister'
    }
    if(len(root.cssselect('#main-content .np-title h2')) > 0):
        data['title'] = root.cssselect('#main-content .np-title h2')[0].text_content()
    if(len(root.cssselect('#main-content .np-title .news-date')) > 0):
        data['datetime'] = dateutil.parser.parse(root.cssselect('#main-content .np-title .news-date')[0].text_content()) 
    segments = root.cssselect('#main-content .np-content')
    if(len(segments)>0):
        data['speech'] = '\n'.join(segment.text_content() for segment in segments) 
    scraperwiki.sqlite.save(unique_keys=['source'], data=data)

