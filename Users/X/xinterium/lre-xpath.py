import scraperwiki
import lxml.html

root = scraperwiki.scrape('http://onethingwell.org/')
content = lxml.html.etree.HTML(root)
linkage = content.xpath("/html/body/div/article/h2/a/@href")

for links in linkage:
    record = { "link" : links }
    scraperwiki.datastore.save(["link"], record)



#import urllib2

#property_url = "http://www.lankarestaurants.com/show.php"
#data = "cmb1=All&cmb2=All&cmb3=All&cmb4=All&cmb5=All&cmb6=All&I2.x=53&I2.y=20&ST=B"
#print property_url + "?" + data
#response = urllib2.urlopen(urllib2.Request(property_url, data))
#html = response.read()
#print html
#content = lxml.html.etree.HTML(html)
#linkage = content.xpath("//td[2]/table/tbody/tr/td")

#for links in linkage:
#    print links