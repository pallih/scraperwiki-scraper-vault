import scraperwiki      
import lxml.html
buzzurl =  "http://cyber.law.harvard.edu/node/7529"     
html = scraperwiki.scrape(buzzurl)

htmlout = "<p>This week's <a href=\'" + buzzurl + "\'>Berkman Buzz</a></p>\r<ul>"  
     
root = lxml.html.fromstring(html)
for tr in root.cssselect("h2"):
    u = tr.cssselect("a") #tr.getnext() #root.cssselect("h2 a")
    for ua in u:
        # print "HREF=" + ua.attrib['href']
        ut = ua
    # out put it
    htmlout = htmlout +  "\r\r<li><p>" + tr.text_content() + " [<a href=\'" + ut.attrib['href'] + "\'>link</a>]</li>"
    # no real point in collecting this data
    data = {
      'h2' : tr.text_content(),
      'u'  : ut.attrib['href']
    }
     # no real point in saving this data
    scraperwiki.sqlite.save(unique_keys=['h2'], data=data)
htmlout = htmlout + "\r</ul>"
print htmlout

import scraperwiki      
import lxml.html
buzzurl =  "http://cyber.law.harvard.edu/node/7529"     
html = scraperwiki.scrape(buzzurl)

htmlout = "<p>This week's <a href=\'" + buzzurl + "\'>Berkman Buzz</a></p>\r<ul>"  
     
root = lxml.html.fromstring(html)
for tr in root.cssselect("h2"):
    u = tr.cssselect("a") #tr.getnext() #root.cssselect("h2 a")
    for ua in u:
        # print "HREF=" + ua.attrib['href']
        ut = ua
    # out put it
    htmlout = htmlout +  "\r\r<li><p>" + tr.text_content() + " [<a href=\'" + ut.attrib['href'] + "\'>link</a>]</li>"
    # no real point in collecting this data
    data = {
      'h2' : tr.text_content(),
      'u'  : ut.attrib['href']
    }
     # no real point in saving this data
    scraperwiki.sqlite.save(unique_keys=['h2'], data=data)
htmlout = htmlout + "\r</ul>"
print htmlout

