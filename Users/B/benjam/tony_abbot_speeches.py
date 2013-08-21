import scraperwiki
import lxml.html
import re
import datetime
import dateutil.parser

#Get official speeches recorded by the The Liberal Party office at http://www.tonyabbott.com.au and attribute to Tony Abbot

base = 'http://www.tonyabbott.com.au'
links = []
html = scraperwiki.scrape(base+'/LatestNews/Speeches.aspx')

print html

root = lxml.html.fromstring(html)
if(root.cssselect("table.PagingTable td a.CommandButton")[len(root.cssselect("table.PagingTable td a.CommandButton"))-2].text_content() == 'Next'):
    next = root.cssselect("table.PagingTable td a.CommandButton")[len(root.cssselect("table.PagingTable td a.CommandButton"))-2]
else:
    next = []

while True:
    for node in root.cssselect("#articles .Speecheshideimage"):
        link = node.cssselect("h2 a")
        print "Saving link:"+link[0].text_content()
        links.append(link[0].get('href'))

    if(root.cssselect("table.PagingTable td a.CommandButton")[len(root.cssselect("table.PagingTable td a.CommandButton"))-2].text_content() == 'Next'):
        print 'Getting next page'+next.get('href')
        html = scraperwiki.scrape(base+next.get('href'))
        root = lxml.html.fromstring(html)
        next = root.cssselect("table.PagingTable td a.CommandButton")[len(root.cssselect("table.PagingTable td a.CommandButton"))-2]
    else:
        break

print links

for link in links:
    print 'Fetching link: '+link
    html = scraperwiki.scrape(link)
    root = lxml.html.fromstring(html)
    data = {
        'speaker': 'Tony Abbot',
        'source' : base+link 
    }
    if(len(root.cssselect('#articles h2')) >0):
        data['title'] = root.cssselect('#articles h2')[0].text_content(),
    if(len(root.cssselect('#articles .articleInfo p')) >0):
        datetime = root.cssselect('#articles .articleInfo p')[0].text_content(),
        datetimesegment = re.split('^.*Posted\son\s',str(datetime))[1]
        datetimesegment = re.split('\W*', datetimesegment)
        data['datetime'] = dateutil.parser.parse(' '.join(str(x) for x in datetimesegment))
    if(len(root.cssselect('#articles .articleListing')) > 0):
        segments = root.cssselect('#articles .articleListing')
        speech = segments[0].text_content()
        data['speech'] = speech

    scraperwiki.sqlite.save(unique_keys=['source'], data=data)