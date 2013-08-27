# Blank Python
"""
This is an example of scraping multiple URLs.
"""

import scraperwiki
import re

import BeautifulSoup
from datetime import datetime
from scraperwiki import datastore

# The URLs we're going to scrape:

urls = """

http://www.oireachtas.ie/viewdoc.asp?DocID=12440&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=12410&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=12385&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=12381&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=12341&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=12333&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=12287&amp;&amp;CatID=59
""".strip()

urls = urls.splitlines()


# This is a useful helper function that you might want to steal.
# It cleans up the data a bit.
# def gettext(html):
  #  """Return the text within html, removing any HTML tags it contained."""
  #  cleaned = re.sub('<.*?>', '', html)  # remove tags
   # cleaned = ' '.join(cleaned.split())  # collapse whitespace
    # return cleaned

# get all the bill links from http://www.oireachtas.ie/viewdoc.asp?m=&DocID=-1&CatID=59
# http://www.oireachtas.ie/viewdoc.asp?DocID=14885&amp;&amp;CatID=59
# 30 April 2010<br /><a href="viewdoc.asp?DocID=14879&amp;&amp;CatID=59" >Non-Medicinal Psychoactive Substances Bill 2010 (PMB)

for url in urls:
    print "Scraping", url
    page = scraperwiki.scrape(url)
    if page is not None:
        # Store all the h2 headings (matching "<h2>...</h2>")
        title = re.findall("<title>(.*?)</title>", page, re.DOTALL)
        # re.DOTALL makes it work across multiple lines as well.
        
        sponsoredby = re.findall("Sponsored by (.*?)<BR>", page, re.DOTALL)  
        enacted = re.findall("Date of Signature: (.*?)<BR>", page, re.DOTALL)  
           #try and extract the date the person went missing
    date = None    
    regex = re.compile('(([0-9][0-9])/([0-9][0-9])/(20)\d\d)', re.IGNORECASE)
    if regex.search(page):
        #date = regex.search(page).group(2)
        #date = date_missing.replace('th ', '')

    #    try:
    #        date = datetime.strptime(date, "%d %B %Y")
    #     except:
      #      try:
      #          date = datetime.strptime(date, "%e %B %Y")
       #     except:
       #         date = None
        # Just keep the heading text
        # (Try commenting this out)
        # headings = [gettext(heading) for heading in headings]

        data = {'url': url, 'title': title, 'sponsoredby':sponsoredby, 'enacted':enacted, 'date':date}
          #datastore.save(unique_keys=['link'], data=data, date=date_missing)
        scraperwiki.datastore.save(['url'], data)   # each entry is identified by its url
# Blank Python
"""
This is an example of scraping multiple URLs.
"""

import scraperwiki
import re

import BeautifulSoup
from datetime import datetime
from scraperwiki import datastore

# The URLs we're going to scrape:

urls = """

http://www.oireachtas.ie/viewdoc.asp?DocID=12440&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=12410&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=12385&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=12381&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=12341&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=12333&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=12287&amp;&amp;CatID=59
""".strip()

urls = urls.splitlines()


# This is a useful helper function that you might want to steal.
# It cleans up the data a bit.
# def gettext(html):
  #  """Return the text within html, removing any HTML tags it contained."""
  #  cleaned = re.sub('<.*?>', '', html)  # remove tags
   # cleaned = ' '.join(cleaned.split())  # collapse whitespace
    # return cleaned

# get all the bill links from http://www.oireachtas.ie/viewdoc.asp?m=&DocID=-1&CatID=59
# http://www.oireachtas.ie/viewdoc.asp?DocID=14885&amp;&amp;CatID=59
# 30 April 2010<br /><a href="viewdoc.asp?DocID=14879&amp;&amp;CatID=59" >Non-Medicinal Psychoactive Substances Bill 2010 (PMB)

