import scraperwiki
import requests
import lxml.html

def get_text_or_none(element, selector):
    # element should be an lxml parent element
    # selector should be a css selector for the child you want
    try:
        r = element.cssselect(selector)[0].text
    except IndexError:
        r = None
    return r

def get_text_content_or_none(element, selector):
    try:
        r = element.cssselect(selector)[0].text
    except IndexError:
        return None
    else:
        minidom = lxml.html.fromstring(r)
        return minidom.text_content()

page = 0
headers = { 'Accept': 'application/xml' }

while True:
    url = "http://blogs.aljazeera.com/api/1/entitylist/ns_flow?offset=" + str(page) + "&limit=100&f[0]=field_ns_topic%3A136"
    req = requests.get(url, headers=headers)
    print "requested", url
    if req.status_code == 200:
        print "parsing XML"
        dom = lxml.html.fromstring(req.text.replace(' encoding="utf-8"', ''))
        items = dom.cssselect('entities > item')
        if len(items):
            print "XML parsed... extracting", len(items), "items"
            data = []
            for item in items:
                data.append({
                    'title': item.cssselect('title')[0].text,
                    'body_html': get_text_or_none(item, 'field_ns_body value'),
                    'body': get_text_content_or_none(item, 'field_ns_body value'),
                    'created': item.cssselect('created')[0].text,
                    'updated': item.cssselect('changed')[0].text
                })
            print "saving", len(data), "items"
            scraperwiki.sqlite.save(['created'], data)
        else:
            print "XML parsed... no more items left!"
            break
    else:
        print "unexpected status code:", req.status_code
        break
    page += 100;import scraperwiki
import requests
import lxml.html

def get_text_or_none(element, selector):
    # element should be an lxml parent element
    # selector should be a css selector for the child you want
    try:
        r = element.cssselect(selector)[0].text
    except IndexError:
        r = None
    return r

def get_text_content_or_none(element, selector):
    try:
        r = element.cssselect(selector)[0].text
    except IndexError:
        return None
    else:
        minidom = lxml.html.fromstring(r)
        return minidom.text_content()

page = 0
headers = { 'Accept': 'application/xml' }

while True:
    url = "http://blogs.aljazeera.com/api/1/entitylist/ns_flow?offset=" + str(page) + "&limit=100&f[0]=field_ns_topic%3A136"
    req = requests.get(url, headers=headers)
    print "requested", url
    if req.status_code == 200:
        print "parsing XML"
        dom = lxml.html.fromstring(req.text.replace(' encoding="utf-8"', ''))
        items = dom.cssselect('entities > item')
        if len(items):
            print "XML parsed... extracting", len(items), "items"
            data = []
            for item in items:
                data.append({
                    'title': item.cssselect('title')[0].text,
                    'body_html': get_text_or_none(item, 'field_ns_body value'),
                    'body': get_text_content_or_none(item, 'field_ns_body value'),
                    'created': item.cssselect('created')[0].text,
                    'updated': item.cssselect('changed')[0].text
                })
            print "saving", len(data), "items"
            scraperwiki.sqlite.save(['created'], data)
        else:
            print "XML parsed... no more items left!"
            break
    else:
        print "unexpected status code:", req.status_code
        break
    page += 100;