"""
This is an example of scraping multiple URLs.
"""

import scraperwiki
import re


# The URLs we're going to scrape:

urls = """

http://www.oireachtas.ie/viewdoc.asp?DocID=16227&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=14760&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=16121&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=14780&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=14035&&CatID=59

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
        billnumber = re.findall("Bill Number (.*?) of 2010", page, re.DOTALL)
        sponsoredby = re.findall("Sponsored by (.*?)<BR>", page, re.DOTALL) 
        source = re.findall("Source: (.*?)<BR>", page, re.DOTALL)
        method = re.findall("Method: (.*?)<BR>", page, re.DOTALL)
        status = re.findall("Status: (.*?)<P>", page, re.DOTALL)  
        start = re.findall("<BR>Presented (.*?) ", page, re.DOTALL)  
        startb = re.findall("<BR>Introduced (.*?) ", page, re.DOTALL)
        enacted = re.findall("Date of Signature (.*?)<BR>", page, re.DOTALL)  
        enactedb = re.findall("Date of Signature: (.*?)<BR>", page, re.DOTALL)
        # Just keep the heading text
        # (Try commenting this out)
        # headings = [gettext(heading) for heading in headings]
#
        data = {'url': url, 'title': title, 'billnumber': billnumber, 'sponsoredby':sponsoredby, 'source':source, 'method':method, 'status':status, 'start':start, 'startb':start, 'enacted':enacted,  'enactedb':enactedb}
      
        scraperwiki.datastore.save(['url'], data)   # each entry is identified by its url
"""
This is an example of scraping multiple URLs.
"""

import scraperwiki
import re


# The URLs we're going to scrape:

urls = """

http://www.oireachtas.ie/viewdoc.asp?DocID=16227&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=14760&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=16121&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=14780&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=14035&&CatID=59

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
        billnumber = re.findall("Bill Number (.*?) of 2010", page, re.DOTALL)
        sponsoredby = re.findall("Sponsored by (.*?)<BR>", page, re.DOTALL) 
        source = re.findall("Source: (.*?)<BR>", page, re.DOTALL)
        method = re.findall("Method: (.*?)<BR>", page, re.DOTALL)
        status = re.findall("Status: (.*?)<P>", page, re.DOTALL)  
        start = re.findall("<BR>Presented (.*?) ", page, re.DOTALL)  
        startb = re.findall("<BR>Introduced (.*?) ", page, re.DOTALL)
        enacted = re.findall("Date of Signature (.*?)<BR>", page, re.DOTALL)  
        enactedb = re.findall("Date of Signature: (.*?)<BR>", page, re.DOTALL)
        # Just keep the heading text
        # (Try commenting this out)
        # headings = [gettext(heading) for heading in headings]
#
        data = {'url': url, 'title': title, 'billnumber': billnumber, 'sponsoredby':sponsoredby, 'source':source, 'method':method, 'status':status, 'start':start, 'startb':start, 'enacted':enacted,  'enactedb':enactedb}
      
        scraperwiki.datastore.save(['url'], data)   # each entry is identified by its url
"""
This is an example of scraping multiple URLs.
"""

import scraperwiki
import re


# The URLs we're going to scrape:

urls = """

http://www.oireachtas.ie/viewdoc.asp?DocID=16227&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=14760&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=16121&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=14780&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=14035&&CatID=59

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
        billnumber = re.findall("Bill Number (.*?) of 2010", page, re.DOTALL)
        sponsoredby = re.findall("Sponsored by (.*?)<BR>", page, re.DOTALL) 
        source = re.findall("Source: (.*?)<BR>", page, re.DOTALL)
        method = re.findall("Method: (.*?)<BR>", page, re.DOTALL)
        status = re.findall("Status: (.*?)<P>", page, re.DOTALL)  
        start = re.findall("<BR>Presented (.*?) ", page, re.DOTALL)  
        startb = re.findall("<BR>Introduced (.*?) ", page, re.DOTALL)
        enacted = re.findall("Date of Signature (.*?)<BR>", page, re.DOTALL)  
        enactedb = re.findall("Date of Signature: (.*?)<BR>", page, re.DOTALL)
        # Just keep the heading text
        # (Try commenting this out)
        # headings = [gettext(heading) for heading in headings]
#
        data = {'url': url, 'title': title, 'billnumber': billnumber, 'sponsoredby':sponsoredby, 'source':source, 'method':method, 'status':status, 'start':start, 'startb':start, 'enacted':enacted,  'enactedb':enactedb}
      
        scraperwiki.datastore.save(['url'], data)   # each entry is identified by its url
"""
This is an example of scraping multiple URLs.
"""

import scraperwiki
import re


# The URLs we're going to scrape:

urls = """

http://www.oireachtas.ie/viewdoc.asp?DocID=16227&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=14760&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=16121&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=14780&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=14035&&CatID=59

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
        billnumber = re.findall("Bill Number (.*?) of 2010", page, re.DOTALL)
        sponsoredby = re.findall("Sponsored by (.*?)<BR>", page, re.DOTALL) 
        source = re.findall("Source: (.*?)<BR>", page, re.DOTALL)
        method = re.findall("Method: (.*?)<BR>", page, re.DOTALL)
        status = re.findall("Status: (.*?)<P>", page, re.DOTALL)  
        start = re.findall("<BR>Presented (.*?) ", page, re.DOTALL)  
        startb = re.findall("<BR>Introduced (.*?) ", page, re.DOTALL)
        enacted = re.findall("Date of Signature (.*?)<BR>", page, re.DOTALL)  
        enactedb = re.findall("Date of Signature: (.*?)<BR>", page, re.DOTALL)
        # Just keep the heading text
        # (Try commenting this out)
        # headings = [gettext(heading) for heading in headings]
#
        data = {'url': url, 'title': title, 'billnumber': billnumber, 'sponsoredby':sponsoredby, 'source':source, 'method':method, 'status':status, 'start':start, 'startb':start, 'enacted':enacted,  'enactedb':enactedb}
      
        scraperwiki.datastore.save(['url'], data)   # each entry is identified by its url
