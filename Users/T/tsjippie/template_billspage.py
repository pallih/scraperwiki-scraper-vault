"""
This is an example of scraping multiple URLs.
"""

import scraperwiki
import re


# The URLs we're going to scrape:

urls = """

http://tkrtp.owinsp.nl/brincode/10BA
http://tkrtp.owinsp.nl/brincode/04HC
http://tkrtp.owinsp.nl/brincode/05GE
http://tkrtp.owinsp.nl/brincode/06CA
http://tkrtp.owinsp.nl/brincode/08SP
http://tkrtp.owinsp.nl/brincode/08YK
http://tkrtp.owinsp.nl/brincode/08YQ
http://tkrtp.owinsp.nl/brincode/09PZ
http://tkrtp.owinsp.nl/brincode/10PC
http://tkrtp.owinsp.nl/brincode/13AN
http://tkrtp.owinsp.nl/brincode/13DM
http://tkrtp.owinsp.nl/brincode/13HR
http://tkrtp.owinsp.nl/brincode/13QN
http://tkrtp.owinsp.nl/brincode/13QN
http://tkrtp.owinsp.nl/brincode/13QN
http://tkrtp.owinsp.nl/brincode/14FU
http://tkrtp.owinsp.nl/brincode/16KK
http://tkrtp.owinsp.nl/brincode/16KK
http://tkrtp.owinsp.nl/brincode/16KK
http://tkrtp.owinsp.nl/brincode/23CL
http://tkrtp.owinsp.nl/brincode/27MB
http://tkrtp.owinsp.nl/brincode/27PR
http://tkrtp.owinsp.nl/brincode/23CL
http://tkrtp.owinsp.nl/brincode/24EJ
http://tkrtp.owinsp.nl/brincode/24MW
http://tkrtp.owinsp.nl/brincode/27MB
http://tkrtp.owinsp.nl/brincode/27YN




""".strip()

urls = urls.splitlines()


# This is a useful helper function that you might want to steal.
# It cleans up the data a bit.
# def gettext(html):
  #  """Return the text within html, removing any HTML tags it contained."""
  #  cleaned = re.sub('<.*?>', '', html)  # remove tags
   # cleaned = ' '.join(cleaned.split())  # collapse whitespace
    # return cleaned



for url in urls:
    print "Scraping", url
    page = scraperwiki.scrape(url)
    if page is not None:
        # Store all the h2 headings (matching "<h2>...</h2>")
        # re.DOTALL makes it work across multiple lines as well.
        
        link = re.findall("zoekresultaat?(.*?)>", page, re.DOTALL)
        
        
        # Just keep the heading text
        # (Try commenting this out)
        # headings = [gettext(heading) for heading in headings]

        data = {'url': url, 'link': link}

        scraperwiki.sqlite.save(['url'], data)   # each entry is identified by its url
"""
This is an example of scraping multiple URLs.
"""

import scraperwiki
import re


# The URLs we're going to scrape:

urls = """

http://tkrtp.owinsp.nl/brincode/10BA
http://tkrtp.owinsp.nl/brincode/04HC
http://tkrtp.owinsp.nl/brincode/05GE
http://tkrtp.owinsp.nl/brincode/06CA
http://tkrtp.owinsp.nl/brincode/08SP
http://tkrtp.owinsp.nl/brincode/08YK
http://tkrtp.owinsp.nl/brincode/08YQ
http://tkrtp.owinsp.nl/brincode/09PZ
http://tkrtp.owinsp.nl/brincode/10PC
http://tkrtp.owinsp.nl/brincode/13AN
http://tkrtp.owinsp.nl/brincode/13DM
http://tkrtp.owinsp.nl/brincode/13HR
http://tkrtp.owinsp.nl/brincode/13QN
http://tkrtp.owinsp.nl/brincode/13QN
http://tkrtp.owinsp.nl/brincode/13QN
http://tkrtp.owinsp.nl/brincode/14FU
http://tkrtp.owinsp.nl/brincode/16KK
http://tkrtp.owinsp.nl/brincode/16KK
http://tkrtp.owinsp.nl/brincode/16KK
http://tkrtp.owinsp.nl/brincode/23CL
http://tkrtp.owinsp.nl/brincode/27MB
http://tkrtp.owinsp.nl/brincode/27PR
http://tkrtp.owinsp.nl/brincode/23CL
http://tkrtp.owinsp.nl/brincode/24EJ
http://tkrtp.owinsp.nl/brincode/24MW
http://tkrtp.owinsp.nl/brincode/27MB
http://tkrtp.owinsp.nl/brincode/27YN




""".strip()

urls = urls.splitlines()


# This is a useful helper function that you might want to steal.
# It cleans up the data a bit.
# def gettext(html):
  #  """Return the text within html, removing any HTML tags it contained."""
  #  cleaned = re.sub('<.*?>', '', html)  # remove tags
   # cleaned = ' '.join(cleaned.split())  # collapse whitespace
    # return cleaned



for url in urls:
    print "Scraping", url
    page = scraperwiki.scrape(url)
    if page is not None:
        # Store all the h2 headings (matching "<h2>...</h2>")
        # re.DOTALL makes it work across multiple lines as well.
        
        link = re.findall("zoekresultaat?(.*?)>", page, re.DOTALL)
        
        
        # Just keep the heading text
        # (Try commenting this out)
        # headings = [gettext(heading) for heading in headings]

        data = {'url': url, 'link': link}

        scraperwiki.sqlite.save(['url'], data)   # each entry is identified by its url
