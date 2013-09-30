from urllib2 import urlopen
from lxml.etree import fromstring, tostring
from scraperwiki.sqlite import save
import datetime

URL = "http://www.skagitcounty.net/jail/HTML/jailbooking.xml"

page = urlopen(URL)
xml = page.read()

currenttime = datetime.datetime.now()
save([], {"xml":xml, "date-scraped":currenttime}, 'raw-files')


x = fromstring(xml)
arrests = x.xpath('//ins/in/descendant::ar')
for arrest in arrests:
    #Get number here


    for of in arrest.xpath('of'):
        data = {}
        try:
            data["offense-date"] = of.xpath('od/text()')[0]
        except:
            data["offense-date"] = None

        
            "offense": of.xpath('ol/text()')[0],
            "offense-i": of.xpath('oi/text()')[0],
            "offense-g": of.xpath('og/text()')[0],
            "offense-c": of.xpath('oc/text()')[0]
        
        print data
    
#        ar.xpath('ol/text()')[0]
#
#        <od>00:00:00 04/21/11</od>
#        <ol>VUCSA</ol>
#        <oi> 11-TF025</oi>
  #      <og>11-1-00397-2</og>
 #       <oc>SC</oc>
from urllib2 import urlopen
from lxml.etree import fromstring, tostring
from scraperwiki.sqlite import save
import datetime

URL = "http://www.skagitcounty.net/jail/HTML/jailbooking.xml"

page = urlopen(URL)
xml = page.read()

currenttime = datetime.datetime.now()
save([], {"xml":xml, "date-scraped":currenttime}, 'raw-files')


x = fromstring(xml)
arrests = x.xpath('//ins/in/descendant::ar')
for arrest in arrests:
    #Get number here


    for of in arrest.xpath('of'):
        data = {}
        try:
            data["offense-date"] = of.xpath('od/text()')[0]
        except:
            data["offense-date"] = None

        
            "offense": of.xpath('ol/text()')[0],
            "offense-i": of.xpath('oi/text()')[0],
            "offense-g": of.xpath('og/text()')[0],
            "offense-c": of.xpath('oc/text()')[0]
        
        print data
    
#        ar.xpath('ol/text()')[0]
#
#        <od>00:00:00 04/21/11</od>
#        <ol>VUCSA</ol>
#        <oi> 11-TF025</oi>
  #      <og>11-1-00397-2</og>
 #       <oc>SC</oc>
