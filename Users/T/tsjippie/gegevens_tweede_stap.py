"""
This is an example of scraping multiple URLs.
"""

import scraperwiki
import re


# The URLs we're going to scrape:

urls = """




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
        
        samengevat = re.findall("Samengevat(.*?)</p>", page, re.DOTALL)
        naam = re.findall("<h1(.*?)</h1>", page, re.DOTALL)
        adres = re.findall("detpag(.*?)</p>", page, re.DOTALL)

        headings = re.findall("<h3>(.*?)</h3>", page, re.DOTALL)

        zwak = re.findall("orange2", page, re.DOTALL)
        zeerzwak = re.findall("red2", page, re.DOTALL)
        basistoezicht = re.findall("green2", page, re.DOTALL)
        
        # Just keep the heading text
        # (Try commenting this out)
        # headings = [gettext(heading) for heading in headings]

        data = {'url': url, 'samengevat': samengevat, 'headings': headings, 'naam': naam, 'adres': adres, 'orange2': zwak, 'red2': zeerzwak, 'green2': basistoezicht}

        scraperwiki.sqlite.save(['url'], data)   # each entry is identified by its url
