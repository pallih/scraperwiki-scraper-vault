import scraperwiki
import urlparse
import lxml.html

def scrapedivs(url):
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    rows = root.cssselect('div."block size3of4"')
    for row in rows:
        print row
        record = {}
        membername = ''
        membertitle = ''
        memberbio = ''
        header4 = row.cssselect("h4")
        if header4:
            membername = header4[0].text

        spans = row.cssselect("h4 span")
        if spans:
            membertitle = spans[0].text

        p = row.cssselect("p")
        if p:
            memberbio = p[-1].text_content()
        
        record['URL'] = url
        record['Name'] = membername
        record['Title'] = membertitle
        record['Biography'] = memberbio
        print record, 'printed!'

        scraperwiki.sqlite.save(["Name"],record)

ccglist = ['www.brentccg.nhs.uk/', 'www.ealingccg.nhs.uk/', 'www.hounslowccg.nhs.uk/', 'www.westlondonccg.nhs.uk/', 'www.centrallondonccg.nhs.uk/', 'www.harrowccg.nhs.uk/', 'www.hammersmithfulhamccg.nhs.uk/']

for ccgs in ccglist:
    scrapedivs('http://'+ccgs+'about-us/board.aspx')

import scraperwiki
import urlparse
import lxml.html

def scrapedivs(url):
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    rows = root.cssselect('div."block size3of4"')
    for row in rows:
        print row
        record = {}
        membername = ''
        membertitle = ''
        memberbio = ''
        header4 = row.cssselect("h4")
        if header4:
            membername = header4[0].text

        spans = row.cssselect("h4 span")
        if spans:
            membertitle = spans[0].text

        p = row.cssselect("p")
        if p:
            memberbio = p[-1].text_content()
        
        record['URL'] = url
        record['Name'] = membername
        record['Title'] = membertitle
        record['Biography'] = memberbio
        print record, 'printed!'

        scraperwiki.sqlite.save(["Name"],record)

ccglist = ['www.brentccg.nhs.uk/', 'www.ealingccg.nhs.uk/', 'www.hounslowccg.nhs.uk/', 'www.westlondonccg.nhs.uk/', 'www.centrallondonccg.nhs.uk/', 'www.harrowccg.nhs.uk/', 'www.hammersmithfulhamccg.nhs.uk/']

for ccgs in ccglist:
    scrapedivs('http://'+ccgs+'about-us/board.aspx')

