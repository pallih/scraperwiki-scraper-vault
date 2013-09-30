import scraperwiki
import lxml.html

# 'http://worldreferee.com/site/copy.php?linkID=837&linkType=referee&contextType=bio'
# Blank Python

baseurl = "http://worldreferee.com/site/copy.php?linkType=referee&contextType=bio&linkID=%s"

html = scraperwiki.scrape('http://worldreferee.com/site/ajax.php?request=getRefs&page=http://worldreferee.com/site/home.php')

root = lxml.html.fromstring(html)

options = root.xpath('//result/option')

ids = []
for option in options:
    ids.append(option.attrib['value'])

def process(id):
    record = {}
    url = baseurl % id
    record['url'] = url
    record['id']  = id  
    html = scraperwiki.scrape(url)
    root = root = lxml.html.fromstring(html)
    record['name'] = root.xpath('//h1/text()')[0].replace('Referee ','').replace(' bio','').strip()
    info = root.xpath('//div[@class="specs"]')
    for div in info:
        
        tr = div.xpath('div[@class="spec"]')
        for t in tr:
            record[(t[0].text).replace('.','')] = t[1].text
    scraperwiki.sqlite.save(['id'],record,verbose=0)

for id in ids:
    process(id)import scraperwiki
import lxml.html

# 'http://worldreferee.com/site/copy.php?linkID=837&linkType=referee&contextType=bio'
# Blank Python

baseurl = "http://worldreferee.com/site/copy.php?linkType=referee&contextType=bio&linkID=%s"

html = scraperwiki.scrape('http://worldreferee.com/site/ajax.php?request=getRefs&page=http://worldreferee.com/site/home.php')

root = lxml.html.fromstring(html)

options = root.xpath('//result/option')

ids = []
for option in options:
    ids.append(option.attrib['value'])

def process(id):
    record = {}
    url = baseurl % id
    record['url'] = url
    record['id']  = id  
    html = scraperwiki.scrape(url)
    root = root = lxml.html.fromstring(html)
    record['name'] = root.xpath('//h1/text()')[0].replace('Referee ','').replace(' bio','').strip()
    info = root.xpath('//div[@class="specs"]')
    for div in info:
        
        tr = div.xpath('div[@class="spec"]')
        for t in tr:
            record[(t[0].text).replace('.','')] = t[1].text
    scraperwiki.sqlite.save(['id'],record,verbose=0)

for id in ids:
    process(id)