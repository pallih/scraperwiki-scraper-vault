import scraperwiki
import requests
import lxml.html
import sys

def get_text_or_none(element, selector):
    # element should be an lxml parent element
    # selector should be a css selector for the child you want
    try:
        r = element.cssselect(selector)[0].text
    except IndexError:
        r = None
    return r

page = 0
headers = { 'Accept': 'application/xml' }

try:
    nids = scraperwiki.sqlite.select("nid from swdata")
except:
    nids = {}
    pass


while True:
    url = "http://blogs.aljazeera.com/api/1/entitylist/ns_flow?offset=" + str(page) + "&limit=100&f[0]=field_ns_topic%3A136"
    req = requests.get(url, headers=headers)
    print "requested", url
    if req.status_code == 200:
        print "parsing XML"
        dom = lxml.html.fromstring(req.text.replace(' encoding="utf-8"', ''))
        items = dom.cssselect('entities > item')
        if len(items):
            print "XML parsed... extracting", len(items), "items and looking for new ones"
            data = []
            for item in items:
                nid = item.cssselect('nid')[0].text
                if not any(d['nid'] == nid for d in nids):
                    data.append({
                       'title': item.cssselect('title')[0].text,
                       'body_html': get_text_or_none(item, 'field_ns_body value'),
                       'created': item.cssselect('created')[0].text,
                       'updated': item.cssselect('changed')[0].text,
                       'nid': item.cssselect('nid')[0].text
                        })
                else:
                    print "XML parsed... found", len(data), ' new items'
                    print "saving", len(data), "items"
                    scraperwiki.sqlite.save(['nid'], data)  
                    sys.exit(0)  
            print "saving", len(data), "items"
            scraperwiki.sqlite.save(['nid'], data)
                
        else:
            print "XML parsed... no more items left!"
            break
    else:
        print "unexpected status code:", req.status_code
        break
    page += 100;