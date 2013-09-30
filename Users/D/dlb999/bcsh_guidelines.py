import urlparse
import lxml.html
import scraperwiki
import datetime

base = 'http://www.bcshguidelines.com/4_HAEMATOLOGY_GUIDELINES.html?dtype=All&dpage=0&dstatus=All&dsdorder=&dstorder=&dmax=9999&dsearch=&sspage=0&ipage=0#gl'

dt = datetime.datetime.now().isoformat()
html = scraperwiki.scrape(base).decode('utf-8', 'ignore')
page = lxml.html.fromstring( unicode(html) )
rows = page.cssselect('tr.topics')
for row in rows:
    topic = row[0].text_content().strip()
    span = row[1].cssselect('.glTitle')[0]
    title = span.text_content()
    a = row[3].cssselect('a')
    if not a:
        continue
    pdf = a[0].attrib.get('href')
    pdf = urlparse.urljoin(base, pdf)

    # TODO: Check if we have the link in the database, if then do nothing.
    # otherwise we should add it with a date of today so that the RSS will 
    # work.
    try:
        results = scraperwiki.sqlite.select("count(*) from swdata where link='%s'" % pdf)
    except:
        results = [{'count(*)':0}]
    if results[0]['count(*)'] == 0:
        scraperwiki.sqlite.save(['title'], {'title': title, 'link': pdf, 'date': dt })


import urlparse
import lxml.html
import scraperwiki
import datetime

base = 'http://www.bcshguidelines.com/4_HAEMATOLOGY_GUIDELINES.html?dtype=All&dpage=0&dstatus=All&dsdorder=&dstorder=&dmax=9999&dsearch=&sspage=0&ipage=0#gl'

dt = datetime.datetime.now().isoformat()
html = scraperwiki.scrape(base).decode('utf-8', 'ignore')
page = lxml.html.fromstring( unicode(html) )
rows = page.cssselect('tr.topics')
for row in rows:
    topic = row[0].text_content().strip()
    span = row[1].cssselect('.glTitle')[0]
    title = span.text_content()
    a = row[3].cssselect('a')
    if not a:
        continue
    pdf = a[0].attrib.get('href')
    pdf = urlparse.urljoin(base, pdf)

    # TODO: Check if we have the link in the database, if then do nothing.
    # otherwise we should add it with a date of today so that the RSS will 
    # work.
    try:
        results = scraperwiki.sqlite.select("count(*) from swdata where link='%s'" % pdf)
    except:
        results = [{'count(*)':0}]
    if results[0]['count(*)'] == 0:
        scraperwiki.sqlite.save(['title'], {'title': title, 'link': pdf, 'date': dt })


