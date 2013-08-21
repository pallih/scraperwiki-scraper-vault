import scraperwiki
import lxml.html
from urlparse import urljoin

root_page = "http://gmc-onlineeducationreports.org/GroupCluster.aspx?agg=AGG44%7c2011"

# Used on both root_page and the deanery pages.
links_css = "ul.my-list li a"
csv_css = ".csv a"

already_fetched = []
try:
    res = scraperwiki.sqlite.select('name from links')
    already_fetched = sum([v.values() for v in res], [])
except:
    pass
print 'We have already fetched %d items' % len(already_fetched)

csv_links = []

# Get list of deaneries
root_html = lxml.html.fromstring( scraperwiki.scrape( root_page ) )
deaneries = root_html.cssselect( links_css )
print 'Processing %d deaneries' % len(deaneries)
current = 1
for deanery in deaneries:
    print 'Processing %d/%d' % (current,len(deaneries),)
    current = current + 1
    deanery_link = urljoin(root_page,deanery.attrib.get('href'))
    deanery_html = lxml.html.fromstring( scraperwiki.scrape( deanery_link ) )
    trusts = deanery_html.cssselect( links_css )
    print 'Processing %d trusts' % len(trusts)
    for trust in trusts:
        if trust.text_content() in already_fetched:
            print 'Skipping %s' % trust.text_content()
            continue
        trust_link = urljoin(root_page,trust.attrib.get('href'))
        page = lxml.html.fromstring( scraperwiki.scrape( trust_link ) )
        csv_link = urljoin(root_page, page.cssselect( csv_css )[0].attrib.get('href') )
        scraperwiki.sqlite.save(['csv'], {'csv':csv_link, 'name': trust.text_content()}, table_name='links')   


