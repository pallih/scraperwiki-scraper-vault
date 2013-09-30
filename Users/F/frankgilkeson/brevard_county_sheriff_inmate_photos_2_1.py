import scraperwiki
import lxml.html
from BeautifulSoup import BeautifulSoup
import os
import urllib
import base64

html = scraperwiki.scrape("http://www.brevardsheriff.com/dar/inmatephotos/index.html")
root = lxml.html.fromstring(html)
for inmates in root.cssselect("p.MsoNormal a"):           
    id = os.path.splitext(inmates.attrib['href'])[0]
    #name = inmates.text
    #photo1 = base64.b64encode(urllib.urlopen("http://www.brevardsheriff.com/dar/inmatephotos/Images/"+id+"-1.jpg").read())
    #photo2 = base64.b64encode(urllib.urlopen("http://www.brevardsheriff.com/dar/inmatephotos/Images/"+id+"-2.jpg").read())
    report = "http://www.brevardsheriff.com/dar/inmatephotos/"+id+".html"
    reporthtml = scraperwiki.scrape(report)
#    print arresttext


    #scraperwiki.sqlite.save(unique_keys=["id"], data={"id":id, "name":name, "photo1_blob":photo1, "photo2_blob":photo2, "report":report})import scraperwiki
import lxml.html
from BeautifulSoup import BeautifulSoup
import os
import urllib
import base64

html = scraperwiki.scrape("http://www.brevardsheriff.com/dar/inmatephotos/index.html")
root = lxml.html.fromstring(html)
for inmates in root.cssselect("p.MsoNormal a"):           
    id = os.path.splitext(inmates.attrib['href'])[0]
    #name = inmates.text
    #photo1 = base64.b64encode(urllib.urlopen("http://www.brevardsheriff.com/dar/inmatephotos/Images/"+id+"-1.jpg").read())
    #photo2 = base64.b64encode(urllib.urlopen("http://www.brevardsheriff.com/dar/inmatephotos/Images/"+id+"-2.jpg").read())
    report = "http://www.brevardsheriff.com/dar/inmatephotos/"+id+".html"
    reporthtml = scraperwiki.scrape(report)
#    print arresttext


    #scraperwiki.sqlite.save(unique_keys=["id"], data={"id":id, "name":name, "photo1_blob":photo1, "photo2_blob":photo2, "report":report})