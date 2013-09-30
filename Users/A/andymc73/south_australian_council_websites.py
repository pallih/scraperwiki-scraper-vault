import scraperwiki
import lxml.html
from pprint import pprint

# Future grand plan - make it work for all of oz
# states = [ 'SA' ]
# councilsSources[ 'SA' ] = "http://www.lga.sa.gov.au/site/page.cfm?u=210";
# TODO: foreach over councilsSources and call method applicable for each state
# But thats a long way away

pageLinkPrefix = "http://www.lga.sa.gov.au/site/"
councilsSources = "http://www.lga.sa.gov.au/site/page.cfm?u=210";

# Load the list of links from here
# Visit each in turn and parse the tables

s = scraperwiki.scrape( councilsSources)
root = lxml.html.fromstring(s)
root.make_links_absolute(pageLinkPrefix, True)
selector = "uContentList"

# Look for the div containing the UL of hyperlinks to council pages
# For now just assume there is only one...

pageList = root.find_class(selector)[0]

# Iterate over all page links, assume only one href..
for h in pageList.cssselect("a"):
    page = h.xpath( "@href")[0]
    council = h.text_content()
#
    print( "%s: %s" % (council, page))

    # and scrape it
    # TODO make this a function...
    c = scraperwiki.scrape( page)

    # find the div called content and extract the table
    croot = lxml.html.fromstring(c)
    cdiv = croot.get_element_by_id("contentDiv")
    cdiv = cdiv.get_element_by_id("content")
    # get the table item
    #t1 = cdiv.xpath("/table/tbody/tr[td/text()='URL:']]/td[last()]/a/text()")
    #print lxml.html.tostring(cdiv)

    t = cdiv.cssselect("table")
    #print lxml.html.tostring(t[0])

    e1 = t[0].xpath("tr[td/text()='General Email:']/td[last()]/a/text()")
    t1 = t[0].xpath("tr[td/text()='URL:']/td[last()]/a/text()")

    # SOme dont exist
    if e1 is None or len(e1)==0:
        e1 = ""
    else:
        e1 = e1[0]
    if t1 is None or len(t1)==0:
        t1 = ""
    else:
        t1 = t1[0]


    print( "%s: %s, %s" % (council, e1, t1))

    data = {
    'id': council,
    'email': e1,
    'url': t1,
    }

    scraperwiki.sqlite.save(unique_keys=['id'], data=data)

# end for

import scraperwiki
import lxml.html
from pprint import pprint

# Future grand plan - make it work for all of oz
# states = [ 'SA' ]
# councilsSources[ 'SA' ] = "http://www.lga.sa.gov.au/site/page.cfm?u=210";
# TODO: foreach over councilsSources and call method applicable for each state
# But thats a long way away

pageLinkPrefix = "http://www.lga.sa.gov.au/site/"
councilsSources = "http://www.lga.sa.gov.au/site/page.cfm?u=210";

# Load the list of links from here
# Visit each in turn and parse the tables

s = scraperwiki.scrape( councilsSources)
root = lxml.html.fromstring(s)
root.make_links_absolute(pageLinkPrefix, True)
selector = "uContentList"

# Look for the div containing the UL of hyperlinks to council pages
# For now just assume there is only one...

pageList = root.find_class(selector)[0]

# Iterate over all page links, assume only one href..
for h in pageList.cssselect("a"):
    page = h.xpath( "@href")[0]
    council = h.text_content()
#
    print( "%s: %s" % (council, page))

    # and scrape it
    # TODO make this a function...
    c = scraperwiki.scrape( page)

    # find the div called content and extract the table
    croot = lxml.html.fromstring(c)
    cdiv = croot.get_element_by_id("contentDiv")
    cdiv = cdiv.get_element_by_id("content")
    # get the table item
    #t1 = cdiv.xpath("/table/tbody/tr[td/text()='URL:']]/td[last()]/a/text()")
    #print lxml.html.tostring(cdiv)

    t = cdiv.cssselect("table")
    #print lxml.html.tostring(t[0])

    e1 = t[0].xpath("tr[td/text()='General Email:']/td[last()]/a/text()")
    t1 = t[0].xpath("tr[td/text()='URL:']/td[last()]/a/text()")

    # SOme dont exist
    if e1 is None or len(e1)==0:
        e1 = ""
    else:
        e1 = e1[0]
    if t1 is None or len(t1)==0:
        t1 = ""
    else:
        t1 = t1[0]


    print( "%s: %s, %s" % (council, e1, t1))

    data = {
    'id': council,
    'email': e1,
    'url': t1,
    }

    scraperwiki.sqlite.save(unique_keys=['id'], data=data)

# end for

