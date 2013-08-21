import scraperwiki

# Blank Python
           


import time
from datetime import date
# this is 1 Jan 1901 ordinal = 693961
#first hansard after 694089
#second run 694202
#third run 698212
#fourth run 711792
#fifth run 721509
#sixth run 724792
#seventh run 724959
#eigth run 725723
#ninth run 729363
#tenth run 730097


#second run 694209
#third run 706652
#fourth run 718883
#fifth run 730097
ordinal = 730098
d = date.fromordinal(ordinal)


import urllib2

def load(url):
    retries = 5
    for i in range(retries):
        try:
            handle = urllib2.urlopen(url)
            return handle.read()
        except urllib2.URLError:
            if i + 1 == retries:
                raise
            else:
                time.sleep(90)
    # never get here


while (d.year < 2013):
    scrapeurl = "http://parlinfo.aph.gov.au/parlInfo/search/display/display.w3p;adv=yes;orderBy=customrank;page=0;query=Date%3A" + str(d.day) + "%2F" + str(d.month) + "%2F" + str(d.year) + "%20Dataset%3Ahansards,hansards80;rec=0;resCount=Default"
    

    html = load(scrapeurl)
    #html = scraperwiki.scrape(scrapeurl)
    import lxml.html           
    root = lxml.html.fromstring(html)
    i = 1
    hreflist = ["", "", "", "", ""]
    for el in root.cssselect("div.box a"):
        if i == 5:
            break
        #if el.text=='<img src="/images/icons/xml.gif" border="0" alt="View Or Save XML" title="View Or Save XML"/>View/Save XML':  
        #print el.attrib['href']
        print el.attrib['href']
        hreflist[i] = el.attrib['href']
        i = i+1
    if hreflist[1] <> "":    
        data1 = {
                'day' : ordinal,
                'URL1' : hreflist[1],
                'URL2' : hreflist[2],
                'URL3' : hreflist[3]
                }
        scraperwiki.sqlite.save(unique_keys=['day'], data=data1)
    ordinal = ordinal + 1
    d = date.fromordinal(ordinal)

print "Scraper finished!"