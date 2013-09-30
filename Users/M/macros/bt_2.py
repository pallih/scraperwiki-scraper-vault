import scraperwiki
import lxml.html
import pprint

def getHTMLvalue(el, css, atr='text', index=0):
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

def getPostcode(adr):
    #find2nd from last space
    parts = adr.split(' ')
    postcode = ''
    if len(parts) >= 2:
        postcode = parts[len(parts)-2] + parts[len(parts)-1]
    return postcode


sourcescraper = 'justeat'
scraperwiki.sqlite.attach(sourcescraper)
data = scraperwiki.sqlite.select('* from justeat.swdata limit 50')
for d in data:
    url = 'http://www.btexchanges.com/' + d['name'].replace(' ','-') + '/' + getPostcode(d['address']) + '.search?type=business'
    print url 
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    results = root.cssselect(".listing")
    if len(results) > 0:
        tel = getHTMLvalue(results[0], ".tel")
        website = getHTMLvalue(results[0], ".url a", "href")
        print tel, website
        d['tel'] = tel
        d['website'] = website
        print d['link']
        scraperwiki.sqlite.save(['link'], d)
import scraperwiki
import lxml.html
import pprint

def getHTMLvalue(el, css, atr='text', index=0):
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

def getPostcode(adr):
    #find2nd from last space
    parts = adr.split(' ')
    postcode = ''
    if len(parts) >= 2:
        postcode = parts[len(parts)-2] + parts[len(parts)-1]
    return postcode


sourcescraper = 'justeat'
scraperwiki.sqlite.attach(sourcescraper)
data = scraperwiki.sqlite.select('* from justeat.swdata limit 50')
for d in data:
    url = 'http://www.btexchanges.com/' + d['name'].replace(' ','-') + '/' + getPostcode(d['address']) + '.search?type=business'
    print url 
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    results = root.cssselect(".listing")
    if len(results) > 0:
        tel = getHTMLvalue(results[0], ".tel")
        website = getHTMLvalue(results[0], ".url a", "href")
        print tel, website
        d['tel'] = tel
        d['website'] = website
        print d['link']
        scraperwiki.sqlite.save(['link'], d)
