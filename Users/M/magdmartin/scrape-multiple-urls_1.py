"""
This is an example of scraping multiple URLs.
"""

import scraperwiki
import re


# The URLs we're going to scrape:

urls = """

http://scholar.google.com/citations?hl=en&user=D8lvl64AAAAJ&view_op=list_works
http://scholar.google.com/citations?user=HwXwfLkAAAAJ&hl=en
""".strip()

urls = urls.splitlines()


# This is a useful helper function that you might want to steal.
# It cleans up the data a bit.
def gettext(html):
    """Return the text within html, removing any HTML tags it contained."""
    cleaned = re.sub('<.*?>', '', html)  # remove tags
    cleaned = ' '.join(cleaned.split())  # collapse whitespace
    return cleaned


for url in urls:
    print "Scraping", url
    page = scraperwiki.scrape(url)
    if page is not None:
        # Store all the h2 headings (matching "<h2>...</h2>")
        moviles = re.findall("div#center-column a,span.price", page, re.DOTALL)
        # re.DOTALL makes it work across multiple lines as well.

        # Just keep the heading text
        # (Try commenting this out)
       

        data = {'url': url, 'moviles': moviles}
        scraperwiki.sqlite.save(['url'], data)   # each entry is identified by its url
"""
This is an example of scraping multiple URLs.
"""

import scraperwiki
import re


# The URLs we're going to scrape:

urls = """

http://scholar.google.com/citations?hl=en&user=D8lvl64AAAAJ&view_op=list_works
http://scholar.google.com/citations?user=HwXwfLkAAAAJ&hl=en
""".strip()

urls = urls.splitlines()


# This is a useful helper function that you might want to steal.
# It cleans up the data a bit.
def gettext(html):
    """Return the text within html, removing any HTML tags it contained."""
    cleaned = re.sub('<.*?>', '', html)  # remove tags
    cleaned = ' '.join(cleaned.split())  # collapse whitespace
    return cleaned


for url in urls:
    print "Scraping", url
    page = scraperwiki.scrape(url)
    if page is not None:
        # Store all the h2 headings (matching "<h2>...</h2>")
        moviles = re.findall("div#center-column a,span.price", page, re.DOTALL)
        # re.DOTALL makes it work across multiple lines as well.

        # Just keep the heading text
        # (Try commenting this out)
       

        data = {'url': url, 'moviles': moviles}
        scraperwiki.sqlite.save(['url'], data)   # each entry is identified by its url
