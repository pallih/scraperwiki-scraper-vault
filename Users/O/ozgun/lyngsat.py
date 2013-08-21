import scraperwiki

import scraperwiki           
import lxml.html
import time
import datetime


def getdata (url):

    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)

    LT =[]
    LC =[]    
    
    for i, el in enumerate(root.cssselect("td")):
        print el.html
        #for i, elf1 in enumerate(el.cssselect("font")):
        #    for i, elf2 in enumerate(elf1.cssselect("font")):

         #       for i, el1 in enumerate(elf2.cssselect("b")):
          #          for i, el2 in enumerate(el1.cssselect("a")):
        #                print el2.text 
        #for i2, el2 in enumerate(el.cssselect("font:nth-child(1)")):           
          




    return



baseurl = "http://www.lyngsat.com/tvchannels/az/AzTV.html"

getdata(baseurl)





