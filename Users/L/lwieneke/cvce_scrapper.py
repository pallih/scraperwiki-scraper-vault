import scraperwiki
import lxml.html 

html = scraperwiki.scrape("http://www.cvce.eu/collections/unit-content/-/unit/89e56c97-d316-4e41-b362-d0a0171fac77/186a4a65-02be-449a-b540-29cc3f0f1c5d") 

root = lxml.html.fromstring(html)

for item in root.cssselect('div.container div.item'):
    for link in item.iterlinks():
        data = {'title':item.text_content(), 'url':link[2]}
        scraperwiki.sqlite.save(unique_keys=['url'], data = data)
              





