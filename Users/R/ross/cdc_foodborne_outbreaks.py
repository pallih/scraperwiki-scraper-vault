import scraperwiki
import lxml.html
import urlparse

def cc(c,s):
    return len([x for x in s if x == c])
    

baseurl = 'http://www.cdc.gov/outbreaknet/outbreaks.html'
html = scraperwiki.scrape(baseurl)
page = lxml.html.fromstring(html)
datarows = []

lis = page.cssselect('.main-inner ul li')
for li in lis:
    tc = li.text_content()
    if cc('-',tc) != 2: 
        source,_,pathogen = tc.rpartition('-')
        if not source.strip():
            if pathogen.find('-') > 0:
                source,_,pathogen = pathogen.rpartition('-')
            else:
                continue
        href = urlparse.urljoin(baseurl, li.cssselect('a')[0].attrib.get('href') )
        datarows.append({'source':source, 'pathogen': pathogen, 'link': href})

scraperwiki.sqlite.save(['link'], datarows, verbose=0)