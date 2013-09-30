import scraperwiki
import re

html = scraperwiki.scrape("http://www.express-bank.ru/alekseevka/offices")
uls = re.findall(r'class="choose-region-item">(.+?)</a.*?class="choose-cities-list">(.+?)</ul', html, re.I|re.U|re.S)
links_re = re.compile(r'<a.*?href="(.+?)".*?>(.+?)</a', re.I|re.U|re.S)
# Blank Python
i=0
for ul in uls:
    links = links_re.findall(ul[1])
    for link in links:
        i+=1
        scraperwiki.sqlite.save(unique_keys=['id'], data={'id':i,'region': ul[0], 'city': link[1], 'link': link[0]}, table_name="swdata_process")


import scraperwiki
import re

html = scraperwiki.scrape("http://www.express-bank.ru/alekseevka/offices")
uls = re.findall(r'class="choose-region-item">(.+?)</a.*?class="choose-cities-list">(.+?)</ul', html, re.I|re.U|re.S)
links_re = re.compile(r'<a.*?href="(.+?)".*?>(.+?)</a', re.I|re.U|re.S)
# Blank Python
i=0
for ul in uls:
    links = links_re.findall(ul[1])
    for link in links:
        i+=1
        scraperwiki.sqlite.save(unique_keys=['id'], data={'id':i,'region': ul[0], 'city': link[1], 'link': link[0]}, table_name="swdata_process")


