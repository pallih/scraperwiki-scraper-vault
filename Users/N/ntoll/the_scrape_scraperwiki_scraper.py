import scraperwiki
import lxml.html
import fluidinfo

# A silly experiment.

page = 0
root_domain = 'http://scraperwiki.com'
url_template = root_domain + '/browse/scrapers/?page=%d'
while True:
    page += 1
    url = url_template % page
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    # Grab data about the scraper scripts.
    script_elements = root.cssselect('li.code_object_line')
    for script in script_elements:
        # some funky stuff to extract data - even scraperwiki's html doesn't make this easy. ;-)
        result = dict()
        try:
            result['screenshot'] = script.cssselect('img')[0].attrib['src']
        except:
            pass
        try:
            anchors = script.cssselect('h3')[0].cssselect('a')
            result['author'] = anchors[0].text
            result['author_url'] = root_domain + anchors[0].attrib['href']
            result['title'] = anchors[1].text
            result['url'] = root_domain + anchors[1].attrib['href']
        except:
            pass
        
        if result.has_key('title'):
            scraperwiki.sqlite.save(unique_keys=['title'], data=result)

    # Only continue if there's more to grab.
    if not root.cssselect('a.next'):
        break