import scraperwiki
import lxml.html as lh
from lxml import etree
from StringIO import StringIO

#for i in range(360000, 380000):
#for i in 373377:
site = "http://nhshw13.mapyourshow.com/5_0/exhibitor_details.cfm?exhid=" + "373377" #change to str() later
scraped_site = scraperwiki.scrape(site)
root = lh.fromstring(site)
#try:
doc = etree.parse(StringIO(site), parser=etree.HTMLParser())
Company_Name =  root.cssselect('h2')
Booth = root.cssselect('h4')
Street = root.xpath('string(//div[@id="mys-exhibitorInfo"]/ul[last()]/li[1])')

print Company_Name
print Booth 
print Street

data = {
        Company_Name.text_content(),
        Booth.text_context(),
        Street.strip()    
       }

scraperwiki.sqlite.save(unique_keys=['Info'], data=data)

#except:
#    print 'Oh dear, failed to scrape %s' % site
#    breakimport scraperwiki
import lxml.html as lh
from lxml import etree
from StringIO import StringIO

#for i in range(360000, 380000):
#for i in 373377:
site = "http://nhshw13.mapyourshow.com/5_0/exhibitor_details.cfm?exhid=" + "373377" #change to str() later
scraped_site = scraperwiki.scrape(site)
root = lh.fromstring(site)
#try:
doc = etree.parse(StringIO(site), parser=etree.HTMLParser())
Company_Name =  root.cssselect('h2')
Booth = root.cssselect('h4')
Street = root.xpath('string(//div[@id="mys-exhibitorInfo"]/ul[last()]/li[1])')

print Company_Name
print Booth 
print Street

data = {
        Company_Name.text_content(),
        Booth.text_context(),
        Street.strip()    
       }

scraperwiki.sqlite.save(unique_keys=['Info'], data=data)

#except:
#    print 'Oh dear, failed to scrape %s' % site
#    break