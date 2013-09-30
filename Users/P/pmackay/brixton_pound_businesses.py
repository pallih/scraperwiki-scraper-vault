import scraperwiki

# Blank Python
html = scraperwiki.scrape("http://directory.brixtonpound.org/")

import re
import json
import lxml.html

# Get JSON
# 'var biz_locations=(.*\])'
#print html[1..4]
match = re.search('biz_locations.(.*\])', html, flags=re.MULTILINE|re.X)
print match
jsonData = match.group(1)
jsonData = jsonData[2:]
jsonData = json.loads(jsonData)
#print jsonData[0]

root = lxml.html.fromstring(html)
for tr in root.cssselect("div[id='bizlist'] tr"):
    tds = tr.cssselect("td")
    # if len(tds)==12: data = { 'country' : tds[0].text_content(), 'years_in_school' : int(tds[4].text_content()) }
#    print tds[0].text_content()
    name = tds[0].text_content().strip()
    data = {'name': name, 'category': tds[1].text_content(), 'address': tds[2].text_content(), 'discount': tds[3].text_content()}
    for b in jsonData:
        if b['name'] == name:
            data['latitude'] = b['latitude']
            data['longitude'] = b['longitude']
            data['signed_up_ecurrency'] = b['signed_up_ecurrency']
            data['url'] = b['url']
            data['monea_username'] = b['monea_username']
            data['id'] = b['id']
            scraperwiki.sqlite.save(unique_keys=['name'], data=data)

    #print data
    #scraperwiki.sqlite.save(unique_keys=['name'], data=data)
    
#    scraperwiki.sqlite.save(unique_keys=['category'], data=tds[1].text_content())
#    scraperwiki.sqlite.save(unique_keys=['address'], data=tds[2].text_content())
#    scraperwiki.sqlite.save(unique_keys=['discount'], data=tds[3].text_content())
#    print tds[1].text_content()
#    print tds[2].text_content()
#    print tds[3].text_content()
    #break

print 'done'
import scraperwiki

# Blank Python
html = scraperwiki.scrape("http://directory.brixtonpound.org/")

import re
import json
import lxml.html

# Get JSON
# 'var biz_locations=(.*\])'
#print html[1..4]
match = re.search('biz_locations.(.*\])', html, flags=re.MULTILINE|re.X)
print match
jsonData = match.group(1)
jsonData = jsonData[2:]
jsonData = json.loads(jsonData)
#print jsonData[0]

root = lxml.html.fromstring(html)
for tr in root.cssselect("div[id='bizlist'] tr"):
    tds = tr.cssselect("td")
    # if len(tds)==12: data = { 'country' : tds[0].text_content(), 'years_in_school' : int(tds[4].text_content()) }
#    print tds[0].text_content()
    name = tds[0].text_content().strip()
    data = {'name': name, 'category': tds[1].text_content(), 'address': tds[2].text_content(), 'discount': tds[3].text_content()}
    for b in jsonData:
        if b['name'] == name:
            data['latitude'] = b['latitude']
            data['longitude'] = b['longitude']
            data['signed_up_ecurrency'] = b['signed_up_ecurrency']
            data['url'] = b['url']
            data['monea_username'] = b['monea_username']
            data['id'] = b['id']
            scraperwiki.sqlite.save(unique_keys=['name'], data=data)

    #print data
    #scraperwiki.sqlite.save(unique_keys=['name'], data=data)
    
#    scraperwiki.sqlite.save(unique_keys=['category'], data=tds[1].text_content())
#    scraperwiki.sqlite.save(unique_keys=['address'], data=tds[2].text_content())
#    scraperwiki.sqlite.save(unique_keys=['discount'], data=tds[3].text_content())
#    print tds[1].text_content()
#    print tds[2].text_content()
#    print tds[3].text_content()
    #break

print 'done'
