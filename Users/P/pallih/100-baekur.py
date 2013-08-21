import scraperwiki
import requests
import lxml.html
import re

utgafu_ar_regex = re.compile(".+\((.+)\)")

hofundur_regex = re.compile("(.+)\(.+")

url = 'http://www.borgarbokasafn.is/desktopdefault.aspx/4886_view-4188/tabid-2880/4650_read-26232/'
html = requests.get(url).text
root = lxml.html.fromstring(html)
baekur = root.xpath('//li/strong')

for bok in baekur:
    record = {}
    record['titill'] = bok.text
    try:
        record['hofundur'] = hofundur_regex.findall(bok.tail.replace('eftir','').strip())[0]
    except:
        record['hofundur'] = ''
    try:
        
        record['utgafu_ar'] = utgafu_ar_regex.findall(bok.tail.replace('eftir','').strip())[0]
    except:
        record['utgafu_ar'] = ''
    scraperwiki.sqlite.save(unique_keys=["titill"], data=record)