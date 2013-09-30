"""
This is an example of scraping multiple URLs.
"""

import scraperwiki
import re

# The URLs we're going to scrape:

urls = """
http://evenementen.uitslagen.nl/2010/amsterdammarathon/details.php?t=en&s=4975
http://evenementen.uitslagen.nl/2010/amsterdammarathon/details.php?t=en&s=4976
http://evenementen.uitslagen.nl/2010/amsterdammarathon/details.php?t=en&s=4977
http://evenementen.uitslagen.nl/2010/amsterdammarathon/details.php?t=en&s=4978
http://evenementen.uitslagen.nl/2010/amsterdammarathon/details.php?t=en&s=4979
http://evenementen.uitslagen.nl/2010/amsterdammarathon/details.php?t=en&s=4980
http://evenementen.uitslagen.nl/2010/amsterdammarathon/details.php?t=en&s=4981
http://evenementen.uitslagen.nl/2010/amsterdammarathon/details.php?t=en&s=4982
http://evenementen.uitslagen.nl/2010/amsterdammarathon/details.php?t=en&s=4983
http://evenementen.uitslagen.nl/2010/amsterdammarathon/details.php?t=en&s=4984
http://evenementen.uitslagen.nl/2010/amsterdammarathon/details.php?t=en&s=4985
http://evenementen.uitslagen.nl/2010/amsterdammarathon/details.php?t=en&s=4986
http://evenementen.uitslagen.nl/2010/amsterdammarathon/details.php?t=en&s=4987
http://evenementen.uitslagen.nl/2010/amsterdammarathon/details.php?t=en&s=4988
http://evenementen.uitslagen.nl/2010/amsterdammarathon/details.php?t=en&s=4989
http://evenementen.uitslagen.nl/2010/amsterdammarathon/details.php?t=en&s=4990
http://evenementen.uitslagen.nl/2010/amsterdammarathon/details.php?t=en&s=4991
http://evenementen.uitslagen.nl/2010/amsterdammarathon/details.php?t=en&s=4992
http://evenementen.uitslagen.nl/2010/amsterdammarathon/details.php?t=en&s=4993
http://evenementen.uitslagen.nl/2010/amsterdammarathon/details.php?t=en&s=4994
http://evenementen.uitslagen.nl/2010/amsterdammarathon/details.php?t=en&s=4995
http://evenementen.uitslagen.nl/2010/amsterdammarathon/details.php?t=en&s=4996
http://evenementen.uitslagen.nl/2010/amsterdammarathon/details.php?t=en&s=4997
http://evenementen.uitslagen.nl/2010/amsterdammarathon/details.php?t=en&s=4998
http://evenementen.uitslagen.nl/2010/amsterdammarathon/details.php?t=en&s=4999
http://evenementen.uitslagen.nl/2010/amsterdammarathon/details.php?t=en&s=5000



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
        
        headings = re.findall("<tr>(.*?)</tr>", page, re.DOTALL)

        bib = re.findall("Bib number(.*?)</b>", page, re.DOTALL)
          

        data = {'bib': bib, 'headings': headings}

        scraperwiki.sqlite.save(['bib'], data) 
"""
This is an example of scraping multiple URLs.
"""

import scraperwiki
import re

# The URLs we're going to scrape:

urls = """
http://evenementen.uitslagen.nl/2010/amsterdammarathon/details.php?t=en&s=4975
http://evenementen.uitslagen.nl/2010/amsterdammarathon/details.php?t=en&s=4976
http://evenementen.uitslagen.nl/2010/amsterdammarathon/details.php?t=en&s=4977
http://evenementen.uitslagen.nl/2010/amsterdammarathon/details.php?t=en&s=4978
http://evenementen.uitslagen.nl/2010/amsterdammarathon/details.php?t=en&s=4979
http://evenementen.uitslagen.nl/2010/amsterdammarathon/details.php?t=en&s=4980
http://evenementen.uitslagen.nl/2010/amsterdammarathon/details.php?t=en&s=4981
http://evenementen.uitslagen.nl/2010/amsterdammarathon/details.php?t=en&s=4982
http://evenementen.uitslagen.nl/2010/amsterdammarathon/details.php?t=en&s=4983
http://evenementen.uitslagen.nl/2010/amsterdammarathon/details.php?t=en&s=4984
http://evenementen.uitslagen.nl/2010/amsterdammarathon/details.php?t=en&s=4985
http://evenementen.uitslagen.nl/2010/amsterdammarathon/details.php?t=en&s=4986
http://evenementen.uitslagen.nl/2010/amsterdammarathon/details.php?t=en&s=4987
http://evenementen.uitslagen.nl/2010/amsterdammarathon/details.php?t=en&s=4988
http://evenementen.uitslagen.nl/2010/amsterdammarathon/details.php?t=en&s=4989
http://evenementen.uitslagen.nl/2010/amsterdammarathon/details.php?t=en&s=4990
http://evenementen.uitslagen.nl/2010/amsterdammarathon/details.php?t=en&s=4991
http://evenementen.uitslagen.nl/2010/amsterdammarathon/details.php?t=en&s=4992
http://evenementen.uitslagen.nl/2010/amsterdammarathon/details.php?t=en&s=4993
http://evenementen.uitslagen.nl/2010/amsterdammarathon/details.php?t=en&s=4994
http://evenementen.uitslagen.nl/2010/amsterdammarathon/details.php?t=en&s=4995
http://evenementen.uitslagen.nl/2010/amsterdammarathon/details.php?t=en&s=4996
http://evenementen.uitslagen.nl/2010/amsterdammarathon/details.php?t=en&s=4997
http://evenementen.uitslagen.nl/2010/amsterdammarathon/details.php?t=en&s=4998
http://evenementen.uitslagen.nl/2010/amsterdammarathon/details.php?t=en&s=4999
http://evenementen.uitslagen.nl/2010/amsterdammarathon/details.php?t=en&s=5000



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
        
        headings = re.findall("<tr>(.*?)</tr>", page, re.DOTALL)

        bib = re.findall("Bib number(.*?)</b>", page, re.DOTALL)
          

        data = {'bib': bib, 'headings': headings}

        scraperwiki.sqlite.save(['bib'], data) 
