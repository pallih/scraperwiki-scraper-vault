"""
This is an example of scraping multiple URLs.
"""
import scraperwiki

import scraperwiki
import BeautifulSoup

import re


# The URLs we're going to scrape:

urls = """
http://www.guildofmasterchimneysweeps.co.uk
http://www.yell.com/
http://www.findacraftsman.com/
http://www.findacraftsman.com/
http://www.guildproperty.co.uk/
http://www.godt.org.uk/Trainers 
http://www.freeindex.co.uk/

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
    soup = BeautifulSoup(gettext(html)) = souptable')
    row = page.table.tr')
    agency = soutr.child[2]
    if page is not None:
        # Store all the h2 headings (matching "<h2>...</h2>")
        tables = re.findall("tr", page, re.DOTALL)
        # re.DOTALL makes it work across multiple lines as well.

        # Just keep the heading text
        # (Try commenting this out)
        table = [gettext(table) for table in tables]

        data = {'url': url, 'table': headings}
        scraperwiki.datastore.save(['url'], data)   # each entry is identified by its url
"""
This is an example of scraping multiple URLs.
"""
import scraperwiki

import scraperwiki
import BeautifulSoup

import re


# The URLs we're going to scrape:

urls = """
http://www.guildofmasterchimneysweeps.co.uk
http://www.yell.com/
http://www.findacraftsman.com/
http://www.findacraftsman.com/
http://www.guildproperty.co.uk/
http://www.godt.org.uk/Trainers 
http://www.freeindex.co.uk/

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
    soup = BeautifulSoup(gettext(html)) = souptable')
    row = page.table.tr')
    agency = soutr.child[2]
    if page is not None:
        # Store all the h2 headings (matching "<h2>...</h2>")
        tables = re.findall("tr", page, re.DOTALL)
        # re.DOTALL makes it work across multiple lines as well.

        # Just keep the heading text
        # (Try commenting this out)
        table = [gettext(table) for table in tables]

        data = {'url': url, 'table': headings}
        scraperwiki.datastore.save(['url'], data)   # each entry is identified by its url
