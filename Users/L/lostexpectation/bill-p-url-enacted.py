"""
This is an example of scraping multiple URLs.
"""

import scraperwiki
import re

import BeautifulSoup
from datetime import datetime
from scraperwiki import sqlite

# The URLs we're going to scrape:

urls = """

http://www.oireachtas.ie/viewdoc.asp?DocID=16321&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=16257&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=16227&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=16121&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=16011&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=15919&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=15769&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=15676&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=15775&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=15629&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=15434&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=15318&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=15565&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=15380&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=15318&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=15347&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=15327&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=15264&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=15226&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=15230&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=15107&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=15109&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=15112&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=15082&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=15060&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=15052&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=14993&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=14983&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=14945&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=14885&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=14879&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=14810&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=14760&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=14780&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=14752&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=14718&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=14668&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=14390&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=14270&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=14035&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=13977&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=13968&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=13965&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=13962&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=13992&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=13908&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=13886&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=13867&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=13566&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=13826&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=13753&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=13695&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=13685&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=13623&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=13551&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=13622&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=13441&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=13418&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=13381&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=13312&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=13289&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=13286&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=13174&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=13121&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=13051&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=12946&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=12755&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=12724&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=12712&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=12714&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=12662&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=12616&&CatID=59&
http://www.oireachtas.ie/viewdoc.asp?DocID=12583&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=12492&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=12489&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=12468&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=12440&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=12410&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=12385&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=12381&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=12341&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=12333&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=12287&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=12251&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=12249&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=12235&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=12202&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=12138&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=12136&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=12132&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=12072&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=12052&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=11974&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=11970&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=11953&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=11922&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=11884&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=11842&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=11787&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=11740&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=11716&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=11749&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=11722&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=11718&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=11709&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=11675&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=11673&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=11651&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=11625&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=11600&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=11586&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=11583&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=11589&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=11572&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=11538&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=11500&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=11437&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=11341&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=11330&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=11303&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=11203&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=11307&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=11236&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=10954&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=10851&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=10844&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=10843&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=10710&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=10698&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=10687&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=10663&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=10648&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=10546&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=10548&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=10421&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=10418&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=10403&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=10401&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=10390&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=10296&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=10255&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=10229&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=10208&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=10132&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=10130&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=10114&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=10087&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=10089&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=10038&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=10023&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=10010&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=9971&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=9866&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=9843&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=9788&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=9722&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=9682&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=9687&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=9655&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=9641&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=9601&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=9597&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=9577&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=9540&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=9480&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=9433&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=9386&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=9302&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=9294&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=9290&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=9270&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=9230&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=9214&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=9186&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=9113&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=9111&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=9086&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=9080&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=9020&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=9017&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=8981&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=8969&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=8967&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=8952&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=8930&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=8876&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=8839&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=8823&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=8749&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=8751&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=8729&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=8720&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=8701&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=8684&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=8585&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=8582&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=8536&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=8534&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=8533&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=8555&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=8268&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=8249&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=8247&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=8245&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=8184&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=8156&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=8107&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=8059&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=7930&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=7927

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
        #   billnumber = re.findall("Bill Number (.*?) of 2010", page, re.DOTALL)
    #    source = re.findall("Source: (.*?)<BR>", page, re.DOTALL)
     #   method = re.findall("Method: (.*?)<BR>", page, re.DOTALL)
     #   status = re.findall("Status: (.*?)<P>", page, re.DOTALL)  
    #    cmte = re.findall("&#40;Select Committee on (.*?)&#41;", page, re.DOTALL)  
      # what do you use for brackets why does this not work for something like this SPAN></SPAN> (Select Committee on Foreign Affairs) <BR>DDMMYY <BR><!--<IMG cl
    print page
    cmte = re.findall("\(Select Committee on (.*?)\)", page, re.DOTALL) 
    
        # Just keep the heading text
        # (Try commenting this out)
        # headings = [gettext(heading) for heading in headings]

     #   data = {'url': url, 'title': title, 'billnumber': billnumber, 'source':source, 'method':method, 'status':status, 'cmte':cmte}
    data = {'url': url, 'title': title, 'cmte':cmte}
    scraperwiki.sqlite.save(['url'], data)   # each entry is identified by its url
"""
This is an example of scraping multiple URLs.
"""

import scraperwiki
import re

import BeautifulSoup
from datetime import datetime
from scraperwiki import sqlite

# The URLs we're going to scrape:

urls = """

