import scraperwiki
import datetime
import lxml.html
import pprint
import urllib2

def get_html_value(el, css, atr='text', index=0):
    try:
        lst = el.cssselect(css)
        val = ''
        if lst != None and len(lst) > 0:
            if index==0 or len(lst) >= index +1:
                if atr=='text':
                    val = lst[index].text_content()
                else:
                    val = lst[index].attrib.get(atr)
    
        return val
    except:
        return ''

# Google search URL
query = 'amazon+repricing'
url = 'https://www.google.com/search?q=' + query + '&pws=0&num=100&gf=0&complete=0'
opener = urllib2.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]
response = opener.open(url)
html = response.read()
root = lxml.html.fromstring(html)
adgrps = root.cssselect("#tads ol li")
adcount = 1
print html
for ad in adgrps:
    record = {}
    record['raw'] = ad
    record['date'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    record['query'] = query
    record['type'] = 'Paid'
    record['position'] = adcount
    record['title'] = get_html_value(ad, 'h3')
    record['displayurl'] = get_html_value(ad, 'div.kv')
    record['href'] = get_html_value(ad, 'h3 a', 'href')
    record['text'] = get_html_value(ad, 'span.ac')
    scraperwiki.sqlite.save(['date', 'raw'], record)
    adcount = adcount+1

sideadgrps = root.cssselect('#rhs_block ol li')
for ad in sideadgrps:
    record = {}
    record['raw'] = ad
    record['date'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    record['query'] = query
    record['type'] = 'Paid'
    record['position'] = adcount
    record['title'] = get_html_value(ad, 'h3')
    record['displayurl'] = get_html_value(ad, 'div.kv')
    record['href'] = get_html_value(ad, 'h3 a', 'href')
    record['text'] = get_html_value(ad, 'span.ac')
    scraperwiki.sqlite.save(['date', 'raw'], record)
    adcount = adcount+1

listingcount = 1
listings = root.cssselect('#ires ol li')
for listing in listings:
    record = {}
    record['raw'] = listing
    record['date'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    record['query'] = query
    record['type'] = 'Organic'
    record['position'] = listingcount
    record['title'] = get_html_value(listing , 'h3')
    record['displayurl'] = get_html_value(listing , 'div.kv')
    record['href'] = get_html_value(listing , 'h3 a', 'href')
    record['text'] = get_html_value(listing, 'span.st')
    scraperwiki.sqlite.save(['date', 'raw'], record)
    listingcount = listingcount +1import scraperwiki
import datetime
import lxml.html
import pprint
import urllib2

def get_html_value(el, css, atr='text', index=0):
    try:
        lst = el.cssselect(css)
        val = ''
        if lst != None and len(lst) > 0:
            if index==0 or len(lst) >= index +1:
                if atr=='text':
                    val = lst[index].text_content()
                else:
                    val = lst[index].attrib.get(atr)
    
        return val
    except:
        return ''

# Google search URL
query = 'amazon+repricing'
url = 'https://www.google.com/search?q=' + query + '&pws=0&num=100&gf=0&complete=0'
opener = urllib2.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]
response = opener.open(url)
html = response.read()
root = lxml.html.fromstring(html)
adgrps = root.cssselect("#tads ol li")
adcount = 1
print html
for ad in adgrps:
    record = {}
    record['raw'] = ad
    record['date'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    record['query'] = query
    record['type'] = 'Paid'
    record['position'] = adcount
    record['title'] = get_html_value(ad, 'h3')
    record['displayurl'] = get_html_value(ad, 'div.kv')
    record['href'] = get_html_value(ad, 'h3 a', 'href')
    record['text'] = get_html_value(ad, 'span.ac')
    scraperwiki.sqlite.save(['date', 'raw'], record)
    adcount = adcount+1

sideadgrps = root.cssselect('#rhs_block ol li')
for ad in sideadgrps:
    record = {}
    record['raw'] = ad
    record['date'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    record['query'] = query
    record['type'] = 'Paid'
    record['position'] = adcount
    record['title'] = get_html_value(ad, 'h3')
    record['displayurl'] = get_html_value(ad, 'div.kv')
    record['href'] = get_html_value(ad, 'h3 a', 'href')
    record['text'] = get_html_value(ad, 'span.ac')
    scraperwiki.sqlite.save(['date', 'raw'], record)
    adcount = adcount+1

listingcount = 1
listings = root.cssselect('#ires ol li')
for listing in listings:
    record = {}
    record['raw'] = listing
    record['date'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    record['query'] = query
    record['type'] = 'Organic'
    record['position'] = listingcount
    record['title'] = get_html_value(listing , 'h3')
    record['displayurl'] = get_html_value(listing , 'div.kv')
    record['href'] = get_html_value(listing , 'h3 a', 'href')
    record['text'] = get_html_value(listing, 'span.st')
    scraperwiki.sqlite.save(['date', 'raw'], record)
    listingcount = listingcount +1