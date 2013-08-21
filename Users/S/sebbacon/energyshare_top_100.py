import scraperwiki
from pyquery import PyQuery as pq
data = []
p = 1
count = 1
while count <= 100:
    url = "http://www.energyshare.com/groups/followers/p:%d" % p
    html = scraperwiki.scrape(url)
    doc = pq(html)
    items = doc("div.new-group-listing div.column")
    for item in items:
        link = pq(item)('h6 a')[0]
        title = link.attrib['title']
        href = link.attrib['href']
        supporters = int(pq(item)("p.color-silver:first").text().replace("Supporters ", ""))
        data = {'rank': count,
                'project':title,
                'url':href,
                'supporters': supporters}
        count += 1
        scraperwiki.sqlite.save(unique_keys=data.keys(), data=data)
    p += 1
        
