import scraperwiki
import urlparse

# Blank Python

#helper function for getting an attribute from a css selector that we beleive results in one element
#[img.get('src') for img in pin.cssselect('.PinImageImg')]
def getAttributeFrom(attribute, page, selector):
    return " ".join([node.get(attribute) for node in page.cssselect(selector)])

def getTextFrom(page, selector):
    return " ".join([node.text for node in page.cssselect(selector)])

html = scraperwiki.scrape("http://pinterest.com/source/guardian.co.uk/")
import lxml.html           
root = lxml.html.fromstring(html)
for pin in root.cssselect("#wrapper .pin"):
    data = {}
    data['img'] = getAttributeFrom('src', pin, '.PinImageImg')
    data['description'] = getTextFrom(pin, '.description')
    data['id'] = pin.get("data-id")
    if not scraperwiki.sqlite.select("id from swdata where id=?",data['id']):
        pinpage = lxml.html.fromstring(scraperwiki.scrape("http://pinterest.com/pin/"+data['id']))
        url = getAttributeFrom('href', pinpage, '#PinImageHolder a')
        o = urlparse.urlparse(url)
        data['url'] = "%s://%s%s" % (o.scheme, o.netloc, o.path)
        scraperwiki.sqlite.save_var(data['url'],scraperwiki.sqlite.get_var(data['url'],0)+1)
        scraperwiki.sqlite.save(unique_keys=["id"], data=data)
        print data
    else:
        print "skipped"