http://www.oireachtas.ie/viewdoc.asp?DocID=16321&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=16257&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=16227&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=16121&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=16011&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=15919&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=15769&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=15676&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=15775&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=15629&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=15434&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=15318&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=15565&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=15380&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=15318&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=15347&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=15327&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=15264&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=15226&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=15230&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=15107&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=15109&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=15112&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=15082&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=15060&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=15052&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=14993&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=14983&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=14945&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=14885&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=14879&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=14810&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=14760&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=14780&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=14752&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=14718&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=14668&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=14390&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=14270&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=14035&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=13977&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=13968&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=13965&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=13962&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=13992&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=13908&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=13886&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=13867&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=13566&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=13826&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=13753&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=13695&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=13685&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=13623&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=13551&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=13622&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=13441&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=13418&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=13381&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=13312&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=13289&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=13286&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=13174&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=13121&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=13051&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=12946&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=12755&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=12724&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=12712&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=12714&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=12662&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=12616&&CatID=59&
http://www.oireachtas.ie/viewdoc.asp?DocID=12583&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=12492&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=12489&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=12468&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=12440&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=12410&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=12385&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=12381&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=12341&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=12333&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=12287&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=12251&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=12249&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=12235&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=12202&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=12138&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=12136&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=12132&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=12072&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=12052&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=11974&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=11970&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=11953&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=11922&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=11884&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=11842&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=11787&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=11740&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=11716&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=11749&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=11722&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=11718&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=11709&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=11675&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=11673&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=11651&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=11625&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=11600&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=11586&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=11583&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=11589&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=11572&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=11538&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=11500&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=11437&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=11341&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=11330&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=11303&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=11203&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=11307&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=11236&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=10954&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=10851&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=10844&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=10843&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=10710&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=10698&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=10687&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=10663&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=10648&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=10546&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=10548&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=10421&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=10418&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=10403&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=10401&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=10390&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=10296&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=10255&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=10229&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=10208&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=10132&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=10130&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=10114&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=10087&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=10089&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=10038&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=10023&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=10010&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=9971&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=9866&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=9843&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=9788&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=9722&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=9682&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=9687&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=9655&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=9641&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=9601&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=9597&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=9577&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=9540&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=9480&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=9433&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=9386&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=9302&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=9294&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=9290&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=9270&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=9230&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=9214&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=9186&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=9113&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=9111&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=9086&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=9080&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=9020&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=9017&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=8981&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=8969&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=8967&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=8952&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=8930&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=8876&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=8839&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=8823&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=8749&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=8751&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=8729&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=8720&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=8701&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=8684&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=8585&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=8582&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=8536&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=8534&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=8533&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=8555&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=8268&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=8249&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=8247&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=8245&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=8184&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=8156&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=8107&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=8059&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=7930&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=7927

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
        #   billnumber = re.findall("Bill Number (.*?) of 2010", page, re.DOTALL)
    #    source = re.findall("Source: (.*?)<BR>", page, re.DOTALL)
     #   method = re.findall("Method: (.*?)<BR>", page, re.DOTALL)
     #   status = re.findall("Status: (.*?)<P>", page, re.DOTALL)  
    #    cmte = re.findall("&#40;Select Committee on (.*?)&#41;", page, re.DOTALL)  
      # what do you use for brackets why does this not work for something like this SPAN></SPAN> (Select Committee on Foreign Affairs) <BR>DDMMYY <BR><!--<IMG cl
    print page
    cmte = re.findall("\(Select Committee on (.*?)\)", page, re.DOTALL) 
    
        # Just keep the heading text
        # (Try commenting this out)
        # headings = [gettext(heading) for heading in headings]

     #   data = {'url': url, 'title': title, 'billnumber': billnumber, 'source':source, 'method':method, 'status':status, 'cmte':cmte}
    data = {'url': url, 'title': title, 'cmte':cmte}
    scraperwiki.sqlite.save(['url'], data)   # each entry is identified by its url
