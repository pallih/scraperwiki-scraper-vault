import scraperwiki           
import lxml.html
import dateutil.parser 

html = scraperwiki.scrape("http://www.ace-centre.org.uk/index.cfm?pageid=F742D5F9-3048-7290-FEA4F588E0848EAE")
root = lxml.html.fromstring(html)
for el in root.cssselect("p.newsheadline a"):           
    #print lxml.html.tostring(el)
    newspurl =  "http://www.ace-centre.org.uk/"+ el.attrib['href']
    newsptitle = el.text
    #now get the code from the actual news page..
    print newspurl
    newsp = scraperwiki.scrape(newspurl)
    proot = lxml.html.fromstring(newsp)
    pel = proot.cssselect("h1")   
    if not pel:
        print "Moved"
    else:
        for bad in proot.xpath("//div[@id=\'contents\']/h1"):
            bad.getparent().remove(bad)        
        pcontent = proot.xpath("//div[@id=\'contents\']")
        newspcontent = lxml.html.tostring(pcontent[0])
        newspcontent = newspcontent[20:len(newspcontent)-31]
        udate = proot.cssselect("p.updated")[0]
        strudate = lxml.html.tostring(udate)[33:41]
        strndate = dateutil.parser.parse(strudate, dayfirst=True).date()
        #strndate = strudate[3:5] + '/' + strudate[0:3] + strudate[6:8]
        #print strndate
        data = { 
          'title':newsptitle, 
          'link' : newspurl,
          'description' : newspcontent,
          'date' : strndate
        }
        scraperwiki.sqlite.save(unique_keys=['title'], data=data)

# Blank Python

import scraperwiki           
import lxml.html
import dateutil.parser 

html = scraperwiki.scrape("http://www.ace-centre.org.uk/index.cfm?pageid=F742D5F9-3048-7290-FEA4F588E0848EAE")
root = lxml.html.fromstring(html)
for el in root.cssselect("p.newsheadline a"):           
    #print lxml.html.tostring(el)
    newspurl =  "http://www.ace-centre.org.uk/"+ el.attrib['href']
    newsptitle = el.text
    #now get the code from the actual news page..
    print newspurl
    newsp = scraperwiki.scrape(newspurl)
    proot = lxml.html.fromstring(newsp)
    pel = proot.cssselect("h1")   
    if not pel:
        print "Moved"
    else:
        for bad in proot.xpath("//div[@id=\'contents\']/h1"):
            bad.getparent().remove(bad)        
        pcontent = proot.xpath("//div[@id=\'contents\']")
        newspcontent = lxml.html.tostring(pcontent[0])
        newspcontent = newspcontent[20:len(newspcontent)-31]
        udate = proot.cssselect("p.updated")[0]
        strudate = lxml.html.tostring(udate)[33:41]
        strndate = dateutil.parser.parse(strudate, dayfirst=True).date()
        #strndate = strudate[3:5] + '/' + strudate[0:3] + strudate[6:8]
        #print strndate
        data = { 
          'title':newsptitle, 
          'link' : newspurl,
          'description' : newspcontent,
          'date' : strndate
        }
        scraperwiki.sqlite.save(unique_keys=['title'], data=data)

# Blank Python

