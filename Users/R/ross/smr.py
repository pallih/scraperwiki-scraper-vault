import scraperwiki
from urlparse import urljoin
from lxml.html import fromstring

u = 'https://indicators.ic.nhs.uk/webview/velocity?mode=searchresult&id=search&word=SMR'

page = fromstring(scraperwiki.scrape(u))
links = page.cssselect(".icon,.nodetext")
for link in links:
    if not link.get('href', '') or link.get('href', '') == 'webview/':
        continue
    newpage = fromstring(scraperwiki.scrape(urljoin("https://indicators.ic.nhs.uk", link.get('href'))))
    title = newpage.cssselect('.topspan')
    if title:
        title = title.text_content()
    else:
        title = "Couldn't find it"

    for l in newpage.cssselect('.ddititle a'):
        print l.get('href', '')
        if l.get('href', '').lower().endswith('.xls'):
            data = {'link': urljoin("https://indicators.ic.nhs.uk",l.get('href')), 'title': title}
            scraperwiki.sqlite.save( ['link'], data )