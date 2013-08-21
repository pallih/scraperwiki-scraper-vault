import scraperwiki
from lxml import etree, html

NSMAP = {
    'a' : "http://www.w3.org/2005/Atom",
    'dcterms': "http://purl.org/dc/terms/",
    'media': "http://search.yahoo.com/mrss/"
}

def scrape_category(category):
    
    feed_url = "http://feeds.bbc.co.uk/iplayer/categories/{category}/radio/list".format(category=category)
    
    xml = scraperwiki.scrape(feed_url)

    root = etree.fromstring(xml)
    for entry in root.xpath('/a:feed/a:entry', namespaces=NSMAP):
        title = entry.find('a:title', namespaces=NSMAP).text
        href = entry.find('a:link[@rel="alternate"]', namespaces=NSMAP).attrib['href']
    
        # Parse the content HTML:
        content = entry.find('a:content', namespaces=NSMAP).text
        croot = html.fromstring(content)
        ps = croot.xpath('p')
        description = ps[-1].text if ps else None
    
        data = {
            'title': title,
            'href': href,
            'description': description,
            'category': category,
        }
    
        scraperwiki.sqlite.save(unique_keys=['title'], data=data)

for category in ['comedy', 'factual']:
    scrape_category(category)