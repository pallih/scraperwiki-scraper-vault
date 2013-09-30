import scraperwiki
import requests
import lxml.html

url = 'http://kvasir.rhi.hi.is/baejatal/search_text.php?searchtext=_'

html = requests.get(url).text

root = lxml.html.fromstring(html)

trs = root.xpath('//tr')
batch = []
print len(trs)
counter = 1
for tr in trs[1:]:
    record = {}
    record['id'] = counter
    record['nafn'] = tr[0][0].text.strip()
    record['sveitarfelag_nuverandi'] = tr[1].text.strip()
    record['sveitarfelag_1970'] = tr[2].text.strip()
    record['sysla'] = tr[3].text.strip()
    batch.append(record)
    counter = counter +1
scraperwiki.sqlite.save(["id"],data=batch)import scraperwiki
import requests
import lxml.html

url = 'http://kvasir.rhi.hi.is/baejatal/search_text.php?searchtext=_'

html = requests.get(url).text

root = lxml.html.fromstring(html)

trs = root.xpath('//tr')
batch = []
print len(trs)
counter = 1
for tr in trs[1:]:
    record = {}
    record['id'] = counter
    record['nafn'] = tr[0][0].text.strip()
    record['sveitarfelag_nuverandi'] = tr[1].text.strip()
    record['sveitarfelag_1970'] = tr[2].text.strip()
    record['sysla'] = tr[3].text.strip()
    batch.append(record)
    counter = counter +1
scraperwiki.sqlite.save(["id"],data=batch)