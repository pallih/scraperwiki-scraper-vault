import scraperwiki
from BeautifulSoup import BeautifulSoup
from urlparse import urlparse,parse_qs


index_pages = ["http://www.direct.gov.uk/en/Diol1/DoItOnline/DoitonlineA-Z/index.htm?indexChar=%s" % x for x in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"]

for page in index_pages:
    html = scraperwiki.scrape(page)
    soup = BeautifulSoup(html)
    subheads = soup.findAll('div', {'class':'subContent'})
    for subhead in subheads:
        parent = subhead.parent
        if not (parent.has_key('class') and parent['class'] == 'subContent'):
            continue
        main_title =  subhead.find("h4").text   
        links = subhead.findAll("li")
        for link in links:
            anchor = link.find("a")
            href = anchor["href"]
            url = urlparse(href)
            query = parse_qs(url.query)     
            if (query.has_key(u'LGIL') and query.has_key(u'LGSL') and query.has_key(u'ServiceName')):
                lgil = query[u'LGIL'][0]
                lgsl = query[u'LGSL'][0]
                service_name = query[u'ServiceName'][0]
            else:
                lgil,lgsl,service_name = "","",""              
            title = anchor.text.replace("Opens new window","")
            record = {
                'title': main_title,
                'url': href,
                'lgil': lgil,
                'lgsl': lgsl,
                'service_name': service_name,
                'service_title': title,
            }
            scraperwiki.sqlite.save(['service_name','title','lgil','url'], record) 
    