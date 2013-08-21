import scraperwiki
import lxml.html
import re

blacklist = [ 'bdi', 'frame', 'frameset', 'isindex', 'nobr', 'spacer', 'noframes', 'rp', 'rt', 'ruby', ]

html = scraperwiki.scrape("https://developer.mozilla.org/en/HTML/Element")

root = lxml.html.fromstring(html)

for element in root.cssselect("#section_1 ul code a"):
    href = element.attrib.get('href')
    name = re.search("[^<>]+", element.text_content()).group(0)

    print scraperwiki.sqlite.show_tables() 

    try:
        # Uncomment this if you want to only get info for elements not already in the db
        # print "attempting to see if " + name + " already is scraped"
        # result = scraperwiki.sqlite.select("* from swdata where name='" + name + "' limit 10")
        # if len(result) > 0:
        #    print name + ' already scraped'
        #    continue
    except:
        print "exception on " + name
        pass
    
    # Don't attempt elements in the blacklist since they don't exist on MDN yet
    if name in blacklist:
        print name + ' is blacklisted'
        continue

    try:
        print "Scraping " + name
        docs = scraperwiki.scrape(href)
    except:
        continue

    docsHtml = lxml.html.fromstring(docs)

    summary = docsHtml.cssselect("#Summary + h2 + p")

    if len(summary) < 1:
        continue

    summaryContent = summary[0].text_content()

    data = {
        'href': href,
        'name': name,
        'summary': summaryContent
    }

    scraperwiki.sqlite.save(unique_keys=['name'], data=data)