"""
This is an example of scraping multiple URLs.
"""

import scraperwiki
import re

import BeautifulSoup
from datetime import datetime
from scraperwiki import sqlite

# The URLs we're going to scrape:

urls = """

http://www.oireachtas.ie/viewdoc.asp?DocID=16321&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=16257&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=16227&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=16121&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=16011&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=15919&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=15769&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=15676&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=15775&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=15629&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=15434&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=15318&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=15565&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=15380&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=15318&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=15347&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=15327&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=15264&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=15226&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=15230&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=15107&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=15109&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=15112&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=15082&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=15060&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=15052&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=14993&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=14983&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=14945&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=14885&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=14879&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=14810&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=14760&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=14780&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=14752&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=14718&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=14668&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=14390&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=14270&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=14035&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=13977&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=13968&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=13965&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=13962&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=13992&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=13908&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=13886&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=13867&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=13566&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=13826&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=13753&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=13695&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=13685&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=13623&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=13551&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=13622&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=13441&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=13418&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=13381&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=13312&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=13289&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=13286&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=13174&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=13121&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=13051&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=12946&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=12755&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=12724&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=12712&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=12714&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=12662&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=12616&&CatID=59&
http://www.oireachtas.ie/viewdoc.asp?DocID=12583&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=12492&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=12489&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=12468&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=12440&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=12410&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=12385&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=12381&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=12341&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=12333&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=12287&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=12251&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=12249&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=12235&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=12202&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=12138&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=12136&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=12132&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=12072&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=12052&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=11974&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=11970&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=11953&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=11922&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=11884&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=11842&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=11787&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=11740&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=11716&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=11749&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=11722&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=11718&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=11709&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=11675&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=11673&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=11651&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=11625&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=11600&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=11586&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=11583&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=11589&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=11572&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=11538&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=11500&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=11437&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=11341&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=11330&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=11303&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=11203&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=11307&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=11236&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=10954&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=10851&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=10844&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=10843&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=10710&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=10698&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=10687&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=10663&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=10648&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=10546&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=10548&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=10421&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=10418&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=10403&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=10401&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=10390&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=10296&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=10255&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=10229&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=10208&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=10132&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=10130&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=10114&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=10087&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=10089&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=10038&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=10023&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=10010&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=9971&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=9866&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=9843&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=9788&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=9722&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=9682&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=9687&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=9655&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=9641&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=9601&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=9597&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=9577&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=9540&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=9480&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=9433&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=9386&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=9302&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=9294&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=9290&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=9270&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=9230&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=9214&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=9186&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=9113&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=9111&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=9086&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=9080&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=9020&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=9017&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=8981&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=8969&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=8967&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=8952&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=8930&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=8876&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=8839&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=8823&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=8749&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=8751&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=8729&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=8720&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=8701&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=8684&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=8585&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=8582&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=8536&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=8534&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=8533&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=8555&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=8268&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=8249&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=8247&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=8245&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=8184&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=8156&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=8107&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=8059&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=7930&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=7927

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
        #   billnumber = re.findall("Bill Number (.*?) of 2010", page, re.DOTALL)
    #    source = re.findall("Source: (.*?)<BR>", page, re.DOTALL)
     #   method = re.findall("Method: (.*?)<BR>", page, re.DOTALL)
     #   status = re.findall("Status: (.*?)<P>", page, re.DOTALL)  
    #    cmte = re.findall("&#40;Select Committee on (.*?)&#41;", page, re.DOTALL)  
      # what do you use for brackets why does this not work for something like this SPAN></SPAN> (Select Committee on Foreign Affairs) <BR>DDMMYY <BR><!--<IMG cl
    print page
    cmte = re.findall("\(Select Committee on (.*?)\)", page, re.DOTALL) 
    
        # Just keep the heading text
        # (Try commenting this out)
        # headings = [gettext(heading) for heading in headings]

     #   data = {'url': url, 'title': title, 'billnumber': billnumber, 'source':source, 'method':method, 'status':status, 'cmte':cmte}
    data = {'url': url, 'title': title, 'cmte':cmte}
    scraperwiki.sqlite.save(['url'], data)   # each entry is identified by its url
"""
This is an example of scraping multiple URLs.
"""

import scraperwiki
import re

import BeautifulSoup
from datetime import datetime
from scraperwiki import sqlite

# The URLs we're going to scrape:

urls = """

