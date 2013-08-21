import scraperwiki
import requests
import lxml.html

url = 'http://www.stadlar.is/verslun/printSearch.asp?avs=True&sn=&se=&si=_&sc=&stc=&p=1'

html = requests.get(url).content
root = lxml.html.fromstring(html)
table = root.xpath('//table/tr')

all = []
i = 1
for tr in table[2:]:
    record = {}
    record['i'] = i
    try:
        record['nafn'] = tr[0].text.strip()
        record['isl'] = tr[1].text.strip()
        record['en'] = tr[2].text.strip()
        record['verd'] = tr[3].text.strip()
    
        all.append(record)
        i = i+1
    except Exception, e:
        print e
scraperwiki.sqlite.save(unique_keys=["i"],data=all, verbose=0)

