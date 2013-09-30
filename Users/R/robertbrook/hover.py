import scraperwiki  
import lxml.html 
import json        
import pprint
        
html = scraperwiki.scrape("https://www.hover.com/pricing")

root = lxml.html.fromstring(html)

data = json.loads(root.cssselect("div[id='pricing-data']")[0].text_content());

# pprint.pprint(data.keys());

records = {};

for domain in data['domains']:
    for key, value in domain.iteritems() :
        print key, value;
        records[key] = value;

    scraperwiki.sqlite.save(unique_keys=['name'], data=records)import scraperwiki  
import lxml.html 
import json        
import pprint
        
html = scraperwiki.scrape("https://www.hover.com/pricing")

root = lxml.html.fromstring(html)

data = json.loads(root.cssselect("div[id='pricing-data']")[0].text_content());

# pprint.pprint(data.keys());

records = {};

for domain in data['domains']:
    for key, value in domain.iteritems() :
        print key, value;
        records[key] = value;

    scraperwiki.sqlite.save(unique_keys=['name'], data=records)