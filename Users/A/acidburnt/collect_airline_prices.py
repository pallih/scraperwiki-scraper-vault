import scraperwiki

import mechanize
br = mechanize.Browser()
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

br.open("http://www.kayak.com/#flights/CLE-SIN/2012-05-30/2012-08-30")
br.select_form(nr=0)
br.set_all_readonly(False)

br["__EVENTTARGET"] = "lnkNext"
br["__EVENTARGUMENT"] = ""
response = br.submit()
print response.read()

#print br.form




#import scraperwiki
#import lxml.html


#url = "http://www.expedia.com/Flights-Search?trip=roundtrip&leg1=from:CLE,to:SIN,departure:05%2F30%2F2012TANYT&leg2=from:SIN,to:CLE,departure:08%2F30%2F2012TANYT&passengers=children:0,adults:1,seniors:0,infantinlap:Y&
#options=cabinclass:coach,nopenalty:N,sortby:price&mode=search" 

#import urllib 
#root = urllib.urlopen(url).read() 
#print root

#html = scraperwiki.scrape("http://www.kayak.com/#flights/CLE-SIN/2012-05-30/2012-08-30")
#root = lxml.html.fromstring(html)
#print root
#div = root.cssselect(".filtermatrixcontainer")
#print div
#    bp = div.cssselect("a")
#    data={
 #       'price' : bp[0].text-content(),
  #      'pricing' : int(bp[0].text-content())
   # }
    #scraperwiki.sqlite.save(unique_keys=['price'], data=data)

# scraperwiki.sqlite.save(unique_keys=["a"], data={"a":1, "bbb":data})
# Blank Python


import scraperwiki

import mechanize
br = mechanize.Browser()
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

br.open("http://www.kayak.com/#flights/CLE-SIN/2012-05-30/2012-08-30")
br.select_form(nr=0)
br.set_all_readonly(False)

br["__EVENTTARGET"] = "lnkNext"
br["__EVENTARGUMENT"] = ""
response = br.submit()
print response.read()

#print br.form




#import scraperwiki
#import lxml.html


#url = "http://www.expedia.com/Flights-Search?trip=roundtrip&leg1=from:CLE,to:SIN,departure:05%2F30%2F2012TANYT&leg2=from:SIN,to:CLE,departure:08%2F30%2F2012TANYT&passengers=children:0,adults:1,seniors:0,infantinlap:Y&
#options=cabinclass:coach,nopenalty:N,sortby:price&mode=search" 

#import urllib 
#root = urllib.urlopen(url).read() 
#print root

#html = scraperwiki.scrape("http://www.kayak.com/#flights/CLE-SIN/2012-05-30/2012-08-30")
#root = lxml.html.fromstring(html)
#print root
#div = root.cssselect(".filtermatrixcontainer")
#print div
#    bp = div.cssselect("a")
#    data={
 #       'price' : bp[0].text-content(),
  #      'pricing' : int(bp[0].text-content())
   # }
    #scraperwiki.sqlite.save(unique_keys=['price'], data=data)

# scraperwiki.sqlite.save(unique_keys=["a"], data={"a":1, "bbb":data})
# Blank Python


