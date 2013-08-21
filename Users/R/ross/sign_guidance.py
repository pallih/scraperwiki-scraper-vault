import re
import urlparse
import lxml.html
import scraperwiki

base = "http://www.sign.ac.uk/guidelines/published/numlist.html"
page = lxml.html.fromstring( scraperwiki.scrape( base ) )

links = page.cssselect('.tabletext a')
for link in links:
    l = urlparse.urljoin( base, link.attrib.get('href') )
    if not l.endswith('.html'):
        continue

    m = re.match('^http://www.sign.ac.uk/guidelines/fulltext/(\d+)/index.html', l)
    if not m:
        continue

    pdf_link = 'http://www.sign.ac.uk/pdf/qrg%s.pdf' % (m.groups(0)[0],)
    title = link.text_content().strip().replace('\r\n', '')
    title = ' '.join(title.split())

    scraperwiki.sqlite.save( ['title'], {'title':title, 'link': pdf_link})

import re
import urlparse
import lxml.html
import scraperwiki

base = "http://www.sign.ac.uk/guidelines/published/numlist.html"
page = lxml.html.fromstring( scraperwiki.scrape( base ) )

links = page.cssselect('.tabletext a')
for link in links:
    l = urlparse.urljoin( base, link.attrib.get('href') )
    if not l.endswith('.html'):
        continue

    m = re.match('^http://www.sign.ac.uk/guidelines/fulltext/(\d+)/index.html', l)
    if not m:
        continue

    pdf_link = 'http://www.sign.ac.uk/pdf/qrg%s.pdf' % (m.groups(0)[0],)
    title = link.text_content().strip().replace('\r\n', '')
    title = ' '.join(title.split())

    scraperwiki.sqlite.save( ['title'], {'title':title, 'link': pdf_link})

