import scraperwiki

import lxml.html
import datetime

url = 'http://www.adp.si/'

doc = lxml.html.parse(url).getroot()
doc.make_links_absolute(url)

tds = doc.xpath('//td[@bgcolor="#FFFEF9"]')

try:
    mm = scraperwiki.sqlite.select('max(guid) from swdata', [])
    nextguid = mm[0]['max(guid)'] + 1
except:
    nextguid = 1

records = []
for td in tds:
    title = unicode(td.xpath('.//p[@class="style18"]/text()')[0])
    content = lxml.html.tostring(td)
    rec = {'title': title, 'description': content, 'pubDate': datetime.datetime.now(), 'link': url, 'guid': nextguid}
    try:
        num = scraperwiki.sqlite.select('* from swdata where description=?', [content])
    except:
        num = None
    if not num:
        records.append(rec)
        nextguid += 1

scraperwiki.sqlite.save(unique_keys=['description'], data=records)
    




