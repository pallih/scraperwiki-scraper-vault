import scraperwiki
import lxml.html
import re
import time
import cookielib
import urllib2
from urlparse import urlparse

# fetch UNSC publications
# could port the UNdemocracy scraper to scraperwiki, but for now, this is a bit of a rewrite #LongHardStupidWay

twocharyear= '11'
baseurl= 'http://www.un.org/Docs/sc/unsc_resolutions'+twocharyear+'.htm'
htmllist = scraperwiki.scrape(baseurl)
tree = lxml.html.fromstring(htmllist) 





def fetch_pdf(url):
    cookies = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookies))
    
    # will need to fake the referer and all the other bits
    proxy_hostname= "daccess-ods.un.org"
    opener.addheaders=[ ("Referer", "http://" + baseurl ), ("Host", proxy_hostname)]
    response = opener.open(url) #, '', headers3)
    interstitial_one = response.read()
    interstitial_one_regex= re.search("(?ism)(/TMP/.*?.html)", interstitial_one)
    tmp_filename= interstitial_one_regex.group(0)

    opener.addheaders=[ ("Referer", "http://" + proxy_hostname+'/'+tmp_filename ), ("Host", proxy_hostname)]
    response2 = opener.open("http://"+proxy_hostname+tmp_filename) #, '', headers2)
    interstitial_two = response2.read()
    #print interstitial_two

    #looking for: URL=http://daccess-dds-ny.un.org/doc/UNDOC/GEN/N11/502/44/PDF/N1150244.pdf?OpenElement">
    interstitial_two_regex= re.search('(?ism)URL=([^"]+)', interstitial_two)
    pdf_url= interstitial_two_regex.group(1)
    #print pdf_filename

    print pdf_url

#XXX not passing cookies correctly in here? :(
    pdf_url_parsed=urlparse(pdf_url)
    opener.addheaders=[ ("Referer", "http://" + proxy_hostname + '/'+tmp_filename), ("Host", pdf_url_parsed.netloc)]
    response3 = opener.open(pdf_url) #, '', headers3)
    print response3.read()


    #print data
    exit
    #return data



# find everything in the list
for matchitems in re.finditer('(?ism)"(http://[^"]+)"[^>]*>\s*(S/RES/\d+).*?</font></td>.*?sans-serif">([^<]+)</font></td>', htmllist): 
    # url=1, code=2, name=3
    print matchitems.group(3)
    pdfdata= fetch_pdf(matchitems.group(1))
    break
    #xmldata = scraperwiki.pdftoxml(pdfdata)
    #scraperwiki.datastore.save(matchitems.group(2), { "name":matchitems.group(3), "en_url":matchitems.group(1), "en_pdf":pdfdata, "en_xml":xmldata } )