http://www.oireachtas.ie/viewdoc.asp?DocID=16321&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=16257&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=16227&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=16121&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=16011&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=15919&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=15769&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=15676&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=15775&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=15629&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=15434&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=15318&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=15565&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=15380&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=15318&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=15347&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=15327&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=15264&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=15226&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=15230&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=15107&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=15109&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=15112&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=15082&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=15060&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=15052&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=14993&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=14983&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=14945&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=14885&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=14879&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=14810&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=14760&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=14780&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=14752&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=14718&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=14668&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=14390&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=14270&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=14035&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=13977&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=13968&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=13965&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=13962&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=13992&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=13908&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=13886&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=13867&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=13566&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=13826&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=13753&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=13695&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=13685&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=13623&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=13551&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=13622&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=13441&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=13418&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=13381&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=13312&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=13289&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=13286&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=13174&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=13121&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=13051&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=12946&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=12755&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=12724&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=12712&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=12714&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=12662&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=12616&&CatID=59&
http://www.oireachtas.ie/viewdoc.asp?DocID=12583&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=12492&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=12489&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=12468&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=12440&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=12410&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=12385&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=12381&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=12341&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=12333&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=12287&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=12251&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=12249&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=12235&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=12202&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=12138&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=12136&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=12132&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=12072&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=12052&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=11974&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=11970&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=11953&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=11922&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=11884&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=11842&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=11787&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=11740&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=11716&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=11749&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=11722&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=11718&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=11709&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=11675&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=11673&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=11651&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=11625&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=11600&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=11586&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=11583&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=11589&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=11572&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=11538&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=11500&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=11437&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=11341&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=11330&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=11303&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=11203&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=11307&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=11236&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=10954&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=10851&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=10844&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=10843&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=10710&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=10698&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=10687&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=10663&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=10648&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=10546&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=10548&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=10421&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=10418&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=10403&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=10401&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=10390&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=10296&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=10255&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=10229&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=10208&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=10132&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=10130&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=10114&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=10087&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=10089&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=10038&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=10023&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=10010&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=9971&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=9866&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=9843&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=9788&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=9722&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=9682&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=9687&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=9655&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=9641&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=9601&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=9597&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=9577&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=9540&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=9480&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=9433&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=9386&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=9302&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=9294&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=9290&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=9270&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=9230&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=9214&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=9186&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=9113&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=9111&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=9086&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=9080&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=9020&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=9017&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=8981&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=8969&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=8967&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=8952&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=8930&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=8876&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=8839&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=8823&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=8749&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=8751&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=8729&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=8720&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=8701&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=8684&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=8585&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=8582&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=8536&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=8534&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=8533&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=8555&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=8268&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=8249&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=8247&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=8245&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=8184&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=8156&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=8107&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=8059&amp;&amp;CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=7930&&CatID=59
http://www.oireachtas.ie/viewdoc.asp?DocID=7927

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
        #   billnumber = re.findall("Bill Number (.*?) of 2010", page, re.DOTALL)
    #    source = re.findall("Source: (.*?)<BR>", page, re.DOTALL)
     #   method = re.findall("Method: (.*?)<BR>", page, re.DOTALL)
     #   status = re.findall("Status: (.*?)<P>", page, re.DOTALL)  
    #    cmte = re.findall("&#40;Select Committee on (.*?)&#41;", page, re.DOTALL)  
      # what do you use for brackets why does this not work for something like this SPAN></SPAN> (Select Committee on Foreign Affairs) <BR>DDMMYY <BR><!--<IMG cl
    print page
    cmte = re.findall("\(Select Committee on (.*?)\)", page, re.DOTALL) 
    
        # Just keep the heading text
        # (Try commenting this out)
        # headings = [gettext(heading) for heading in headings]

     #   data = {'url': url, 'title': title, 'billnumber': billnumber, 'source':source, 'method':method, 'status':status, 'cmte':cmte}
    data = {'url': url, 'title': title, 'cmte':cmte}
    scraperwiki.sqlite.save(['url'], data)   # each entry is identified by its url
