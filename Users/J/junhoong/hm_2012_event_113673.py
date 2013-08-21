import scraperwiki
import re

runner = "1255"
pagenum = "1"
event = "113673"
siteURL = "http://hm12eng.allsports.jp/photo/photo_list_tag_search.php?page_id=113673&tag=" + runner + "&tag_code=zekken&page=" + pagenum
html = scraperwiki.scrape(siteURL)
print html

import lxml.html
root = lxml.html.fromstring(html)

for tr in root.cssselect("div[class='photo_box'] tr"):
    tds = tr.cssselect("td")
    data = tds[0].cssselect("img[src]")[0].attrib['src']
    data2 = re.split('=', data)

    url0 = 'http://hm12eng.allsports.jp/photo/photo_'
    url = url0 + data2[1][:-2] + '_' + data2[2][:-2] + '_' + data2[3][:-2] + '_' + event + '_' + data2[5][:-2] + '_' + data2[4][:-2] + '_t'
    data3 = { 'url' : url }
    scraperwiki.sqlite.save(unique_keys=['url'], data=data3)