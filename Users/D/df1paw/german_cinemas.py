import scraperwiki
import urlparse
import lxml.html
import re
from lxml.html.clean import Cleaner

html = scraperwiki.scrape("http://www.kinofenster.de/adressen-rubrik/")
# print html


root = lxml.html.fromstring(html)
for el in root.cssselect("div.auswahlfeld a"):
    html2 = urlparse.urljoin("http://www.kinofenster.de/adressen-rubrik/",el.attrib.get('href'))
    # print html2
    scrapepage = scraperwiki.scrape(html2)    
    #print scrapepage
    scraperoot = lxml.html.fromstring(scrapepage)
    for elroot in scraperoot.cssselect("div.ergebnisliste a"):
        kinourl = urlparse.urljoin("http://www.kinofenster.de/",elroot.attrib.get('href'))
        kinoname = elroot.attrib.get('title')
        # print kinoname
        try:
            scrapekino = scraperwiki.scrape(kinourl)
        except:
            continue
        kinoroot = lxml.html.fromstring(scrapekino)
        # print scrapekino
        for elkino in kinoroot.cssselect("div.fliesstext"):
            cleaner = Cleaner(remove_tags=['div','br','a','span'], remove_unknown_tags=True, )
            #print lxml.html.tostring(elkino)
            anschrift1 = kinoroot.cssselect("div.fliesstext br")[0]
            anschrift2 = kinoroot.cssselect("div.fliesstext br")[1]
            anschrift3 = kinoroot.cssselect("div.fliesstext br")[2]
            anschrift4 = kinoroot.cssselect("div.fliesstext br")[3]
            try:
                tel = kinoroot.cssselect("div.fliesstext br")[4] 
            except:
                continue
            try:
                fax = kinoroot.cssselect("div.fliesstext br")[5]
            except:
                continue
            try:
                email = kinoroot.cssselect("div.fliesstext a")[0]
            except:
                continue
            try:
                url = kinoroot.cssselect("div.fliesstext a")[1]
            except:
                continue
            # print lxml.html.tostring(anschrift1)
            data = { 
            'kinoname' : kinoname, 
            'anschrift1' : re.sub('<\/{0,1}div>',' ',cleaner.clean_html(lxml.html.tostring(anschrift1,encoding=unicode))), 
            'anschrift2' : re.sub('<\/{0,1}div>',' ',cleaner.clean_html(lxml.html.tostring(anschrift2,encoding=unicode))), 
            'anschrift3' : re.sub('<\/{0,1}div>',' ',cleaner.clean_html(lxml.html.tostring(anschrift3,encoding=unicode))), 
            'anschrift4' : re.sub('<\/{0,1}div>',' ',cleaner.clean_html(lxml.html.tostring(anschrift4,encoding=unicode))), 
            'email' : re.sub('<\/{0,1}div>',' ',cleaner.clean_html(lxml.html.tostring(email,encoding=unicode))),
            'url' : re.sub('<\/{0,1}div>',' ',cleaner.clean_html(lxml.html.tostring(url,encoding=unicode))),
            'tel' : re.sub('<\/{0,1}div>',' ',cleaner.clean_html(lxml.html.tostring(tel,encoding=unicode))),
            'fax' : re.sub('<\/{0,1}div>',' ',cleaner.clean_html(lxml.html.tostring(fax,encoding=unicode))),
            }
            # print data
            scraperwiki.sqlite.save(unique_keys=['kinoname'], data=data)
