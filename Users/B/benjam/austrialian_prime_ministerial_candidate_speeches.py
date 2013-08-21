import scraperwiki
import lxml.html
import datetime
import dateutil.parser

#Get official speeches recorded by the Prime Ministers office at http://www.pm.gov.au and attribute to Julia Gillard

base = 'http://www.pm.gov.au'
links = []
html = scraperwiki.scrape(base+'/press-office?tid%5B%5D=363&keys=&date_filter%5Bvalue%5D%5Byear%5D=&date_filter%5Bvalue%5D%5Bmonth%5D=')

root = lxml.html.fromstring(html)
next = root.cssselect("ul.pager .pager-next a")

while True:
    for node in root.cssselect("#main .node.press-office-listing"):
        link = node.cssselect("h3 a")
        print "Saving link:"+link[0].text_content()
        links.append(link[0].get('href'))

    if(len(next)>0):
        print 'Getting next page'+next[0].get('href')
        html = scraperwiki.scrape(base+next[0].get('href'))
        root = lxml.html.fromstring(html)
        next = root.cssselect("ul.pager .pager-next a")
    else:
        break

print links

for link in links:
    print 'Fetching link: '+link
    html = scraperwiki.scrape(base+link)
    root = lxml.html.fromstring(html)
    
    data = {        
        'source': base+link 
    }
    if(len(root.cssselect('#main h1')) > 0):
        data['title'] = root.cssselect('#main h1')[0].text_content()
    if(len(root.cssselect('#main .content h3.date')) > 0):
        data['datetime'] = dateutil.parser.parse(root.cssselect('#main .content h3.date')[0].text_content()) 
    if(len(root.cssselect('#main .content h3')) > 1):
        data['speaker'] = root.cssselect('#main .content h3')[1].text_content()
    if(len(root.cssselect('#main .content h3')) > 2):
        data['location'] = root.cssselect('#main .content h3')[2].text_content()
    segments = root.cssselect('#main .content p')
    if(len(segments)>0):
        data['speech'] = '\n'.join(segment.text_content() for segment in segments) 
    
    scraperwiki.sqlite.save(unique_keys=['source'], data=data)