for url in urls:
    print "Scraping", url
    page = scraperwiki.scrape(url)
    if page is not None:
        # Store all the h2 headings (matching "<h2>...</h2>")
        title = re.findall("<title>(.*?)</title>", page, re.DOTALL)
        # re.DOTALL makes it work across multiple lines as well.
        
        sponsoredby = re.findall("Sponsored by (.*?)<BR>", page, re.DOTALL)  
        enacted = re.findall("Date of Signature: (.*?)<BR>", page, re.DOTALL)  
           #try and extract the date the person went missing
    date = None    
    regex = re.compile('(([0-9][0-9])/([0-9][0-9])/(20)\d\d)', re.IGNORECASE)
    if regex.search(page):
        #date = regex.search(page).group(2)
        #date = date_missing.replace('th ', '')

    #    try:
    #        date = datetime.strptime(date, "%d %B %Y")
    #     except:
      #      try:
      #          date = datetime.strptime(date, "%e %B %Y")
       #     except:
       #         date = None
        # Just keep the heading text
        # (Try commenting this out)
        # headings = [gettext(heading) for heading in headings]

        data = {'url': url, 'title': title, 'sponsoredby':sponsoredby, 'enacted':enacted, 'date':date}
          #datastore.save(unique_keys=['link'], data=data, date=date_missing)
        scraperwiki.datastore.save(['url'], data)   # each entry is identified by its url
# Blank Python
"""
This is an example of scraping multiple URLs.
"""

import scraperwiki
import re

import BeautifulSoup
from datetime import datetime
from scraperwiki import datastore

# The URLs we're going to scrape:

urls = """

http://www.oireachtas.ie/viewdoc.asp?DocID=12440&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=12410&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=12385&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=12381&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=12341&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=12333&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=12287&amp;&amp;CatID=59
""".strip()

urls = urls.splitlines()


# This is a useful helper function that you might want to steal.
# It cleans up the data a bit.
# def gettext(html):
  #  """Return the text within html, removing any HTML tags it contained."""
  #  cleaned = re.sub('<.*?>', '', html)  # remove tags
   # cleaned = ' '.join(cleaned.split())  # collapse whitespace
    # return cleaned

# get all the bill links from http://www.oireachtas.ie/viewdoc.asp?m=&DocID=-1&CatID=59
# http://www.oireachtas.ie/viewdoc.asp?DocID=14885&amp;&amp;CatID=59
# 30 April 2010<br /><a href="viewdoc.asp?DocID=14879&amp;&amp;CatID=59" >Non-Medicinal Psychoactive Substances Bill 2010 (PMB)

for url in urls:
    print "Scraping", url
    page = scraperwiki.scrape(url)
    if page is not None:
        # Store all the h2 headings (matching "<h2>...</h2>")
        title = re.findall("<title>(.*?)</title>", page, re.DOTALL)
        # re.DOTALL makes it work across multiple lines as well.
        
        sponsoredby = re.findall("Sponsored by (.*?)<BR>", page, re.DOTALL)  
        enacted = re.findall("Date of Signature: (.*?)<BR>", page, re.DOTALL)  
           #try and extract the date the person went missing
    date = None    
    regex = re.compile('(([0-9][0-9])/([0-9][0-9])/(20)\d\d)', re.IGNORECASE)
    if regex.search(page):
        #date = regex.search(page).group(2)
        #date = date_missing.replace('th ', '')

    #    try:
    #        date = datetime.strptime(date, "%d %B %Y")
    #     except:
      #      try:
      #          date = datetime.strptime(date, "%e %B %Y")
       #     except:
       #         date = None
        # Just keep the heading text
        # (Try commenting this out)
        # headings = [gettext(heading) for heading in headings]

        data = {'url': url, 'title': title, 'sponsoredby':sponsoredby, 'enacted':enacted, 'date':date}
          #datastore.save(unique_keys=['link'], data=data, date=date_missing)
        scraperwiki.datastore.save(['url'], data)   # each entry is identified by its url
