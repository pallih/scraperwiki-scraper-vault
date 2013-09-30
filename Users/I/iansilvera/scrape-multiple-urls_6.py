"""
This is an example of scraping multiple URLs.
"""

import scraperwiki
import re


# The URLs we're going to scrape:

urls = """

http://www.wwe.com/superstars/cmpunk
http://www.wwe.com/superstars/sheamus
http://www.wwe.com/superstars/themiz
http://www.wwe.com/superstars/antoniocesaro
http://www.wwe.com/superstars/divas/layla
http://www.wwe.com/superstars/kofikingston
http://www.wwe.com/superstars/rtruth
http://www.wwe.com/superstars/abdullahthebutcher
http://www.wwe.com/superstars/divas/aj





urls = urls.splitlines()





for url in urls:
    print "Scraping", url
    page = scraperwiki.scrape(url)
    if page is not None:
        # Store all the h2 headings (matching "<h2>...</h2>")
        headings = re.findall("<h2>(.*?)</h2>", page, re.DOTALL)
        # re.DOTALL makes it work across multiple lines as well.

        # Just keep the heading text
        # (Try commenting this out)
        headings = [gettext(heading) for heading in headings]

        data = {'url': url, 'headings': headings}
        scraperwiki.datastore.save(['url'], data)   # each entry is identified by its url
"""
This is an example of scraping multiple URLs.
"""

import scraperwiki
import re


# The URLs we're going to scrape:

urls = """

http://www.wwe.com/superstars/cmpunk
http://www.wwe.com/superstars/sheamus
http://www.wwe.com/superstars/themiz
http://www.wwe.com/superstars/antoniocesaro
http://www.wwe.com/superstars/divas/layla
http://www.wwe.com/superstars/kofikingston
http://www.wwe.com/superstars/rtruth
http://www.wwe.com/superstars/abdullahthebutcher
http://www.wwe.com/superstars/divas/aj





urls = urls.splitlines()





for url in urls:
    print "Scraping", url
    page = scraperwiki.scrape(url)
    if page is not None:
        # Store all the h2 headings (matching "<h2>...</h2>")
        headings = re.findall("<h2>(.*?)</h2>", page, re.DOTALL)
        # re.DOTALL makes it work across multiple lines as well.

        # Just keep the heading text
        # (Try commenting this out)
        headings = [gettext(heading) for heading in headings]

        data = {'url': url, 'headings': headings}
        scraperwiki.datastore.save(['url'], data)   # each entry is identified by its url
