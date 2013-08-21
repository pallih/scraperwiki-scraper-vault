import scraperwiki
import lxml.html


STARTURL = 'http://www.lombardiabeniculturali.it/opere-arte/autori/2974/'
BASEURL = 'http://www.lombardiabeniculturali.it'

def scrapepage(url):
    '''Scrapes the link we need from a record page.'''

    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)

    print('Start scraping record page')

    for el in root.cssselect("div#permalink a"):
        if 'schede-complete' in el.attrib['href']:
            pdfurl = el.attrib['href'] # Full URL here, not relative
            data = {
                'pdfurl': pdfurl,
                'permalink': url,
            }
            scraperwiki.sqlite.save(unique_keys=['pdfurl'], data=data)

def scrapeindex(url):
    '''Moves through a single index page, retrieves links and goes on.'''
    
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)

    print('Start scraping index page')

    for el in root.cssselect("tr.rigaimg a"):
        pageurl = BASEURL + el.attrib['href']
        scrapepage(pageurl)

    nextpage = '' # there are two such elements
    for el in root.cssselect("p.pag a"):
        if el.text == 'next':
            nextpage = el.attrib['href']
    
    if nextpage is not '':
        nexturl = BASEURL + nextpage
        print('Moving to next page')
        scrapeindex(nexturl)

scrapeindex(STARTURL)
