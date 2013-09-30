import scraperwiki
import lxml.etree, lxml.html
import mechanize
import re
import urlparse

def Main():
    url = "http://cordis.europa.eu/fp6/projects.htm"
    
    br = mechanize.Browser()
    br.open(url)
    br.select_form(name='partnerForm')
    br["QM_EP_CY_D"] = ["Ireland"]
    response = br.submit()
    
    while True:
        print "Page", br.geturl()
        root = lxml.html.parse(response).getroot() 
        ParsePage(root, br.geturl())
        lnextpage = [s.get("href")  for s in root.cssselect("p strong a")  if s.text == 'Next page']
        nextlinks = list(br.links(text_regex="Next page"))

        print lnextpage
        #br.follow_link(text_regex="Next page", nr=1)
        if nextlinks:
            response = br.follow_link(nextlinks[0])
        else:
            break


def ParsePage(root, baseurl):
    for dt in root.cssselect('dt'):
        #break
        data = { }
        data["link"] = urlparse.urljoin(baseurl, dt[0].get("href"))
        data["title"] = dt[0].text
        dd1=dt.getnext()
        data[dd1.text.strip(": ")] = dd1[0][0].text + dd1[0].tail
    
        dd2 = dd1.getnext()
        refk, refv = dd2.text.split(":")
        data[refk] = refv.strip()
    
        dd3 = dd2.getnext()
        refk, refv = dd3.text.split(":")
        data[refk] = refv.strip()
    
        dd4 = dd3.getnext()
        mactionline = re.match("(Action Line):\s*([A-Z0-9\-a-z]+)\s*(.*)", dd4.text)
        #assert mactionline, [dd4.text]
        #data[mactionline.group(1)] = mactionline.group(2)
        #data[mactionline.group(1)+" title"] = mactionline.group(3)
        
        dd5 = dd4.getnext()

        scraperwiki.sqlite.save(["Project Reference"], data)


Main()
    





import scraperwiki
import lxml.etree, lxml.html
import mechanize
import re
import urlparse

def Main():
    url = "http://cordis.europa.eu/fp6/projects.htm"
    
    br = mechanize.Browser()
    br.open(url)
    br.select_form(name='partnerForm')
    br["QM_EP_CY_D"] = ["Ireland"]
    response = br.submit()
    
    while True:
        print "Page", br.geturl()
        root = lxml.html.parse(response).getroot() 
        ParsePage(root, br.geturl())
        lnextpage = [s.get("href")  for s in root.cssselect("p strong a")  if s.text == 'Next page']
        nextlinks = list(br.links(text_regex="Next page"))

        print lnextpage
        #br.follow_link(text_regex="Next page", nr=1)
        if nextlinks:
            response = br.follow_link(nextlinks[0])
        else:
            break


def ParsePage(root, baseurl):
    for dt in root.cssselect('dt'):
        #break
        data = { }
        data["link"] = urlparse.urljoin(baseurl, dt[0].get("href"))
        data["title"] = dt[0].text
        dd1=dt.getnext()
        data[dd1.text.strip(": ")] = dd1[0][0].text + dd1[0].tail
    
        dd2 = dd1.getnext()
        refk, refv = dd2.text.split(":")
        data[refk] = refv.strip()
    
        dd3 = dd2.getnext()
        refk, refv = dd3.text.split(":")
        data[refk] = refv.strip()
    
        dd4 = dd3.getnext()
        mactionline = re.match("(Action Line):\s*([A-Z0-9\-a-z]+)\s*(.*)", dd4.text)
        #assert mactionline, [dd4.text]
        #data[mactionline.group(1)] = mactionline.group(2)
        #data[mactionline.group(1)+" title"] = mactionline.group(3)
        
        dd5 = dd4.getnext()

        scraperwiki.sqlite.save(["Project Reference"], data)


Main()
    





import scraperwiki
import lxml.etree, lxml.html
import mechanize
import re
import urlparse

def Main():
    url = "http://cordis.europa.eu/fp6/projects.htm"
    
    br = mechanize.Browser()
    br.open(url)
    br.select_form(name='partnerForm')
    br["QM_EP_CY_D"] = ["Ireland"]
    response = br.submit()
    
    while True:
        print "Page", br.geturl()
        root = lxml.html.parse(response).getroot() 
        ParsePage(root, br.geturl())
        lnextpage = [s.get("href")  for s in root.cssselect("p strong a")  if s.text == 'Next page']
        nextlinks = list(br.links(text_regex="Next page"))

        print lnextpage
        #br.follow_link(text_regex="Next page", nr=1)
        if nextlinks:
            response = br.follow_link(nextlinks[0])
        else:
            break


def ParsePage(root, baseurl):
    for dt in root.cssselect('dt'):
        #break
        data = { }
        data["link"] = urlparse.urljoin(baseurl, dt[0].get("href"))
        data["title"] = dt[0].text
        dd1=dt.getnext()
        data[dd1.text.strip(": ")] = dd1[0][0].text + dd1[0].tail
    
        dd2 = dd1.getnext()
        refk, refv = dd2.text.split(":")
        data[refk] = refv.strip()
    
        dd3 = dd2.getnext()
        refk, refv = dd3.text.split(":")
        data[refk] = refv.strip()
    
        dd4 = dd3.getnext()
        mactionline = re.match("(Action Line):\s*([A-Z0-9\-a-z]+)\s*(.*)", dd4.text)
        #assert mactionline, [dd4.text]
        #data[mactionline.group(1)] = mactionline.group(2)
        #data[mactionline.group(1)+" title"] = mactionline.group(3)
        
        dd5 = dd4.getnext()

        scraperwiki.sqlite.save(["Project Reference"], data)


Main()
    





