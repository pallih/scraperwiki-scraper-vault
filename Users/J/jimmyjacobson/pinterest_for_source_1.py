import scraperwiki
import urlparse
import re
import urllib2
import simplejson

# Blank Python

#helper function for getting an attribute from a css selector that we beleive results in one element
#[img.get('src') for img in pin.cssselect('.PinImageImg')]
def getAttributeFrom(attribute, page, selector):
    return " ".join([node.get(attribute) for node in page.cssselect(selector)])

def getTextFrom(page, selector):
    return " ".join([node.text for node in page.cssselect(selector)])

html = scraperwiki.scrape("http://pinterest.com/source/zappos.com/")
import lxml.html           
root = lxml.html.fromstring(html)
for pin in root.cssselect("#wrapper .pin"):
    data = {}
    data['id'] = pin.get("data-id")
    pinpage = lxml.html.fromstring(scraperwiki.scrape("http://pinterest.com/pin/"+data['id']))
    url = getAttributeFrom('href', pinpage, '#PinImageHolder a')
    o = urlparse.urlparse(url)
    url = "%s://%s%s" % (o.scheme, o.netloc, o.path)
    m = re.match(r'http://www.zappos.com/product/(\d+?)/color\/.*', url)
    if (m):
        if not scraperwiki.sqlite.select("id from swdata where id=?",data['id']): 
            zapposAPI = "http://api.zappos.com/Product/id/"+m.group(1)+"?key=445d5e8434e7b6f2f2640aa18da3936f6453828b"
            req = urllib2.Request(zapposAPI)
            opener = urllib2.build_opener()
            f = opener.open(req)
            json = simplejson.load(f)
            print json['product'][0]
            data['productId'] = m.group(1)
            data['url'] = json['product'][0]['defaultProductUrl']
            data['img'] = json['product'][0]['defaultImageUrl']
            data['description'] = json['product'][0]['productName']
            data['brand'] = json['product'][0]['brandName']
            scraperwiki.sqlite.save_var(data['url'],scraperwiki.sqlite.get_var(data['url'],0)+1)
            scraperwiki.sqlite.save(unique_keys=["id"], data=data)
            print data
        else:
            print "already saw this pin"
    else:
        print "affiliate pin"