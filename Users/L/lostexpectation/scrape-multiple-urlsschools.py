"""
This is an example of scraping multiple URLs.
"""

import scraperwiki
import re


# The URLs we're going to scrape:

urls = """
http://www.education.ie/en/find-a-school/School-Detail/?roll=00359V
http://www.education.ie/en/find-a-school/School-Detail/?roll=00373P
http://www.education.ie/en/find-a-school/School-Detail/?roll=00467B
http://www.education.ie/en/find-a-school/School-Detail/?roll=00512D
http://www.education.ie/en/find-a-school/School-Detail/?roll=00538V
http://www.education.ie/en/find-a-school/School-Detail/?roll=00590A
http://www.education.ie/en/find-a-school/School-Detail/?roll=00606M
http://www.education.ie/en/find-a-school/School-Detail/?roll=00651R
http://www.education.ie/en/find-a-school/School-Detail/?roll=00697S
http://www.education.ie/en/find-a-school/School-Detail/?roll=00714P
"""

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
        headings = re.findall("<script>(.*?)</script>", page, re.DOTALL)
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
http://www.education.ie/en/find-a-school/School-Detail/?roll=00359V
http://www.education.ie/en/find-a-school/School-Detail/?roll=00373P
http://www.education.ie/en/find-a-school/School-Detail/?roll=00467B
http://www.education.ie/en/find-a-school/School-Detail/?roll=00512D
http://www.education.ie/en/find-a-school/School-Detail/?roll=00538V
http://www.education.ie/en/find-a-school/School-Detail/?roll=00590A
http://www.education.ie/en/find-a-school/School-Detail/?roll=00606M
http://www.education.ie/en/find-a-school/School-Detail/?roll=00651R
http://www.education.ie/en/find-a-school/School-Detail/?roll=00697S
http://www.education.ie/en/find-a-school/School-Detail/?roll=00714P
"""

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
        headings = re.findall("<script>(.*?)</script>", page, re.DOTALL)
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
http://www.education.ie/en/find-a-school/School-Detail/?roll=00359V
http://www.education.ie/en/find-a-school/School-Detail/?roll=00373P
http://www.education.ie/en/find-a-school/School-Detail/?roll=00467B
http://www.education.ie/en/find-a-school/School-Detail/?roll=00512D
http://www.education.ie/en/find-a-school/School-Detail/?roll=00538V
http://www.education.ie/en/find-a-school/School-Detail/?roll=00590A
http://www.education.ie/en/find-a-school/School-Detail/?roll=00606M
http://www.education.ie/en/find-a-school/School-Detail/?roll=00651R
http://www.education.ie/en/find-a-school/School-Detail/?roll=00697S
http://www.education.ie/en/find-a-school/School-Detail/?roll=00714P
"""

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
        headings = re.findall("<script>(.*?)</script>", page, re.DOTALL)
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
http://www.education.ie/en/find-a-school/School-Detail/?roll=00359V
http://www.education.ie/en/find-a-school/School-Detail/?roll=00373P
http://www.education.ie/en/find-a-school/School-Detail/?roll=00467B
http://www.education.ie/en/find-a-school/School-Detail/?roll=00512D
http://www.education.ie/en/find-a-school/School-Detail/?roll=00538V
http://www.education.ie/en/find-a-school/School-Detail/?roll=00590A
http://www.education.ie/en/find-a-school/School-Detail/?roll=00606M
http://www.education.ie/en/find-a-school/School-Detail/?roll=00651R
http://www.education.ie/en/find-a-school/School-Detail/?roll=00697S
http://www.education.ie/en/find-a-school/School-Detail/?roll=00714P
"""

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
        headings = re.findall("<script>(.*?)</script>", page, re.DOTALL)
        # re.DOTALL makes it work across multiple lines as well.

        # Just keep the heading text
        # (Try commenting this out)
        headings = [gettext(heading) for heading in headings]

        data = {'url': url, 'headings': headings}
        scraperwiki.datastore.save(['url'], data)   # each entry is identified by its url
