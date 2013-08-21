import scraperwiki
import lxml.html

# Blank Python

idx = 0

for i in range(1,8):
    base_url = 'http://goteo.org/project/yuwa-at-donosti-cup/supporters?page='+str(i)
    
    html = scraperwiki.scrape(base_url)
    root = lxml.html.fromstring(html)
    links = root.cssselect("div.supporter dl")
    
    for link in links:

        record = {}

        amount = link.cssselect("dd.amount")[0].cssselect("strong")
        date = link.cssselect("dd.date")
    
        print amount[0].text+', '+date[0].text

        record['idx'] = idx
        record['amount'] = amount[0].text
        record['date'] = date[0].text

        scraperwiki.sqlite.save(['idx'], record)

        idx = idx + 1
