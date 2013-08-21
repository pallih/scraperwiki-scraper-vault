# FIXME: Better url would be livenation's page.

# Ents24 uses RDF, nice.  But it doesn't seem to contain events,
# just metadata about the Guildhall.  They do make use of the
# hCalendar microformat, though.
#from rdflib.graph import Graph
#g = Graph()
#g.parse("http://www.ents24.com/web/venue/Southampton/Guildhall-1712.html", format="rdfa")

import scraperwiki
import lxml.html

html = scraperwiki.scrape("http://www.ents24.com/web/venue/Southampton/Guildhall-1712.html")
root = lxml.html.fromstring(html)

for event in root.cssselect(".vevent"):
    e = {
        'start': event.cssselect(".dtstart")[0].attrib.get("title"),
        'url': event.cssselect(".url")[0].attrib.get("href"),
        'summary': event.cssselect(".summary")[0].text_content().strip(),
    }

    scraperwiki.sqlite.save(["url"], e)
